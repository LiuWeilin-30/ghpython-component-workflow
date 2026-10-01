# External source iteration and automatic ports

## Set up once

Copy [component_starter.py](../assets/component_starter.py) to `tests/<workflow>/<component>.py`. Edit its descriptive header, specs and business function. Keep that path stable throughout iteration. All configuration and implementation live in this source; do not create a separate configuration JSON or runtime dependency on the skill installation.

The [loader_template.py](../assets/loader_template.py) contains the minimal loader as a copyable source asset. For an actual component, run [make_loader.py](../scripts/make_loader.py) using the confirmed Python interpreter, passing the implementation path as its positional argument and optionally `--output` for the loader file. It verifies the source exists, uses an absolute correctly escaped Python string, writes UTF-8, and prints the full loader. By default it writes a sibling `<component>_loader.py`. Do not create a separate loader file if an existing loader artifact already provides that role.

Put only this loader in a Rhino 8 Python 3 Script component, substituting the actual absolute workspace source path once:

```python
SOURCE_PATH = r"<absolute workspace path to the component .py>"
with open(SOURCE_PATH, "r", encoding="utf-8") as source_file:
    source = source_file.read()
exec(compile(source, SOURCE_PATH, "exec"), globals(), globals())
```

When delivering generated component code, replace the placeholder with the verified real source path and put the complete loader in a fenced Python code block in the user-facing response. Also link the implementation `.py` and, if created, the loader file. A file link alone makes the user open another artifact to copy; supply the actual code. Preserve spaces, Unicode and quotes through correct string escaping. If the agent placed the loader through MCP, still provide the copyable code for reuse and recovery; report actual canvas placement separately.

`globals(), globals()` exposes the component inputs and ghenv to the script and returns its output variables to GH. `compile` retains the source filename in tracebacks. This executes the source again on each solve; plain module import would need separate cache/reload management. Imported helper modules still have their own import cache. Saving a file is not itself a GH solve and this loader is not a file watcher.

Agent cycle: modify the same source → syntax/targeted checks → trigger a GH solve → allow scheduled port setup and its following solve to complete → read outputs and runtime messages → modify the same source again. The first user action may be adding a component and pasting the loader; with a working bridge the agent can do that setup too. Change the loader only when its source path changes. Do not repeatedly replace the component or paste business code.

## Declare ports

Inputs: `(Name, NickName, Description, Access, Hint, Optional)`.
Outputs: `(Name, NickName, Description, Access)`.

Use short PascalCase English names, usually `Data`, `Curve`, `Distance`, `Domain`, `Debug`; keep Name/NickName/VariableName aligned. Descriptions explain accepted values, units, defaults and effect. Internal Python variables need not follow port capitalization.

| Setting | Concrete choice |
| --- | --- |
| `item` | One item per invocation; consider GH data matching and repeated execution |
| `list` | One input branch per invocation; not automatically the whole tree |
| `tree` | Entire tree for topology-preserving or cross-branch operations |
| `object` hint | Structured packets, mixed objects, or values requiring deliberate parsing such as Panel text and Interval ranges |
| `number`, `bool`, `point`, `interval` | Use only when those conversions match the accepted input; starter supports these five hint names |
| `Optional=True` | Script runs with missing input; handle None and implement the documented default/idle behavior |
| `Optional=False` | Required input; GH may block execution before code runs when no data is available |

Use `object` for geometry when this starter has no dedicated geometry hint, then check/unpack the actual runtime value. Do not label a port curve-hinted unless that hint was implemented and selected successfully. Avoid an Interval hint for an input that must accept textual `0 to 2`; it may reject the text before the parser sees it.

## Update timing and connection protection

The starter embeds the project's existing generic port functions. Its geometry-free migration tests exercise parameter reuse and scheduling; actual GH marshalling/persistence still needs target-version validation. Do not rewrite these functions to rediscover the same decisions.

| Event | Behavior |
| --- | --- |
| New component, first solve in a session, or restored component with no in-session applied stamp | Validate specs; create templates and preflight both sides; queue configuration; skip business computation until the following solve |
| Number/order/name/access changes; Hint/Optional or descriptions change; parameter objects replaced | Queue one callback for the new specs/parameter stamp; reuse same-name or explicitly aliased parameter objects; then recompute |
| Same specs and parameter identities after configuration | No reconstruction and no new scheduling; the existing implementation reapplies display/Hint/Optional in place |
| Algorithm-only edit, component message or revision marker edit | Does not trigger port reconstruction; business code is still reread on the next solve |
| Identical configuration already pending | Do not queue a duplicate callback or compute against stale ports |
| Component detached or moved to another document before callback | Abort mutation; clear pending state |

Detailed mechanism:

- Track state per component InstanceGuid in the loader execution globals. The stamp includes full specs and port InstanceGuids; exclude component revision/message.
- At the top-level entry, use `_ensure_ports(ghenv.Component)` before business computation. If it returns False, leave initialized outputs and wait for scheduled configuration.
- Prepare **all** input/output templates with `RhinoCodePluginGH.Parameters.ScriptVariableParam`; validate both sides before unregistering anything. This class and `TypeHints.Select` are implementation-sensitive; retain target-runtime checks and verify against the installed Rhino 8 assembly.
- Use `document.ScheduleSolution(1, callback)` outside the current solve. Recheck the document, wires and persistent data in the callback; record an undo event.
- Match existing parameters by stable VariableName and explicit `PORT_ALIASES`, not only display position. A same-name input and output are separate sides. Reordering reuses the original parameter without isolating its wires. Duplicate/ambiguous aliases abort migration.
- Update Access, Hint and Optional even when names are unchanged. Preserve parameter objects, Sources, Recipients and persistent values. If deleting a port that still has wires or persistent data, report the blocked migration and propose a fresh component or an explicit migration; never silently discard it.
- Call `Params.OnParametersChanged()` and `VariableParameterMaintenance()`, save the applied stamp, then `ExpireSolution(False)` within the scheduled callback. The scheduled solution runs after it; do not recursively call `NewSolution` during a solve.
- A preflight protects ordinary migration failures, not an atomic rollback of every possible registration failure. Keep an undo/snapshot before structural changes and report any callback error.

Required inputs deserve attention: if GH refuses to execute because an old required input is empty or a type hint rejects its data, the loader cannot repair ports until execution is possible. Supply compatible initialization data, repair that blocking setting through the bridge/UI, or use a fresh component. Do not promise that scheduling inside a script can bypass a script that never runs.

When an input and output share a name, capture the input value before initializing that output. Initialize every result each execution so removed names and previous successful outputs are not mistaken for current results. Explicit caches must identify stale results.

## Confirm setup

Check a blank component first, then an already connected component. Verify initial configuration, a Hint/Optional-only change, an algorithm-only change, repeated solves, preserved wire identities and save/reopen. The starter's Data tree pass-through can confirm branch paths and item counts before adding a geometry algorithm. Do not call syntax checks or substitutes actual GH acceptance.

The bundled [check_starter.py](../scripts/check_starter.py) runs with the confirmed Python interpreter and only the standard library. It contains 7 existing port migration tests and 1 loader-cycle test covering nonzero paths, an empty branch, source-marker changes without reconstruction, fresh Debug tokens and clearing results on failure. They use substitutes, not a running GH instance.
