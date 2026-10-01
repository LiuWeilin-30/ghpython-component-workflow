# First working component

Use once per new environment; subsequent edits only need the component header and target function. Rhino 8 with Grasshopper Python 3 and a skill-capable AI client are required. MCP is optional. The helper scripts require Python 3.8+ and the standard library; use a working interpreter, not an OS store launcher. They do not require Rhino imports.

## Generate, place, test

1. Choose a writable workspace that **Rhino can also read**. Run with your actual skill folder and helper interpreter:

   ```text
   python "<skill>/scripts/create_component.py" "<workspace>/tests/curve-divide/curve_divide.py" --example curve-divide
   ```

   The tool creates a complete source and sibling loader, refusing existing files. AI returns the source link and full printed loader. For a tree-only baseline, use `--example tree`. Run tools directly; do not read or paste their full implementation into the conversation.
2. Place a fresh **Python 3 Script** component in GH (Maths / Script). Open its editor, replace the default code with the complete loader, save/run, and let the scheduled port update and next solve finish. The curve example should show inputs `Curve` (Item, curve), `Count` (Item, integer), and outputs `Points` (List, point), `Parameters` (List, number), `Debug` (List, text). Empty Curve intentionally reports `waiting`.
3. Connect a line from `(0,0,0)` to `(10,0,0)` to Curve and integer `5` to Count. Points must be `(0,0,0)`, `(2,0,0)`, ..., `(10,0,0)`: six points. Connect Points to a Point parameter and Debug to a Panel. Debug should say `ok` with a new RunToken. Parameters are native curve parameters, not necessarily 0,2,4,... .
4. Set Count to `2`: expect three points at x=0,5,10. Use a circle with Count=4: expect four distinct points at quarter-arc intervals, without a duplicate seam. Count=0 should produce an error and clear geometry; disconnecting Curve should return to `waiting`.
5. Ask AI to change `COMPONENT_MESSAGE`, then explicitly force recomputation (GH Solution menu / Recompute). Confirm the new message and run token, unchanged port identities and connections. Saving the `.py` alone is not a file watcher.
6. Save/reopen the test GH definition and recompute. Confirm correct ports and outputs, and verify that the loader path still exists. Record Rhino build and completed checks once in the project control file.

This is an acceptance recipe, not a claim that these GH checks ran on the user's machine. The source header documents behavior; do not create another component manual. A boolean region difference is better as a later example because coplanarity, closure and tolerance complicate diagnosing setup failures.

## Paths across machines

The generator validates the source on the **agent host** only. If Rhino uses another filesystem, supply `--rhino-source "<absolute path on Rhino host>"` and arrange a shared mount or explicit synchronization. That argument changes the loader string; it neither copies files nor proves Rhino access. Confirm the same source marker and fresh run token after the first solve. Prefer a shared writable folder; do not keep editing an unsynchronized local copy. Do not use the agent's Linux/container path in a Windows Rhino loader.

## If first setup fails

- File-not-found: verify the Rhino-side path, permissions and shared/synchronized source.
- Old ports remain: ensure the script actually runs; an old Required input or incompatible hint can block execution. Use a fresh component if appropriate.
- Unsupported Type Hint: inspect only that runtime's catalog using [type-hints.md](type-hints.md); do not silently use object.
- No bridge: user pastes the loader and returns bounded Debug text; AI can still edit and test pure logic. Do not install or reconnect MCP unless requested.

Offline helper checks (run when modifying infrastructure, not on every algorithm edit):

```text
python "<skill>/scripts/check_loader.py"
python "<skill>/scripts/check_starter.py"
python "<skill>/scripts/check_examples.py"
```
