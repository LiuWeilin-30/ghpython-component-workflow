---
name: ghpython-component-workflow
description: Develop Rhino 8 Grasshopper Python 3 components with external-source loaders, automatically typed input/output ports, preserved connections and data trees, and optional portable ghuser delivery.
---

# Grasshopper Python Component Workflow

Keep implementation in a stable workspace `.py`; paste its small loader into GH once. AI edits the file, and a GH recompute reads it again. Automatically configure **every input and output**: name, description, Item/List/Tree access and an appropriate type hint; inputs also declare Optional. This skill is self-contained; the author's paths, project rules and MCP setup are not prerequisites.

## Read only what the task needs

| Task | Read / run |
| --- | --- |
| First component or unfamiliar setup | [quickstart.md](references/quickstart.md); run `scripts/create_component.py` |
| New ports, type changes or loader setup | [loader-and-ports.md](references/loader-and-ports.md); consult [type-hints.md](references/type-hints.md) for relevant types |
| Algorithm-only edit | Component header, specs and target function; reuse known infrastructure |
| Trees or diagnostic failures | [data-and-debug.md](references/data-and-debug.md), [troubleshooting.md](references/troubleshooting.md) as needed |
| Runtime/API, geometry or substantial edits | Relevant section of [development.md](references/development.md) |
| Shared helper changes, backups or release maintenance | Relevant section of [maintenance.md](references/maintenance.md) |
| Validation or requested packaging | [validation.md](references/validation.md); [packaging-mcp.md](references/packaging-mcp.md) only for packaging |

Do not load all references, tests, READMEs or templates each turn. Use the generator to copy tested infrastructure instead of reproducing it in chat. Inspect that infrastructure when changing it or diagnosing it. Reuse recorded runtime, source path and hint catalog; do not re-enumerate types or browse unchanged APIs for every component. Prefer bounded Debug summaries and focused tests. Read additional material when a failure or uncertainty requires it; token savings must not hide unverified behavior.

## Essential workflow

1. Follow applicable project instructions. Inspect an existing component's header/specs and preserve agreed behavior. For a new workspace, use `project-control.md` and `tests/<workflow>/`; the [control template](assets/project-control-template.md) records only environment, paths, interface decisions and verification state. Keep existing project layouts.
2. Confirm Rhino 8 Python 3 versus legacy IronPython, a usable helper interpreter, and whether Rhino can read the **same current source file**. Remote/container paths require explicit Rhino-side mapping or synchronization. A running Rhino does not prove an MCP connection. MCP is optional; provide manual steps when unavailable or declined.
3. Generate a standalone source plus loader with `scripts/create_component.py <source.py> --example curve-divide` (or `tree`). Keep the generated helpers; change the usage header, specs and algorithm. The example body alone is not a complete component. Preserve recoverable originals before edits; do not overwrite an accepted release.
4. Match type hints deliberately on both sides. Prefer Curve, Point3d, number, integer, bool, etc. when the contract requires those types; use object for genuinely mixed/custom data. Never silently fall back to object because a requested hint failed. The starter accepts aliases or explicit CLR types and verifies selection before changing ports. Legacy four-field outputs remain accepted as object; new outputs have five fields including Hint.
5. Schedule port changes outside the current solve, discard superseded callbacks and preserve compatible parameter identities, wires and persistent values. Revisions/messages alone do not rebuild ports. Wait for configuration and the following solve before evaluating output. Required/invalid old inputs can prevent the loader from executing; resolve that blocking input or use a fresh component.
6. Verify unfamiliar API signatures against installed XML or official Rhino documentation. Preserve meaningful tree paths and empty branches, distinguish geometry from display samples, and declare units/tolerance where relevant. Keep complete component usage in its source header, not a separate per-component manual.
7. Run checks relevant to the change. Use current Debug/source identity for fragile or repeatedly failing components. Distinguish offline tests, real Rhino geometry, live GH ports and save/reopen checks. If live access is unavailable, deliver the useful source and concrete manual acceptance steps; do not imply live verification.

## Delivery

Link the source and provide the **complete ready-to-paste loader in a fenced Python block**, with the actual Rhino-readable path substituted. A downloadable loader alone is insufficient. For later same-path edits, only remind the user to recompute; repeat the loader when requested or when its path changes. Report the result, relevant checks and remaining limits concisely; do not echo the entire source or standard workflow.

Package only when requested or already authorized. If useful after successful testing, ask once whether `.ghuser` delivery is wanted and where. Embed standalone source in a fresh packaging component; do not change connected development instances or assume `.ghuser` is a compiled `.gha`. Packaging details stay in the conditional reference.
