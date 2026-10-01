"""Run geometry-free port migration and loader tests with the standard library.
These substitutes do not validate actual Rhino/GH marshalling or persistence.
"""
from pathlib import Path
import sys
from types import SimpleNamespace as NS
import unittest
from unittest.mock import patch
import json

SOURCE = Path(__file__).resolve().parents[1] / 'assets' / 'component_starter.py'

def runtime():
    namespace = {}
    exec(compile(SOURCE.read_text(encoding='utf-8'), str(SOURCE), 'exec'), namespace)
    return namespace

class Ports(list):
    Count=property(len)

class Param:
    def __init__(self,name):
        self.VariableName=self.Name=self.NickName=name
        self.Description=''
        self.Access='item'
        self.Optional=False
        self.Sources=[]
        self.Recipients=Ports()
        self.PersistentData=NS(DataCount=0)
        self.selected=None
        self.TypeHints=NS(Select=self.select)
    SourceCount=property(lambda self:len(self.Sources))
    def select(self,value):
        self.selected=value
        return value

class Component:
    def __init__(self,inputs,outputs):
        self.queue=[]; self.messages=[]; self.operations=[]; self.expired=0
        self.doc=NS(ScheduleSolution=lambda delay,callback:self.queue.append(callback))
        self.Params=NS(Input=Ports(inputs),Output=Ports(outputs),OnParametersChanged=lambda:None)
        def unregister(side,param,isolate):
            self.operations.append(('remove',param,isolate))
            side.remove(param)
        def register(side,param,index):
            self.operations.append(('add',param,index))
            side.insert(index,param)
            return True
        self.Params.UnregisterInputParameter=lambda p,i:unregister(self.Params.Input,p,i)
        self.Params.UnregisterOutputParameter=lambda p,i:unregister(self.Params.Output,p,i)
        self.Params.RegisterInputParam=lambda p,i:register(self.Params.Input,p,i)
        self.Params.RegisterOutputParam=lambda p,i:register(self.Params.Output,p,i)
    def OnPingDocument(self):return self.doc
    def RecordUndoEvent(self,name):pass
    def VariableParameterMaintenance(self):pass
    def ExpireSolution(self,recompute):self.expired+=1
    def AddRuntimeMessage(self,level,message):self.messages.append(message)
    def flush(self):
        jobs,self.queue=self.queue,[]
        for callback in jobs:callback(self.doc)

class PortArchitectureTests(unittest.TestCase):
    def setUp(self):
        self.ns=runtime()
        self.ns.update(INPUT_SPECS=[('Domain','Domain','range','item','object',True)],
                       OUTPUT_SPECS=[('Path','Path','result','item')],PORT_ALIASES={'domain':'Domain'})
        self.mocks=patch.dict(sys.modules,{
            'Grasshopper':NS(Kernel=NS(GH_ParamAccess=NS(item='item',list='list',tree='tree'),
                                      GH_RuntimeMessageLevel=NS(Error='error'))),
            'System':NS(Object=object,Double=float,Boolean=bool),
            'clr':NS(GetClrType=lambda t:t),
            'RhinoCodePluginGH':NS(),
            'RhinoCodePluginGH.Parameters':NS(ScriptVariableParam=Param)})
        self.mocks.start()
        self.addCleanup(self.mocks.stop)

    def test_legacy_rename_preserves_wires_and_data(self):
        old=Param('domain'); old.Sources=[object()];old.PersistentData.DataCount=1
        out=Param('Path');out.Recipients.append(object())
        component=Component([old],[out])
        self.assertFalse(self.ns['_ensure_ports'](component))
        self.assertFalse(self.ns['_ensure_ports'](component))
        self.assertEqual(len(component.queue),1)
        component.flush()
        self.assertFalse(component.messages)
        self.assertEqual(component.operations,[])
        self.assertIs(component.Params.Input[0],old)
        self.assertEqual(old.VariableName,'Domain')
        self.assertEqual(old.SourceCount,1)
        self.assertEqual(old.PersistentData.DataCount,1)
        self.assertTrue(old.Optional)
        self.assertIs(old.selected,object)
        self.assertTrue(self.ns['_ensure_ports'](component))

    def test_matching_names_still_migrate_hint_and_optional(self):
        old=Param('Domain');old.selected='Interval';old.Sources=[object()]
        component=Component([old],[Param('Path')])
        self.assertFalse(self.ns['_ensure_ports'](component))
        self.assertEqual(old.selected,'Interval')
        component.flush()
        self.assertIs(old.selected,object)
        self.assertTrue(old.Optional)
        self.assertEqual(component.operations,[])
        self.ns['COMPONENT_MARKER']='irrelevant:r99'
        self.assertTrue(self.ns['_ensure_ports'](component))
        self.assertEqual(component.queue,[])

    def test_append_and_reorder_reuse_objects(self):
        old=Param('Domain');old.Sources=[object()]
        extra=Param('Width');extra.Sources=[object()]
        self.ns['INPUT_SPECS'].append(('Width','Width','width','item','number',True))
        component=Component([extra,old],[Param('Path')])
        self.ns['_ensure_ports'](component);component.flush()
        self.assertEqual(component.Params.Input,[old,extra])
        self.assertTrue(all(not op[2] for op in component.operations if op[0]=='remove'))
        self.ns['INPUT_SPECS'].append(('Angle','Angle','angle','item','number',True))
        self.ns['_ensure_ports'](component);component.flush()
        self.assertEqual([p.Name for p in component.Params.Input],['Domain','Width','Angle'])
        self.assertEqual(old.SourceCount,1)
        self.assertFalse(component.messages)

    def test_preflight_both_sides_prevents_partial_removal(self):
        removed=Param('x')
        wired=Param('OldResult');wired.Recipients.append(object())
        component=Component([removed],[wired])
        with self.assertRaises(ValueError):self.ns['_ensure_ports'](component)
        self.assertEqual(component.Params.Input,[removed])
        self.assertEqual(component.operations,[])

    def test_callback_rechecks_new_connection(self):
        old=Param('x')
        component=Component([old],[Param('a')])
        self.ns['_ensure_ports'](component)
        old.Sources.append(object())
        component.flush()
        self.assertTrue(component.messages)
        self.assertEqual(component.operations,[])
        old.Sources.clear()
        self.ns['_ensure_ports'](component);component.flush()
        self.assertEqual(component.Params.Input[0].Name,'Domain')

    def test_duplicate_aliases_and_bad_names_rejected(self):
        component=Component([Param('domain'),Param('Domain')],[Param('Path')])
        with self.assertRaises(ValueError):self.ns['_ensure_ports'](component)
        for name in ('domain','D omain','_Domain','1Domain'):
            self.ns['INPUT_SPECS']=[(name,name,'','item','object',True)]
            with self.subTest(name=name),self.assertRaises(ValueError):self.ns['_validate_port_specs']()

    def test_detached_callback_does_not_mutate(self):
        component=Component([Param('x')],[Param('a')])
        self.ns['_ensure_ports'](component)
        original=component.doc
        component.doc=None
        component.queue[0](original)
        self.assertEqual(component.operations,[])
        self.assertNotIn('pending',self.ns['_PATH_PORT_STATES'].get(str(id(component)),{}))

class Tree:
    @classmethod
    def __class_getitem__(cls, kind):
        return cls
    def __init__(self):
        self.Paths = []
        self.values = []
    BranchCount = property(lambda self: len(self.Paths))
    DataCount = property(lambda self: sum(len(branch) for branch in self.values))
    def EnsurePath(self, path):
        if path not in self.Paths:
            self.Paths.append(path)
            self.values.append([])
    def Add(self, value, path):
        self.EnsurePath(path)
        self.values[self.Paths.index(path)].append(value)
    def Branch(self, index):
        return self.values[index]


class LoaderWorkflowTests(unittest.TestCase):
    def test_exec_reload_preserves_paths_empty_branches_and_reads_new_source(self):
        class Hints:
            def Select(self, value):
                return value
        gh = NS(DataTree=Tree, Kernel=NS(
            GH_ParamAccess=NS(item='item', list='list', tree='tree'),
            GH_RuntimeMessageLevel=NS(Error='error')))
        component = Component([], [])
        data = Tree()
        data.Add('value', (1, 2))
        data.EnsurePath((3, 0))
        namespace = {'ghenv': NS(Component=component), 'Data': data}
        source = SOURCE.read_text(encoding='utf-8')
        modules = {'Grasshopper': gh, 'System': NS(Object=object, Double=float, Boolean=bool),
                   'clr': NS(GetClrType=lambda kind: kind), 'RhinoCodePluginGH': NS(),
                   'RhinoCodePluginGH.Parameters': NS(ScriptVariableParam=Param)}
        with patch.dict(sys.modules, modules):
            exec(compile(source, str(SOURCE), 'exec'), namespace, namespace)
            self.assertEqual(json.loads(namespace['Debug'][0])['Status'], 'pending')
            component.flush()
            exec(compile(source, str(SOURCE), 'exec'), namespace, namespace)
            result = namespace['Result']
            self.assertEqual(result.Paths, [(1, 2), (3, 0)])
            self.assertEqual(result.Branch(0), ['value'])
            self.assertEqual(result.Branch(1), [])
            first = json.loads(namespace['Debug'][0])
            previous_operations = list(component.operations)
            updated = source.replace("TreePassThrough:r1", "TreePassThrough:r2")
            exec(compile(updated, str(SOURCE), 'exec'), namespace, namespace)
            second = json.loads(namespace['Debug'][0])
            self.assertNotEqual(first['RunToken'], second['RunToken'])
            self.assertEqual(second['Source'], 'TreePassThrough:r2')
            self.assertEqual(component.queue, [])
            self.assertEqual(component.operations, previous_operations)
            namespace['Data'] = object()
            exec(compile(updated, str(SOURCE), 'exec'), namespace, namespace)
            failure = json.loads(namespace['Debug'][0])
            self.assertEqual(failure['Status'], 'error')
            self.assertEqual(namespace['Result'].DataCount, 0)
            self.assertTrue(component.messages)


if __name__ == '__main__':
    unittest.main()
