# 高中物理电磁学可视化

一套专为高中物理电磁学教学设计的 AI Skill，包括 Manim 动画生成和 html交互式仿真实验。

## 项目信息

| 项目 | 详情 |
|------|------|
| 主题范围 | 高中物理电磁学基础（第五-十四章） |
| 应用场景 | 教学演示视频、课堂现场实验、学生自主探索 |
| 预期输出 | 教学视频、交互工具、参考资源 |

## 安装使用

本项目的 Skill 可在 **Codex** 中直接安装使用。

将以下链接粘贴到 Codex 的 Skill 导入框即可：

```
https://github.com/1503905909/Physical-visualization-skill
```

安装后在对话中用自然语言触发：
- 说"帮我做库仑定律动画" → 自动触发 Manim 动画生成
- 说"生成一个欧姆定律交互实验" → 自动触发 Streamlit 仿真实验

---

## 两个核心 Skill

### Skill 1：Manim 物理动画生成器

制作高质量物理教学演示视频。

**使用场景**：PPT 教学内嵌视频、教学资源库、学生预习视频

**输出**：MP4 视频文件

**特点**：分步骤展示公式推导、彩色强调物理量、适合高中生理解

### Skill 2：Python 交互式物理仿真实验

课堂现场演示和参数探索工具。

**使用场景**：课堂实时演示、学生参数调节验证规律、探索型学习

**输出**：Streamlit 网页应用

**特点**：实时参数调整、动态图表反馈、直观因果关系展示

---

## 项目结构

```
Physical-visualization-skill/
├── .github/skills/
│   ├── manim-physics-animator/       (Skill 1)
│   │   ├── SKILL.md
│   │   └── examples/
│   └── physics-interactive-sim-lab/  (Skill 2)
│       ├── SKILL.md
│       └── examples/
├── docs/
│   ├── physics-topics.md
│   └── setup-guide.md
├── scripts/
└── README.md
```

---

## 运行环境

Skill 生成的代码需要本地运行环境：

| Skill | 需要安装 |
|-------|---------|
| Manim 动画 | `pip install manim` + LaTeX |
| 交互仿真 | `pip install streamlit numpy matplotlib` |

详细配置见 [docs/setup-guide.md](docs/setup-guide.md)。

---

## 首批主题

| 优先级 | 主题 | 公式 |
|--------|------|------|
| 核心 | 库仑定律 | F = k·q₁·q₂/r² |
| 核心 | 电场强度 | E = F/q |
| 核心 | 电势和电势差 | U = Ed |
| 核心 | 欧姆定律 | U = IR |
| 进阶 | 平行板电容器 | C = εS/d |
| 进阶 | 串并联电路 | 分压/分流规律 |

---

## 课堂教学建议（45 分钟）

1. **导入阶段**（5 分钟）- 播放 Manim 动画引入概念
2. **讲解阶段**（15 分钟）- 讲解理论和公式
3. **演示阶段**（15 分钟）- 用交互工具现场改参数演示
4. **练习阶段**（10 分钟）- 学生分组用工具探索

---

## 许可证

本项目用于教学目的。
