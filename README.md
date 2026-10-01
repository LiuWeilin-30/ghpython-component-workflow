# GHPython Component Workflow

A reusable agent skill for developing and maintaining Rhino 8 Grasshopper Python 3 components. It guides an agent through external-source iteration, connection-preserving port changes, DataTree handling, readable diagnostics, and portable User Object delivery.

## Requirements

- An agent environment that supports local Agent Skills, such as Codex.
- Rhino 8 with Grasshopper Python 3 for live component execution and verification.
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
ready-to-paste loader, and preserve compatible ports and connections.
```

For existing components, provide the implementation or loader path and describe the expected behavior. Existing project instructions, interfaces, and release policies remain authoritative.

The agent edits the external implementation; recomputing the Grasshopper component reloads it. After verification, portable delivery embeds standalone source into `.ghuser` objects. A workflow of multiple objects also needs a connecting `.gh` example. A User Object is not a compiled `.gha` plugin.

## Files

| Path | Purpose |
| --- | --- |
| [SKILL.md](SKILL.md) | Agent entry point, metadata, workflow, and reference routing |
| [agents/openai.yaml](agents/openai.yaml) | Display information and invocation policy |
| `references/` | Detailed development, maintenance, diagnostics, and packaging guidance |
| `assets/` | Component starter, loader template, and project-control template |
| `scripts/` | Loader generator and focused helper checks |

`README.md` explains installation and use; `SKILL.md` contains the instructions the agent loads. Upload both files at the repository root, alongside the supporting folders.

The helper checks cover loader behavior and simulated port handling. They do not replace live Rhino/GH verification. No author-specific project guide or machine path is required.

## License

The GitHub repository is distributed under the MIT License. See its [LICENSE](https://github.com/LiuWeilin-30/ghpython-component-workflow/blob/main/LICENSE).
