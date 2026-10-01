# Related work and implementation context

Research checked on 2026-10-01. This is a bounded comparison of public examples, not an exhaustive code-similarity audit or a determination of authorship.

## External source execution

- [McNeel forum: RhinoScriptSyntax vs RhinoCommon](https://discourse.mcneel.com/t/rhinoscriptsyntax-vs-rhinocommon/74690?page=2). A 2021 post describes feeding a `.py` file through the Python component's Code input; a 2023 contribution discusses executing remotely read source with `exec`.
- [EPFL IBOIS Script-sync](https://github.com/ibois-epfl/script-sync) and its [2024 author discussion](https://discourse.mcneel.com/t/connect-vscode-to-rhino-grasshopper/172328). The project connects VSCode scripts to Rhino/GH. The discussion identifies `exec(code, globals, locals)` in its GH implementation. This review checked the repository overview and forum excerpt, not a full audit of that project's source.

This repository uses a small filesystem loader that runs on each GH solve. It does not add file watching or an editor transport. Its shared namespace gives executed code access to GH input variables and makes result variables available to the component.

## Dynamic parameters

| Public example | Relevant mechanism |
| --- | --- |
| [yuhan0, auto_annotate.py, 2018-04-04](https://gist.github.com/yuhan0/3c6ef309ef3205e972ac6eeaed32383c) | Ensures named inputs exist, configures hints/access, schedules callbacks, and checks connections before removing default parameters. |
| [Creating inputs dynamically, 2023](https://discourse.mcneel.com/t/creating-inputs-dynamically-based-on-the-value-of-the-inputs/165390) | Discusses parameter changes outside the current solution and avoiding repeated update cycles. |
| [OBucklin, Generate inputs to Python components, 2024-02-16](https://discourse.mcneel.com/t/generate-inputs-to-python-components/156921/6) | Provides parameter addition/removal code driven by input metadata. |
| [McNeel, programmatic script-component creation, 2025](https://discourse.mcneel.com/t/programmatically-creating-new-c-python-script-components/199692) | Documents Rhino 8 script parameters, type-hint selection, variable-parameter maintenance and signature-based parameter updates. Also explains that connections are stored on parameter objects. |

## This package's design

The starter combines explicit input/output declarations, parameter identity stamps, scheduled updates, name/alias matching, parameter reuse during reordering, two-sided preflight, callback-time checks, undo recording and current-run diagnostics. It separates port configuration from business computation and keeps the implementation in one external source file during development.

These are engineering choices in a reusable workflow. External loading, automatic port creation, scheduling and retaining connections through parameter reuse are not claimed as first inventions. No single complete implementation matching all of this package's details was identified in the sources reviewed; that does not establish uniqueness.

## Attribution scope

The links record related work found during review. They do not establish that the bundled implementation was derived from those projects, nor do they certify its complete historical provenance. Similar API calls alone are not evidence of copying. Linked projects retain their own licenses; this repository's license does not relicense their code. Contributors adapting third-party code must document its source and retain required notices.
