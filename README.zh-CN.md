# GHPython 组件开发工作流

[English](README.md) | [简体中文](README.zh-CN.md)

面向 Rhino 8 Grasshopper Python 3 组件开发与维护的可复用 AI skill。核心优势是：**以链接外部 Python 文件的方式在 GH 中运行组件，提高修改与测试效率；让 AI 生成端口及输入数据类型配置，省去在 Python 3 Script 电池中逐项手动设置的操作。**

## 两项核心优势

### 1. 外部源码链接到 GH，缩短修改与测试循环

首次使用时，在 Python 3 Script 电池中粘贴一段指向外部 `.py` 文件的加载代码（loader）。完整组件代码保存在该文件中，由 AI 直接修改；后续只需重新计算 GH 组件，就会读取并执行最新代码，无需每次打开电池编辑器、复制粘贴整段实现。

**一次置入 loader → AI 修改同一份源码 → GH 重新计算 → 查看结果并继续迭代。** 源码路径不变时，loader 无需更换，让连续调试与测试更方便。这里的“链接”是通过文件路径加载源码；保存文件本身不会自动触发 GH 重新计算。

### 2. AI 生成端口与数据类型配置，减少手动点击

描述组件需要接收什么数据、输出什么结果，AI 就会在源码中生成 `INPUT_SPECS` 和 `OUTPUT_SPECS`，由组件脚本自动创建或更新输入、输出端口，并应用相应设置：

- **端口名称与说明**：输入、输出的名称、简称和用途。
- **输入数据类型**：按需求配置受支持的 Type Hint，例如数值、布尔值、点或区间。
- **数据访问方式**：按处理逻辑配置 Item、List 或 Tree，以及输入是否可选。

无需在 Python 3 Script 电池中逐个增删端口、改名，再逐项点击设置输入类型与访问方式。接口变化时，AI 修改源码中的配置，脚本在运行后安排端口更新，并在兼容的情况下保留原有端口与连线。首次使用通常只需放置电池并粘贴 loader；具备可用桥接工具时，AI 也可以完成这一步。

此外，skill 还覆盖 DataTree 处理、可读诊断信息与可移植 `.ghuser` 用户对象交付。

## 环境要求

- 支持本地 Agent Skills 的 AI 环境，例如 Codex。
- Rhino 8 及 Grasshopper Python 3，用于实际运行与验证组件。
- 当 AI 需要检查或操作正在运行的画布时，需配置 Rhino/GH 桥接工具，例如 RhinoMCP。本 skill 不会自动安装或连接桥接工具。

修改旧版 GHPython/IronPython 组件前，需要先评估其运行环境。没有 Rhino/GH 访问能力时，AI 仍可准备代码和测试步骤，但不能确认实际几何结果或封装结果。

## 在 Codex 中安装

下载本仓库，将文件完整保存在名为 `ghpython-component-workflow` 的文件夹中，再将该文件夹放入以下任一位置：

- `~/.agents/skills/`：供个人跨项目使用。
- `<项目目录>/.agents/skills/`：仅供对应项目使用。

安装后的入口应为 `ghpython-component-workflow/SKILL.md`。请保留这个文件名及其配套目录，不要将它改名为 `README.md`，也不要只复制入口文件。如果安装后没有显示该 skill，可重启 Codex。

也可以请 Codex 的 `$skill-installer` 从[本仓库](https://github.com/LiuWeilin-30/ghpython-component-workflow)安装。识别目录与安装方式见[官方 skill 文档](https://learn.chatgpt.com/docs/build-skills)。

## 使用

示例提示词：

```text
使用 $ghpython-component-workflow 帮我开发一个 Rhino 8 Grasshopper Python 3 组件。
将实现保存在工作目录的 .py 文件中，提供可以直接粘贴的 loader，
根据功能需求自动生成输入、输出端口及输入类型、Item/List/Tree 和可选设置，保留兼容的端口和现有连线。
```

修改既有组件时，请提供源码或 loader 路径，并说明预期行为。已有项目规范、接口约定和发布政策继续适用。

AI 修改外部实现文件后，需要重新计算 Grasshopper 组件来加载新代码；保存源码本身不会触发重新计算。完成验证后，可将独立源码嵌入 `.ghuser` 用户对象，以便移植。多个用户对象组成的工作流还需要提供连接示例 `.gh` 文件。用户对象不等同于编译后的 `.gha` 插件。

## 文件说明

| 路径 | 用途 |
| --- | --- |
| [SKILL.md](SKILL.md) | AI 加载的入口、元数据、开发流程与参考文档导航 |
| [agents/openai.yaml](agents/openai.yaml) | 显示信息与调用策略 |
| `references/` | 开发、维护、诊断与封装的详细说明 |
| `assets/` | 组件模板、loader 模板与项目控制文件模板 |
| `scripts/` | loader 生成工具及相关检查脚本 |

`README.md` 和 `README.zh-CN.md` 分别提供英文与中文安装、使用说明；`SKILL.md` 保留英文，供 AI 加载。上传 GitHub 时，将这三个文件及配套目录一起放在仓库根目录。

辅助检查覆盖 loader 行为与模拟端口处理，不能代替实际 Rhino/GH 验证。使用本 skill 不需要原作者的个人项目规范或机器路径。

## 许可证

本 GitHub 仓库采用 MIT 许可证，详见 [LICENSE](https://github.com/LiuWeilin-30/ghpython-component-workflow/blob/main/LICENSE)。
