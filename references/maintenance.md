# Maintain components without a personal project guide

Use this reference with the bundled development, loader/port, data/debug and packaging guidance. Local guides contain paths, domain contracts and release choices; their absence must not block development.

## Scope the work and its evidence

| Change | Read and preserve | Checks |
| --- | --- | --- |
| Documentation only | Target documents and recoverable originals | Accuracy, references and consistency; no unrelated geometry tests |
| One component | Source header/specs, changed implementation and relevant tests; preserve affected files | Parse/compile and focused behavioral checks; actual GH checks when ports, marshalling or geometry changed |
| Shared helpers, packet contract or multiple components | Producers, editors and consumers affected; snapshot source, loaders and needed fixtures before mutation | Shared-code/port checks and affected-chain regression; expand to full project verification when the shared contract requires it |
| Packaging/release | Accepted source and representative workflow cases; preserve prior release | Fresh-component, standalone dependency, ports, connections and save/reopen verification described in packaging guidance |

Keep snapshots or version-control history recoverable; exclude backup directories and caches from normal test/component discovery. For a batch snapshot, retain relative paths and a file/hash manifest when needed for reliable comparison. A backup is not a second live implementation.

Do not reread unchanged rules or historical reports every turn. Read component usage from the source header. Plans describe unimplemented work; historical results describe that batch and cannot prove a current run. Report code/document discrepancies rather than changing prose to pretend a defect was fixed.

## Confirm the environment once

Establish the target Rhino/GH/Python runtime and a usable test interpreter, then record and reuse them. Do not require the author's executable path, or repeatedly probe a confirmed environment. Distinguish the helper/test interpreter from the in-GH runtime and know which tests need Rhino-loaded assemblies. A Python executable on PATH may be a Windows Store stub or the wrong environment.

For complex PowerShell operations or multiline Python transformations, use a script file and correctly quoted arguments; avoid inline commands whose pipes, substitutions or encodings change the script. Invoke the confirmed interpreter explicitly when the environment needs it. Rerun detection only when its assumptions change or fail.

## Shared helpers and standalone delivery

For multiple independent components using the same infrastructure, maintain one development source for those helpers. Embed its selected functions into each component at development/build time when single-file delivery is required; do not leave a runtime dependency on the development tools directory or skill installation.

Synchronize every affected component when the shared helper changes. Use AST-directed function replacement, compare the embedded implementation with the authoritative helper, and keep component-specific algorithms separate. A repeated synchronization with unchanged helpers must not change files or increment revisions. The skill supplies a reusable port starter; project-specific synchronization tools are optional, not prerequisites for a first component.

Prefer machine checks for port names, Access, Hint/Optional, loader paths and embedded-helper drift over maintaining a duplicate manual checklist. If the project generates an inventory, regenerate it only when its recorded files/interfaces change. Batch diff reports are for relevant audits, not mandatory on every solve. Do not claim a synchronization/check tool exists unless it is actually available.

## Component identity and cache freshness

Use one internal `COMPONENT_MARKER` containing stable component identity and revision for each source, as in the starter. Preserve known counts; increment once per completed modification round, not on every save, retry or packaging step. Do not invent historical counts. Distinguish experimental implementations with distinct identities.

Keep the displayed `COMPONENT_MESSAGE` concise, normally two or three functional lines. Revision identity is for source/Debug/cache tracking and must never trigger port reconstruction. When a cache depends on source revision, refer to the same marker rather than maintaining a second hardcoded version. A run token identifies a solve, while the source marker identifies the implementation; neither proves geometric correctness.

Initialize outputs and diagnostics consistently and document each component's retain/clear policy. Reused cached results must be labeled with their source/input validity and stale status after failure. Do not assume every component in a workflow follows the same cache policy.

## Release maintenance

Keep accepted delivery artifacts separate from active tests and retain their release baseline. Develop fixes in the test workspace, revalidate, and publish according to the agreed update policy. Do not directly edit or overwrite a frozen release. Projects that permit replacement still need a recoverable prior artifact and deliberate release action; no specific personal release directory or naming convention is required.

Reorganization alone should not rename/move an existing implementation and break its loader. Draft text, old diagnostics and an earlier test count are not validated current source. Do not introduce versioned filename copies on every edit; use a stable active path and the project's release/history mechanism.
