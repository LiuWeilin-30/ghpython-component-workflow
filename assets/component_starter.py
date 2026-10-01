"""Tree pass-through | Rhino 8 Grasshopper Python 3 Script.
Purpose: verify external source iteration, automatic ports and unchanged tree topology.
Responsibility: copy branch structure and item references; no geometry editing or export.

Inputs:
  Data: Tree Access, object hint, optional, default None. Accepts a GH data tree;
        an empty or missing input produces an empty result without invented geometry.
Outputs:
  Result: Tree Access, object hint; original GH paths, empty branches and item order are preserved.
          Items are passed through by reference, not deep-copied or baked.
  Debug: List Access, text hint; one JSON string for the current solve, including a run token,
         source marker, status, bounded path sample, counts or exception details.

Units/tolerance: none are required for this structural copy; item units are unchanged.
Assumptions/limits: no Flatten/Simplify or padding dimensions; no conversion of plain
Python lists into trees. Business algorithms replacing this example must declare
their own geometric assumptions, tolerance and approximation/error criteria.
Run: each GH solve rereads the workspace source through its loader. Initial port
configuration schedules a following solve; saving source alone does not recompute GH.
Failure/cache: no result cache; initialize an empty Result each run, report failure
in Debug and a GH Runtime Message. Pending port configuration skips processing.
Delivery: development source; embed the complete source in a fresh component for
standalone packaging and remove Debug there unless supported diagnostics are wanted.
Dependencies: Rhino 8 Python 3 component, RhinoCodePluginGH port parameters and GH SDK;
no external helper module or configuration file is required at component runtime.
Verification: substitute port/loader tests cover logic; actual GH marshalling and
save/reopen behavior must be verified in the recipient's runtime.
"""
INPUT_SPECS = [('Data', 'Data', 'Complete data tree; missing input produces an empty tree', 'tree', 'object', True)]
OUTPUT_SPECS = [('Result', 'Result', 'Data tree preserving paths and item order', 'tree', 'object'),
                ('Debug', 'Debug', 'Current solve status, counts or errors; may be removed for packaging', 'list', 'text')]
PORT_ALIASES = {}
COMPONENT_MARKER = 'TreePassThrough:r3'
COMPONENT_MESSAGE = 'Tree pass-through\nExternal source iteration'

def _port_name(param):
    return str(getattr(param, "VariableName", param.NickName))

def _canonical_port_name(param):
    name = _port_name(param)
    return globals().get("PORT_ALIASES", {}).get(name, name)

def _validate_port_specs():
    import re
    for specs, is_input in ((INPUT_SPECS, True), (OUTPUT_SPECS, False)):
        seen = set()
        for spec in specs:
            if len(spec) not in ((6,) if is_input else (4, 5)):
                raise ValueError("Input specs need 6 fields; output specs need 5 (legacy 4 accepted).")
            name = spec[0]
            if not isinstance(name, str) or re.fullmatch(r"[A-Z][A-Za-z0-9]*", name) is None:
                raise ValueError("Ports require short PascalCase English names: " + str(name))
            if name in seen or spec[1] != name:
                raise ValueError("Duplicate port name or inconsistent Name/NickName: " + name)
            seen.add(name)
            if spec[3] not in ("item", "list", "tree"):
                raise ValueError("Invalid port Access: " + name)
            if is_input and not isinstance(spec[5], bool):
                raise ValueError("Optional must be bool: " + name)
            # Resolve hints during preflight, on BOTH sides, before any mutation.
            _resolve_hint(spec[4] if len(spec) >= 5 else 'object')

def _ports_match(component):
    import Grasshopper as gh
    for ports, specs, is_input in ((component.Params.Input, INPUT_SPECS, True),
                                   (component.Params.Output, OUTPUT_SPECS, False)):
        if len(list(ports)) != len(specs):
            return False
        for param, spec in zip(ports, specs):
            if (_port_name(param) != spec[0] or param.Name != spec[0]
                    or param.NickName != spec[1]
                    or param.Access != getattr(gh.Kernel.GH_ParamAccess, spec[3])
                    or param.Optional != (spec[5] if is_input else False)):
                return False
    return True

def _port_has_data(param):
    persistent = getattr(param, "PersistentData", None)
    return bool(getattr(param, "SourceCount", 0)
                or getattr(getattr(param, "Recipients", None), "Count", 0)
                or (persistent is not None and getattr(persistent, "DataCount", 0)))

def _plan_port_side(ports, templates):
    existing = {}
    for param in ports:
        name = _canonical_port_name(param)
        if name in existing:
            raise ValueError("Duplicate existing port mapping; migration stopped: " + name)
        existing[name] = param
    names = [_port_name(p) for p in templates]
    if len(set(names)) != len(names):
        raise ValueError("Duplicate target port names.")
    removed = [p for name, p in existing.items() if name not in names]
    for param in removed:
        if _port_has_data(param):
            raise ValueError("Port scheduled for removal has connections or persistent data; keep the old component and load a fresh one: " + _port_name(param))
    return [existing.get(_port_name(p), p) for p in templates], removed

def _migrate_port_side(ports, templates, unregister, register):
    desired, removed = _plan_port_side(list(ports), templates)
    for param in removed:
        unregister(param, True)
    for index, (param, template) in enumerate(zip(desired, templates)):
        current = list(ports)
        if index >= len(current) or current[index] is not param:
            if any(p is param for p in current):
                unregister(param, False)
            if register(param, index) is False:
                raise ValueError("Port registration failed: " + _port_name(template))
        param.VariableName = template.VariableName
        param.Name, param.NickName = template.Name, template.NickName
        param.Description, param.Access = template.Description, template.Access
        param.Optional = template.Optional

def _resolve_hint(hint):
    """Resolve aliases or an explicit CLR type; Select still verifies availability."""
    import importlib
    import clr
    aliases = {
        'object': 'System.Object', 'number': 'System.Double', 'float': 'System.Double',
        'integer': 'System.Int32', 'int': 'System.Int32', 'bool': 'System.Boolean',
        'text': 'System.String', 'string': 'System.String', 'str': 'System.String',
        'datetime': 'System.DateTime', 'guid': 'System.Guid',
        'color': 'System.Drawing.Color', 'complex': 'Grasshopper.Kernel.Types.Complex',
        'point': 'Rhino.Geometry.Point3d', 'vector': 'Rhino.Geometry.Vector3d',
        'plane': 'Rhino.Geometry.Plane', 'interval': 'Rhino.Geometry.Interval',
        'uvinterval': 'Grasshopper.Kernel.Types.UVInterval', 'transform': 'Rhino.Geometry.Transform',
        'line': 'Rhino.Geometry.Line', 'circle': 'Rhino.Geometry.Circle',
        'arc': 'Rhino.Geometry.Arc', 'rectangle': 'Rhino.Geometry.Rectangle3d',
        'box': 'Rhino.Geometry.Box', 'polyline': 'Rhino.Geometry.Polyline',
        'curve': 'Rhino.Geometry.Curve', 'surface': 'Rhino.Geometry.Surface',
        'extrusion': 'Rhino.Geometry.Extrusion', 'brep': 'Rhino.Geometry.Brep',
        'subd': 'Rhino.Geometry.SubD', 'mesh': 'Rhino.Geometry.Mesh',
        'pointcloud': 'Rhino.Geometry.PointCloud', 'geometry': 'Rhino.Geometry.GeometryBase',
        'hatch': 'Rhino.Geometry.Hatch', 'textdot': 'Rhino.Geometry.TextDot',
        'textentity': 'Rhino.Geometry.TextEntity', 'leader': 'Rhino.Geometry.Leader',
        'dimension': 'Rhino.Geometry.Dimension', 'annotation': 'Rhino.Geometry.AnnotationBase',
    }
    if isinstance(hint, str):
        path = aliases.get(hint.lower(), hint)
        if '.' not in path:
            raise ValueError('Unknown type hint: ' + hint + '; inspect the installed hint catalog.')
        module, name = path.rsplit('.', 1)
        try:
            hint = getattr(importlib.import_module(module), name)
        except (ImportError, AttributeError) as exc:
            raise ValueError('Type hint is unavailable: ' + path) from exc
    if hasattr(hint, 'FullName'):
        return hint
    return clr.GetClrType(hint)

def _apply_port_spec(param, spec, is_input):
    import Grasshopper as gh
    import System
    param.VariableName = param.Name = spec[0]
    param.NickName, param.Description = spec[1], spec[2]
    param.Access = getattr(gh.Kernel.GH_ParamAccess, spec[3])
    param.Optional = spec[5] if is_input else False
    hint = spec[4] if len(spec) >= 5 else 'object'
    # Python.NET may otherwise bind Select(String) for a System.RuntimeType.
    selected = param.TypeHints.Select.Overloads[System.Type](_resolve_hint(hint))
    if selected is None:
        side = 'input' if is_input else 'output'
        raise ValueError('Unsupported ' + side + ' Type Hint: ' + spec[0] + ' = ' + str(hint))

def _spec_stamp():
    return (tuple(tuple(s) for s in INPUT_SPECS), tuple(tuple(s) for s in OUTPUT_SPECS),
            tuple(sorted(globals().get('PORT_ALIASES', {}).items())))

def _port_stamp(component):
    return (_spec_stamp(), tuple(str(getattr(p, 'InstanceGuid', id(p)))
            for p in list(component.Params.Input) + list(component.Params.Output)))

def _ensure_ports(component):
    import Grasshopper as gh
    from RhinoCodePluginGH.Parameters import ScriptVariableParam
    _validate_port_specs()
    # Per-component, in-session state. No serialized/runtime external dependency.
    states = globals().setdefault("_GH_PORT_STATES", {})
    key = str(getattr(component, "InstanceGuid", id(component)))
    stamp = _port_stamp(component)
    state = states.get(key, {})
    if _ports_match(component) and state.get("applied") == stamp:
        for specs, ports, is_input in ((INPUT_SPECS, component.Params.Input, True),
                                       (OUTPUT_SPECS, component.Params.Output, False)):
            for spec, param in zip(specs, ports):
                _apply_port_spec(param, spec, is_input)
        return True
    if state.get("pending") == stamp:
        return False
    # Construct all templates and preflight both sides before any unregister.
    inputs, outputs = [], []
    for specs, target, is_input in ((INPUT_SPECS, inputs, True), (OUTPUT_SPECS, outputs, False)):
        for spec in specs:
            param = ScriptVariableParam(spec[0])
            _apply_port_spec(param, spec, is_input)
            target.append(param)
    _plan_port_side(list(component.Params.Input), inputs)
    _plan_port_side(list(component.Params.Output), outputs)
    document = component.OnPingDocument()
    if document is None:
        return False
    snapshot = _spec_stamp()
    input_specs, output_specs = snapshot[:2]
    # Ownership token prevents an old callback from mutating or clearing a new job.
    token = object()
    states[key] = {"pending": stamp, "token": token}
    def configure(doc):
        try:
            if (states.get(key, {}).get('token') is not token
                    or _spec_stamp() != snapshot
                    or component.OnPingDocument() != doc):
                return
            # Recheck wires/persistent data added while the callback was pending.
            _plan_port_side(list(component.Params.Input), inputs)
            _plan_port_side(list(component.Params.Output), outputs)
            component.RecordUndoEvent("Update component ports")
            _migrate_port_side(component.Params.Input, inputs,
                               component.Params.UnregisterInputParameter, component.Params.RegisterInputParam)
            _migrate_port_side(component.Params.Output, outputs,
                               component.Params.UnregisterOutputParameter, component.Params.RegisterOutputParam)
            for specs, ports, is_input in ((input_specs, component.Params.Input, True),
                                           (output_specs, component.Params.Output, False)):
                for spec, param in zip(specs, ports):
                    _apply_port_spec(param, spec, is_input)
            component.Params.OnParametersChanged()
            component.VariableParameterMaintenance()
            states[key] = {"applied": _port_stamp(component)}
            component.ExpireSolution(False)
        except Exception as exc:
            component.AddRuntimeMessage(gh.Kernel.GH_RuntimeMessageLevel.Error, str(exc))
        finally:
            if states.get(key, {}).get('token') is token:
                states.pop(key, None)
    try:
        document.ScheduleSolution(1, configure)
    except Exception:
        states.pop(key, None)
        raise
    return False

def _process_tree(data):
    from Grasshopper import DataTree
    result = DataTree[object]()
    if data is None:
        return result
    if not hasattr(data, 'Paths') or not hasattr(data, 'BranchCount'):
        raise TypeError('Data requires a GH tree supplied through Tree Access; check port configuration and input type.')
    for index, path in enumerate(data.Paths):
        result.EnsurePath(path)
        for value in data.Branch(index):
            result.Add(value, path)
    return result


def _run_component():
    import json
    import traceback
    import uuid
    import Grasshopper as gh
    from Grasshopper import DataTree
    global Result, Debug
    # Capture inputs before resetting any same-name outputs in adapted components.
    input_data = globals().get('Data')
    component = ghenv.Component
    Result = DataTree[object]()
    token = str(uuid.uuid4())
    status = {'RunToken': token, 'Source': COMPONENT_MARKER,
              'Stage': 'ports', 'Status': 'pending', 'Cached': False}
    Debug = [json.dumps(status, ensure_ascii=False)]
    try:
        component.Message = COMPONENT_MESSAGE
        if not _ensure_ports(component):
            return
        status['Stage'] = 'process'
        status['InputType'] = type(input_data).__name__
        Result = _process_tree(input_data)
        status.update(Status='ok', BranchCount=Result.BranchCount,
                      ItemCount=Result.DataCount,
                      Paths=[str(path) for path in list(Result.Paths)[:12]])
    except Exception as exc:
        status.update(Status='error', ErrorType=type(exc).__name__,
                      Error=str(exc), Traceback=traceback.format_exc()[-4000:])
        component.AddRuntimeMessage(gh.Kernel.GH_RuntimeMessageLevel.Error, str(exc))
    Debug = [json.dumps(status, ensure_ascii=False)]


if 'ghenv' in globals():
    _run_component()
