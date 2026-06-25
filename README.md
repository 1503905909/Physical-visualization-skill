# 高中物理电磁学可视化 Skills

本仓库提供两个 Codex skills，用于生成高中物理电磁学可视化教学资源，重点面向人教版高中物理必修第三册和选择性必修第二册。

## 这两个 skills 是什么

| Skill | 作用 | 主要产物 | 适合场景 |
|---|---|---|---|
| `physics-interactive-sim-lab` | 生成交互式物理仿真 | 单文件 HTML，必要时也可生成 Streamlit 应用 | 课堂投影、学生拖拽探究、参数调节演示 |
| `manim-physics-animator` | 生成物理讲解动画 | Manim `.py` 脚本和 MP4 视频 | 课堂导入、过程讲解、公式关系演示、PPT 插入 |

两者可以配合使用：HTML 负责“让学生操作和观察”，Manim 负责“让教师分步讲清过程”。

## 怎么安装使用

把 GitHub 链接发给 Codex 后Codex解析安装。更稳妥的方式是把具体 skill 路径安装到 Codex 的 skills 目录，安装后重启 Codex。

如果 Codex 的界面支持从 GitHub 导入 skill，可以分别导入下面两个路径：

```text
https://github.com/1503905909/Physical-visualization-skill/tree/main/.github/skills/physics-interactive-sim-lab
https://github.com/1503905909/Physical-visualization-skill/tree/main/.github/skills/manim-physics-animator
```

如果使用 Codex 的 skill 安装脚本，可以按这种形式安装：

```bash
install-skill-from-github.py --repo 1503905909/Physical-visualization-skill --path .github/skills/physics-interactive-sim-lab .github/skills/manim-physics-animator
```

安装后重启 Codex，然后在对话中用自然语言触发即可。

## 典型用法

生成 HTML 交互资源：

```text
使用 $physics-interactive-sim-lab，生成一个高中物理必修第三册“电场线”交互式 HTML 可视化资源。要求展示正点电荷、负点电荷、等量异种电荷和等量同种电荷，支持场景切换、方向箭头显示和课堂观察问题。
```

生成 Manim 讲解动画：

```text
使用 $manim-physics-animator，生成一个高中物理“回旋加速器”课堂讲解动画。要求分步展示 D 形盒、垂直纸面的磁场、缝隙电场加速、轨道半径增大和周期公式，并渲染预览视频。
```

同时生成配套资源：

```text
请分别使用 $physics-interactive-sim-lab 和 $manim-physics-animator，为“带电粒子在匀强电场中的运动”生成一个 HTML 交互资源和一个 Manim 讲解动画。HTML 用于学生调参观察，Manim 用于教师讲解运动分解。
```

## 项目结构

```text
Physical-visualization-skill/
├── .github/skills/
│   ├── physics-interactive-sim-lab/    # 交互式 HTML 仿真 Skill
│   │   ├── SKILL.md                    # Skill 定义与工作流
│   │   ├── agents/openai.yaml          # Agent 配置
│   │   └── examples/                   # 示例资源
│   └── manim-physics-animator/         # Manim 动画 Skill
│       ├── SKILL.md                    # Skill 定义与工作流
│       ├── agents/openai.yaml          # Agent 配置
│       └── examples/                   # 示例脚本
├── docs/                               # 论文附录与使用说明
│   ├── appendix_charged_particle_example.md
│   ├── physics-topics.md
│   └── setup-guide.md
├── build/                              # 构建产物（截图、视频帧等）
└── README.md
```

## 已包含示例

HTML 交互资源：

- `coulombs_law_html.html`
- `electric_field_lines_html.html`
- `electric_potential_equipotential_html.html`
- `charged_particle_uniform_field_html.html`
- `cyclotron_html.html`

Manim 动画资源：

- `coulombs_law.py`
- `electric_field_lines.py`
- `electric_potential_equipotential.py`
- `charged_particle_uniform_field.py`
- `cyclotron.py`

## 运行环境

生成 HTML 文件通常可直接用浏览器打开。

渲染 Manim 视频需要本地安装 Manim 和相关依赖：

```bash
pip install manim
```

如果涉及复杂公式或中文字体，需确认本机 LaTeX、中文字体和 Manim 环境可用。

## 示例详细说明（论文附录用）

如需将示例资源写入论文附录，可参考以下文档（含截图建议和操作说明）：

- [`docs/appendix_charged_particle_example.md`](docs/appendix_charged_particle_example.md) — 「带电粒子在匀强电场中的运动」HTML 仿真详细说明
## 教学资源设计思路

本仓库服务于“生成式人工智能辅助高中物理电磁学可视化教学资源设计”的流程：

1. 教师用自然语言提出教学需求。
2. Codex 根据 skill 工作流生成代码。
3. 在本地运行、预览、截图或渲染视频。
4. 教师检查物理科学性和课堂可读性。
5. Codex 根据反馈修改资源。
6. 形成可复用、可扩展的教学资源案例。
