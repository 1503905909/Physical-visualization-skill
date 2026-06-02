import csv
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import streamlit as st
from matplotlib import rcParams


st.set_page_config(
    page_title="高中物理交互式仿真实验模板",
    layout="wide",
    initial_sidebar_state="expanded",
)

rcParams["font.sans-serif"] = ["SimHei", "Microsoft YaHei", "DejaVu Sans"]
rcParams["axes.unicode_minus"] = False

APP_NAME = "template_streamlit"
PROJECT_ROOT = Path(__file__).resolve().parents[4]
OUTPUT_ROOT = PROJECT_ROOT / "output" / "results" / APP_NAME
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


def coulomb_force(q1_uc: float, q2_uc: float, r_cm: float) -> float:
    k = 8.99e9
    q1 = q1_uc * 1e-6
    q2 = q2_uc * 1e-6
    r = max(r_cm * 1e-2, 1e-5)
    return k * abs(q1 * q2) / (r ** 2)


def ohm_current(voltage: float, resistance: float) -> float:
    if resistance <= 0:
        return 0.0
    return voltage / resistance


def plot_coulomb_curve(q1_uc: float, q2_uc: float, current_r_cm: float, max_r_cm: float):
    r_values = np.linspace(1, max_r_cm, 180)
    force_values = [coulomb_force(q1_uc, q2_uc, r) for r in r_values]

    fig, ax = plt.subplots(figsize=(8, 4.8))
    ax.plot(r_values, force_values, color="#0f766e", linewidth=2.4, label="F-r 曲线")
    ax.scatter([current_r_cm], [coulomb_force(q1_uc, q2_uc, current_r_cm)], color="#dc2626", s=60, zorder=3, label="当前取值")
    ax.set_xlabel("距离 r (cm)")
    ax.set_ylabel("静电力 F (N)")
    ax.set_title("库仑力随距离变化")
    ax.grid(True, alpha=0.3)
    ax.legend()
    return fig, r_values, force_values


def plot_ohm_lines(resistances, voltage):
    u_values = np.linspace(0, 12, 120)
    fig, ax = plt.subplots(figsize=(8, 4.8))
    for resistance in resistances:
        i_values = [ohm_current(u, resistance) for u in u_values]
        ax.plot(u_values, i_values, linewidth=2.2, label=f"R = {resistance} ohm")
        ax.scatter([voltage], [ohm_current(voltage, resistance)], s=46)
    ax.set_xlabel("电压 U (V)")
    ax.set_ylabel("电流 I (A)")
    ax.set_title("欧姆定律 U-I 图像")
    ax.grid(True, alpha=0.3)
    ax.legend()
    return fig


st.title("高中物理交互式仿真实验模板")
st.caption("模板目标：用少量参数、实时计算和图像反馈帮助学生观察物理量之间的关系。")

tab_coulomb, tab_ohm = st.tabs(["库仑定律", "欧姆定律"])

with tab_coulomb:
    st.header("库仑定律参数探究")
    st.markdown(r"物理模型：$F = k\frac{|q_1q_2|}{r^2}$，内部计算统一使用 SI 单位。")

    left, right = st.columns([0.9, 1.4])
    with left:
        st.subheader("参数设置")
        q1_uc = st.slider("电荷量 q1 (uC)", min_value=-10.0, max_value=10.0, value=-4.0, step=0.5)
        q2_uc = st.slider("电荷量 q2 (uC)", min_value=-10.0, max_value=10.0, value=8.0, step=0.5)
        r_cm = st.slider("距离 r (cm)", min_value=1.0, max_value=10.0, value=3.0, step=0.1)
        max_r_cm = st.slider("图像显示上限 (cm)", min_value=10.0, max_value=50.0, value=25.0, step=1.0)

        interaction = "排斥" if q1_uc * q2_uc > 0 else "吸引" if q1_uc * q2_uc < 0 else "无明显作用"
        force = coulomb_force(q1_uc, q2_uc, r_cm)
        st.metric("相互作用", interaction)
        st.metric("静电力大小", f"{force:.3e} N")

    with right:
        st.subheader("图像反馈")
        fig, r_values, force_values = plot_coulomb_curve(q1_uc, q2_uc, r_cm, max_r_cm)
        st.pyplot(fig)

        st.markdown(
            """
            课堂观察建议：
            - 保持电荷量不变，将距离加倍，比较静电力变化。
            - 保持距离不变，只改变一个电荷量，观察力是否随之成比例变化。
            - 改变电荷正负号，比较吸引和排斥的区别。
            """
        )

        if st.button("导出库仑定律数据"):
            rows = [[float(r), float(f)] for r, f in zip(r_values, force_values)]
            csv_path = save_csv(rows, "coulomb_force_curve.csv", ["r_cm", "F_N"])
            png_path = save_plot(fig, "coulomb_force_curve.png")
            st.success(f"已导出：{csv_path}；{png_path}")

with tab_ohm:
    st.header("欧姆定律图像探究")
    st.markdown(r"物理模型：$I=\frac{U}{R}$。")

    left, right = st.columns([0.9, 1.4])
    with left:
        st.subheader("参数设置")
        voltage = st.slider("当前电压 U (V)", min_value=0.0, max_value=12.0, value=6.0, step=0.1)
        show_r10 = st.checkbox("显示 R = 10 ohm", value=True)
        show_r20 = st.checkbox("显示 R = 20 ohm", value=True)
        show_r50 = st.checkbox("显示 R = 50 ohm", value=False)
        resistances = []
        if show_r10:
            resistances.append(10)
        if show_r20:
            resistances.append(20)
        if show_r50:
            resistances.append(50)

        if resistances:
            for resistance in resistances:
                st.metric(f"R={resistance} ohm 时电流", f"{ohm_current(voltage, resistance):.3f} A")
        else:
            st.warning("请至少选择一个电阻。")

    with right:
        if resistances:
            fig = plot_ohm_lines(resistances, voltage)
            st.pyplot(fig)
            st.markdown("课堂观察建议：同一电阻对应一条过原点的直线；电阻越大，图线斜率越小。")
