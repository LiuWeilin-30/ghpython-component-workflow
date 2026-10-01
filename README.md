# GHPython Component Workflow

[English](README.md) | [简体中文](README.zh-CN.md)

A reusable agent skill for developing and maintaining Rhino 8 Grasshopper Python 3 components. Its two main advantages are **linking external Python source into GH for faster edit-and-test cycles**, and **having AI generate port and input data type configuration to save manual setup in the Python 3 Script component**.

## Two main advantages

### 1. Link external source into GH for faster testing

Paste a short loader pointing to an external `.py` file into the Python 3 Script component once. AI edits the full implementation in that file; recomputing the GH component reads and executes the latest code. You no longer need to open the component editor and paste the entire implementation after every change.

**Set up the loader once → AI edits the same source → recompute GH → inspect results and iterate.** The loader stays unchanged while the source path remains the same, making repeated debugging and testing easier. This link loads source through a file path; saving the file alone does not trigger a GH recompute.

### 2. Let AI configure ports and input data types

Describe the data the component should accept and the results it should produce. AI generates `INPUT_SPECS` and `OUTPUT_SPECS` in the source, and the component script automatically creates or updates the input and output ports and applies their settings:

- **Port names and descriptions:** names, nicknames, and purposes for inputs and outputs.
- **Types on both sides:** match every input and output to a Type Hint, including object, number, integer, bool, text, point, curve, brep and mesh.
- **Data access:** Item, List, or Tree access to match the processing logic, plus whether inputs are optional.

This saves manually adding or removing individual ports, renaming them, and clicking through input type and access settings in the Python 3 Script component. When the interface changes, AI updates the source specifications; after execution, the script schedules the port update and preserves compatible ports and connections. Initial setup usually means placing a component and pasting the loader; with an available bridge, AI can perform that step too.

The skill also covers DataTree handling, readable diagnostics, and portable `.ghuser` User Object delivery.

Inspection of the local Rhino 8.20 assemblies identified **35 built-in semantic hint categories**. The starter includes corresponding aliases plus explicit CLR type support. This is not a fixed total for all GH versions, plugins or Python menus: selection is checked against the actual component and unsupported hints fail explicitly. See [type coverage](references/type-hints.md).

## First component: divide a curve into points

After installation, give AI a workspace Rhino can also read and ask:

```text
Use $ghpython-component-workflow to generate the equal-arc-length curve example
in my workspace using create_component.py. Configure Curve and Count inputs;
Points, Parameters and Debug outputs; match types on both sides. Give me the
source link and complete pasteable loader. Explain the length-10, 5-segment check.
Deliver source and loader first; no MCP or ghuser packaging is needed.
```

Paste the loader into a fresh Python 3 Script component and allow automatic setup and its following solve to finish. Connect a line from (0,0,0) to (10,0,0), Count=5: expect six points at x=0,2,4,6,8,10. Closed curves omit the duplicate seam point. See [quickstart](references/quickstart.md) for exact setup, troubleshooting and save/reopen acceptance.

This example avoids the planarity, closed-region and Boolean tolerance prerequisites of region difference. Generated source headers contain component usage.

## Keep token use focused

- Route by task: an algorithm edit reads the header, specs and target function, not every reference.
- Generate shared helpers directly; AI need not rewrite, echo or reread boilerplate each time.
- Reuse known environment, path mapping and hint catalogs; enumerate only for a new runtime or unsupported type.
- Same-path updates only need a recompute reminder, not repeated loaders, full source or packaging instructions. Run relevant tests.

These reduce repeated work; no fixed token-saving percentage has been measured.

## Requirements

- An agent environment that supports local Agent Skills, such as Codex.
- Rhino 8 with Grasshopper Python 3 for live component execution and verification.
- A working Python 3.8+ interpreter for generation/offline checks; those helpers use only the standard library.
- AI and Rhino must read the same current source. Remote/container setups need shared access or synchronization; `--rhino-source` supplies the Rhino-side absolute path but does not transfer files.
- A configured Rhino/GH bridge, such as RhinoMCP, when the agent needs to inspect or operate a live canvas. The skill does not install or connect a bridge automatically.

Legacy GHPython/IronPython components require runtime-specific assessment before changes. Without Rhino/GH access, the agent can still prepare code and test instructions, but cannot confirm live geometry or packaging results.

## Install in Codex

Download this repository and keep its files together in a folder named `ghpython-component-workflow`. Place that folder in either:

- `~/.agents/skills/` for personal use across projects.
- `<project>/.agents/skills/` for a project-specific skill.

The installed entry must be `ghpython-component-workflow/SKILL.md`. Do not rename it to `README.md` or copy it without its supporting folders. If the skill does not appear, restart Codex.

Alternatively, ask Codex's `$skill-installer` to install the skill from [this repository](https://github.com/LiuWeilin-30/ghpython-component-workflow). See the [official skill documentation](https://learn.chatgpt.com/docs/build-skills) for discovery locations and installation guidance.

## Use

Example prompt:

```text
Use $ghpython-component-workflow to develop a Rhino 8 Grasshopper Python 3
component. Keep its implementation in a workspace .py file, provide a
ready-to-paste loader, and automatically configure input/output ports,
type hints on both sides, Item/List/Tree access, and optional inputs for the task.
Preserve compatible ports and connections.
```

For existing components, provide the implementation or loader path and describe the expected behavior. Existing project instructions, interfaces, and release policies remain authoritative.

The agent edits the external implementation; recomputing the Grasshopper component reloads it. After verification, portable delivery embeds standalone source into `.ghuser` objects. A workflow of multiple objects also needs a connecting `.gh` example. A User Object is not a compiled `.gha` plugin.

## Files

| Path | Purpose |
| --- | --- |
| [SKILL.md](SKILL.md) | Agent entry point, metadata, workflow, and reference routing |
| [agents/openai.yaml](agents/openai.yaml) | Display information and invocation policy |
| `references/` | Detailed development, maintenance, diagnostics, and packaging guidance |
| `assets/` | Shared starter, curve-division body, loader and project-control templates |
| `scripts/` | Component/loader generators, on-demand hint catalog and focused checks |

`README.md` explains installation and use; `SKILL.md` contains the instructions the agent loads. Upload both files at the repository root, alongside the supporting folders.

The helper checks cover loader behavior and simulated port handling. They do not replace live Rhino/GH verification. No author-specific project guide or machine path is required.

## License

MIT License, Copyright (c) 2026 LiuWeilin-30. The license travels with the skill folder; see [LICENSE](LICENSE).
