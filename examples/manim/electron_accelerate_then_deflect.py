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

“动态约去同类项”一段（第 6、9 镜）的做法，参考真实网课的板书习惯：
  ① 被替换的式子写成蓝色方框（#4D9BFF，淡蓝底色）放在旁边，
     再用箭头指到代入位置；
  ② 被约去的符号上画红色斜线（#FF4D4D），由 Create 动画从左上往右下
     “划下去”，两条线分两批出现（先 e 后 m）；
  ③ 划掉的整项随后淡出，留下的式子用黄色收口。
  为了让红斜线精确落在具体字母上（而不是歪在字符旁边），本例不把整条
  公式写成一个字符串，而是按“令牌”拆成多个 MathTex 参数（见 eq()）：
  LaTeX 的基线、间距、\\frac 横线完全不变，但每个符号都是独立子对象，
  斜线长度按“沿斜线方向穿过整个字框”计算（见 slash()），
  所以短胖的 m 与瘦高的 e 都能被跨满而不会甩出很远。

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
CANCEL = "#FF4D4D"        # 约去：红色斜线
SUBST = "#4D9BFF"         # 待代入式：蓝色方框

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


# ---------------- 代入 / 约去 专用元件
def eq(*parts, size=42, color=INK):
    """把一条公式按“令牌”写成多个 MathTex 参数。

    manim 会把每个参数包成独立的 SVG 分组，所以 LaTeX 版式（基线、间距、
    \\frac 的横线）与整串书写完全一致，但每个符号都能单独取出，
    替换、箭头指向、画约去线都不会“压偏”。
    """
    return MathTex(*parts, font_size=size, color=color)


def place_like(mob, ref, idx=0):
    """让 mob 的第 idx 个令牌与 ref 的第 idx 个重合 —— 换式子时左侧不跳动。"""
    mob.shift(ref[idx].get_center() - mob[idx].get_center())
    return mob


def slash(mobj, angle=-52, sw=5.6, color=CANCEL, extra=0.0, grow=1.22):
    """红色斜线：从左上方划到右下方，比字符略长，斜跨整个符号。

    长度按“沿该方向穿过整个字框”算：w·|cos| + h·|sin|，再放大 22%，
    于是短胖的 m 和瘦高的 e 都能被跨满，两侧各露出一点，像手写的删除线。
    """
    w, h = float(mobj.width), float(mobj.height)
    a = np.deg2rad(angle)
    length = max(grow * (w * abs(np.cos(a)) + h * abs(np.sin(a))), 0.30) + extra
    d = np.array([np.cos(a), np.sin(a), 0.0])
    c = mobj.get_center()
    ln = Line(c - d * length / 2.0, c + d * length / 2.0,
              color=color, stroke_width=sw, stroke_opacity=0.96)
    ln.set_z_index(6)
    return ln


def subst_box(formula, tag):
    """蓝色方框（带淡蓝底色）圈住待代入式，上方一行小标签。"""
    box = RoundedRectangle(
        width=formula.width + 0.46, height=formula.height + 0.30,
        corner_radius=0.12, stroke_color=SUBST, stroke_width=3.0,
        fill_color=SUBST, fill_opacity=0.10,
    )
    formula.move_to(box.get_center())
    lab = cn(tag, 20, SUBST, BOLD).next_to(box, UP, buff=0.10)
    box.set_z_index(1)
    return VGroup(box, formula, lab)


def point_at(box_group, target, color=SUBST, sw=3.0):
    """蓝框左沿 → 被替换位置的箭头；停在符号外侧，不压住字符。"""
    start = box_group[0].get_left() + LEFT * 0.02
    c = target.get_center()
    v = np.array([c[0] - start[0], c[1] - start[1], 0.0])
    v = v / (np.linalg.norm(v) or 1.0)
    end = c - v * (0.55 * float(target.width) + 0.14)
    return Arrow(start, end, buff=0.0, color=color, stroke_width=sw,
                 max_tip_length_to_length_ratio=0.11)


def kill_list(mob, idxs):
    """取出若干令牌（用于淡出）并从父对象里摘掉；返回可 FadeOut 的 VGroup。"""
    picked = VGroup(*[mob[i] for i in idxs])
    mob.remove(*[mob[i] for i in idxs])
    return picked


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
        self.beat_substitute()
        self.beat_speed()
        self.beat_angle()
        self.beat_displacement()
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

    # ------------------------------------------------------------ 换式子
    def retarget(self, old, new, keep, drop=(), add=(), extra=(), run_time=1.0):
        """把 old 换成 new，但只对“对得上号”的令牌做 Transform。

        直接 ReplacementTransform 整条公式，两次 LaTeX 排版在中间帧会互相
        错位成一团；这里分两步走：
          ① 先让 kept 的令牌平移到新位置（可拉伸），被替换的项淡出；
          ② 再把新写进去的令牌淡入 —— 先腾位置、再落笔，不会糊在半空。
        """
        t1 = run_time * 0.58
        self.play(*[Transform(a, b) for a, b in keep],
                  *[FadeOut(a) for a in drop], *extra, run_time=t1)
        if add:
            self.play(*[FadeIn(b) for b in add], run_time=run_time - t1)
        self.remove(old, *add)
        self.add(new)
        return new


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

    # ------------------------------------------------------------ 06 代入与约去（tanθ）
    def beat_substitute(self):
        self.set_tag("④ 代入与约去：e、m 相消")

        # 每一式都拆成“令牌”，下标固定：0 = tanθ=，2 = 分子 e，6/12 = 分母两个 m ...
        E0 = eq(r"\tan\theta=", r"\frac{", "v_y", r"}{", "v_0", r"}", size=48
                ).move_to([-1.55, 1.05, 0])
        E1 = place_like(eq(r"\tan\theta=", r"\frac{", "e", "E", "L", r"}{",
                           "m", "v_0^{2}", r"}", size=48), E0)
        E2 = place_like(eq(r"\tan\theta=", r"\frac{", "e", "E", "L", r"}{",
                           "m", r"\cdot", "2", "e", "U_0", "/", "m", r"}", size=48), E0)
        E3 = place_like(eq(r"\tan\theta=", r"\frac{", "E", "L", r"}{",
                           "2", "U_0", r"}", size=48), E0)

        self.play(FadeOut(self.panel, shift=LEFT * 0.12), FadeOut(self.tri), run_time=0.6)
        self.play(FadeIn(E0, scale=0.92), run_time=0.6)
        self.say("从正切定义出发：tanθ = v_y / v₀", 0.7)

        # —— 代入 ①：v_y = eEL/(m v₀)
        b1 = subst_box(mth(r"v_y=\dfrac{eEL}{m v_0}", 34), "代入 ①")
        b1.move_to([4.30, 2.00, 0])
        a1 = point_at(b1, E0[2])
        self.say("竖直分速度 v_y = eEL/(m v₀)：先代这一项")
        self.play(FadeIn(b1, shift=LEFT * 0.10), GrowArrow(a1), run_time=0.7)
        self.play(Circumscribe(E0[2], color=SUBST, run_time=0.8))
        # v_y → eEL（v_y 的首字变成 e）、v₀ → v₀²，新出现的 E、L、m 淡入
        self.retarget(E0, E1,
                      [(E0[0], E1[0]), (E0[1], E1[1]), (E0[2], E1[2]),
                       (E0[3], E1[5]), (E0[4], E1[7])],
                      add=[E1[3], E1[4], E1[6]],
                      extra=[FadeOut(b1), FadeOut(a1)], run_time=1.0)
        self.say("分母随之出现 v₀² —— 它要用加速段的结论换掉", 0.7)

        # —— 代入 ②：v₀² = 2eU₀/m（蓝框 + 箭头）
        b2 = subst_box(mth(r"v_0^{2}=\dfrac{2eU_0}{m}", 34), "待代入")
        b2.move_to([4.30, 0.32, 0])
        a2 = point_at(b2, E1[7])
        self.play(FadeIn(b2, shift=LEFT * 0.10), GrowArrow(a2), run_time=0.7)
        self.play(Indicate(b2[1], color=SUBST, scale_factor=1.05), run_time=0.8)
        self.say("把 v₀² 整项换成 2eU₀/m：分母变成 m·2eU₀/m")
        # v₀² 淡出，·2eU₀/m 就地淡入；分式横线与分子随之被拉宽
        self.retarget(E1, E2, [(E1[i], E2[i]) for i in range(7)],
                      drop=[E1[7]], add=[E2[i] for i in range(7, 13)],
                      extra=[FadeOut(a2)], run_time=1.1)
        ins = VGroup(*E2[7:13])
        self.play(ins.animate.set_color(SUBST), run_time=0.4)
        self.play(ins.animate.set_color(INK), FadeOut(b2), run_time=0.5)
        self.say("接下来 e 与 e、m 与 m 各约掉一个", 0.6)

        # —— 动态约去：红斜线从左上划到右下
        se_n, se_d = slash(E2[2]), slash(E2[9])
        lab_e = cn("e 约去", 22, CANCEL, BOLD).next_to(se_n, UP, buff=0.12)
        self.say("约 e：分子一个 e，分母 2eU₀ 里一个 e", 0.4)
        self.play(Create(se_n), Create(se_d), run_time=0.85)
        self.play(FadeIn(lab_e, shift=UP * 0.05), run_time=0.3)

        sm_a, sm_b = slash(E2[6]), slash(E2[12])
        lab_m = cn("m 约去", 22, CANCEL, BOLD).next_to(sm_a, DOWN, buff=0.16)
        self.say("约 m：分母开头的 m 与 /m 里的 m 相消", 0.4)
        self.play(Create(sm_a), Create(sm_b), run_time=0.8)
        self.play(FadeIn(lab_m, shift=DOWN * 0.05), run_time=0.3)

        # —— 划掉的整项淡出，剩下的自己“收口”
        self.say("被划掉的整项消失，只剩 EL 与 2U₀", 0.6)
        alive = {i: E2[i] for i in (0, 1, 3, 4, 5, 8, 10, 13)}
        dead = kill_list(E2, [2, 6, 7, 9, 11, 12])
        self.play(FadeOut(VGroup(dead, se_n, se_d, sm_a, sm_b, lab_e, lab_m)), run_time=0.85)
        self.retarget(E2, E3,
                      [(alive[0], E3[0]), (alive[1], E3[1]), (alive[3], E3[2]),
                       (alive[4], E3[3]), (alive[5], E3[4]), (alive[8], E3[5]),
                       (alive[10], E3[6]), (alive[13], E3[7])], run_time=1.0)
        ring = SurroundingRectangle(E3, color=KEY, buff=0.14, stroke_width=2.4)
        self.play(E3.animate.set_color(KEY), Create(ring), run_time=0.7)
        self.play(Circumscribe(E3, color=KEY, run_time=1.0))
        self.say("约干净了：tanθ = EL/(2U₀) —— e、m 全部被约去", 0.8)

        num = mth(r"=\frac{5000\times 0.06}{2\times 1000}=\frac{3}{20}", 40, KEY)
        num.next_to(E3, RIGHT, buff=0.52)
        self.say("代入数值：5000×0.06/(2×1000) = 3/20")
        self.play(FadeIn(num, shift=LEFT * 0.12), run_time=0.6)
        self.play(Circumscribe(num, color=KEY, run_time=1.0))
        self.say("3/20 是正切值 —— 它只由 E、L、U₀ 决定", 0.8)
        self.play(FadeOut(VGroup(E3, num, ring)), run_time=0.7)

    # ------------------------------------------------------------ 07 出射速度大小
    def beat_speed(self):
        self.set_tag("⑤ 出射速度：用上 3/20")
        b1 = mth(r"v=\sqrt{v_0^{2}+v_y^{2}}"
                 r"=\sqrt{1+\left(\frac{3}{20}\right)^{2}}\;v_0"
                 r"=\frac{\sqrt{409}}{20}\,v_0", 38)
        b2 = mth(r"=\frac{\sqrt{409}}{20}\sqrt{\frac{2eU_0}{m_e}}"
                 r"\approx 1.9\times10^{7}\ \mathrm{m/s}", 38, KEY)
        blk = column([b1, b2], 0, 1.30, gap=0.42, max_w=12.4)

        self.play(FadeIn(b1, shift=UP * 0.10), run_time=0.7)
        self.say("合成：v = √(1+(3/20)²)·v₀ = (√409/20)·v₀")
        self.play(FadeIn(b2, shift=UP * 0.10), run_time=0.7)
        self.play(Circumscribe(b2, color=KEY, run_time=1.0))
        self.say("再把 v₀ = √(2eU₀/mₑ) 代进去，得到出射速度的精确式", 1.0)
        self.play(FadeOut(blk), run_time=0.6)

    # ------------------------------------------------------------ 08 夹角
    def beat_angle(self):
        self.set_tag("⑥ 夹角：3/20 是正切值")
        c1 = mth(r"\tan\theta=\frac{3}{20}", 52, KEY).move_to([0, 1.60, 0])
        c2 = mth(r"\theta=\arctan\frac{3}{20}\approx 8.5^{\circ}", 50, KEY).move_to([0, 0.35, 0])
        warn = cn("3/20 是正切值，不是角度", 30, WARN, BOLD).move_to([0, -1.05, 0])

        self.say("比值 3/20 是正切值，它决定夹角，不是角度本身")
        self.play(FadeIn(c1, shift=UP * 0.10), run_time=0.6)
        self.play(FadeIn(c2, shift=UP * 0.10), run_time=0.6)
        self.play(FadeIn(warn, scale=0.92), run_time=0.5)
        self.say("严格写法是 θ = arctan(3/20)，约 8.5°", 0.9)
        self.blk_angle = VGroup(c1, c2, warn)
        self.play(FadeOut(self.blk_angle), run_time=0.6)

    # ------------------------------------------------------------ 09 偏转位移（同样代入 + 约去）
    def beat_displacement(self):
        self.set_tag("⑦ 偏转位移：再代一次、再约一次")

        Y1 = eq(r"|y|=\frac{1}{2}a_y t^{2}=", r"\frac{", "e", "E", "L^{2}", r"}{",
                "2", "m", "v_0^{2}", r"}", size=42).move_to([-1.30, 1.10, 0])
        Y2 = place_like(eq(r"|y|=\frac{1}{2}a_y t^{2}=", r"\frac{", "e", "E", "L^{2}", r"}{",
                           "2", "m", r"\cdot", "2", "e", "U_0", "/", "m", r"}", size=42), Y1)
        Y3 = place_like(eq(r"|y|=\frac{1}{2}a_y t^{2}=", r"\frac{", "E", "L^{2}", r"}{",
                           "4", "U_0", r"}", size=42), Y1)

        self.say("再看偏转位移：|y| = ½a_y t²，代入 a_y 与 t")
        self.play(FadeIn(Y1, shift=UP * 0.10), run_time=0.7)
        self.play(Circumscribe(Y1[4], color=KEY, run_time=0.9))
        self.say("竖直位移 = ½·(eE/m)·(L/v₀)² = eEL²/(2m v₀²)", 0.7)

        b3 = subst_box(mth(r"v_0^{2}=\dfrac{2eU_0}{m}", 32), "待代入")
        b3.move_to([4.30, 0.52, 0])
        a3 = point_at(b3, Y1[8])
        self.play(FadeIn(b3, shift=LEFT * 0.10), GrowArrow(a3), run_time=0.7)
        self.say("还是同一个待代入式：v₀² = 2eU₀/m")
        self.retarget(Y1, Y2, [(Y1[i], Y2[i]) for i in range(8)],
                      drop=[Y1[8]], add=[Y2[i] for i in range(8, 14)],
                      extra=[FadeOut(a3)], run_time=1.0)
        self.play(Indicate(VGroup(*Y2[8:14]), color=SUBST, scale_factor=1.10), run_time=0.9)
        self.play(FadeOut(b3), run_time=0.4)
        self.say("分母成了 2m·2eU₀/m —— 和上一段一样收拾", 0.6)

        se_n, se_d = slash(Y2[2]), slash(Y2[10])
        lab_e = cn("e 约去", 22, CANCEL, BOLD).next_to(se_n, UP, buff=0.12)
        self.say("约 e：分子一个 e，分母 2eU₀ 里一个 e", 0.4)
        self.play(Create(se_n), Create(se_d), run_time=0.85)
        self.play(FadeIn(lab_e, shift=UP * 0.05), run_time=0.3)

        sm_a, sm_b = slash(Y2[7]), slash(Y2[13])
        lab_m = cn("m 约去", 22, CANCEL, BOLD).next_to(sm_a, DOWN, buff=0.16)
        self.say("约 m：2m 里的 m 与 /m 里的 m 相消", 0.4)
        self.play(Create(sm_a), Create(sm_b), run_time=0.8)
        self.play(FadeIn(lab_m, shift=DOWN * 0.05), run_time=0.3)

        self.say("e、m 约去，分母 2×2 = 4：|y| = EL²/(4U₀)", 0.6)
        alive = {i: Y2[i] for i in (0, 1, 3, 4, 5, 6, 9, 11, 14)}
        dead = kill_list(Y2, [2, 7, 8, 10, 12, 13])
        self.play(FadeOut(VGroup(dead, se_n, se_d, sm_a, sm_b, lab_e, lab_m)), run_time=0.85)
        # 分母两个 2 合成 4：第一个 2 变成 4，第二个 2 淡出
        self.retarget(Y2, Y3,
                      [(alive[0], Y3[0]), (alive[1], Y3[1]), (alive[3], Y3[2]),
                       (alive[4], Y3[3]), (alive[5], Y3[4]), (alive[6], Y3[5]),
                       (alive[11], Y3[6]), (alive[14], Y3[7])],
                      drop=[alive[9]], run_time=1.0)
        self.play(Y3.animate.set_color(KEY), run_time=0.5)
        self.play(Circumscribe(Y3, color=KEY, run_time=1.0))

        num = mth(r"=\frac{5000\times(0.06)^{2}}{4\times 1000}"
                  r"=\frac{18}{4000}=\frac{9}{2000}\ \mathrm{m}", 36, KEY)
        num.move_to([-0.30, -0.80, 0])
        self.say("代入数值：5000×0.06²/(4×1000) = 18/4000 = 9/2000 m")
        self.play(FadeIn(num, shift=UP * 0.10), run_time=0.7)
        self.play(Circumscribe(num, color=KEY, run_time=1.0))

        note = cn("方向向上；全程只用 E、L、U₀，不需要偏转板间距", 22, MUTED)
        note.move_to([0, -1.80, 0])
        self.play(FadeIn(note, shift=UP * 0.08), run_time=0.5)
        self.say("推导全程没有用到偏转板间距 —— 题目也没给这个量", 1.0)
        self.blk_y = VGroup(Y3, num, note)
        self.play(FadeOut(self.blk_y), run_time=0.7)

    # ------------------------------------------------------------ 10 教材第5题
    def beat_exam(self):
        head = cn("回到教材第 5 题", 34, KEY, BOLD).move_to([0, 2.95, 0])
        r1 = VGroup(
            cn("出射速度大小", 26, MUTED),
            mth(r"v=\frac{\sqrt{409}}{20}\sqrt{\frac{2eU_0}{m_e}}", 34),
            mth(r"\approx 1.9\times10^{7}\ \mathrm{m/s}", 28, MUTED),
        ).arrange(RIGHT, buff=0.35).move_to([0, 2.10, 0])
        r2 = VGroup(
            cn("与入射方向的夹角", 26, MUTED),
            mth(r"\theta=\arctan\frac{3}{20}", 34, KEY),
            mth(r"\approx 8.5^{\circ}", 28, MUTED),
        ).arrange(RIGHT, buff=0.35).move_to([0, 1.42, 0])
        r3 = VGroup(
            cn("出板竖直偏移", 26, MUTED),
            mth(r"|y|=\frac{EL^{2}}{4U_0}=\frac{9}{2000}\ \mathrm{m}", 34, KEY),
            cn("向上", 26, MUTED),
        ).arrange(RIGHT, buff=0.35).move_to([0, 0.76, 0])
        divider = Line([-6.30, 0.34, 0], [6.30, 0.34, 0],
                       color="#243040", stroke_width=1.5)
        steps = VGroup(
            cn("① 加速段：静电力做功 = 动能增量，定出入射速度", 24, INK),
            cn("② 偏转段：水平匀速 + 竖直匀加速，求出时间与竖直分速度", 24, INK),
            cn("③ 合成与约去：e、m 全消，结果只由 E、L、U₀ 决定", 24, INK),
        ).arrange(DOWN, buff=0.32).move_to([0, -0.62, 0])
        concl = cn("先定入射速度 → 再分解求分速度 → 代入约去 → 合成", 26, KEY, BOLD
                   ).move_to([0, -2.35, 0])

        for m in (r1, r2, r3, steps):
            fit(m, max_w=12.4)

        self.say("回到教材第 5 题：写出最终答案")
        self.play(FadeIn(head, shift=DOWN * 0.10), run_time=0.6)
        self.play(FadeIn(r1, shift=UP * 0.10), run_time=0.6)
        self.say("出射速度 (√409/20)√(2eU₀/mₑ)，约 1.9×10⁷ m/s")
        self.play(FadeIn(r2, shift=UP * 0.10), run_time=0.6)
        self.say("与入射方向夹角 θ = arctan(3/20)，约 8.5°")
        self.play(FadeIn(r3, shift=UP * 0.10), run_time=0.6)
        self.say("出板竖直偏移 9/2000 m，方向向上")
        self.play(Create(divider), run_time=0.5)
        self.play(LaggedStart(*[FadeIn(s, shift=RIGHT * 0.12) for s in steps],
                              lag_ratio=0.35), run_time=1.4)
        self.say("分析顺序：先加速、再分解、代入约去、最后合成", 0.8)
        self.play(FadeIn(concl, shift=UP * 0.10), run_time=0.6)
        self.say("两段场、两个模型：动能定理 + 类平抛", 2.4)
