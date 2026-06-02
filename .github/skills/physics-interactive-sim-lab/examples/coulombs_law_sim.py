import csv
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import streamlit as st
from matplotlib import rcParams


st.set_page_config(
    page_title="库仑定律数据探究",
    layout="wide",
    initial_sidebar_state="expanded",
)

rcParams["font.sans-serif"] = ["SimHei", "Microsoft YaHei", "DejaVu Sans"]
rcParams["axes.unicode_minus"] = False

PROJECT_ROOT = Path(__file__).resolve().parents[4]
OUTPUT_ROOT = PROJECT_ROOT / "output" / "results" / "coulombs_law_sim"
OUTPUT_ROOT.mkdir(parents=True, exist_ok=True)


def save_plot(fig, file_name: str) -> Path:
    output_path = OUTPUT_ROOT / file_name
    fig.savefig(output_path, dpi=150, bbox_inches="tight")
    return output_path


def save_csv(rows, file_name: str, headers) -> Path:
    output_path = OUTPUT_ROOT / file_name
    with output_path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(headers)
        writer.writerows(rows)
    return output_path


def coulomb_force(q1_uc: float, q2_uc: float, r_cm: float) -> tuple[float, str]:
    """Return Coulomb force magnitude in N and interaction type."""
    k = 8.99e9
    q1 = q1_uc * 1e-6
    q2 = q2_uc * 1e-6
    r = max(r_cm * 1e-2, 1e-5)
    magnitude = k * abs(q1 * q2) / (r ** 2)
    if q1_uc == 0 or q2_uc == 0:
        interaction = "无明显作用"
    elif q1_uc * q2_uc > 0:
        interaction = "排斥"
    else:
        interaction = "吸引"
    return magnitude, interaction


def electric_field(q_uc: float, r_cm: float) -> float:
    k = 8.99e9
    q = q_uc * 1e-6
    r = max(r_cm * 1e-2, 1e-5)
    return k * abs(q) / (r ** 2)


def plot_charge_diagram(q1_uc: float, q2_uc: float, r_cm: float):
    fig, ax = plt.subplots(figsize=(8.5, 3.2))
    x1 = -r_cm / 2
    x2 = r_cm / 2
    color1 = "#dc2626" if q1_uc >= 0 else "#2563eb"
    color2 = "#dc2626" if q2_uc >= 0 else "#2563eb"
    force, interaction = coulomb_force(q1_uc, q2_uc, r_cm)

    ax.scatter([x1, x2], [0, 0], s=900, c=[color1, color2], edgecolors="white", linewidths=2, zorder=3)
    ax.text(x1, 0, "q1", ha="center", va="center", color="white", fontsize=14, fontweight="bold")
    ax.text(x2, 0, "q2", ha="center", va="center", color="white", fontsize=14, fontweight="bold")
    ax.text(x1, -0.55, f"{q1_uc:g} uC", ha="center", fontsize=11)
    ax.text(x2, -0.55, f"{q2_uc:g} uC", ha="center", fontsize=11)

    if interaction != "无明显作用":
        attract = interaction == "吸引"
        direction_left = 1 if attract else -1
        direction_right = -direction_left
        arrow_len = min(max(r_cm * 0.18, 0.6), 2.2)
        ax.arrow(x1, 0.72, direction_left * arrow_len, 0, head_width=0.12, head_length=0.18,
                 length_includes_head=True, color="#f59e0b", linewidth=2.4)
        ax.arrow(x2, 0.72, direction_right * arrow_len, 0, head_width=0.12, head_length=0.18,
                 length_includes_head=True, color="#f59e0b", linewidth=2.4)
        ax.text((x1 + x2) / 2, 1.02, f"{interaction}，F = {force:.3e} N", ha="center", color="#92400e", fontsize=12)

    ax.plot([x1, x2], [-0.95, -0.95], color="#059669", linewidth=2)
    ax.text((x1 + x2) / 2, -1.2, f"r = {r_cm:g} cm", ha="center", color="#047857", fontsize=12)

    margin = max(4, r_cm * 0.4)
    ax.set_xlim(x1 - margin, x2 + margin)
    ax.set_ylim(-1.55, 1.45)
    ax.set_yticks([])
    ax.set_xlabel("位置 (cm)")
    ax.set_title("点电荷布局与静电力方向")
    ax.grid(axis="x", alpha=0.25)
    return fig


def plot_force_distance(q1_uc: float, q2_uc: float, r_cm: float, max_r_cm: float):
    r_values = np.linspace(1, max_r_cm, 220)
    force_values = np.array([coulomb_force(q1_uc, q2_uc, r)[0] for r in r_values])
    current_force = coulomb_force(q1_uc, q2_uc, r_cm)[0]

    fig, ax = plt.subplots(figsize=(8.5, 4.8))
    ax.plot(r_values, force_values, color="#0f766e", linewidth=2.4, label="F-r 曲线")
    ax.scatter([r_cm], [current_force], color="#dc2626", s=64, zorder=4, label="当前点")
    ax.set_xlabel("距离 r (cm)")
    ax.set_ylabel("静电力 F (N)")
    ax.set_title("库仑力随距离变化")
    ax.grid(True, alpha=0.3)
    ax.legend()
    return fig, r_values, force_values


def plot_inverse_square_check(q1_uc: float, q2_uc: float, max_r_cm: float):
    r_values = np.linspace(1, max_r_cm, 220)
    inv_square = 1 / (r_values ** 2)
    force_values = np.array([coulomb_force(q1_uc, q2_uc, r)[0] for r in r_values])

    fig, ax = plt.subplots(figsize=(8.5, 4.8))
    ax.plot(inv_square, force_values, color="#7c3aed", linewidth=2.4)
    ax.set_xlabel("1 / r^2 (1/cm^2)")
    ax.set_ylabel("静电力 F (N)")
    ax.set_title("反平方关系检验：F 与 1/r^2 近似成线性关系")
    ax.grid(True, alpha=0.3)
    return fig


def export_force_data(q1_uc: float, q2_uc: float, max_r_cm: float):
    r_values = np.linspace(1, max_r_cm, 120)
    rows = []
    for r in r_values:
        force, interaction = coulomb_force(q1_uc, q2_uc, r)
        rows.append([float(r), float(force), interaction])
    return rows


def main():
    st.title("库仑定律数据探究")
    st.caption("用于定量分析库仑力与电荷量、距离之间的关系；课堂即时演示可优先使用 HTML 版。")

    with st.sidebar:
        st.header("参数设置")
        q1_uc = st.slider("电荷量 q1 (uC)", min_value=-10.0, max_value=10.0, value=-4.0, step=0.5)
        q2_uc = st.slider("电荷量 q2 (uC)", min_value=-10.0, max_value=10.0, value=8.0, step=0.5)
        r_cm = st.slider("两电荷距离 r (cm)", min_value=1.0, max_value=10.0, value=3.0, step=0.1)
        max_r_cm = st.slider("曲线距离上限 (cm)", min_value=10.0, max_value=60.0, value=30.0, step=1.0)
        show_inverse_square = st.checkbox("显示反平方关系检验", value=True)
        show_field = st.checkbox("显示电场强度估算", value=False)

    force, interaction = coulomb_force(q1_uc, q2_uc, r_cm)

    metric_1, metric_2, metric_3, metric_4 = st.columns(4)
    metric_1.metric("q1", f"{q1_uc:g} uC")
    metric_2.metric("q2", f"{q2_uc:g} uC")
    metric_3.metric("距离 r", f"{r_cm:g} cm")
    metric_4.metric("静电力", f"{force:.3e} N")

    st.info(f"当前相互作用类型：{interaction}。计算时统一转换为 SI 单位：uC -> C，cm -> m。")

    left, right = st.columns([1, 1])
    with left:
        st.subheader("电荷布局与力方向")
        st.pyplot(plot_charge_diagram(q1_uc, q2_uc, r_cm))

    with right:
        st.subheader("物理模型")
        st.latex(r"F = k \frac{|q_1 q_2|}{r^2}")
        st.markdown(
            """
            - 采用点电荷模型，忽略介质极化和其他外场影响。
            - 力的大小由电荷量乘积和距离平方决定。
            - 力的方向沿两电荷连线；同号相斥，异号相吸。
            """
        )
        if show_field:
            e1 = electric_field(q1_uc, r_cm)
            e2 = electric_field(q2_uc, r_cm)
            st.metric("q1 在 r 处产生的电场强度大小", f"{e1:.3e} N/C")
            st.metric("q2 在 r 处产生的电场强度大小", f"{e2:.3e} N/C")

    tab_curve, tab_check, tab_teach = st.tabs(["F-r 曲线", "关系检验", "教学提示"])

    with tab_curve:
        fig, r_values, force_values = plot_force_distance(q1_uc, q2_uc, r_cm, max_r_cm)
        st.pyplot(fig)
        if st.button("导出当前 F-r 数据和图像"):
            rows = export_force_data(q1_uc, q2_uc, max_r_cm)
            csv_path = save_csv(rows, "coulombs_law_force_distance.csv", ["r_cm", "F_N", "interaction"])
            png_path = save_plot(fig, "coulombs_law_force_distance.png")
            st.success(f"已导出：{csv_path}；{png_path}")

    with tab_check:
        if show_inverse_square:
            st.pyplot(plot_inverse_square_check(q1_uc, q2_uc, max_r_cm))
            st.markdown("若 q1、q2 保持不变，F 与 1/r^2 的图像应近似为过原点的直线。")
        else:
            st.write("可在侧边栏勾选“显示反平方关系检验”。")

    with tab_teach:
        st.markdown(
            """
            课堂使用建议：

            1. 先固定 q1 和 q2，只改变距离 r，让学生记录 r 加倍时 F 的变化。
            2. 再固定距离，只改变一个电荷量，观察 F 是否随电荷量成比例变化。
            3. 最后改变电荷正负号，引导学生区分“力的大小”和“力的方向”。

            可追问学生：

            - 为什么距离不能取 0？
            - 为什么本实验要把 uC 和 cm 转换成 C 和 m 后再计算？
            - 反平方关系在图像上有什么特征？
            """
        )


if __name__ == "__main__":
    main()
