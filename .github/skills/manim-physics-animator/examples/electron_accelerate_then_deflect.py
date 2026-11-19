# -*- coding: utf-8 -*-
"""电子先加速、再偏转 —— 教材第 5 题分步推导动画（16:9）

教材依据：人教版《普通高中教科书·物理》必修第三册
          第十章第 5 节“练习与应用”第 5 题（教材 P49）
题设：电子由静止经 U₀ = 1000 V 加速，再垂直进入 E = 5000 N/C 的匀强偏转电场，
      偏转电极长 L = 6 cm。求出射速度大小及其与入射方向的夹角。

统一物理约定：
  e > 0 是电子电荷量的大小，电子实际电荷为 −e；mₑ 为电子质量。
  取向右为 +x、向上为 +y：电子向右加速、向上偏转。
    加速区：左板负、右板正 → 电场向左，静电力向右；
    偏转区：上板正、下板负 → 电场向下，静电力向上。
  电子由静止出发，偏转场匀强，忽略重力、边缘效应与相对论修正。
  教材题未给偏转板间距，全程不把板距当已知量。

精确结果（不把近似小数当标准答案）：
  v_y/v₀ = eEL/(mₑv₀²) = EL/(2U₀) = 3/20
  v出 = √(v₀²+v_y²) = (√409/20)v₀ = (√409/20)√(2eU₀/mₑ)
  tanθ = 3/20，θ = arctan(3/20)（3/20 是正切值，不是角度）
  |y| = ½a_y t² = EL²/(4U₀) = 9/2000 m，方向向上

画面比例：L = 6 cm 对应 3.8 个画面单位，纵向用同一比例，故出板纵向位移
0.0045 m 对应 0.285 单位；出射切线与水平方向夹角恰为 arctan(3/20)，
与第 5 镜的速度三角形一致（角度没有夸大）。

渲染：
  D:\\python3.14\\python.exe -m manim -qh --media_dir "<仓库>\\build" ^
      electron_accelerate_then_deflect.py ElectronAccelerateThenDeflectScene
  （低清预览把 -qh 换成 -ql）

环境：MathTex 依赖 TeX 发行版（latex + dvisvgm）。本机已安装用户级 MiKTeX，
      bin 目录已写入用户 PATH；若命令提示找不到 latex，重开终端，或先把
      C:\\Users\\<用户>\\AppData\\Local\\Programs\\MiKTeX\\miktex\\bin\\x64 加到 PATH。
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
from manim import *

ROOT = Path(__file__).resolve().parents[4]
config.media_dir = str(ROOT / "build")
config.frame_width = 14.222
config.frame_height = 8.0
config.background_color = "#0a0f15"

FONT = "Microsoft YaHei"

INK = "#e8eef7"
MUTED = "#8ea3bd"
DIM = "#5f7590"
POS = "#e0566a"
NEG = "#5b8def"
PLATE = "#98a2b3"
FIELD = "#34d399"
FORCE = "#ffd166"
TRAJ = "#ff7ab6"
KEY = "#ffe066"
WARN = "#ffb86b"
ELEC = "#7ce7ff"
VY = "#9fb8d6"

# ---------------- 版面（画面示意图坐标）
ACC_X0, ACC_X1 = -6.28, -5.08      # 加速区两极板
ACC_H = 1.12                       # 加速板半高
DEF_X0, DEF_X1 = -4.45, -0.65      # 偏转板起止
DEF_Y = 0.95                       # 偏转板到中线的距离
DEF_LEN = DEF_X1 - DEF_X0
SCALE_M2U = DEF_LEN / 0.06         # 63.3 画面单位 / 米（x、y 同比例）
EXIT_Y = 0.0045 * SCALE_M2U        # 出板纵向位移 = 0.285 单位，与真实比例一致
FX = 3.40                          # 右侧公式列中心
PANEL_TOP = 2.55

THETA = float(np.arctan(3.0 / 20.0))   # 出射角（弧度）


# ---------------- 辅助
def cn(text, size=26, color=INK, weight=NORMAL):
    return Text(text, font=FONT, font_size=size, color=color, weight=weight)


def mth(tex, size=32, color=INK):
    return MathTex(tex, font_size=size, color=color)


def fit(mobj, max_w=None, max_h=None):
    if max_w and mobj.width > max_w:
        mobj.scale_to_fit_width(max_w)
    if max_h and mobj.height > max_h:
        mobj.scale_to_fit_height(max_h)
    return mobj


def arrow(p0, p1, color=FORCE, sw=4.0, tip=0.30):
    return Arrow(p0, p1, buff=0.0, color=color, stroke_width=sw,
                 max_tip_length_to_length_ratio=tip)


def column(items, x, top, gap=0.18, max_w=5.0, max_h=None):
    """把若干对象从上往下排成一列，返回已定位的 VGroup（顶部对齐 top）。"""
    y = 0.0
    for it in items:
        fit(it, max_w=max_w)
        y -= it.height / 2
        it.move_to([0, y, 0])
        y -= it.height / 2 + gap
    group = VGroup(*items)
    if max_h and group.height > max_h:
        group.scale_to_fit_height(max_h)
    group.move_to([x, top - group.height / 2, 0])
    return group


def parabola_points(u0=None, u1=1.0, n=41):
    pts = []
    for k in range(n):
        u = (u0 or 0.0) + (u1 - (u0 or 0.0)) * k / (n - 1)
        pts.append(np.array([DEF_X0 + DEF_LEN * u, EXIT_Y * u ** 2, 0.0]))
    return pts


# ---------------- 场景
class ElectronAccelerateThenDeflectScene(Scene):
    def construct(self):
        self.cap = None
        self.tag = None
        self.stage = VGroup()      # 装置图上会被整体收起的对象
        self.panel = None

        self.header = VGroup(
            cn("带电粒子先加速、再偏转", 21, MUTED, BOLD),
            Line([0, 0, 0], [0, 0.26, 0], color=DIM, stroke_width=1.6),
            cn("教材第 5 题", 19, DIM),
        ).arrange(RIGHT, buff=0.28).to_corner(UL, buff=0.30)

        # 右侧推导列：逐条出现，位置预先固定
        self.panel = column(
            [
                mth(r"eU_0=\tfrac{1}{2}m_e v_0^{2}", 30),
                mth(r"v_0=\sqrt{\dfrac{2eU_0}{m_e}}", 30),
                mth(r"t=\dfrac{L}{v_0}", 30),
                mth(r"a_y=\dfrac{eE}{m_e}", 30),
                mth(r"v_y=a_y t=\dfrac{eEL}{m_e v_0}", 30),
                mth(r"v=\sqrt{v_0^{2}+v_y^{2}}", 30),
                mth(r"\tan\theta=\dfrac{v_y}{v_0}", 30),
            ],
            FX, PANEL_TOP, gap=0.15, max_w=5.0, max_h=4.45,
        )

        self.beat_open()
        self.beat_apparatus()
        self.beat_accel()
        self.beat_deflect()
        self.beat_compose()
        self.beat_ratio()
        self.beat_angle()
        self.beat_exam()

    # ------------------------------------------------------------ 字幕
    def caption_box(self, text, size=26):
        label = cn(text, size, "#f4f8fc")
        fit(label, max_w=11.5)
        bg = RoundedRectangle(
            width=label.width + 0.62, height=label.height + 0.30,
            corner_radius=0.12, fill_color="#05090e", fill_opacity=0.90,
            stroke_width=0,
        )
        return VGroup(bg, label).move_to([0, -3.44, 0])

    def say(self, text, hold=0.55, size=26):
        box = self.caption_box(text, size)
        if self.cap is not None:
            self.play(FadeOut(self.cap), run_time=0.12)
        self.play(FadeIn(box, shift=UP * 0.06), run_time=0.22)
        self.cap = box
        self.wait(hold)

    def set_tag(self, text):
        new = cn(text, 24, KEY, BOLD).move_to([FX, 3.35, 0])
        if self.tag is None:
            self.tag = new
            self.play(FadeIn(new, shift=DOWN * 0.10), run_time=0.45)
        else:
            old = self.tag
            self.tag = new
            self.play(FadeOut(old, shift=UP * 0.10), FadeIn(new, shift=DOWN * 0.10), run_time=0.50)

    @staticmethod
    def electron_at(point):
        body = Circle(radius=0.135, fill_color=ELEC, fill_opacity=1.0,
                      stroke_color="#0a0f15", stroke_width=2)
        sign = Text("−", font=FONT, font_size=20, color="#06121d", weight=BOLD)
        return VGroup(body, sign).move_to(point)

    # ------------------------------------------------------------ 01 开场
    def beat_open(self):
        t1 = cn("带电粒子先加速、再偏转", 46, INK, BOLD)
        t2 = cn("人教版必修第三册 · 第十章第 5 节 练习与应用 第 5 题", 22, MUTED)
        givens = VGroup(
            mth(r"U_0=1000\ \mathrm{V}", 34),
            mth(r"E=5000\ \mathrm{N/C}", 34),
            mth(r"L=6\ \mathrm{cm}", 34),
        ).arrange(RIGHT, buff=0.95)
        ask = cn("求：出射速度大小 v 与偏角 θ", 26, KEY)
        note = cn("电子由静止出发 · 忽略重力、边缘效应与相对论修正", 20, DIM)
        block = VGroup(t1, t2, givens, ask, note).arrange(DOWN, buff=0.40).move_to([0, 0.20, 0])

        self.play(Write(t1), run_time=1.1)
        self.play(FadeIn(t2, shift=UP * 0.10), run_time=0.5)
        self.play(FadeIn(givens, shift=UP * 0.10), run_time=0.6)
        self.play(FadeIn(ask, shift=UP * 0.10), FadeIn(note, shift=UP * 0.10), run_time=0.6)
        self.wait(1.8)
        self.play(FadeOut(block, shift=UP * 0.2), run_time=0.7)
        self.play(FadeIn(self.header, shift=DOWN * 0.12), run_time=0.5)

    # ------------------------------------------------------------ 02 装置
    def beat_apparatus(self):
        left_plate = Rectangle(width=0.15, height=2 * ACC_H, fill_color=PLATE,
                               fill_opacity=0.85, stroke_color="#0b0f14",
                               stroke_width=2).move_to([ACC_X0, 0, 0])
        right_plate = left_plate.copy().move_to([ACC_X1, 0, 0])
        neg_mark = cn("−", 30, NEG, BOLD).move_to([ACC_X0, ACC_H + 0.24, 0])
        pos_mark = cn("+", 30, POS, BOLD).move_to([ACC_X1, ACC_H + 0.24, 0])
        u0_arrow = DoubleArrow([ACC_X0, ACC_H + 0.62, 0], [ACC_X1, ACC_H + 0.62, 0],
                               buff=0, color=MUTED, stroke_width=2.2,
                               max_tip_length_to_length_ratio=0.14)
        u0_label = mth(r"U_0=1000\ \mathrm{V}", 23, KEY).next_to(u0_arrow, UP, buff=0.12)
        e0_arrows = VGroup(*[
            arrow([ACC_X1 - 0.10, y, 0], [ACC_X0 + 0.10, y, 0], FIELD, 3.0, 0.26)
            for y in (-0.86, 0.86)
        ])
        e0_label = VGroup(
            mth("E_0", 22, FIELD), cn("向左", 18, FIELD),
        ).arrange(RIGHT, buff=0.14).move_to([(ACC_X0 + ACC_X1) / 2, -1.40, 0])
        elec_label = cn("电子（电荷 −e）", 19, ELEC).move_to([(ACC_X0 + ACC_X1) / 2, -1.82, 0])

        top_plate = Rectangle(width=DEF_LEN, height=0.12, fill_color=PLATE,
                              fill_opacity=0.85, stroke_color="#0b0f14",
                              stroke_width=2).move_to([(DEF_X0 + DEF_X1) / 2, DEF_Y, 0])
        bot_plate = top_plate.copy().move_to([(DEF_X0 + DEF_X1) / 2, -DEF_Y, 0])
        d_pos = cn("+", 28, POS, BOLD).move_to([DEF_X1 - 0.24, DEF_Y + 0.24, 0])
        d_neg = cn("−", 28, NEG, BOLD).move_to([DEF_X1 - 0.24, -DEF_Y - 0.24, 0])
        e_arrows = VGroup(*[
            arrow([x, DEF_Y - 0.10, 0], [x, -DEF_Y + 0.10, 0], FIELD, 3.0, 0.20)
            for x in np.linspace(DEF_X0 + 0.52, DEF_X1 - 0.52, 5)
        ])
        e_label = VGroup(
            mth("E", 22, FIELD), cn("向下", 18, FIELD),
        ).arrange(RIGHT, buff=0.14).move_to([DEF_X1 + 0.50, 0.62, 0])
        l_arrow = DoubleArrow([DEF_X0, -DEF_Y - 0.44, 0], [DEF_X1, -DEF_Y - 0.44, 0],
                              buff=0, color=MUTED, stroke_width=2.2,
                              max_tip_length_to_length_ratio=0.05)
        l_label = mth(r"L=6\ \mathrm{cm}", 22, MUTED).next_to(l_arrow, DOWN, buff=0.08)

        traj_pts = [np.array([ACC_X0, 0.0, 0.0]), np.array([DEF_X0, 0.0, 0.0])]
        traj_pts += parabola_points()[1:]
        traj = VMobject(color=TRAJ, stroke_width=4.0).set_points_as_corners(traj_pts)

        self.electron = self.electron_at([ACC_X0 + 0.02, 0, 0])

        self.say("电子由静止出发，先经过一段加速电场")
        self.play(FadeIn(left_plate), FadeIn(right_plate),
                  FadeIn(neg_mark), FadeIn(pos_mark), run_time=0.6)
        self.play(GrowArrow(u0_arrow), FadeIn(u0_label), run_time=0.5)
        self.play(LaggedStart(*[GrowArrow(a) for a in e0_arrows], lag_ratio=0.12),
                  FadeIn(e0_label), FadeIn(elec_label), run_time=0.8)
        self.say("加速区：左板接负极、右板接正极 —— 电场向左")
        self.play(FadeIn(top_plate), FadeIn(bot_plate),
                  FadeIn(d_pos), FadeIn(d_neg), run_time=0.6)
        self.play(LaggedStart(*[GrowArrow(a) for a in e_arrows], lag_ratio=0.07),
                  FadeIn(e_label), run_time=0.8)
        self.say("偏转区：上板为正、下板为负 —— 电场向下")
        self.play(GrowArrow(l_arrow), FadeIn(l_label), run_time=0.5)
        self.say("电子进入偏转场后受力向上，轨迹向上弯曲")
        self.play(Create(traj), run_time=1.7)
        self.play(FadeIn(self.electron, scale=0.6),
                  Flash(self.electron, color=ELEC, flash_radius=0.28), run_time=0.7)
        self.say("全程忽略重力，只考虑静电力", 0.8)

        self.stage.add(left_plate, right_plate, neg_mark, pos_mark, u0_arrow, u0_label,
                       e0_arrows, e0_label, elec_label,
                       top_plate, bot_plate, d_pos, d_neg, e_arrows, e_label,
                       l_arrow, l_label, traj, self.electron)

    # ------------------------------------------------------------ 03 加速
    def beat_accel(self):
        self.set_tag("① 加速：定出入射速度 v₀")
        self.say("加速段只有静电力做功 —— 用动能定理")
        f0 = arrow([ACC_X0 + 0.06, 0.30, 0], [ACC_X0 + 0.94, 0.30, 0], FORCE, 4.0, 0.32)
        f0_label = mth(r"F=eE_0", 20, FORCE).move_to([ACC_X0 + 0.50, 0.62, 0])
        self.play(GrowArrow(f0), FadeIn(f0_label), run_time=0.6)
        self.play(Indicate(self.electron, color=FORCE, scale_factor=1.55), run_time=0.9)
        self.say("静电力与电场方向相反，所以电子向右加速")
        self.play(FadeIn(self.panel[0], shift=LEFT * 0.12), run_time=0.5)
        self.say("静电力做的功是 eU₀，等于电子动能的增加量")
        self.play(FadeIn(self.panel[1], shift=LEFT * 0.12), run_time=0.5)
        self.play(Circumscribe(self.panel[1], color=KEY, run_time=1.0))
        self.say("v₀ = √(2eU₀/mₑ)：入射速度只由加速电压决定")
        self.play(MoveAlongPath(self.electron,
                                Line([ACC_X0 + 0.02, 0, 0], [ACC_X1 - 0.10, 0, 0])),
                  run_time=1.8, rate_func=lambda t: t ** 1.8)
        self.stage.add(f0, f0_label)
        self.wait(0.4)

    # ------------------------------------------------------------ 04 偏转
    def beat_deflect(self):
        self.set_tag("② 偏转：定 t 与 v_y")
        self.say("进入偏转场时速度水平 —— 水平方向做匀速直线运动")
        v0_arrow = arrow([DEF_X0 + 0.10, 0.0, 0], [DEF_X0 + 1.15, 0.0, 0], INK, 3.5, 0.26)
        v0_label = mth("v_0", 22, INK).move_to([DEF_X0 + 0.55, 0.26, 0])
        f1 = arrow([DEF_X0 + 2.15, 0.34, 0], [DEF_X0 + 2.15, 0.86, 0], FORCE, 4.0, 0.32)
        f1_label = mth(r"F=eE", 20, FORCE).next_to(f1, RIGHT, buff=0.10)
        self.play(GrowArrow(v0_arrow), FadeIn(v0_label), run_time=0.6)
        self.play(GrowArrow(f1), FadeIn(f1_label), run_time=0.6)
        self.say("竖直方向受恒力，加速度大小 a = eE/mₑ")
        self.play(FadeIn(self.panel[2], shift=LEFT * 0.12), run_time=0.45)
        self.say("水平方向走完板长 L 需要时间 t = L/v₀")
        self.play(FadeIn(self.panel[3], shift=LEFT * 0.12),
                  FadeIn(self.panel[4], shift=LEFT * 0.12), run_time=0.55)
        self.say("竖直分速度 = eEL/(mₑv₀)：几何量只需要板长 L")
        self.play(MoveAlongPath(self.electron, self.move_path()), run_time=2.8,
                  rate_func=linear)
        self.say("出板时竖直分速度向上", 0.8)
        self.stage.add(v0_arrow, v0_label, f1, f1_label)

    def move_path(self):
        pts = [np.array([ACC_X1 - 0.10, 0, 0]), np.array([DEF_X0, 0, 0])]
        pts += parabola_points()[1:]
        return VMobject().set_points_as_corners(pts)

    # ------------------------------------------------------------ 05 合成
    def beat_compose(self):
        self.set_tag("③ 合成：出射速度与夹角")
        self.say("出射速度是水平分速度与竖直分速度的合成")
        self.play(FadeOut(self.stage), run_time=0.7)

        o = np.array([-6.45, -1.95, 0.0])
        a = np.array([-0.95, -1.95, 0.0])
        b = a + np.array([0.0, (a[0] - o[0]) * 0.15, 0.0])   # tanθ = 3/20，长度同比例

        v0_a = arrow(o, a, INK, 4.0, 0.05)
        vy_a = arrow(a, b, VY, 4.0, 0.35)
        v_a = arrow(o, b, KEY, 4.5, 0.05)
        right_angle = Rectangle(width=0.16, height=0.16, stroke_color=MUTED,
                                stroke_width=1.5, fill_opacity=0
                                ).move_to(a + LEFT * 0.08 + UP * 0.08)
        theta_arc = Arc(radius=2.40, start_angle=0, angle=THETA, arc_center=o,
                        color=KEY, stroke_width=2.2)
        theta_lab = mth(r"\theta", 24, KEY).move_to(
            o + 3.00 * np.array([np.cos(THETA / 2), np.sin(THETA / 2), 0.0]))
        lab_v0 = mth("v_0", 26, INK).move_to((o + a) / 2 + DOWN * 0.28)
        lab_vy = mth("v_y", 24, VY).move_to(b + RIGHT * 0.34 + DOWN * 0.10)
        lab_v = mth("v", 26, KEY).move_to((o + b) / 2 + UP * 0.26 + LEFT * 0.30)
        title = cn("速度合成", 26, KEY, BOLD).move_to([-3.70, 0.62, 0])
        subtitle = cn("矢量三角形按真实比例：tanθ = 3/20", 20, MUTED).move_to([-3.70, 0.14, 0])

        self.play(FadeIn(title), FadeIn(subtitle), run_time=0.5)
        self.play(GrowArrow(v0_a), FadeIn(lab_v0), run_time=0.7)
        self.play(GrowArrow(vy_a), FadeIn(lab_vy), FadeIn(right_angle), run_time=0.7)
        self.play(GrowArrow(v_a), Create(theta_arc), FadeIn(theta_lab), FadeIn(lab_v), run_time=0.9)
        self.tri = VGroup(title, subtitle, v0_a, vy_a, v_a, right_angle,
                          theta_arc, theta_lab, lab_v0, lab_vy, lab_v)
        self.say("合速度大小用勾股定理，方向用正切表示")
        self.play(FadeIn(self.panel[5], shift=LEFT * 0.12), run_time=0.5)
        self.say("合速度大小的精确式就是勾股定理")
        self.play(FadeIn(self.panel[6], shift=LEFT * 0.12), run_time=0.5)
        self.say("方向：tanθ 等于竖直分速度与水平分速度之比", 0.9)

    # ------------------------------------------------------------ 06 比值
    def beat_ratio(self):
        self.play(FadeOut(self.tag), FadeOut(self.tri), FadeOut(self.panel), run_time=0.7)
        self.say("先算比值：e 与 mₑ 全部约去")
        a1 = mth(r"\frac{v_y}{v_0}=\frac{eEL}{m_e v_0^{2}}=\frac{EL}{2U_0}", 36)
        a2 = mth(r"=\frac{5000\times 0.06}{2\times 1000}=\frac{3}{20}", 36, KEY)
        note = cn("e、mₑ 被约去：这个比值只由 E、L、U₀ 决定", 21, MUTED)
        b1 = mth(r"v=\sqrt{v_0^{2}+v_y^{2}}=\sqrt{1+\left(\frac{3}{20}\right)^{2}}"
                 r"\;v_0=\frac{\sqrt{409}}{20}\,v_0", 32)
        b2 = mth(r"=\frac{\sqrt{409}}{20}\sqrt{\frac{2eU_0}{m_e}}"
                 r"\approx 1.9\times10^{7}\ \mathrm{m/s}", 32, KEY)
        self.block5 = column([a1, a2, note, b1, b2], 0, 2.05, gap=0.30,
                             max_w=11.4, max_h=4.85)

        self.play(FadeIn(a1, shift=UP * 0.10), run_time=0.6)
        self.say("先写出比值，再用 eU₀ = ½mₑv₀² 把 v₀² 换掉")
        self.play(FadeIn(a2, shift=UP * 0.10), run_time=0.6)
        self.play(Circumscribe(a2, color=KEY, run_time=1.0))
        self.say("比值 = EL/(2U₀) = 5000×0.06/(2×1000) = 3/20")
        self.play(FadeIn(note, shift=UP * 0.10), run_time=0.5)
        self.play(FadeIn(b1, shift=UP * 0.10), run_time=0.6)
        self.say("合成：v = √(1+(3/20)²)·v₀ = (√409/20)·v₀")
        self.play(FadeIn(b2, shift=UP * 0.10), run_time=0.6)
        self.say("把 v₀ = √(2eU₀/mₑ) 代进去即得精确式", 1.0)

    # ------------------------------------------------------------ 07 夹角与位移
    def beat_angle(self):
        self.play(FadeOut(self.block5), run_time=0.6)
        self.say("比值 3/20 是正切值，它决定夹角，不是角度本身")
        c1 = mth(r"\frac{v_y}{v_0}=\tan\theta=\frac{3}{20}", 42, KEY)
        c2 = mth(r"\theta=\arctan\frac{3}{20}\approx 8.5^{\circ}", 42, KEY)
        warn = cn("3/20 是正切值，不是角度", 26, WARN, BOLD)
        d1 = mth(r"|y|=\frac{1}{2}a_y t^{2}=\frac{EL^{2}}{4U_0}"
                 r"=\frac{9}{2000}\ \mathrm{m}\approx 4.5\ \mathrm{mm}", 32)
        d2 = cn("方向向上；只用 E、L、U₀，不需要偏转板间距", 21, MUTED)
        self.block6 = column([c1, c2, warn, d1, d2], 0, 1.95, gap=0.30,
                             max_w=11.4, max_h=4.90)

        self.play(FadeIn(c1, shift=UP * 0.10), run_time=0.6)
        self.say("tanθ = 3/20，所以 θ = arctan(3/20)")
        self.play(FadeIn(c2, shift=UP * 0.10), run_time=0.6)
        self.play(FadeIn(warn, shift=UP * 0.10), run_time=0.5)
        self.say("严格写法是 θ = arctan(3/20)，约 8.5°", 0.8)
        self.play(FadeIn(d1, shift=UP * 0.10), run_time=0.6)
        self.say("顺带核对偏转位移：精确值 9/2000 m，方向向上")
        self.play(FadeIn(d2, shift=UP * 0.10), run_time=0.5)
        self.say("推导全程没有用到偏转板间距 —— 题目也没给这个量", 1.0)

    # ------------------------------------------------------------ 08 教材第5题
    def beat_exam(self):
        self.play(FadeOut(self.block6), run_time=0.6)
        head = cn("回到教材第 5 题", 34, KEY, BOLD).move_to([0, 2.95, 0])
        r1 = VGroup(
            cn("出射速度大小", 26, MUTED),
            mth(r"v=\frac{\sqrt{409}}{20}\sqrt{\frac{2eU_0}{m_e}}", 34),
            mth(r"\approx 1.9\times10^{7}\ \mathrm{m/s}", 28, MUTED),
        ).arrange(RIGHT, buff=0.35).move_to([0, 2.15, 0])
        r2 = VGroup(
            cn("与入射方向的夹角", 26, MUTED),
            mth(r"\theta=\arctan\frac{3}{20}", 34, KEY),
            mth(r"\approx 8.5^{\circ}", 28, MUTED),
        ).arrange(RIGHT, buff=0.35).move_to([0, 1.45, 0])
        divider = Line([-6.30, 0.95, 0], [6.30, 0.95, 0],
                       color="#243040", stroke_width=1.5)
        steps = VGroup(
            cn("① 加速段：静电力做功 = 动能增量，定出入射速度", 24, INK),
            cn("② 偏转段：水平匀速 + 竖直匀加速，求出时间与竖直分速度", 24, INK),
            cn("③ 速度合成：出射速度大小与夹角一并得到", 24, INK),
        ).arrange(DOWN, buff=0.34).move_to([0, -0.05, 0])
        concl = cn("先定入射速度 → 再分解求分速度 → 最后合成", 26, KEY, BOLD
                   ).move_to([0, -2.00, 0])

        for m in (r1, r2, steps):
            fit(m, max_w=12.2)

        self.say("回到教材第 5 题：写出最终答案")
        self.play(FadeIn(head, shift=DOWN * 0.10), run_time=0.6)
        self.play(FadeIn(r1, shift=UP * 0.10), run_time=0.6)
        self.say("出射速度 (√409/20)√(2eU₀/mₑ)，约 1.9×10⁷ m/s")
        self.play(FadeIn(r2, shift=UP * 0.10), run_time=0.6)
        self.say("与入射方向夹角 θ = arctan(3/20)，约 8.5°")
        self.play(Create(divider), run_time=0.5)
        self.play(LaggedStart(*[FadeIn(s, shift=RIGHT * 0.12) for s in steps],
                              lag_ratio=0.35), run_time=1.4)
        self.say("分析顺序：先加速、再分解、最后合成", 0.8)
        self.play(FadeIn(concl, shift=UP * 0.10), run_time=0.6)
        self.say("两段场、两个模型：动能定理 + 类平抛", 2.4)
