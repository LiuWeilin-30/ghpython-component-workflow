---
name: ghpython-component-workflow
description: Develop and maintain Rhino 8 Grasshopper Python 3 components through external .py loaders, wire-preserving automatic ports, DataTree-safe processing, agent-readable Debug outputs, and portable .ghuser packaging. Use for GHPython component development and workflow delivery.
---

# Grasshopper Python Component Workflow

Make the established development process reusable: official API lookup → editable workspace source → loader-driven GH iteration → stable ports and trees → readable diagnostics → tested, portable User Objects. Default new components to Rhino 8 Python 3; identify legacy GHPython/IronPython before modifying existing code.

This skill is the complete reusable workflow; no author-specific development guide, path, tool or protocol is required. Project instructions supplement it with local constraints. If no project guide exists, proceed using these references/assets and record the actual project decisions in `project-control.md`.

## Scope and environment

This skill targets Rhino 8 Grasshopper Python 3 component work. It does not install Rhino, configure a bridge, or authorize publishing. Assess legacy GHPython/IronPython separately. RhinoMCP or another live bridge is optional for source preparation, but live canvas inspection and packaging require actual available capabilities.

## Start with the user's project

Follow applicable AGENTS.md and project instructions. Use an existing authoritative guide rather than creating a competing one. For a new project, keep `project-control.md` at the root and all development code, loaders, tests and temporary packaging scripts under `tests/`, grouped by workflow. The control file records environment, workflow boundaries, source paths, accepted interfaces, test state and agreed release locations; it is not a transcript or a second copy of this skill. See [the new-project control template](assets/project-control-template.md). Do not relocate an established project merely to match this layout.

For an existing component, inspect its source, port definitions, loader if present, and relevant tests. Establish runtime, input access/type hints, units/tolerance, and the expected result from available artifacts. Ask only for missing information that materially changes implementation; do not require the user to complete an intake questionnaire.

Before editing, apply [maintenance.md](references/maintenance.md) for task-scoped backups/checks, environment reuse, shared-code synchronization and revision/cache identity. Read the relevant parts rather than loading all history or every component.

## Essential workflow

1. Verify unfamiliar or changed API calls using official RhinoCommon, RhinoScriptSyntax and Grasshopper SDK documentation, preferably the installed version's XML. Read [development.md](references/development.md) for geometry/runtime boundaries.
2. For iterative work, place a small loader in the Python 3 component and keep the full implementation, `INPUT_SPECS` and `OUTPUT_SPECS` in one stable workspace `.py`. The agent edits that file; a GH solve reads it again. Read [loader-and-ports.md](references/loader-and-ports.md) before setup or port changes and reuse the supplied [single-file starter](assets/component_starter.py). Do not make users repeatedly paste business code into GH.
3. Automatically configure ports on first session use and meaningful specification/parameter changes through a scheduled callback. Preserve compatible parameter objects and their wires. Revision/message changes are not reconstruction triggers. Exact timing, hints, migration rules and the two-solve initialization are in the loader reference.
4. Preserve input tree paths, meaningful grouping, item ordering and required empty branches. Do not append zero indices at each processing stage or simplify meaningful zeros. Read [data-and-debug.md](references/data-and-debug.md) for path construction and data contracts.
5. Add a `Debug` output early for repeatedly failing or predictably fragile components. Trigger a fresh solve and have the agent read the actual output through an available Rhino/GH bridge or a deterministic export. The data/debug reference defines the content and freshness checks.
6. Verify the component and its workflow with actual GH inputs when available. After test completion, ask whether to package and where to store that workflow's deliverables, unless already specified. Use **RhinoMCP** or another available bridge to embed the standalone source and create `.ghuser` objects through official GH APIs. Read [packaging-mcp.md](references/packaging-mcp.md) and [validation.md](references/validation.md). A workflow of separate User Objects also needs a connecting example `.gh`; `.ghuser` is not automatically a compiled `.gha` plugin or a complete workflow bundle.

## Conditional guidance

- Errors, wrong geometry, stale output, or damaged connections: read [troubleshooting.md](references/troubleshooting.md).
- Test design, performance comparisons, or release evidence: read [validation.md](references/validation.md).

Read only the relevant references. Simple explanations do not require inspecting an entire project or running geometry tests.

## Working principles

- Apply these workflow defaults unless the user or existing project directs otherwise. Existing release policies, protocols and backup requirements remain authoritative.
- Preserve working behavior outside the requested change. When the algorithm itself is wrong, fix it with a focused reproducer; preservation is not a ban on necessary algorithm changes.
- Keep each component within its agreed responsibility. Reuse infrastructure without embedding another component's complete business function unless requested. For large edits, use context-aware patches or AST-based replacement and inspect the resulting diff and syntax. See [development.md](references/development.md).
- Keep the complete component usage description at the top of its implementation `.py`; update it with interface/behavior changes. Do not create a separate per-component Markdown manual. Users should be able to open the source header to understand the component.
- Verify unfamiliar or changed API signatures against the installed RhinoCommon XML/documentation or official references. Do not invent a method from a similar API name. Record version-dependent assumptions.
- Distinguish geometry from display samples and manufacturing instructions. A visually acceptable approximation is not automatically acceptable for downstream fabrication.
- Do the checks available in the current environment. If Rhino/GH is unavailable, still deliver the useful implementation and a concrete in-GH test; state what remains unverified without claiming live execution.

## Delivery

Provide the changed artifact, the required port setup or existing loader path, and a short result describing what was verified and what remains to be exercised. Include units, tolerance, or approximation limits when they affect the result. Do not claim that the canvas was updated, a User Object was installed, or a machine path was validated without corresponding evidence.

After generating a component for loader-based development, provide its source link and the **complete ready-to-paste loader in a fenced Python code block**, with the real source path already substituted and correctly quoted. Use the chat/UI's copyable code-block facility; a path, downloadable file or statement that a loader exists is not sufficient. If code blocks are unavailable, present the full plain-text loader through an available copyable surface. Do not claim a copy button exists without evidence or require a separate browser/app solely for copying. See [loader-and-ports.md](references/loader-and-ports.md) and the bundled loader generator. For later same-path edits, remind the user to recompute; resend the loader when requested or its path changes.

## Official references

- [Grasshopper Python component, ports, marshalling and SDK mode](https://developer.rhino3d.com/guides/scripting/scripting-gh-python/)
- [RhinoCommon API](https://developer.rhino3d.com/api/rhinocommon/)
- [RhinoScriptSyntax API](https://developer.rhino3d.com/api/RhinoScriptSyntax/)
- [C# component reference for requested comparisons or migrations](https://developer.rhino3d.com/guides/scripting/scripting-gh-csharp/)
