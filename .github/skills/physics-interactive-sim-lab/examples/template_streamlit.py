"""
Streamlit 物理仿真模板 - 基础交互工具
适用于: 参数调整、实时计算、动态绘图
"""

import csv
from pathlib import Path

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rcParams

# ========== 配置 ==========
st.set_page_config(
    page_title="物理交互式实验",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 设置项目输出目录
APP_NAME = "template_streamlit"
PROJECT_ROOT = Path(__file__).resolve().parents[4]
OUTPUT_ROOT = PROJECT_ROOT / "output" / "results" / APP_NAME
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


def create_csv_data(headers, rows):
    return np.array(rows)

# 设置中文字体
rcParams['font.sans-serif'] = ['SimHei', 'DejaVu Sans']
rcParams['axes.unicode_minus'] = False


# ========== 物理计算函数 ==========
def calculate_force(q1, q2, r):
    """
    计算库仑力（库仑定律）
    
    参数:
        q1: 电荷 1 (nC)
        q2: 电荷 2 (nC)  
        r: 距离 (cm)
    
    返回:
        F: 力 (N)
    """
    k = 8.99e9  # 库仑常数
    q1_c = q1 * 1e-9  # 转换为库伦
    q2_c = q2 * 1e-9
    r_m = r * 1e-2   # 转换为米
    
    if r_m == 0:
        return 0
    
    F = k * q1_c * q2_c / (r_m ** 2)
    return F


def calculate_electric_field(Q, r):
    """
    计算点电荷的电场强度
    
    参数:
        Q: 场源电荷 (nC)
        r: 距离 (cm)
    
    返回:
        E: 电场强度 (N/C)
    """
    k = 8.99e9
    Q_c = Q * 1e-9
    r_m = r * 1e-2
    
    if r_m == 0:
        return 0
    
    E = k * Q_c / (r_m ** 2)
    return E


def ohms_law(U, R):
    """
    欧姆定律计算电流
    
    参数:
        U: 电压 (V)
        R: 电阻 (Ω)
    
    返回:
        I: 电流 (A)
    """
    if R == 0:
        return 0
    return U / R


# ========== 绘图函数 ==========
def plot_coulombs_law(q1, q2, r_max=10):
    """绘制库仑力随距离变化的曲线"""
    r_values = np.linspace(0.1, r_max, 100)
    F_values = [calculate_force(q1, q2, r) for r in r_values]
    
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.semilogy(r_values, F_values, 'b-', linewidth=2, label='F = kq₁q₂/r²')
    ax.set_xlabel('距离 r (cm)', fontsize=12)
    ax.set_ylabel('力 F (N)', fontsize=12)
    ax.set_title('库仑力随距离变化', fontsize=14, fontweight='bold')
    ax.grid(True, alpha=0.3)
    ax.legend()
    return fig


def plot_ohms_law(R_values, U_max=10):
    """绘制欧姆定律 U-I 曲线对比"""
    U_range = np.linspace(0, U_max, 100)
    
    fig, ax = plt.subplots(figsize=(10, 6))
    colors = plt.cm.viridis(np.linspace(0, 1, len(R_values)))
    
    for R, color in zip(R_values, colors):
        if R > 0:
            I_values = U_range / R
            ax.plot(U_range, I_values, linewidth=2, label=f'R = {R} Ω', color=color)
    
    ax.set_xlabel('电压 U (V)', fontsize=12)
    ax.set_ylabel('电流 I (A)', fontsize=12)
    ax.set_title('欧姆定律: U-I 特性曲线', fontsize=14, fontweight='bold')
    ax.grid(True, alpha=0.3)
    ax.legend()
    return fig


# ========== Streamlit 主界面 ==========
st.title("🔬 高中物理交互式实验室")

st.markdown("""
这是一个演示 Streamlit 物理实验的模板。
选择下面的选项卡进行不同的实验。
""")

# 使用标签页组织不同实验
tab1, tab2 = st.tabs(["库仑定律", "欧姆定律"])

# ========== 标签页 1：库仑定律 ==========
with tab1:
    st.header("库仑定律实验")
    
    st.markdown("""
    **物理规律**: $F = k \\frac{q_1 q_2}{r^2}$
    
    其中:
    - F 是相互作用力 (N)
    - k = 8.99×10⁹ N·m²/C² 是库仑常数
    - q₁, q₂ 是电荷量 (C)
    - r 是两电荷间距离 (m)
    """)
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("参数设置")
        q1 = st.slider("电荷 q₁ (nC)", min_value=1, max_value=100, value=10, step=1)
        q2 = st.slider("电荷 q₂ (nC)", min_value=1, max_value=100, value=10, step=1)
        r = st.slider("距离 r (cm)", min_value=1, max_value=50, value=10, step=1)
        r_max = st.slider("显示范围上限 (cm)", min_value=5, max_value=50, value=20, step=1)
    
    with col2:
        st.subheader("实验结果")
        
        # 计算力
        F = calculate_force(q1, q2, r)
        
        # 显示数值结果
        col_metric1, col_metric2, col_metric3 = st.columns(3)
        with col_metric1:
            st.metric("当前距离", f"{r} cm")
        with col_metric2:
            st.metric("当前力", f"{F:.3e} N")
        with col_metric3:
            force_type = "吸引" if q1 * q2 < 0 else "排斥"
            st.metric("力的性质", force_type)
        
        # 绘制曲线
        fig = plot_coulombs_law(q1, q2, r_max)
        # 在曲线上标出当前点
        ax = fig.get_axes()[0]
        ax.plot(r, F, 'ro', markersize=10, label='当前点')
        ax.legend()
        
        st.pyplot(fig)

        # 导出结果
        if st.button("导出本次库仑定律结果"):
            png_path = save_plot(fig, "coulombs_law_plot.png")
            csv_data = create_csv_data(
                ["r (cm)", "F (N)"],
                [[rv, fv] for rv, fv in zip(np.linspace(0.1, r_max, 100), [calculate_force(q1, q2, rv) for rv in np.linspace(0.1, r_max, 100)])]
            )
            csv_path = save_csv(csv_data, "coulombs_law_data.csv", headers=["r (cm)", "F (N)"])
            st.success(f"已导出结果到:\n{png_path}\n{csv_path}")

    # 物理解释
    st.markdown(f"""
    ### 物理意义
    
    - 电荷 q₁ = {q1} nC，电荷 q₂ = {q2} nC
    - 当前距离 r = {r} cm
    - 相互作用力 F = {F:.3e} N
    
    **观察现象**:
    - 当距离减小时，力的大小迅速增大（反平方律）
    - 两个同号电荷相斥，异号电荷相吸
    - 通过调整滑块可以观察力如何随参数变化
    """)


# ========== 标签页 2：欧姆定律 ==========
with tab2:
    st.header("欧姆定律实验")
    
    st.markdown("""
    **物理规律**: $U = IR$ 或 $I = \\frac{U}{R}$
    
    其中:
    - U 是电压 (V)
    - I 是电流 (A)
    - R 是电阻 (Ω)
    """)
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("参数设置")
        
        U = st.slider("电压 U (V)", min_value=0, max_value=10, value=5, step=0.1)
        
        # 多个电阻用于对比
        st.write("**电阻选择**")
        R1 = st.checkbox("R₁ = 10 Ω", value=True)
        R2 = st.checkbox("R₂ = 20 Ω", value=True)
        R3 = st.checkbox("R₃ = 50 Ω", value=False)
        
        # 收集选中的电阻
        R_selected = []
        if R1:
            R_selected.append(10)
        if R2:
            R_selected.append(20)
        if R3:
            R_selected.append(50)
    
    with col2:
        st.subheader("实验结果")
        
        # 计算电流
        if R_selected:
            currents = []
            for R in R_selected:
                I = ohms_law(U, R)
                currents.append(I)
                st.metric(f"当 R = {R} Ω 时的电流", f"{I:.3f} A")
            
            # 绘制 U-I 曲线
            fig = plot_ohms_law(R_selected, U_max=max(10, U*1.5))
            
            # 在曲线上标出当前点
            ax = fig.get_axes()[0]
            colors = plt.cm.viridis(np.linspace(0, 1, len(R_selected)))
            for R, I, color in zip(R_selected, currents, colors):
                ax.plot(U, I, 'o', markersize=10, color=color)
            
            st.pyplot(fig)

            if st.button("导出本次欧姆定律结果"):
                png_path = save_plot(fig, "ohms_law_plot.png")
                csv_rows = []
                U_range = np.linspace(0, max(10, U * 1.5), 100)
                for R in R_selected:
                    I_values = U_range / R
                    for u_val, i_val in zip(U_range, I_values):
                        csv_rows.append([R, u_val, i_val])
                csv_data = create_csv_data(["R (Ω)", "U (V)", "I (A)"], csv_rows)
                csv_path = save_csv(csv_data, "ohms_law_data.csv", headers=["R (Ω)", "U (V)", "I (A)"])
                st.success(f"已导出结果到:\n{png_path}\n{csv_path}")
        else:
            st.warning("请至少选择一个电阻")
    
    # 物理解释
    st.markdown(f"""
    ### 物理意义
    
    - 电压 U = {U} V
    
    **观察现象**:
    - 对于同一电阻，电流与电压成正比（线性关系）
    - 对于同一电压，电流与电阻成反比
    - 通过调整滑块可以观察 U-I 曲线的变化
    - 电阻越小，在相同电压下电流越大
    """)


# 页脚
st.markdown("---")
st.markdown("""
💡 **提示**: 这个模板展示了如何用 Streamlit 创建物理交互式实验。
你可以参照这个结构为其他物理主题创建类似的工具。
""")
