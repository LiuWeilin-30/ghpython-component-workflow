"""Offline scaffold and curve-example contracts; substitutes are not Rhino geometry."""
import math
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
from types import SimpleNamespace as NS
import sys
import json
from create_component import build_source, create
from check_starter import Component, Param


class Line:
    IsValid = True
    IsClosed = False
    def GetLength(self): return 10.0
    def DivideByCount(self, count, include_ends):
        # Nonuniform parameters ensure the example uses Rhino's returned values.
        return [math.sqrt(i / count) for i in range(count + 1)]
    def PointAt(self, t): return (10*t*t, 0, 0)


class Circle(Line):
    IsClosed = True
    def GetLength(self): return 2*math.pi
    def DivideByCount(self, count, include_ends):
        return [2*math.pi*i/count for i in range(count+1)]
    def PointAt(self, t): return (math.cos(t), math.sin(t), 0)


class ExampleTests(unittest.TestCase):
    def setUp(self):
        self.ns = {}
        exec(compile(build_source('curve-divide'), '<generated>', 'exec'), self.ns)

    def test_open_curve_points_follow_arc_division_parameters(self):
        pts, parameters = self.ns['_divide_curve'](Line(), 5)
        self.assertEqual(len(pts), 6)
        for i, point in enumerate(pts): self.assertAlmostEqual(point[0], 2*i)
        self.assertAlmostEqual(parameters[1], math.sqrt(0.2))

    def test_closed_seam_is_not_duplicated(self):
        pts, parameters = self.ns['_divide_curve'](Circle(), 4)
        self.assertEqual(len(pts), 4)
        self.assertEqual(len(parameters), 4)
        expected=[(1,0), (0,1), (-1,0), (0,-1)]
        for point, xy in zip(pts, expected):
            self.assertAlmostEqual(point[0],xy[0]); self.assertAlmostEqual(point[1],xy[1])

    def test_defaults_missing_and_invalid_inputs(self):
        self.assertEqual(self.ns['_divide_curve'](None, None), ([], []))
        self.assertEqual(len(self.ns['_divide_curve'](Line(), None)[0]), 11)
        for count in (0, -1, 1.5, True):
            with self.subTest(count=count), self.assertRaises(ValueError):
                self.ns['_divide_curve'](Line(), count)
        bad=Line(); bad.IsValid=False
        with self.assertRaises(ValueError): self.ns['_divide_curve'](bad, 2)

    def test_kernel_failure_is_not_silently_empty_success(self):
        bad=Line(); bad.DivideByCount=lambda *args:None
        with self.assertRaises(ValueError): self.ns['_divide_curve'](bad, 2)

    def test_generated_component_runs_and_clears_after_failure(self):
        component=Component([],[])
        modules={'Grasshopper':NS(Kernel=NS(GH_ParamAccess=NS(item='item',list='list',tree='tree'),
                                          GH_RuntimeMessageLevel=NS(Error='error'))),
                 'System':NS(Object=object,Double=float,Boolean=bool,Int32=int,String=str,Type=type),
                 'clr':NS(GetClrType=lambda t:t),'Rhino.Geometry':NS(Curve=Line,Point3d=tuple),
                 'RhinoCodePluginGH':NS(), 'RhinoCodePluginGH.Parameters':NS(ScriptVariableParam=Param)}
        self.ns.update(ghenv=NS(Component=component), Curve=Line(), Count=5)
        with patch.dict(sys.modules,modules):
            self.ns['_run_component'](); component.flush(); self.ns['_run_component']()
            self.assertEqual(len(self.ns['Points']),6)
            self.assertEqual([p.selected for p in component.Params.Output],[tuple,float,str])
            self.ns['Count']=0; self.ns['_run_component']()
            self.assertEqual(self.ns['Points'],[])
            self.assertEqual(self.ns['Parameters'],[])
            self.assertEqual(json.loads(self.ns['Debug'][0])['Status'],'error')

    def test_generated_file_and_loader_are_self_contained_and_protected(self):
        with tempfile.TemporaryDirectory() as directory:
            source=Path(directory)/"space ' 功能.py"
            src,loader,code=create(source)
            namespace={}
            exec(code,namespace,namespace)
            self.assertEqual(len(namespace['_divide_curve'](Line(),2)[0]),3)
            self.assertTrue(callable(namespace['_ensure_ports']))
            self.assertEqual(loader.read_text(encoding='utf-8'),code)
            original=src.read_bytes()
            with self.assertRaises(FileExistsError):create(source)
            self.assertEqual(src.read_bytes(),original)


if __name__=='__main__':
    unittest.main()
