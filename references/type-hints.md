# Type matching on every input and output

Choose a semantic type for **each port**, then configure its Hint and Access independently. Inputs also specify Optional. Outputs must emit values matching the selected type; do not call a numeric output point-typed merely to get a preview. Object is a deliberate choice for mixed/custom packets, not a fallback for missing implementation.

Rhino's [Python component documentation](https://developer.rhino3d.com/guides/scripting/scripting-gh-python/#type-hints) explicitly supports hints on both sides. Python 3 Script hints, GH parameter classes, CLR geometry types and installed plugin types are different sets. There is no single universal count for “all GH types”.

## Built-in coverage

Offline reflection of Rhino **8.20.25133.14001** found 39 concrete built-in hint classes in Grasshopper's hint namespace, excluding separators, the server and an open generic helper. Merging the four VB/C# primitive pairs gives **35 semantic categories**. This is an assembly inventory, not a verified Python menu count. The starter supplies aliases for those categories:

| Aliases | CLR types / purpose |
| --- | --- |
| `object` | System.Object; mixed/custom values |
| `number` / `float`, `integer` / `int`, `bool`, `text` / `string` / `str` | System.Double, Int32, Boolean, String |
| `datetime`, `guid`, `color` | System.DateTime, System.Guid, System.Drawing.Color |
| `complex`, `uvinterval` | **Grasshopper.Kernel.Types**.Complex / UVInterval (not System.Numerics.Complex or Rhino.Geometry.UVInterval) |
| `point`, `vector`, `plane`, `interval`, `transform` | Rhino.Geometry.Point3d, Vector3d, Plane, Interval, Transform |
| `line`, `circle`, `arc`, `rectangle`, `box`, `polyline` | Rhino.Geometry.Line, Circle, Arc, Rectangle3d, Box, Polyline |
| `curve`, `surface`, `extrusion`, `brep`, `subd`, `mesh` | Corresponding Rhino.Geometry classes |
| `pointcloud`, `geometry` | Rhino.Geometry.PointCloud / GeometryBase |
| `hatch`, `textdot`, `textentity`, `leader`, `dimension`, `annotation` | Rhino.Geometry.Hatch, TextDot, TextEntity, Leader, Dimension, AnnotationBase |

Prefer curve for algorithms accepting any Curve subclass; polyline for a Polyline value; point for Point3d. A point value differs from a document Guid and a GH wrapper. Use number for continuous lengths and integer for counts; GH conversion can occur before Python sees the value. Use object when textual range input must reach a custom parser unchanged. Keep boolean semantics explicit rather than accepting arbitrary strings as truthy.

```python
INPUT_SPECS = [('Curve', 'Curve', 'Curve to divide', 'item', 'curve', True),
               ('Count', 'Count', 'Segment count; default 10', 'item', 'integer', True)]
OUTPUT_SPECS = [('Points', 'Points', 'Division points', 'list', 'point'),
                ('Debug', 'Debug', 'Current diagnostics', 'list', 'text')]
```

New outputs use `(Name, NickName, Description, Access, Hint)`. Legacy four-field outputs resolve to object for compatibility; migrate them deliberately when editing the interface. Inputs remain six-field specs. An explicit fully qualified CLR name (e.g. `Rhino.Geometry.Curve`), imported CLR class or System.Type is also accepted. This allows installed extensions without continually enlarging the alias dictionary; the assembly must already be available and **the component's hint set must accept it**. Not every CLR type has a selectable GH hint.

## Verify availability only when needed

Use `param.TypeHints.Select.Overloads[System.Type](clr_type)` for both input and output templates before any live port is removed. Explicit dispatch is essential: a user-reported Rhino Python runtime chose `Select(System.String)` for a System.RuntimeType when the overload was left implicit. Do not stringify the CLR type or silently fall back to object. None or an exception is a configuration failure. The installed 8.20 assembly exposes the Type overload, GetSelected and enumeration; behavior on a live component still requires GH validation. Explicit overload syntax follows the [Python.NET documentation](https://pythonnet.github.io/pythonnet/python.html#using-methods).

For a new runtime or an unsupported type, execute [inspect_type_hints.py](../scripts/inspect_type_hints.py) inside Rhino with Grasshopper loaded. It only constructs a temporary parameter and prints versioned JSON with Name/Id/Class and count; it does not add objects or change the canvas. Save the catalog once under project diagnostics, consult relevant entries, and do not reprint/re-enumerate the full list each turn. If no live access is available, use known built-in aliases and mark actual menu selection unverified.
