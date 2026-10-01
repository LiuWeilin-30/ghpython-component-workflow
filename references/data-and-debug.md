# Preserve structure and make failures readable

## Tree structure

Treat paths as semantic identifiers, not nesting depth produced by Python containers. With Tree access, construct an explicit `DataTree[object]` and reuse each original GH_Path for one-to-one processing. Use `EnsurePath(path)` for a required empty branch; add results to that branch in intended order. Do not implicitly convert repeatedly nested lists into a tree if the wrapper will add meaningless dimensions.

Avoid growing `{1;2}` into `{1;0;0;0;0;2}` merely because data passed through four components. Do not append an index for each function call, wrapper or stage. When genuinely adding a grouping dimension, define its meaning once and maintain a stable schema. Prefer GroupId/Role metadata for provenance that does not require a tree dimension.

Zero is a valid semantic index. An existing `{1;0;0;0;0;2}` might be meaningful: do not strip all zeros, Flatten or Simplify paths blindly. If historical padding is demonstrably meaningless, define an explicit collision-checked mapping, preserve provenance and validate all consumers before migrating. Merging `{1;0;2}` with `{1;2}` by simplification can destroy grouping.

Preserve input paths, item/branch order, independent groups, required empty branches and source identifiers unless the requested algorithm changes them. Test a nonzero path such as `{1;2}`, an empty branch and multiple groups. Read resulting path indices, not only a viewport screenshot. For explicit reordering/repartitioning, document the mapping and downstream expectations.

Keep authoritative curves, attribute samples and display meshes distinct. Sparse Points may encode attributes while Curve contains the real arc. Editing a curve invalidates derived parameters, arc records, lengths or caches unless updated. A viewable preview is not proof of valid machine output.

## When to add Debug

Add a `Debug` output when repeated modifications have failed to explain the result, or before implementing likely failures: boolean/offset/split degeneracies, tiny geometry near tolerance, ambiguous wrappers, complex tree/attribute transfers, or large inputs with expensive search/preview. Prefer an explicit List/object output with bounded strings or JSON records the bridge can reliably read. Do not wait for more blind algorithm rewrites.

Include:

- Unique solve/run token and source marker; success, failure, skipped configuration or cache status.
- Input runtime types, units/tolerance, branch paths/counts and item counts.
- Stage name, intermediate counts, rejected indices/paths and a concise reason.
- Relevant distances/deviations, timing and approximation decisions.
- Exception type/message and bounded traceback with source filename/line.

Initialize Debug on every execution, including failures. Never output only `failed` or thousands of unbounded points. Use summary counts plus bounded samples; omit private file contents unrelated to the case. Add a GH Runtime Message for actionable failure as well as Debug details.

## Agent reads the result

Identify the target component InstanceGuid, trigger a fresh solve, wait for scheduled configuration if needed, then read that instance's Debug output through the connected bridge's actual output-reading capability. Verify the run token/source marker, paths/counts, status and messages. Do not treat an MCP success envelope or an old Panel/cache as a successful solve.

If output-reading tools are unavailable but in-Rhino script execution is available, inspect the target output's VolatileData and write a bounded UTF-8 JSON diagnostic under `tests/<workflow>/diagnostics/`; then read that file. GH objects must be inspected in the appropriate Rhino/GH thread context. If neither route is available, ask for the Debug text or provide exact retrieval steps; do not invent output.

Run gates and caches must say whether data is current, retained or cleared. If cached geometry remains after a failure, the new Debug still reports the failure. Remove pure debugging ports during final packaging unless the user explicitly wants supported diagnostic behavior; perform this removal in a fresh packaging component so connected development instances are preserved.
