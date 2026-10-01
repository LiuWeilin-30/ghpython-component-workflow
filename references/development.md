# Component development decisions

## Large edits

Read the current target functions, specs and relevant tests before replacement; retain a recoverable baseline. Use precise context-aware patches for bounded changes and AST-based function/assignment selection for large generated transformations. Do not use broad line-number slicing that can remove neighboring code when offsets change. For transformations replacing more than 200 lines, use AST-directed selection/replacement and parse/compile the result; honor stricter project rules.

Match the intended symbol uniquely and stop if the match is missing or ambiguous. Preserve decorators and adjacent definitions; AST positions are a locator, not permission to rewrite the whole module. After editing, parse/compile the entire resulting file, inspect the diff for unrelated deletions or altered ports, and run the relevant behavioral tests. A successful parse alone does not establish preserved behavior. Put complex transformation code in a script file rather than a fragile multiline shell argument.

## Component responsibility

Keep the component's accepted input, transformation and output responsibility explicit. Do not copy, embed or call another component's entire business function just to make the current result look complete, unless the user requests that integration. For example, a slicer should not silently absorb grouping, infill scheduling or machine export. Connect those components through the workflow instead. Shared port configuration, input conversion and protocol validation are reusable infrastructure and do not constitute business-function merging.

For an authorized boundary change, identify affected producers and consumers and verify the connecting workflow; do not silently expand the task while fixing a local error.

## Source header as the component manual

The implementation `.py` is the authoritative per-component usage document. Put a complete, readable module docstring first, before imports and implementation. Include:

- Component name, purpose, supported Rhino/GH/Python runtime and responsibility.
- Every input: name, Item/List/Tree access, accepted type/hint, required/optional behavior, default, units and effect.
- Every output: name, access, meaning and grouping/path semantics.
- Tolerance and geometric assumptions, approximation/error criteria, unsupported cases and limits.
- Run/recompute behavior, failure/cache policy, Debug use and warnings that affect operation.
- Development loader versus standalone packaging status, intentional dependencies and actual verification level.

Update this header, INPUT_SPECS/OUTPUT_SPECS and port descriptions together whenever the interface, behavior or limitations change. Compare documentation to the actual implementation; do not resolve a code defect by changing only the description. Keep the header current rather than accumulating a revision diary. Use the user's documentation language; the distributed skill/templates remain English.

Do not create or maintain a separate `<component>.md` manual merely to explain a component. Link users to the implementation `.py` so opening its header is enough. Workflow-level notes may describe how components connect, but should refer to source headers instead of duplicating individual manuals. This is a forward-looking authoring rule: do not bulk-delete or migrate legacy manuals as part of an unrelated component task.

## Runtime and ports

Rhino 8 Python 3 and legacy IronPython components differ in Python syntax, available packages and .NET interoperation. Confirm the actual component/runtime when migrating; do not combine snippets from both environments without checking conversion behavior.

Describe each input by name, Item/List/Tree access, type hint, optional/default behavior, and units where relevant. In Grasshopper, Item access can invoke the component repeatedly through data matching; List access supplies a branch, not necessarily the entire input tree. Tree access preserves the whole tree. Changing access can change execution count and output structure, not just the Python type.

For this loader workflow, configure ports automatically using the supplied starter and the exact [port rules](loader-and-ports.md). Prefer the project's existing conventions when modifying an established component. Do not replace automatic configuration with repeated manual port setup merely because a component is small.

## Geometry and API boundaries

Use RhinoCommon geometry objects directly for object-based GH algorithms where appropriate. RhinoScriptSyntax remains useful, but check whether each operation expects document IDs, adds document objects, or depends on scriptcontext.doc. If switching document context is necessary, restore it in finally; do not accidentally bake temporary geometry.

Inspect actual input types before writing conversion code. A Curve, GH wrapper and Guid require different treatment. Unwrap only the supported types and resolve IDs against the correct document; do not silently coerce every unknown input into a guessed geometry.

For each unfamiliar API call, verify overload arguments, collection types, return values, failure result and supported runtime. A short real-kernel probe is often more useful than a large mock reproducing an assumed signature. Link the authoritative method reference when the choice is material.

Set tolerance from the user's requirement or the established model context, with explicit units. Check whether an operation requires closed, planar, consistently oriented curves. A failed Join/Split/Offset should produce a diagnosable result, not a secretly tightened tolerance or arbitrary endpoint repair.

Do not silently relax process constraints such as clearance, wall dimensions or support distances to obtain a result. Describe rescue, approximation and degraded outputs with their measured limits; a computed output is not necessarily compliant with the requested constraints.

## Trees and cross-component data

Preserve GH_Path identity when branches carry semantic grouping; flatten only when intended. Explicitly create required empty branches. Distinguish no input, an empty branch, an invalid item, and a valid operation producing no geometry.

For structured component chains, identify producer and consumer expectations before changing fields. Determine which representation is authoritative: analytic curve, polyline, sampled points, per-point attributes, or machine moves. If geometry changes, update or invalidate dependent parameters, arc records, lengths and caches. Do not assume sparse attribute points define the full curve.

## Reusable code without new coupling

Reuse a tested project helper before introducing another wrapper. Keep geometry operations separate from input conversion and GH output wiring when that simplifies testing. Use external modules, embedded helpers or build-time code generation according to deployment needs; single-file packaging is not mandatory for every project.

When saving a reusable example, include the supported runtime, minimal input, expected behavior, tolerance, failure behavior and actual verification level. Exclude personal paths, customer models and machine-specific process settings from shared examples unless explicitly intended for distribution.

## Performance and language choice

Measure representative inputs before proposing a rewrite. Separate solve multiplicity, Python loops, interop conversions, RhinoCommon calls and viewport mesh generation. First consider duplicate work, repeated closest-point searches, unnecessary resampling and oversized previews.

C# can help typed SDK integration and measured loop/interop hotspots. It does not automatically improve a geometry operation already dominated by the same Rhino kernel. Compare equivalent algorithms and output accuracy; do not trade away manufacturing tolerance to report a speedup. Migrate a bounded hotspot before proposing a full rewrite.
