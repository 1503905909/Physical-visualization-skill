# 案例二 · 物理校验记录（教材第 5 题）

> 对应论文第四章案例二「带电粒子先加速、再偏转」。本页记录资源所用物理模型、统一约定、精确解与实测读数的一致性，供论文交稿前复核。

## 1. 题目与来源

人教版《普通高中教科书·物理 必修第三册》第十章第 5 节「练习与应用」第 5 题（教材第 49 页）：
电子由静止经 1000 V 电压加速，再垂直进入场强 5000 N/C 的匀强偏转电场，偏转电极长 6 cm，求出射速度大小及其与入射方向的夹角。

## 2. 统一约定（Manim 与 HTML 一致）

| 项目 | 约定 |
|---|---|
| 符号 | $e>0$ 为电子电荷量**大小**，电子实际电荷 $-e$；$m_e$ 为电子质量 |
| 已知量 | $U_0=1000\ \mathrm{V}$、$E=5000\ \mathrm{N/C}$、$L=6\ \mathrm{cm}$ |
| 坐标 | 向右 $+x$、向上 $+y$ |
| 运动 | 电子**向右加速、向上偏转** |
| 加速区 | 左板负、右板正；电场向左，电子受力向右 |
| 偏转区 | 上板正、下板负；电场向下，电子受力向上 |
| 假设 | 电子由静止出发；偏转场匀强；忽略重力、边缘效应、相对论修正 |
| 板距 | **题目未给出**，推导中不作为已知量 |

## 3. 精确解（应与资源显示一致）

$$
eU_0=\tfrac12 m_e v_0^2 \;\Rightarrow\; v_0=\sqrt{\frac{2eU_0}{m_e}}
$$

$$
t=\frac{L}{v_0},\qquad a_y=\frac{eE}{m_e},\qquad
v_y=a_y t=\frac{eEL}{m_ev_0}
$$

$$
\frac{v_y}{v_0}=\frac{EL}{2U_0}=\frac{3}{20},\qquad
v_{\text{出}}=\sqrt{v_0^2+v_y^2}=\frac{\sqrt{409}}{20}\,v_0
=\frac{\sqrt{409}}{20}\sqrt{\frac{2eU_0}{m_e}}
$$

$$
\tan\theta=\frac{3}{20},\qquad \theta=\arctan\!\left(\frac{3}{20}\right),\qquad
|y|=\frac{EL^2}{4U_0}=\frac{9}{2000}\ \mathrm{m}
$$

> 注意：$3/20$ 是**正切值**，不是角度本身；偏转位移**大小**为 $9/2000\ \mathrm{m}=4.5\ \mathrm{mm}$，方向向上。

## 4. 数值核算（脚本独立复算）

| 量 | 精确式 | 数值 |
|---|---|---|
| $v_0$ | $\sqrt{2eU_0/m_e}$ | $1.87554\times10^{7}\ \mathrm{m/s}$ |
| $t$ | $L/v_0$ | $3.199\times10^{-9}\ \mathrm{s}$ |
| $v_y/v_0$ | $EL/2U_0$ | **0.150000** $=3/20$ |
| $|y|$ | $EL^2/4U_0$ | **$4.500\times10^{-3}\ \mathrm{m}=9/2000$** |
| $\theta$ | $\arctan(3/20)$ | **$8.5308^\circ$** |
| $v_{\text{出}}/v_0$ | $\sqrt{409}/20$ | **1.01118742** |
| $v_{\text{出}}$ | — | $1.89652\times10^{7}\ \mathrm{m/s}$ |

## 5. 资源实测对照

### HTML（`charged_particle_uniform_field_html.html`，「教材第 5 题」预设）

| 量 | 页面读数 | 与精确解 |
|---|---|---|
| $v_0$ | $1.88\times10^{7}\ \mathrm{m/s}$ | 一致（3 位有效数字） |
| $v_y$ | $2.81\times10^{6}\ \mathrm{m/s}$ | 一致 |
| $v_y/v_0$ | 0.150 | 一致 |
| $\theta$ | $8.53^\circ$ | 一致 |
| $v_{\text{出}}$ | $1.90\times10^{7}\ \mathrm{m/s}$ | 一致 |
| $|y|$ | $4.5\ \mathrm{mm}$ | 一致 |
| $t$ | $3.20\ \mathrm{ns}$ | 一致 |

变量趋势检验（与公式方向一致）：

| 操作 | $|y|$ | $\theta$ | 说明 |
|---|---|---|---|
| $U$ 100 V → 200 V | 4.5 → 9.0 mm | 8.53° → 16.70° | $|y|=\frac{|U|L^2}{4dU_0}\propto U$ |
| $U_0$ 1000 V → 2000 V | 4.5 → 2.25 mm | 8.53° → 4.29° | $|y|\propto 1/U_0$ |
| $U=0$ | 0.0 mm | 0.00° | 轨迹为直线，无偏转 |

撞板处理：$L=10\ \mathrm{cm}$、$d=1\ \mathrm{cm}$、$U=400\ \mathrm{V}$ 时判「已打到上极板」，$t=1.19\ \mathrm{ns}$、$x=2.2\ \mathrm{cm}$，轨迹在撞板处截断。

### HTML 中「题给」与「画图设置」的区分

页面上 $E=5000\ \mathrm{N/C}$ 是题目条件；面板里的 $d=2\ \mathrm{cm}$、$U=100\ \mathrm{V}$ 只是为了让网页按 $E=U/d$ 画出这个场强，**题目没有给出板距**。资源在 HUD、面板说明、画布标尺、抽屉四处都作了标注。

### Manim（`electron_accelerate_then_deflect.py`）

动画分两段：加速段由动能定理给出 $v_0$；偏转段依次给出 $t$、$v_y$、速度合成与夹角；收尾回到教材题给出上述精确式。画面数值与第 3 节一致，未使用近似小数替代精确式。

## 6. 表述校正（本案例相关）

1. 原「偏转量与粒子种类无关」改为「**偏转位移大小**相同，$|y|=|U|L^2/(4dU_0)$」；不同电性的粒子在同一偏转场中**方向相反**，不能笼统说成相同。
2. 加速区极性随粒子电荷符号自动调整：电子为左负右正，质子/α 为左正右负，任何粒子都从静止被加速进入偏转区。
3. 回旋加速器（案例三）：「半径只由速度决定」改为「对同一粒子且磁感应强度不变时，轨道半径随速度增大」；$r\propto\sqrt{n}$ 中的 $n$ 明确为**从静止开始、每次经过相同加速电压的累计加速次数**；周期不变的结论限定为固定粒子、匀强磁场、非相对论模型。

## 7. 资源清单

| 资源 | 文件 |
|---|---|
| 动画（本案例） | `.github/skills/manim-physics-animator/examples/electron_accelerate_then_deflect.py` |
| 动画视频 | `.github/skills/manim-physics-animator/examples/videos/electron_accelerate_then_deflect.mp4` |
| 交互仿真 | `.github/skills/physics-interactive-sim-lab/examples/charged_particle_uniform_field_html.html` |
| 回旋加速器脚本（案例三） | `.github/skills/manim-physics-animator/examples/cyclotron.py` |
| 回旋加速器视频 | `.github/skills/manim-physics-animator/examples/videos/cyclotron.mp4` |

以上资源均可在资源画廊 `index.html` 中按章节检索并直接打开。
