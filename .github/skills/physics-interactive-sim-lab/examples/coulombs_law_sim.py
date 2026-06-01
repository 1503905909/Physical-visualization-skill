import csv
from pathlib import Path

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rcParams

# ========== 配置 ==========
st.set_page_config(
    page_title="库仑定律交互仿真实验",
    layout="wide",
    initial_sidebar_state="expanded"
)

rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'DejaVu Sans']
rcParams['axes.unicode_minus'] = False

PROJECT_ROOT = Path(__file__).resolve().parents[4]
OUTPUT_ROOT = PROJECT_ROOT / "output" / "results" / "physics_interactive_sim_lab"
OUTPUT_ROOT.mkdir(parents=True, exist_ok=True)


def save_plot(fig, file_name: str) -> Path:
    output_path = OUTPUT_ROOT / file_name
    fig.savefig(output_path, dpi=150, bbox_inches="tight")
    return output_path


def save_csv(data: np.ndarray, file_name: str, headers=None) -> Path:
    output_path = OUTPUT_ROOT / file_name
    if headers is not None:
        with output_path.open("w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(headers)
            writer.writerows(data)
    else:
        np.savetxt(output_path, data, delimiter=",")
    return output_path


def coulomb_force(q1_nC: float, q2_nC: float, r_cm: float) -> tuple[float, str]:
    """计算两点电荷之间的库仑力大小和作用性质。"""
    k = 8.99e9
    q1 = q1_nC * 1e-9
    q2 = q2_nC * 1e-9
    r = max(r_cm * 1e-2, 1e-5)
    magnitude = k * abs(q1 * q2) / (r ** 2)
    interaction = "吸引" if q1 * q2 < 0 else "排斥"
    return magnitude, interaction


def electric_field(q_nC: float, r_cm: float) -> float:
    """计算点电荷在 r 处的电场强度。"""
    k = 8.99e9
    q = q_nC * 1e-9
    r = max(r_cm * 1e-2, 1e-5)
    return k * abs(q) / (r ** 2)


def plot_force_vs_distance(q1_nC, q2_nC, max_r_cm=30):
    r_values = np.linspace(1, max_r_cm, 200)
    F_values = [coulomb_force(q1_nC, q2_nC, r)[0] for r in r_values]
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(r_values, F_values, color="#1f77b4", linewidth=2)
    ax.set_xlabel('距离 r (cm)', fontsize=12)
    ax.set_ylabel('力 F (N)', fontsize=12)
    ax.set_title('库仑力随距离的变化', fontsize=14, fontweight='bold')
    ax.grid(True, alpha=0.3)
    ax.set_yscale('log')
    ax.annotate(
        '反平方规律: F∝1/r²',
        xy=(max_r_cm * 0.6, F_values[int(len(F_values) * 0.6)]),
        xytext=(max_r_cm * 0.6, max(F_values) * 0.2),
        arrowprops=dict(arrowstyle='->', color='red'),
        fontsize=11,
        color='red'
    )
    return fig, r_values, F_values


def plot_charge_diagram(q1_nC, q2_nC, r_cm):
    fig, ax = plt.subplots(figsize=(8, 3))
    x1, x2 = -r_cm / 2, r_cm / 2
    ax.scatter([x1, x2], [0, 0], s=300, c=['red' if q1_nC >= 0 else 'blue', 'red' if q2_nC >= 0 else 'blue'])
    ax.text(x1, 0.1, f'q₁={q1_nC} nC', ha='center', fontsize=11)
    ax.text(x2, 0.1, f'q₂={q2_nC} nC', ha='center', fontsize=11)
    ax.set_xlim(-max(40, abs(x1) + 10), max(40, abs(x2) + 10))
    ax.set_ylim(-5, 5)
    ax.set_xlabel('位置 (cm)', fontsize=12)
    ax.set_yticks([])
    ax.set_title('点电荷布局与作用方向', fontsize=14, fontweight='bold')
    ax.axhline(0, color='#666666', linewidth=0.8)
    magnitude, interaction = coulomb_force(q1_nC, q2_nC, r_cm)
    direction = '← →' if interaction == '排斥' else '→ ←'
    offset = 5 if interaction == '排斥' else -5
    ax.annotate(
        direction,
        xy=(x1, 0),
        xytext=(x1 + offset, 0),
        fontsize=24,
        color='orange',
        ha='center',
        va='center'
    )
    ax.annotate(
        direction,
        xy=(x2, 0),
        xytext=(x2 - offset, 0),
        fontsize=24,
        color='orange',
        ha='center',
        va='center'
    )
    return fig


def prepare_export_data(q1_nC, q2_nC, r_cm, max_r_cm):
    r_values = np.linspace(1, max_r_cm, 100)
    rows = []
    for r in r_values:
        F_value, _ = coulomb_force(q1_nC, q2_nC, r)
        rows.append([round(r, 3), F_value])
    return np.array(rows)


def main():
    st.title("📘 高中物理库仑定律交互仿真实验")

    st.markdown(
        r"""
        ### 实验目标
        通过调节两个点电荷的电荷量和间距，观察库仑力的大小与性质变化，验证“同号相斥、异号相吸”及“力与距离的平方成反比”的规律。

        ### 实验说明
        - 库仑定律公式：$F = k \frac{|q_1 q_2|}{r^2}$
        - 其中 $k = 8.99 \times 10^9\, \mathrm{N\cdot m^2 / C^2}$
        - 本实验采用“点电荷模型”，两电荷沿一条直线放置，电荷量单位为 nC，距离单位为 cm。
        """,
        unsafe_allow_html=True,
    )

    with st.sidebar:
        st.header("参数设置")
        q1_nC = st.slider("电荷 q₁ (nC)", min_value=-100, max_value=100, value=10, step=1)
        q2_nC = st.slider("电荷 q₂ (nC)", min_value=-100, max_value=100, value=-10, step=1)
        r_cm = st.slider("电荷间距离 r (cm)", min_value=1, max_value=50, value=10, step=1)
        max_r_cm = st.slider("曲线显示距离上限 (cm)", min_value=10, max_value=60, value=30, step=5)
        show_field = st.checkbox("显示点电荷电场强度曲线", value=True)
        st.markdown("---")
        st.write(
            "🔎 建议实验：保持 q₁、q₂ 同号观察排斥；保持异号观察吸引；逐步加大距离验证反平方规律。"
        )

    force_magnitude, interaction = coulomb_force(q1_nC, q2_nC, r_cm)
    field_q1 = electric_field(q1_nC, r_cm)
    field_q2 = electric_field(q2_nC, r_cm)

    left, right = st.columns([1, 1])

    with left:
        st.subheader("当前参数与结果")
        st.metric("q₁", f"{q1_nC} nC")
        st.metric("q₂", f"{q2_nC} nC")
        st.metric("距离 r", f"{r_cm} cm")
        st.metric("力的性质", interaction)
        st.metric("力的大小", f"{force_magnitude:.3e} N")
        st.markdown(
            f"- 当前所求为两电荷间相互作用力的大小，方向由电荷性质决定。"
        )
        st.markdown(
            f"- 若 q₁×q₂ < 0，则电荷吸引；若 q₁×q₂ > 0，则电荷排斥。"
        )

    with right:
        st.subheader("物理模型说明")
        st.markdown(
            """
            - 物理假设：两点电荷之间只存在静电相互作用，忽略介质极化和磁效应。
            - 距离采用电荷中心间距，若距离减小到 0，则模型不适用。
            - 电荷量转换：1 nC = 1e-9 C，距离转换：1 cm = 1e-2 m。
            """
        )
        st.latex(r"F = k \frac{|q_1 q_2|}{r^2}")
        st.markdown(
            """
            进一步可说明：
            - 这里采用的是标量形式的大小计算，符号性质由电荷符号决定。
            - 实际电场方向与力方向一致，力大小与距离平方成反比。
            """
        )

    st.divider()

    tab1, tab2 = st.tabs(["图像演示", "教学提示"])

    with tab1:
        st.subheader("位置与力的可视化")
        charge_fig = plot_charge_diagram(q1_nC, q2_nC, r_cm)
        st.pyplot(charge_fig)

        st.subheader("库仑力随距离变化")
        force_fig, r_values, F_values = plot_force_vs_distance(q1_nC, q2_nC, max_r_cm)
        ax = force_fig.get_axes()[0]
        ax.scatter([r_cm], [force_magnitude], color='red', s=60, zorder=5, label='当前距离点')
        ax.legend()
        st.pyplot(force_fig)

        if show_field:
            st.subheader("点电荷电场强度示意")
            st.markdown(
                "通过电场强度帮助学生理解：电场是空间中每个点的性质，与试探电荷无关。"
            )
            fig, ax = plt.subplots(figsize=(8, 4))
            rx = np.linspace(1, max_r_cm, 150)
            eq1 = [electric_field(q1_nC, x) for x in rx]
            eq2 = [electric_field(q2_nC, x) for x in rx]
            ax.plot(rx, eq1, label='q₁ 电场强度', linewidth=2)
            ax.plot(rx, eq2, label='q₂ 电场强度', linewidth=2)
            ax.set_yscale('log')
            ax.set_xlabel('r (cm)', fontsize=12)
            ax.set_ylabel('电场强度 E (N/C)', fontsize=12)
            ax.set_title('点电荷电场强度随距离变化', fontsize=14, fontweight='bold')
            ax.grid(True, alpha=0.3)
            ax.legend()
            st.pyplot(fig)

    with tab2:
        st.subheader("教师讲解要点")
        st.markdown(
            """
            1. **实验目标**：让学生理解库仑力的定量关系，即“力与电荷量成正比、与距离的平方成反比”。
            2. **现象观察**：通过调节 q₁、q₂、r 的值，比较同号与异号两种情况，明确排斥和吸引的方向。
            3. **教学建议**：
               - 先保持 q₁=q₂ 同号，观察距离变化时力的趋势。
               - 再让 q₁ 和 q₂ 异号，观察力的性质如何从排斥变为吸引。
            4. **习题思考**：
               - 若 q₁ 变为 2 倍，而 r 保持不变，F 会变为多少？
               - 若 r 从 10 cm 变为 20 cm，力会变为原来的几分之几？
               - 为什么距离取 0 的时候模型不能直接使用？
            5. **课堂拓展**：
               - 可以在图像中观察到对数坐标下的直线趋势，说明反平方关系在对数图上的表现。
               - 引导学生讨论点电荷模型的假设和实际电荷分布的差异。"""
        )
        st.markdown(
            """
            ### 课堂练习建议
            - 让学生记录 3 组不同电荷组合的结果，并比较力的大小与方向。
            - 讨论为什么电荷量带符号，以及力的性质由电荷符号决定。
            - 结合实验，引导学生写出自己的结论句：`同号电荷相斥，异号电荷相吸；力的大小与距离的平方成反比。`
            """
        )

    if st.button("导出当前实验数据"):
        csv_data = prepare_export_data(q1_nC, q2_nC, r_cm, max_r_cm)
        csv_path = save_csv(csv_data, "coulombs_law_sim_data.csv", headers=["r (cm)", "F (N)"])
        plot_path = save_plot(force_fig, "coulombs_law_sim_plot.png")
        st.success(f"已导出实验数据和图像：\n{csv_path}\n{plot_path}")


if __name__ == '__main__':
    main()


if __name__ == '__main__':
    main()
