# Diagnose the smallest failing boundary

Start with one failing input and a known expected result. When a component previously worked, compare with a known working artifact and separate algorithm changes from loader, conversion, port and output-mapping changes. Historical examples are evidence about their original case, not universal parameter defaults.

| Symptom | First useful checks |
| --- | --- |
| Changed file has no effect | Actual loader path; explicit source encoding; whether a new solve occurred; Run gate and cache. Saving a file alone need not expire a component. |
| Chinese source raises a decoding error | Read source explicitly as UTF-8 when that is its actual encoding; inspect the loader before changing business logic. |
| Python code is valid but GH input fails | Runtime type, wrapper/Guid conversion, type hint, Item/List/Tree access, missing optional input. |
| Output count equals input despite intended splitting | Cutter types and intersection/split results; confirm the algorithm was reached with valid geometry. |
| Connections disappear after updating or reopening | Port recreation, renamed internal variables, changed access and parameter identity; a changed display message should not recreate ports. |
| Old output remains after a failure | Cache policy and solve status; stale geometry is not evidence of success. |
| Region creation misses some boundaries | Closedness, planarity, self-intersections and model tolerance; preserve rejected inputs for diagnosis. |
| Curves become straight in preview or export | Which consumer reads Curve versus Points; sparse endpoints may encode attributes rather than shape. |
| Component is slow | Solve count, geometry size, sampling density, repeated API calls, output capture and viewport generation; time stages before changing language. |

Inspect intermediate counts, types and geometry validity close to the failure. Use runtime messages for actionable errors and bounded diagnostics for large inputs. Avoid dumping every point or rebuilding the whole chain when a small case reproduces the problem.

If a fix depends on an approximation, make its error criterion explicit. Keep preview resolution separate from geometric or manufacturing tolerance. If no valid result is available, follow the component's documented clear/retain policy and communicate the failure; never present retained cached output as a successful current solve.

For cross-component regressions, reproduce at both sides of the boundary: what the producer emits and what the consumer actually reads. Add a regression for the observable result, not just the presence of a metadata field.
