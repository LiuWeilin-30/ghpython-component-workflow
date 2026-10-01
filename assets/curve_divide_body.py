"""Curve equal-arc-length division | Rhino 8 Grasshopper Python 3 Script.
Build with scripts/create_component.py --example curve-divide; the generator
embeds the shared port helpers to produce one standalone development source.

Inputs:
  Curve: Item / curve / optional. One valid Rhino.Geometry.Curve; None waits.
  Count: Item / integer / optional / default 10. Positive segment count.
Outputs:
  Points: List / point. Ordered division points; open curves include both ends.
          Closed curves contain Count points, with no duplicate seam point.
  Parameters: List / number. Corresponding original curve parameters (not lengths).
  Debug: List / text. Current source/run identity and ok/waiting/pending/error status.
Units: model units unchanged. Equal distance means arc length along the curve,
not straight-line distance between points or uniform parameter spacing.
Limits: valid positive-length curves; GH Item matching handles multiple inputs.
No baking, document edits, external modules, cache, or tolerance override.
Failure: empty Points/Parameters plus Debug and a runtime error. Missing Curve waits.
Run: paste the generated loader once; recompute after source edits. First port
setup uses a scheduled callback and following solve. Saved source alone is not a solve.
Check: line (0,0,0) to (10,0,0), Count=5 gives x=0,2,4,6,8,10; a circle
with Count=4 gives four distinct quarter-arc points. Increase Count and recompute.
Verification: offline contract tests only; actual GH ports, marshalling and
save/reopen require recipient-runtime acceptance. Keep Debug during development.
"""
INPUT_SPECS = [
    ('Curve', 'Curve', 'Curve to divide; missing input waits', 'item', 'curve', True),
    ('Count', 'Count', 'Positive segment count; default 10', 'item', 'integer', True),
]
OUTPUT_SPECS = [
    ('Points', 'Points', 'Equal-arc-length points; no duplicate closed seam', 'list', 'point'),
    ('Parameters', 'Parameters', 'Original curve parameters at the points', 'list', 'number'),
    ('Debug', 'Debug', 'Current solve status and identity', 'list', 'text'),
]
PORT_ALIASES = {}
COMPONENT_MARKER = 'CurveDivide:r2'
COMPONENT_MESSAGE = 'Divide curve\nEqual arc length'


def _divide_curve(curve, count):
    if curve is None:
        return [], []
    count = 10 if count is None else count
    if isinstance(count, bool) or int(count) != count or count < 1:
        raise ValueError('Count must be a positive integer.')
    count = int(count)
    if not curve.IsValid or not curve.GetLength() > 0:
        raise ValueError('Curve must be valid and have positive length.')
    values = curve.DivideByCount(count, True)
    if values is None:
        raise ValueError('Rhino could not divide this curve.')
    parameters = list(values)
    # Some versions include the duplicate closed endpoint; exclude it explicitly.
    if curve.IsClosed and len(parameters) == count + 1:
        parameters = parameters[:-1]
    expected = count if curve.IsClosed else count + 1
    if len(parameters) != expected:
        raise ValueError('Unexpected division count: expected %s, got %s.' % (expected, len(parameters)))
    return [curve.PointAt(t) for t in parameters], parameters


def _run_component():
    import json
    import uuid
    import Grasshopper as gh
    global Points, Parameters, Debug
    curve, count = globals().get('Curve'), globals().get('Count')
    Points, Parameters = [], []
    component = ghenv.Component
    status = {'RunToken': str(uuid.uuid4()), 'Source': COMPONENT_MARKER, 'Status': 'pending'}
    try:
        component.Message = COMPONENT_MESSAGE
        if _ensure_ports(component):
            Points, Parameters = _divide_curve(curve, count)
            status.update(Status='waiting' if curve is None else 'ok', PointCount=len(Points))
    except Exception as exc:
        Points, Parameters = [], []
        status.update(Status='error', ErrorType=type(exc).__name__, Error=str(exc))
        component.AddRuntimeMessage(gh.Kernel.GH_RuntimeMessageLevel.Error, str(exc))
    Debug = [json.dumps(status, ensure_ascii=False)]


if 'ghenv' in globals():
    _run_component()
