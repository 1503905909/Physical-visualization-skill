# 环境配置指南

本指南帮你快速搭建 Manim 和 Streamlit 的开发环境。

## 前置要求

- **操作系统**: Windows 10/11, macOS, 或 Linux
- **Python**: 3.8 或更高版本
- **包管理器**: pip 或 conda（推荐 conda）

### 检查 Python 版本

```bash
python --version
```

如果版本低于 3.8，请先升级 Python。

---

## 方案 A：使用 Conda（推荐）

Conda 可以自动处理复杂的依赖关系和编译工具。

### 1. 安装 Anaconda 或 Miniconda

- **Anaconda**: https://www.anaconda.com/download (完整版，包含 ~500 个库)
- **Miniconda**: https://docs.conda.io/projects/miniconda/en/latest/ (精简版，推荐)

### 2. 创建虚拟环境

```bash
conda create -n physics-viz python=3.11
conda activate physics-viz
```

选择 Python 3.11 是因为它足够新且稳定。

### 3. 安装 Manim

```bash
conda install -c conda-forge manim
```

这会自动安装 Manim 及其所有依赖（包括 FFmpeg、LaTeX 等）。

**验证安装**：
```bash
manim --version
```

### 4. 安装 Streamlit 及相关库

```bash
pip install streamlit numpy matplotlib plotly scipy sympy
```

**验证安装**：
```bash
streamlit --version
```

### 5. 激活环境时使用

每次使用前，激活环境：

```bash
conda activate physics-viz
```

完成后退出：

```bash
conda deactivate
```

---

## 方案 B：使用 Pip（简化版）

如果你已经有 Python 3.8+ 环境，可以直接用 pip。

### 1. 创建虚拟环境

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python -m venv venv
source venv/bin/activate
```

### 2. 安装 Manim

```bash
pip install manim
```

**注意**: 在 Windows 上，Manim 的安装可能需要以下额外工具：
- **FFmpeg** - 视频编码（https://ffmpeg.org/download.html）
- **LaTeX** - 数学公式渲染（MiKTeX 或 TeX Live）

如果安装失败，建议用方案 A（Conda）。

### 3. 安装 Streamlit 及相关库

```bash
pip install streamlit numpy matplotlib plotly scipy sympy
```

### 4. 后续使用

每次使用前激活虚拟环境：

```bash
# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

---

## VS Code 配置

### 1. 安装必要扩展

在 VS Code 中安装：
- **Python** (Microsoft)
- **Pylance** (Microsoft) - Python 语言支持
- **Trae AI** (或当前使用的 AI 插件)

### 2. 选择 Python 解释器

在 VS Code 中：
1. 打开命令面板 (`Ctrl+Shift+P`)
2. 搜索 "Python: Select Interpreter"
3. 选择虚拟环境中的 Python
   - Conda: 选择 `./envs/physics-viz/python.exe`
   - Venv: 选择 `./venv/Scripts/python.exe`

### 3. 终端配置

VS Code 的集成终端会自动使用选定的解释器，但如果需要手动激活虚拟环境：

```bash
# 在 VS Code 终端中
conda activate physics-viz
# 或
venv\Scripts\activate
```

---

## 验证完整环境

### 快速测试脚本

在项目目录中创建 `test_environment.py`：

```python
#!/usr/bin/env python
"""验证环境是否正确配置"""

import sys
print(f"Python 版本: {sys.version}")

# 测试 Manim
try:
    import manim
    print(f"✓ Manim 已安装 (版本: {manim.__version__})")
except ImportError as e:
    print(f"✗ Manim 导入失败: {e}")

# 测试 Streamlit
try:
    import streamlit
    print(f"✓ Streamlit 已安装 (版本: {streamlit.__version__})")
except ImportError as e:
    print(f"✗ Streamlit 导入失败: {e}")

# 测试数值计算库
try:
    import numpy as np
    import matplotlib.pyplot as plt
    import plotly.express as px
    import scipy
    import sympy
    print("✓ 所有数值和绘图库已安装")
except ImportError as e:
    print(f"✗ 库导入失败: {e}")

print("\n环境检查完毕！")
```

运行测试：

```bash
python test_environment.py
```

### 测试 Manim

创建 `test_manim.py`：

```python
from manim import *

class TestScene(Scene):
    def construct(self):
        circle = Circle()
        self.play(Create(circle))
        self.wait()

if __name__ == "__main__":
    # 运行这个文件后会自动生成视频
    pass
```

运行：

```bash
manim -pql test_manim.py TestScene
```

（`-q` 表示质量，`l` 表示低质量以加快生成速度，`-p` 表示完成后播放）

### 测试 Streamlit

创建 `test_streamlit.py`：

```python
import streamlit as st

st.title("Streamlit 测试")
st.write("环境配置成功！")

import numpy as np
import matplotlib.pyplot as plt

# 绘制简单图像
x = np.linspace(0, 10, 100)
y = np.sin(x)

fig, ax = plt.subplots()
ax.plot(x, y)
ax.set_title("正弦波")
st.pyplot(fig)
```

运行：

```bash
streamlit run test_streamlit.py
```

---

## 常见问题排查

### 问题 1: Manim 安装失败

**症状**: `pip install manim` 出错

**解决方案**:
1. 确保 Python 版本 ≥ 3.8
2. 尝试使用 Conda: `conda install -c conda-forge manim`
3. 在 Windows 上，确保安装了 FFmpeg 和 LaTeX

### 问题 2: Manim 运行缓慢

**症状**: 生成视频时非常慢

**解决方案**:
- 使用 `-l` (low quality) 而不是 `-h` (high quality) 进行测试
- 减少动画时长
- 关闭其他应用释放系统资源

### 问题 3: 中文字体显示为方块

**症状**: Manim 中的中文显示为方块 □

**解决方案**:
- 使用 `config.tex_template = TexTemplateLibrary.ctex` 在代码中指定
- 或在命令行添加: `manim -pqh --tex_template='ctex' scene.py SceneName`

### 问题 4: Streamlit 无法访问

**症状**: 运行 `streamlit run app.py` 后无法打开页面

**解决方案**:
- 检查是否打开了代理或防火墙
- 尝试手动访问 `http://localhost:8501`
- 使用 `streamlit run app.py --server.port 8080` 改变端口

### 问题 5: 导入错误

**症状**: `ModuleNotFoundError: No module named 'xxx'`

**解决方案**:
- 确保虚拟环境已激活
- 运行 `pip list` 确认库已安装
- 重新安装库: `pip install --upgrade xxx`

---

## 性能优化建议

### 对于 Manim

1. **降低质量进行快速测试**
   ```bash
   manim -ql scene.py SceneName  # 最低质量，最快
   manim -qm scene.py SceneName  # 中等质量
   manim -qh scene.py SceneName  # 高质量（默认）
   ```

2. **使用 `--disable_caching` 避免缓存问题**
   ```bash
   manim --disable_caching -pql scene.py SceneName
   ```

3. **并行处理**（对于多个场景）
   ```bash
   manim -pql scene.py -n 2  # 使用 2 个 CPU 核心
   ```

### 对于 Streamlit

1. **使用缓存加速重复计算**
   ```python
   @st.cache_data
   def expensive_calculation(x):
       return x ** 2
   ```

2. **使用 `st.session_state` 保存状态**
   ```python
   if 'counter' not in st.session_state:
       st.session_state.counter = 0
   ```

3. **减少图形刷新频率**
   ```python
   # 绘图后立即显示，而不是多次更新
   ```

---

## 推荐的项目目录结构

```
Physical-visualization-skill/
│
├── venv/                     # 虚拟环境（Conda 是 envs/）
├── .trae/
│   └── skills/              # Skill 定义
│
├── notebooks/               # Jupyter notebooks（可选）
│
├── scripts/
│   ├── manim/               # Manim 脚本
│   │   ├── coulombs_law.py
│   │   └── ...
│   └── streamlit/           # Streamlit 应用
│       ├── app.py
│       └── ...
│
├── output/
│   ├── videos/              # Manim 输出视频
│   └── results/             # Streamlit 结果输出
│
├── test_environment.py      # 环境测试脚本
└── README.md
```

---

## 后续步骤

配置完成后：

1. ✅ 运行 `test_environment.py` 确认环境完整
2. ✅ 在 VS Code 中打开项目文件夹
3. ✅ 尝试使用 Trae AI 插件调用 Manim Skill
4. ✅ 测试生成第一个动画
5. ✅ 在终端运行 `streamlit run app.py` 测试仿真应用

祝你使用愉快！

---

**更新日期**: 2026-05-24
