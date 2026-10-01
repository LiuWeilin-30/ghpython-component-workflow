# Project Control

Use this template for a new workspace. If AGENTS.md or an authoritative development guide already exists, follow that entry point instead of creating competing instructions.

## Environment and Scope

Record the Rhino/GH version, Python runtime, available MCP bridge and live validation capabilities. Identify the workflow, each component's responsibility and dependencies. Reuse confirmed environment information instead of probing it every turn.

Record the agent-side source and Rhino-side path mapping, if different, and how they share/synchronize current contents. Keep a hint-catalog path/version only if it was actually inspected; no need to paste the catalog here. Mark MCP as unavailable or declined when appropriate.

## Files and Development

- Keep `project-control.md` at the project root. Place development source, loaders, tests, diagnostics and temporary packaging scripts under `tests/<workflow>/`.
- Give each component one complete `.py` file at a stable path, containing its description, INPUT_SPECS, OUTPUT_SPECS, port configuration and algorithm. A GH loader reads that file.
- After editing source, trigger a GH solve and inspect actual results. Saving alone does not guarantee recomputation.
- Keep recoverable backups proportional to the change. Do not create a numbered source copy for every edit.

## Interfaces and Data Contracts

Record accepted ports, units, tolerances, meanings of tree path dimensions, packet contracts and cache/failure policies. The skill supplies general methods; this file records project-specific decisions.

Every input and output has a deliberate semantic type/Hint and Access; inputs also declare Optional. Refer to source specs rather than duplicating large port tables.

## Validation and Delivery

Record representative cases, completed validation levels and pending checks. After testing, ask whether to package and confirm a workflow-specific delivery directory. Record and reuse the decision without asking repeatedly. Separate release artifacts from tests; replace existing releases only under the agreed policy.
