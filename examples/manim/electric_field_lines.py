# -*- coding: utf-8 -*-
"""电场线 · 从场强的定义到场线的读法（16:9 / 1080p60）

教材依据：人教版《普通高中教科书·物理》必修第三册
          第九章 静电场 —— 电场强度、电场线

分镜表（9 镜，约 82 s）：
  00 开场      标题 + 本节问题“电场看不见，怎么描述它？”
  01 场强的定义 试探电荷 q 受力 F → E = F/q（E 由场源决定，与 q 无关）
  02 点电荷场强 库仑定律 → E = kQ/r²；r 是场点到点电荷的距离
  03 场线画法   从正电荷出发、到负电荷终止；疏密表示强弱；切线即 E 方向
  04 单个正电荷 等通量（等立体角）取角度采样，辐射状；面密度 ∝ 1/r²
  05 等量异种   场线从正到负；连线中点两个分场强同向叠加，中点场强最大
  06 等量同种   连线中点两个分场强等大反向，合场强为零（画面画出两箭头再抵消）
  07 三条性质   不相交 / 不闭合（静电场）/ 切线方向即场强方向
  08 收口       一屏三条结论

物理约定（改字幕、改箭头时一并遵守）：
  * 场线从正电荷表面发出、到负电荷表面终止，绝不穿过电荷本身；
    所有场线都在电荷表面处起笔/收笔（起止半径 = 电荷半径 + 0.01）。
  * 场线不相交：用数值积分（RK4）沿 E 方向逐点推进，物理上就不会出现交点。
  * 静电场场线不闭合；但“起于正电荷、止于负电荷”只在电荷总量为零的理想
    图景里成立，严格说法是“起于正电荷、止于负电荷，或伸向/来自无穷远”。
  * 单个点电荷按等立体角取样（二维截面里就是等角度），所以远处自然变稀；
    场线面密度 ∝ 1/r² 由“同一立体角内条数不变 + 球面面积 ∝ r²”给出。
  * E = kQ/r² 中的 r 是“场点到点电荷 Q 的距离”，不是两个电荷之间的距离。
  * 等量同种电荷连线中点：两个分场强等大反向，合场强为零；
    等量异种电荷连线中点：两个分场强同向，合场强 2·kQ/(d/2)² = 8kQ/d²。

画面数值（同一组数，前后镜自洽，便于核对）：
  k = 9.0×10⁹ N·m²/C²，Q = 1.0×10⁻⁹ C ⟹ kQ = 9.0 N·m²/C
  r = 0.30 m：E = 9.0/0.09 = 100 N/C
  r = 0.60 m：E = 9.0/0.36 = 25 N/C = 100/4（验证 E ∝ 1/r²）
  试探电荷 q = 1.0×10⁻⁶ C 在同一点受力 F = qE = 1.0×10⁻⁴ N（验证 E = F/q）
  等量异种/同种，d = 0.60 m，中点距各电荷 d/2 = 0.30 m：
      每个分场强 kQ/(d/2)² = 9.0/0.09 = 100 N/C
      异种：同向 ⟹ 100 + 100 = 200 N/C；同种：反向 ⟹ 100 − 100 = 0

渲染：
  D:\\python3.14\\python.exe -m manim -qh --media_dir "<仓库>\\build" ^
      electric_field_lines.py ElectricFieldLinesScene
  （低清预览把 -qh 换成 -ql；-qh = 1920×1080 / 60 fps）

环境：MathTex 依赖 TeX 发行版（latex + dvisvgm）。本机为用户级 MiKTeX，
      bin 目录在 %LOCALAPPDATA%\\Programs\\MiKTeX\\miktex\\bin\\x64。
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

# ---------------------------------------------------------------- 调色板
FONT = "Microsoft YaHei"

INK = "#e8eef7"
MUTED = "#8ea3bd"
DIM = "#5f7590"
POS = "#e0566a"
NEG = "#5b8def"
FIELD = "#34d399"
FORCE = "#ffd166"
KEY = "#ffe066"
WARN = "#ffb86b"
ELEC = "#7ce7ff"
PANEL = "#0e161e"
LINE = "#243040"
CANCEL = "#FF4D4D"

CAPTION_Y = -3.44
CHARGE_R = 0.26


# ---------------------------------------------------------------- 基础元件
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


def head(pos, direction, color=FIELD, size=0.155, opacity=1.0):
    """小三角箭头：贴在曲线上的方向标记（长度短，不会盖住场线）。"""
    d = np.asarray(direction, dtype=float)
    n = float(np.linalg.norm(d))
    if n < 1e-9:
        return VGroup()
    d = d / n
    side = np.array([-d[1], d[0], 0.0])
    tip = np.asarray(pos, dtype=float) + d * size * 0.95
    b1 = np.asarray(pos, dtype=float) - d * size * 0.55 + side * size * 0.62
    b2 = np.asarray(pos, dtype=float) - d * size * 0.55 - side * size * 0.62
    return Polygon(tip, b1, b2, color=color, fill_color=color,
                   fill_opacity=opacity, stroke_width=0)


def charge(sign, center, name="Q", radius=CHARGE_R, label_dir=UP):
    """带电小球：深色符号 + 电荷量标签（标签在球外，不挡场线）。

    符号用深色（不是白色）：与基准视频里电子小球的处理一致，深色字在
    高饱和的红/蓝圆面上更清楚，也不会在暗场里发灰。
    """
    color = POS if sign > 0 else NEG
    body = Circle(radius=radius, fill_color=color, fill_opacity=1.0,
                  stroke_color="#0a0f15", stroke_width=2.0).move_to(center)
    mark = cn("+" if sign > 0 else "-", 30 if radius < 0.32 else 34,
              "#0a0f15", BOLD).move_to(np.asarray(center) + UP * 0.02)
    group = VGroup(body, mark)
    if name:
        lab = mth(name, 28, color).next_to(body, label_dir, buff=0.13)
        group.add(plate(lab, pad_x=0.09, pad_y=0.03))
    return group


def dashed_tie(p0, p1, color=MUTED, sw=1.6):
    return DashedLine(p0, p1, color=color, stroke_width=sw, dash_length=0.11)


def panel_box(width, height, center, stroke=LINE, fill=PANEL, opacity=0.90):
    return RoundedRectangle(width=width, height=height, corner_radius=0.14,
                            stroke_color=stroke, stroke_width=1.8,
                            fill_color=fill, fill_opacity=opacity).move_to(center)


def plate(mobj, pad_x=0.11, pad_y=0.06, opacity=0.93):
    """给贴着场线的标签垫一块暗底，保证压在场线上也能读清（不挡线本身）。"""
    bg = RoundedRectangle(
        width=mobj.width + 2 * pad_x, height=mobj.height + 2 * pad_y,
        corner_radius=0.06, fill_color="#0a0f15", fill_opacity=opacity,
        stroke_width=0,
    ).move_to(mobj)
    bg.set_z_index(8)
    mobj.set_z_index(9)
    return VGroup(bg, mobj)


# ---------------------------------------------------------------- 场与场线
def field_at(p, charges):
    """charges = [(q, center), ...]；q 带正负号，取 kQ 归一为 1。"""
    e = np.zeros(3)
    for q, s in charges:
        d = np.asarray(p, dtype=float) - np.asarray(s, dtype=float)
        r2 = float(d[0] ** 2 + d[1] ** 2)
        if r2 < 1e-9:
            continue
        e += q * d / (r2 * np.sqrt(r2))
    return e


def _unit(v):
    n = float(np.linalg.norm(v))
    return v / n if n > 1e-12 else np.zeros(3)


def in_bounds(p, bounds):
    xmin, xmax, ymin, ymax = bounds
    return xmin <= p[0] <= xmax and ymin <= p[1] <= ymax


def trace(seed, charges, bounds, hit=(), step=0.020, max_steps=1100, stall=1e-3):
    """RK4 沿场方向推进，得到一条场线。

    hit：需要“落在表面”的电荷 [(center, radius), ...] —— 走到表面立刻收笔，
    所以场线只会终止在负电荷表面，不会扎进电荷内部。
    stall：场强小到可以视为零（等量同种电荷的中点鞍点）时停笔。
    """
    pts = [np.array(seed, dtype=float)]
    p = np.array(seed, dtype=float)
    for _ in range(max_steps):
        k1 = _unit(field_at(p, charges))
        if not k1.any():
            break
        k2 = _unit(field_at(p + step * 0.5 * k1, charges))
        k3 = _unit(field_at(p + step * 0.5 * k2, charges))
        k4 = _unit(field_at(p + step * k3, charges))
        d = (k1 + 2.0 * k2 + 2.0 * k3 + k4) / 6.0
        if float(np.linalg.norm(d)) < 1e-9:
            break
        p = p + step * _unit(d)

        for c, r in hit:
            dv = p - np.asarray(c, dtype=float)
            dist = float(np.linalg.norm(dv))
            if dist < r:
                pts.append(np.asarray(c, dtype=float) + dv / max(dist, 1e-9) * r)
                return pts
        if not in_bounds(p, bounds):
            pts.append(p)
            return pts
        pts.append(p)
        if float(np.linalg.norm(field_at(p, charges))) < stall:
            break
    return pts


def line_heads(pts, color=FIELD, fractions=(0.52,), size=0.155, opacity=1.0):
    grp = VGroup()
    n = len(pts)
    for f in fractions:
        i = int(f * (n - 1))
        i = min(max(i, 2), n - 3)
        grp.add(head(pts[i], np.asarray(pts[i + 2]) - np.asarray(pts[i - 2]),
                     color=color, size=size, opacity=opacity))
    return grp


def field_lines(seeds, charges, bounds, hit=(), color=FIELD, sw=2.2,
                fractions=(0.52,), size=0.155, opacity=0.92):
    curves, heads = VGroup(), VGroup()
    for seed in seeds:
        pts = trace(seed, charges, bounds, hit=hit)
        if len(pts) < 6:
            continue
        curve = VMobject(color=color, stroke_width=sw)
        curve.set_points_smoothly([np.array(p, dtype=float) for p in pts])
        curve.set_stroke(color=color, width=sw, opacity=opacity)
        curves.add(curve)
        heads.add(line_heads(pts, color=color, fractions=fractions,
                             size=size, opacity=min(1.0, opacity + 0.08)))
    return curves, heads


def radial_rays(center, bounds, sign=1, count=24, r0=0.36, r_end=4.2,
                fractions=(0.42, 0.74), color=FIELD, sw=2.0):
    """点电荷的辐射状场线：等角度（= 等立体角）取样，向外/向内。"""
    curves, heads = VGroup(), VGroup()
    for i in range(count):
        a = TAU * i / count + 0.06
        d = np.array([np.cos(a), np.sin(a), 0.0])
        r = r0
        end = r0
        while r < r_end:
            p = np.asarray(center, dtype=float) + d * r
            if not in_bounds(p, bounds):
                break
            end = r
            r += 0.02
        if end <= r0 + 0.15:
            continue
        if sign > 0:
            p0 = np.asarray(center, dtype=float) + d * r0
            p1 = np.asarray(center, dtype=float) + d * end
        else:
            p0 = np.asarray(center, dtype=float) + d * end
            p1 = np.asarray(center, dtype=float) + d * r0
        curves.add(Line(p0, p1, color=color, stroke_width=sw, stroke_opacity=0.92))
        length = float(np.linalg.norm(p1 - p0))
        for f in fractions:
            if sign > 0:
                pos = p0 + d * length * f
                heads.add(head(pos, d, color=color, size=0.135))
            else:
                pos = p1 + d * length * (1.0 - f)
                heads.add(head(pos, -d, color=color, size=0.135))
    return curves, heads


# ---------------------------------------------------------------- 场景
class ElectricFieldLinesScene(Scene):
    """电场线：定义、画法、三种典型分布、三条性质。"""

    def construct(self):
        self.cap = None
        self.tag = None
        self.cap_times = []
        self.tag_times = []

        self.header = VGroup(
            cn("电场线", 21, MUTED, BOLD),
            Line([0, 0, 0], [0, 0.26, 0], color=DIM, stroke_width=1.6),
            cn("电场强度的可视化", 19, DIM),
        ).arrange(RIGHT, buff=0.28).to_corner(UL, buff=0.30)

        self.beat_open()
        self.beat_define()
        self.beat_point_charge()
        self.beat_rules()
        self.beat_single()
        self.beat_dipole()
        self.beat_like()
        self.beat_properties()
        self.beat_summary()

    # ------------------------------------------------------------ 字幕 / 标签
    def caption_box(self, text, size=26):
        label = cn(text, size, "#f4f8fc")
        fit(label, max_w=11.5)
        bg = RoundedRectangle(
            width=label.width + 0.62, height=label.height + 0.30,
            corner_radius=0.12, fill_color="#05090e", fill_opacity=0.90,
            stroke_width=0,
        )
        return VGroup(bg, label).move_to([0, CAPTION_Y, 0])

    def say(self, text, hold=0.30, size=26):
        box = self.caption_box(text, size)
        if self.cap is not None:
            self.play(FadeOut(self.cap), run_time=0.12)
        self.play(FadeIn(box, shift=UP * 0.06), run_time=0.22)
        self.cap = box
        self.cap_times.append((text, self.renderer.time))
        print(f"CAPMARK {len(self.cap_times)} {self.renderer.time:.3f}", flush=True)
        self.wait(hold)

    def set_tag(self, text):
        new = cn(text, 24, KEY, BOLD).to_corner(UR, buff=0.30)
        if self.tag is None:
            self.tag = new
            self.play(FadeIn(new, shift=DOWN * 0.10), run_time=0.45)
        else:
            old = self.tag
            old_cap = self.cap
            self.cap = None
            fade_out = [FadeOut(old, shift=UP * 0.10)]
            if old_cap is not None:
                fade_out.append(FadeOut(old_cap))
            self.play(*fade_out, run_time=0.22)
            self.tag = new
            self.play(FadeIn(new, shift=DOWN * 0.10), run_time=0.26)
        self.tag_times.append((text, self.renderer.time))
        print(f"TAGMARK {len(self.tag_times)} {self.renderer.time:.3f}", flush=True)

    def clear_stage(self, *groups, run_time=0.5):
        self.play(*[FadeOut(g) for g in groups], run_time=run_time)

    # ------------------------------------------------------------ 00 开场
    def beat_open(self):
        t1 = cn("电场线", 68, INK, BOLD)
        t2 = cn("电场看不见，怎么描述它？", 34, KEY)
        rule = Line([-3.95, 0, 0], [3.95, 0, 0], color=LINE, stroke_width=2)
        route = cn("场的定义  ·  点电荷场强  ·  场线画法  ·  三种典型分布  ·  三条性质",
                   22, MUTED)
        src = cn("人教版 · 必修第三册  第九章 静电场", 20, DIM)
        block = VGroup(t1, t2, rule, route, src).arrange(DOWN, buff=0.34)
        block.move_to([0, 0.18, 0])
        fit(route, max_w=12.0)

        self.play(Write(t1), run_time=1.05)
        self.play(FadeIn(t2, shift=UP * 0.12), run_time=0.45)
        self.play(Create(rule), FadeIn(route, shift=UP * 0.08), run_time=0.55)
        self.play(FadeIn(src), run_time=0.45)
        self.wait(0.9)
        self.play(FadeOut(block, shift=UP * 0.25), run_time=0.75)
        self.play(FadeIn(self.header, shift=DOWN * 0.12), run_time=0.5)

    # ------------------------------------------------------------ 01 E = F/q
    def beat_define(self):
        self.set_tag("① 场强的定义")

        qc = np.array([-5.35, 0.25, 0.0])
        pc = np.array([-2.30, 1.55, 0.0])
        src = charge(1, qc, "Q", 0.30)
        probe = charge(1, pc, "q", 0.19, label_dir=DOWN)
        # 试探电荷换个颜色，和场源区分开（符号仍为正，正试探电荷）
        probe[0].set_fill(ELEC, 1.0)
        probe[1].set_color("#06121d")
        probe[2][1].set_color(ELEC)

        tie = dashed_tie(qc, pc)
        dvec = _unit(pc - qc)
        perp = np.array([-dvec[1], dvec[0], 0.0])
        r_lab = mth("r", 28, MUTED).move_to((qc + pc) / 2 + perp * 0.46)
        f_arrow = arrow(pc + dvec * 0.28, pc + dvec * 1.55, FORCE, 4.5, 0.30)
        f_lab = mth("F", 30, FORCE).move_to(pc + dvec * 1.55 + perp * 0.30 + dvec * 0.18)
        src_lab = cn("场源电荷", 19, POS).next_to(src[0], DOWN, buff=0.30)
        probe_lab = cn("试探电荷", 19, ELEC).move_to(pc + DOWN * 0.90)

        eq_main = mth(r"E=\frac{F}{q}", 54).move_to([4.30, 2.20, 0])
        n1 = cn("q 足够小，几乎不改变原来的场", 21, MUTED).move_to([4.30, 1.20, 0])
        n2 = cn("E 由场源电荷和位置决定", 23, INK).move_to([4.30, 0.66, 0])
        n3 = cn("与 q 的大小、正负都无关", 23, KEY, BOLD).move_to([4.30, 0.24, 0])
        n4 = mth(r"1\ \mathrm{N/C}=1\ \mathrm{V/m}", 26, DIM).move_to([4.30, -0.40, 0])
        n5 = cn("例：q = 1.0×10⁻⁶ C，受力 F = 1.0×10⁻⁴ N", 21,
                MUTED).move_to([4.30, -1.05, 0])
        n6 = mth(r"E=\frac{1.0\times10^{-4}}{1.0\times10^{-6}}=100\ \mathrm{N/C}",
                 28, WARN).move_to([4.30, -1.62, 0])
        fit(n6, max_w=5.4)
        n7 = cn("方向：正电荷在该点的受力方向", 21, FIELD).move_to([4.30, -2.35, 0])

        self.say("把一个电荷量很小的正试探电荷 q 放进电场，测出它受的力 F")
        self.play(FadeIn(src, scale=0.8), FadeIn(src_lab), run_time=0.55)
        self.play(Create(tie), FadeIn(r_lab), run_time=0.45)
        self.play(FadeIn(probe, scale=0.7), FadeIn(probe_lab), run_time=0.5)
        self.play(GrowArrow(f_arrow), FadeIn(f_lab), run_time=0.6)

        self.say("单位电荷受的力，就定义为该点的电场强度")
        self.play(FadeIn(eq_main, shift=LEFT * 0.12), run_time=0.6)
        self.play(Circumscribe(eq_main, color=KEY, run_time=0.75))

        self.say("E 由场源电荷决定，与试探电荷无关", 0.35)
        self.play(FadeIn(n1, shift=UP * 0.06), FadeIn(n2, shift=UP * 0.06),
                  FadeIn(n3, scale=0.94), run_time=0.55)

        self.say("代入一组数：1.0×10⁻⁴ N 除以 1.0×10⁻⁶ C，得 100 N/C", 0.4)
        self.play(FadeIn(n4), run_time=0.35)
        self.play(FadeIn(n5, shift=UP * 0.06), FadeIn(n6, shift=UP * 0.06), run_time=0.6)
        self.play(FadeIn(n7, shift=UP * 0.06), run_time=0.45)

        self.def_stage = VGroup(src, src_lab, probe, probe_lab, tie, r_lab,
                                f_arrow, f_lab)
        self.def_col = VGroup(eq_main, n1, n2, n3, n4, n5, n6, n7)
        self.clear_stage(self.def_stage, self.def_col, run_time=0.55)

    # ------------------------------------------------------------ 02 E = kQ/r²
    def beat_point_charge(self):
        self.set_tag("② 点电荷的场强")

        qc = np.array([-5.55, -0.15, 0.0])
        src = charge(1, qc, "Q", 0.30, label_dir=LEFT)
        d = np.array([np.cos(np.deg2rad(32)), np.sin(np.deg2rad(32)), 0.0])
        p1 = qc + d * 2.00
        p2 = qc + d * 4.00

        tie1 = dashed_tie(qc, p1)
        tie2 = dashed_tie(p1, p2)
        perp = np.array([-d[1], d[0], 0.0])
        r1 = mth("r", 28, MUTED).move_to((qc + p1) / 2 + perp * 0.42)
        r2 = mth("r", 28, MUTED).move_to((p1 + p2) / 2 + perp * 0.42)

        dot1 = Dot(p1, radius=0.055, color=INK)
        dot2 = Dot(p2, radius=0.055, color=INK)
        e1 = arrow(p1, p1 + d * 1.00, FIELD, 4.5, 0.28)
        e2 = arrow(p2, p2 + d * 0.42, FIELD, 4.5, 0.35)
        e1_lab = mth("E", 30, FIELD).move_to(p1 + d * 0.55 + perp * 0.34)
        e2_lab = mth(r"\frac{E}{4}", 26, FIELD).move_to(p2 + d * 0.16 - perp * 0.58)
        p_lab = cn("P₁", 19, MUTED).next_to(dot1, DOWN, buff=0.10)
        p2_lab = cn("P₂", 19, MUTED).next_to(dot2, DOWN, buff=0.10)

        eq_main = mth(r"E=k\frac{Q}{r^{2}}", 52).move_to([4.35, 2.10, 0])
        n_k = mth(r"k=9.0\times10^{9}\ \mathrm{N\cdot m^{2}/C^{2}}", 24,
                  MUTED).move_to([4.35, 1.32, 0])
        warn1 = cn("r 是场点到点电荷 Q 的距离", 24, WARN, BOLD).move_to([4.35, 0.68, 0])
        warn2 = cn("不是两个电荷之间的距离", 21, MUTED).move_to([4.35, 0.28, 0])
        n_q = cn("Q 是场源电荷：正 Q 向外，负 Q 向内", 21, INK).move_to([4.35, -0.32, 0])
        n_num0 = cn("取 Q = 1.0×10⁻⁹ C", 21, MUTED).move_to([4.35, -0.95, 0])
        n_num1 = mth(r"r=0.30\ \mathrm{m}\ \Rightarrow\ E=100\ \mathrm{N/C}",
                     26, INK).move_to([4.35, -1.45, 0])
        n_num2 = mth(r"r=0.60\ \mathrm{m}\ \Rightarrow\ E=25\ \mathrm{N/C}",
                     26, KEY).move_to([4.35, -1.95, 0])
        n_scale = cn("图中箭头长度按 1 : 1/4 画", 20, DIM).move_to([4.35, -2.55, 0])

        self.say("场源是一个点电荷 Q 时，把库仑定律代入定义式")
        self.play(FadeIn(src, scale=0.8), run_time=0.5)
        self.play(Create(tie1), FadeIn(r1), FadeIn(dot1), FadeIn(p_lab), run_time=0.5)
        self.play(GrowArrow(e1), FadeIn(e1_lab), run_time=0.55)
        self.play(FadeIn(eq_main, shift=LEFT * 0.12), run_time=0.6)
        self.play(Circumscribe(eq_main, color=KEY, run_time=0.75))

        self.say("r 是场点到点电荷的距离，不是两个电荷之间的距离", 0.45)
        self.play(Create(tie2), FadeIn(r2), FadeIn(dot2), FadeIn(p2_lab), run_time=0.5)
        self.play(GrowArrow(e2), FadeIn(e2_lab), run_time=0.55)
        self.play(FadeIn(warn1, scale=0.95), FadeIn(warn2, shift=UP * 0.05), run_time=0.6)

        self.say("距离加倍，场强只剩四分之一：E 与 r² 成反比", 0.35)
        self.play(FadeIn(n_k, shift=UP * 0.05), FadeIn(n_q, shift=UP * 0.05), run_time=0.5)
        self.play(FadeIn(n_num0), run_time=0.35)
        self.play(FadeIn(n_num1, shift=UP * 0.06), run_time=0.4)
        self.play(FadeIn(n_num2, shift=UP * 0.06), run_time=0.4)
        self.play(Circumscribe(n_num2, color=KEY, run_time=0.7))
        self.play(FadeIn(n_scale), run_time=0.35)

        self.qc_stage = VGroup(src, tie1, tie2, r1, r2, dot1, dot2, e1, e2,
                               e1_lab, e2_lab, p_lab, p2_lab)
        self.qc_col = VGroup(eq_main, n_k, warn1, warn2, n_q, n_num0,
                             n_num1, n_num2, n_scale)
        self.clear_stage(self.qc_stage, self.qc_col, run_time=0.55)

    # ------------------------------------------------------------ 03 场线画法
    def beat_rules(self):
        self.set_tag("③ 场线的画法")

        pos = np.array([-4.35, 0.20, 0.0])
        neg = np.array([-1.15, 0.20, 0.0])
        bounds = (-6.95, 0.35, -3.25, 3.25)
        charges = [(1.0, pos), (-1.0, neg)]
        r0 = CHARGE_R + 0.02
        angles = np.deg2rad([-72, -50, -28, -8, 12, 34, 56, 78])
        seeds = [pos + np.array([np.cos(a), np.sin(a), 0.0]) * r0 for a in angles]
        curves, heads = field_lines(seeds, charges, bounds,
                                    hit=[(neg, r0)], sw=2.3,
                                    fractions=(0.48,), size=0.16)

        c_pos = charge(1, pos, "+Q", 0.28, label_dir=UP)
        c_neg = charge(-1, neg, "-Q", 0.28, label_dir=UP)
        lab_out = plate(cn("从这里出发", 19, POS).move_to(pos + DOWN * 0.66))
        lab_in = plate(cn("到这里终止", 19, NEG).move_to(neg + DOWN * 0.66))

        dense = plate(cn("中间密 → 场强大", 19, FIELD).move_to([-2.75, -1.62, 0]))
        leader = Line([-2.75, -1.28, 0], [-2.75, -0.55, 0], color=FIELD,
                      stroke_width=1.4, stroke_opacity=0.55)

        title = cn("场线怎么画", 28, KEY, BOLD).move_to([4.35, 2.55, 0])
        rows = VGroup(
            VGroup(cn("①", 24, KEY, BOLD),
                   cn("从正电荷出发，到负电荷终止", 23, INK)).arrange(RIGHT, buff=0.16),
            VGroup(cn("②", 24, KEY, BOLD),
                   cn("疏密表示场强大小：密则强", 23, INK)).arrange(RIGHT, buff=0.16),
            VGroup(cn("③", 24, KEY, BOLD),
                   cn("切线方向就是该点的场强方向", 23, INK)).arrange(RIGHT, buff=0.16),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.34)
        rows.move_to([4.35, 1.35, 0])
        for r in rows:
            fit(r, max_w=5.1)
        rows.move_to([4.35, 1.35, 0])

        note = cn("场线是“画出来的场”，每一条都从正电荷的表面起笔", 20, MUTED)
        fit(note, max_w=4.9)
        note.move_to([4.35, -0.55, 0])
        note2 = cn("不会穿进电荷内部", 20, WARN).move_to([4.35, -1.05, 0])

        self.say("画场线有三条规矩：起点、疏密、切线")
        self.play(FadeIn(c_pos, scale=0.8), FadeIn(c_neg, scale=0.8), run_time=0.55)
        self.play(LaggedStart(*[Create(c) for c in curves], lag_ratio=0.05),
                  run_time=1.3)
        self.play(FadeIn(heads), run_time=0.35)
        self.play(FadeIn(lab_out, shift=UP * 0.06), FadeIn(lab_in, shift=UP * 0.06),
                  run_time=0.5)

        self.say("场线从正电荷表面出发，到负电荷表面终止", 0.5)
        self.play(FadeIn(title, shift=DOWN * 0.08), FadeIn(rows[0], shift=RIGHT * 0.10),
                  FadeIn(note, shift=UP * 0.06), run_time=0.55)

        self.say("哪里的场线密，哪里的场就强 —— 疏密就是场强的大小", 0.5)
        self.play(FadeIn(rows[1], shift=RIGHT * 0.10), Create(leader),
                  FadeIn(dense, shift=UP * 0.06), run_time=0.55)

        self.say("曲线上每一点的切线方向，就是那一点的场强方向", 0.7)
        self.play(FadeIn(rows[2], shift=RIGHT * 0.10), FadeIn(note2), run_time=0.5)

        self.rules_stage = VGroup(c_pos, c_neg, curves, heads, lab_out, lab_in,
                                  dense, leader, title, rows, note, note2)
        self.clear_stage(self.rules_stage, run_time=0.5)

    # ------------------------------------------------------------ 04 单个正电荷
    def beat_single(self):
        self.set_tag("④ 单个正点电荷")

        c = np.array([-3.80, -0.05, 0.0])
        bounds = (-6.95, 0.75, -3.30, 3.30)
        curves, heads = radial_rays(c, bounds, sign=1, count=22, r0=0.36,
                                    r_end=4.2, fractions=(0.38, 0.70))
        c_pos = charge(1, c, "+Q", 0.34, label_dir=UP)

        ring1 = DashedVMobject(Circle(radius=1.35, color=WARN, stroke_width=1.6,
                                      stroke_opacity=0.55).move_to(c),
                               num_dashes=44, dashed_ratio=0.55)
        ring2 = DashedVMobject(Circle(radius=2.70, color=WARN, stroke_width=1.6,
                                      stroke_opacity=0.45).move_to(c),
                               num_dashes=60, dashed_ratio=0.55)
        da = np.deg2rad(58)
        dirs = np.array([np.cos(da), np.sin(da), 0.0])
        lab_r = plate(mth("r", 26, WARN).move_to(c + dirs * 1.55),
                      pad_x=0.08, pad_y=0.02)
        lab_2r = plate(mth("2r", 26, WARN).move_to(c + dirs * 2.92),
                       pad_x=0.08, pad_y=0.02)

        eq_main = mth(r"E=k\frac{Q}{r^{2}}", 44)
        eq_prop = mth(r"\propto\ \frac{1}{r^{2}}", 44, KEY)
        eq_group = VGroup(eq_main, eq_prop).arrange(RIGHT, buff=0.26)
        eq_group.move_to([4.35, 2.32, 0])
        fit(eq_group, max_w=5.7)
        eq_main, eq_prop = eq_group[0], eq_group[1]
        n1 = cn("同一立体角内的场线条数不变", 22, INK).move_to([4.35, 1.42, 0])
        n2 = cn("球面面积 ∝ r²，故面密度 ∝ 1/r²", 22, INK).move_to([4.35, 0.94, 0])
        n3 = cn("r 加倍 → 场线密度只剩 1/4", 23, KEY, BOLD).move_to([4.35, 0.42, 0])
        n4 = mth(r"r=0.30\ \mathrm{m}:\ E=100\ \mathrm{N/C}", 24, MUTED
                 ).move_to([4.35, -0.22, 0])
        n5 = mth(r"r=0.60\ \mathrm{m}:\ E=25\ \mathrm{N/C}", 24, MUTED
                 ).move_to([4.35, -0.64, 0])

        base = Line([2.20, -1.78, 0], [6.60, -1.78, 0], color=DIM, stroke_width=1.2)
        a_e = arrow([2.35, -1.78, 0], [3.85, -1.78, 0], KEY, 5.0, 0.30)
        a_e4 = arrow([4.35, -1.78, 0], [4.725, -1.78, 0], FIELD, 5.0, 0.55)
        l_e = mth("E", 24, KEY).next_to(a_e, UP, buff=0.10)
        l_e4 = mth(r"\frac{E}{4}", 22, FIELD).next_to(a_e4, UP, buff=0.16)
        l_txt = cn("箭头长度按比例：1 : 1/4", 19, DIM).move_to([4.35, -2.30, 0])

        self.say("单个正点电荷：场线沿半径向外，均匀铺满整个空间", 0.3)
        self.play(FadeIn(c_pos, scale=0.8), run_time=0.45)
        self.play(LaggedStart(*[Create(l) for l in curves], lag_ratio=0.025),
                  run_time=1.5)
        self.play(FadeIn(heads), run_time=0.4)

        self.say("取角度均匀采样，就是等立体角 —— 每份立体角里的场线条数一样", 0.3)
        self.play(Create(ring1), run_time=0.45)
        self.play(FadeIn(lab_r), run_time=0.3)
        self.play(Create(ring2), run_time=0.45)
        self.play(FadeIn(lab_2r), run_time=0.3)

        self.say("同一份立体角，在 2r 处摊到的球面面积是 r 处的 4 倍", 0.3)
        self.play(FadeIn(eq_group, shift=LEFT * 0.12), run_time=0.6)
        self.play(Circumscribe(eq_group, color=KEY, run_time=0.8))
        self.play(FadeIn(n1, shift=UP * 0.06), FadeIn(n2, shift=UP * 0.06), run_time=0.55)
        self.play(FadeIn(n3, scale=0.94), run_time=0.45)

        self.say("所以场线密度按 1/r² 衰减：r 从 0.30 m 到 0.60 m，场强 100 → 25 N/C", 0.45)
        self.play(FadeIn(n4), FadeIn(base), FadeIn(n5), run_time=0.45)
        self.play(GrowArrow(a_e), FadeIn(l_e), run_time=0.5)
        self.play(GrowArrow(a_e4), FadeIn(l_e4), run_time=0.5)
        self.play(FadeIn(l_txt), run_time=0.4)

        self.single_stage = VGroup(c_pos, curves, heads, ring1, ring2, lab_r, lab_2r,
                                   eq_group, n1, n2, n3, n4, n5, base, a_e, a_e4,
                                   l_e, l_e4, l_txt)
        self.clear_stage(self.single_stage, run_time=0.5)

    # ------------------------------------------------------------ 05 等量异种
    def beat_dipole(self):
        self.set_tag("⑤ 等量异种电荷")

        pos = np.array([-4.95, 0.0, 0.0])
        neg = np.array([-1.55, 0.0, 0.0])
        mid = (pos + neg) / 2
        bounds = (-6.95, 0.40, -3.25, 3.25)
        charges = [(1.0, pos), (-1.0, neg)]
        r0 = CHARGE_R + 0.02
        angles = np.deg2rad([-100, -80, -60, -40, -20, 0, 20, 40, 60, 80, 100,
                             -140, 140, 180])
        seeds = [pos + np.array([np.cos(a), np.sin(a), 0.0]) * r0 for a in angles]
        curves, heads = field_lines(seeds, charges, bounds, hit=[(neg, r0)],
                                    sw=2.2, fractions=(0.50,), size=0.155)

        c_pos = charge(1, pos, "+Q", 0.28)
        c_neg = charge(-1, neg, "-Q", 0.28)
        mid_dot = Dot(mid, radius=0.065, color=INK)
        mid_lab = plate(cn("M", 22, INK, BOLD).next_to(mid_dot, DOWN, buff=0.10),
                        pad_x=0.07, pad_y=0.02)
        e_mid = arrow(mid + RIGHT * 0.10, mid + RIGHT * 1.15, KEY, 5.0, 0.26)
        e_mid_lab = plate(mth("E", 28, KEY).next_to(e_mid, UP, buff=0.10),
                          pad_x=0.07, pad_y=0.02)

        eq1 = mth(r"E_M=E_+ +E_-", 34).move_to([4.35, 2.30, 0])
        eq2 = mth(r"=2\cdot\frac{kQ}{(d/2)^{2}}=\frac{8kQ}{d^{2}}", 32
                  ).move_to([4.35, 1.68, 0])
        fit(eq2, max_w=4.9)
        note1 = cn("两个分场强同向 → 同向叠加", 22, KEY, BOLD).move_to([4.35, 1.02, 0])

        ins = panel_box(4.70, 2.10, [4.35, -0.30, 0])
        ins_t = cn("中点 M 的两个分场强", 18, MUTED).move_to([4.35, 0.56, 0])
        m0 = np.array([2.52, -0.30, 0.0])
        up_a = arrow([m0[0], 0.06, 0], [m0[0] + 0.95, 0.06, 0], POS, 5.0, 0.30)
        dn_a = arrow([m0[0], -0.46, 0], [m0[0] + 0.95, -0.46, 0], NEG, 5.0, 0.30)
        res_a = arrow([m0[0], -0.98, 0], [m0[0] + 1.90, -0.98, 0], KEY, 5.5, 0.20)
        conn = dashed_tie([m0[0], 0.26, 0], [m0[0], -0.80, 0])
        l_up = mth("E_+", 24, POS).move_to([m0[0] + 1.16, 0.06, 0])
        l_dn = mth("E_-", 24, NEG).move_to([m0[0] + 1.16, -0.46, 0])
        l_res = mth("E_M", 24, KEY).move_to([m0[0] + 2.14, -0.98, 0])
        l_m = cn("M", 20, INK, BOLD).move_to([m0[0] - 0.24, -0.30, 0])

        num0 = cn("Q=1.0×10⁻⁹ C，d=0.60 m", 21, MUTED).move_to([4.35, -1.78, 0])
        num1 = mth(r"E_M=100+100=200\ \mathrm{N/C}", 26, WARN
                   ).move_to([4.35, -2.28, 0])

        self.say("等量异种电荷：场线从正电荷出发，全部落到负电荷上")
        self.play(FadeIn(c_pos, scale=0.8), FadeIn(c_neg, scale=0.8), run_time=0.55)
        self.play(LaggedStart(*[Create(c) for c in curves], lag_ratio=0.055),
                  run_time=1.7)
        self.play(FadeIn(heads), run_time=0.45)

        self.say("看连线中点 M：两个分场强都指向负电荷，方向相同", 0.3)
        self.play(FadeIn(mid_dot, scale=0.7), FadeIn(mid_lab), run_time=0.4)
        self.play(GrowArrow(e_mid), FadeIn(e_mid_lab), run_time=0.6)

        self.say("同向叠加，中点场强最大", 0.2)
        self.play(FadeIn(eq1, shift=LEFT * 0.12), run_time=0.55)
        self.play(FadeIn(eq2, shift=LEFT * 0.12), run_time=0.55)
        self.play(FadeIn(note1, scale=0.95), run_time=0.45)

        self.play(FadeIn(ins), FadeIn(ins_t), run_time=0.45)
        self.play(GrowArrow(up_a), FadeIn(l_up), run_time=0.45)
        self.play(GrowArrow(dn_a), FadeIn(l_dn), Create(conn), FadeIn(l_m), run_time=0.45)
        self.play(GrowArrow(res_a), FadeIn(l_res), run_time=0.6)

        self.say("代数上：每个分场强 100 N/C，同向相加得 200 N/C", 0.7)
        self.play(FadeIn(num0), run_time=0.35)
        self.play(FadeIn(num1, shift=UP * 0.06), run_time=0.45)
        self.play(Circumscribe(num1, color=KEY, run_time=0.9))

        self.dip_stage = VGroup(c_pos, c_neg, curves, heads, mid_dot, mid_lab,
                                e_mid, e_mid_lab, eq1, eq2, note1, ins, ins_t,
                                up_a, dn_a, res_a, conn, l_up, l_dn, l_res, l_m,
                                num0, num1)
        self.clear_stage(self.dip_stage, run_time=0.5)

    # ------------------------------------------------------------ 06 等量同种
    def beat_like(self):
        self.set_tag("⑥ 等量同种电荷")

        left = np.array([-4.95, 0.0, 0.0])
        right = np.array([-1.55, 0.0, 0.0])
        mid = (left + right) / 2
        bounds = (-6.95, 0.40, -3.25, 3.25)
        charges = [(1.0, left), (1.0, right)]
        r0 = CHARGE_R + 0.02

        # 对称取样：避开连线（连线由下面的两个箭头单独画），其余成对出现
        base_angles = [20, 46, 72, 98, 124, 150, 180]
        seeds = []
        for a in base_angles:
            ang = np.deg2rad(a)
            seeds.append(left + np.array([np.cos(ang), np.sin(ang), 0.0]) * r0)
            mirrored = np.deg2rad(180 - a)
            seeds.append(right + np.array([np.cos(mirrored), np.sin(mirrored), 0.0]) * r0)
            if a not in (0, 180):
                ang2 = np.deg2rad(-a)
                seeds.append(left + np.array([np.cos(ang2), np.sin(ang2), 0.0]) * r0)
                m2 = np.deg2rad(180 + a)
                seeds.append(right + np.array([np.cos(m2), np.sin(m2), 0.0]) * r0)

        curves, heads = field_lines(seeds, charges, bounds, sw=2.1,
                                    fractions=(0.46,), size=0.15)

        c_l = charge(1, left, "+Q", 0.28)
        c_r = charge(1, right, "+Q", 0.28)

        # 连线上的两个分场强：从两侧同时顶向中点，箭头在 M 处相向
        axis_l = Arrow([mid[0] - 1.34, 0, 0], [mid[0] - 0.20, 0, 0], buff=0.0,
                       color=POS, stroke_width=5.0,
                       max_tip_length_to_length_ratio=0.30)
        axis_r = Arrow([mid[0] + 1.34, 0, 0], [mid[0] + 0.20, 0, 0], buff=0.0,
                       color=NEG, stroke_width=5.0,
                       max_tip_length_to_length_ratio=0.30)
        lab_ep = plate(mth("E_+", 24, POS).move_to([mid[0] - 0.86, 0.40, 0]),
                       pad_x=0.08, pad_y=0.02)
        lab_em = plate(mth("E_-", 24, NEG).move_to([mid[0] + 0.86, 0.40, 0]),
                       pad_x=0.08, pad_y=0.02)

        zero_ring = DashedVMobject(Circle(radius=0.22, color=KEY, stroke_width=2.0,
                                          stroke_opacity=0.9).move_to(mid),
                                   num_dashes=18, dashed_ratio=0.55)
        zero_lab = plate(mth("E=0", 30, KEY).move_to([mid[0], 1.02, 0]),
                         pad_x=0.10, pad_y=0.03)
        zero_leader = Line([mid[0], 0.78, 0], [mid[0], 0.30, 0], color=KEY,
                           stroke_width=1.6, stroke_opacity=0.8)
        mid_dot = Dot(mid, radius=0.05, color=INK)

        eq1 = mth(r"E_M=\frac{kQ}{(d/2)^{2}}-\frac{kQ}{(d/2)^{2}}=0", 30
                  ).move_to([4.35, 2.20, 0])
        fit(eq1, max_w=5.0)
        note1 = cn("两个分场强等大反向，矢量和为零", 22, KEY, BOLD
                   ).move_to([4.35, 1.45, 0])
        note2 = cn("中点场强为零 ≠ 那里没有场线", 21, MUTED).move_to([4.35, 0.98, 0])
        note3 = cn("两电荷之间的场线被挤开，互不相交", 21, MUTED).move_to([4.35, 0.60, 0])

        ins = panel_box(4.70, 2.05, [4.35, -0.72, 0])
        ins_t = cn("分场强等大反向", 18, MUTED).move_to([4.35, 0.16, 0])
        m0 = np.array([4.35, -0.72, 0.0])
        a_p = arrow(m0 + UP * 0.34, m0 + UP * 0.34 + RIGHT * 1.05, POS, 4.5, 0.30)
        a_n = arrow(m0 + DOWN * 0.34, m0 + DOWN * 0.34 + LEFT * 1.05, NEG, 4.5, 0.30)
        conn = Line(m0 + UP * 0.34, m0 + DOWN * 0.34, color=DIM, stroke_width=1.2,
                    stroke_opacity=0.7)
        ring0 = DashedVMobject(Circle(radius=0.24, color=KEY, stroke_width=1.8,
                                      stroke_opacity=0.85).move_to(m0),
                               num_dashes=20, dashed_ratio=0.55)
        z0 = cn("0", 26, KEY, BOLD).move_to(m0)
        l_p = mth("E_+", 22, POS).move_to(m0 + UP * 0.34 + RIGHT * 1.40)
        l_n = mth("E_-", 22, NEG).move_to(m0 + DOWN * 0.34 + LEFT * 1.40)
        l_zero = cn("合场强 0", 19, KEY).move_to([4.35, -1.60, 0])

        num = cn("每个分场强 100 N/C：100 - 100 = 0", 21, WARN
                 ).move_to([4.35, -2.20, 0])

        self.say("等量同种电荷：场线互相排开，中间留出一片稀疏区")
        self.play(FadeIn(c_l, scale=0.8), FadeIn(c_r, scale=0.8), run_time=0.5)
        self.play(LaggedStart(*[Create(c) for c in curves], lag_ratio=0.02),
                  run_time=1.6)
        self.play(FadeIn(heads), run_time=0.35)

        self.say("连线上，两条对称场线从两侧同时顶向中点", 0.2)
        self.play(GrowArrow(axis_l), GrowArrow(axis_r), run_time=0.9)
        self.play(FadeIn(lab_ep), FadeIn(lab_em), run_time=0.35)
        self.play(FadeIn(mid_dot), FadeIn(zero_ring), run_time=0.35)

        self.say("在 M 点，两个分场强等大反向，合场强为零", 0.2)
        self.play(FadeIn(zero_lab, scale=0.95), Create(zero_leader), run_time=0.45)
        self.play(FadeIn(eq1, shift=LEFT * 0.12), run_time=0.55)
        self.play(FadeIn(note1, scale=0.95), run_time=0.4)
        self.play(FadeIn(note2, shift=UP * 0.06), FadeIn(note3, shift=UP * 0.06),
                  run_time=0.45)

        self.play(FadeIn(ins), FadeIn(ins_t), run_time=0.4)
        self.play(GrowArrow(a_p), FadeIn(l_p), run_time=0.45)
        self.play(GrowArrow(a_n), FadeIn(l_n), Create(conn), run_time=0.45)
        self.play(FadeIn(ring0), FadeIn(z0), FadeIn(l_zero), run_time=0.5)

        self.say("数值上也对得上：100 N/C 与 100 N/C 反向，合起来就是 0", 0.9)
        self.play(FadeIn(num, shift=UP * 0.06), run_time=0.45)

        self.like_stage = VGroup(c_l, c_r, curves, heads, axis_l, axis_r,
                                 lab_ep, lab_em, zero_ring, zero_lab, zero_leader,
                                 mid_dot, eq1, note1, note2, note3, ins, ins_t,
                                 a_p, a_n, conn, ring0, z0, l_p, l_n, l_zero, num)
        self.clear_stage(self.like_stage, run_time=0.5)

    # ------------------------------------------------------------ 07 三条性质
    def beat_properties(self):
        self.set_tag("⑦ 三条性质")

        xs = [-4.78, 0.0, 4.78]
        pieces = [panel_box(4.15, 3.45, [x, -0.24, 0]) for x in xs]
        titles = VGroup(
            cn("不相交", 24, KEY, BOLD).move_to([xs[0], 1.74, 0]),
            cn("不闭合", 24, KEY, BOLD).move_to([xs[1], 1.74, 0]),
            cn("切线即 E 方向", 24, KEY, BOLD).move_to([xs[2], 1.74, 0]),
        )

        # —— 面板 1：两条场线相交（反例）
        cxa = VGroup(
            VMobject(color=FIELD, stroke_width=2.6).set_points_smoothly([
                np.array([xs[0] - 1.45, -0.92, 0]), np.array([xs[0] - 0.60, -0.12, 0]),
                np.array([xs[0], 0.0, 0]), np.array([xs[0] + 0.60, 0.12, 0]),
                np.array([xs[0] + 1.45, 0.92, 0])]),
            VMobject(color=FIELD, stroke_width=2.6).set_points_smoothly([
                np.array([xs[0] - 1.45, 0.92, 0]), np.array([xs[0] - 0.60, 0.12, 0]),
                np.array([xs[0], 0.0, 0]), np.array([xs[0] + 0.60, -0.12, 0]),
                np.array([xs[0] + 1.45, -0.92, 0])]),
        )
        cross = VGroup(
            Line([xs[0] - 0.22, -0.20, 0], [xs[0] + 0.22, 0.20, 0],
                 color=CANCEL, stroke_width=4.0),
            Line([xs[0] - 0.22, 0.20, 0], [xs[0] + 0.22, -0.20, 0],
                 color=CANCEL, stroke_width=4.0),
        )
        cross_lab = cn("同一点两个方向？", 19, CANCEL).move_to([xs[0], -1.55, 0])
        p1_note = cn("同一点只能有一个 E", 19, MUTED).move_to([xs[0], -1.12, 0])

        # —— 面板 2：闭合曲线（反例）
        loop = Ellipse(width=2.45, height=1.35, color=FIELD, stroke_width=2.6
                       ).move_to([xs[1], 0.05, 0])
        loop_h1 = head([xs[1] + 1.225, 0.05, 0], DOWN, color=FIELD, size=0.16)
        loop_h2 = head([xs[1] - 1.225, 0.05, 0], UP, color=FIELD, size=0.16)
        loop_x = VGroup(
            Line([xs[1] - 0.16, 0.56, 0], [xs[1] + 0.16, 0.88, 0],
                 color=CANCEL, stroke_width=4.0),
            Line([xs[1] - 0.16, 0.88, 0], [xs[1] + 0.16, 0.56, 0],
                 color=CANCEL, stroke_width=4.0),
        )
        p2_note = cn("静电场是保守场", 19, MUTED).move_to([xs[1], -1.12, 0])
        p2_note2 = cn("场线不能首尾相接", 19, CANCEL).move_to([xs[1], -1.55, 0])

        # —— 面板 3：切线方向
        curve3 = VMobject(color=FIELD, stroke_width=2.6).set_points_smoothly([
            np.array([xs[2] - 1.45, -0.55, 0]), np.array([xs[2] - 0.55, -0.12, 0]),
            np.array([xs[2] + 0.25, 0.22, 0]), np.array([xs[2] + 1.40, 0.52, 0])])
        ppos = np.array([xs[2] + 0.25, 0.22, 0.0])
        tangent = np.array([0.955, 0.196, 0.0])
        tline = DashedLine(ppos - tangent * 1.15, ppos + tangent * 1.15,
                           color=MUTED, stroke_width=1.6, dash_length=0.10)
        tarrow = arrow(ppos + tangent * 0.10, ppos + tangent * 1.10, KEY, 4.5, 0.26)
        pdot = Dot(ppos, radius=0.07, color=INK)
        plab = cn("P", 20, INK, BOLD).move_to(ppos + LEFT * 0.30 + DOWN * 0.28)
        elab = mth("E", 26, KEY).move_to(ppos + tangent * 1.05 + UP * 0.26)
        p3_note = cn("切线方向 = 场强方向", 19, MUTED).move_to([xs[2], -1.12, 0])
        p3_note2 = cn("也是正电荷受力方向", 19, MUTED).move_to([xs[2], -1.55, 0])

        self.say("第一条：场线不相交 —— 否则同一点就有两个场强方向")
        self.play(FadeIn(pieces[0]), FadeIn(titles[0]), run_time=0.45)
        self.play(Create(cxa[0]), Create(cxa[1]), run_time=0.85)
        self.play(FadeIn(cross, scale=0.8), FadeIn(cross_lab), run_time=0.5)
        self.play(FadeIn(p1_note), run_time=0.35)

        self.say("第二条：静电场场线不闭合，它起于正电荷、止于负电荷或伸向无穷远")
        self.play(FadeIn(pieces[1]), FadeIn(titles[1]), run_time=0.45)
        self.play(Create(loop), FadeIn(loop_h1), FadeIn(loop_h2), run_time=0.8)
        self.play(FadeIn(loop_x, scale=0.8), FadeIn(p2_note2), run_time=0.5)
        self.play(FadeIn(p2_note), run_time=0.35)

        self.say("第三条：场线上每一点的切线方向，就是那一点的场强方向")
        self.play(FadeIn(pieces[2]), FadeIn(titles[2]), run_time=0.45)
        self.play(Create(curve3), run_time=0.8)
        self.play(FadeIn(pdot, scale=0.7), FadeIn(plab), Create(tline), run_time=0.55)
        self.play(GrowArrow(tarrow), FadeIn(elab), run_time=0.55)
        self.play(FadeIn(p3_note), FadeIn(p3_note2), run_time=0.4)

        self.prop_stage = VGroup(*pieces, titles, cxa, cross, cross_lab, p1_note,
                                 loop, loop_h1, loop_h2, loop_x, p2_note, p2_note2,
                                 curve3, pdot, plab, tline, tarrow, elab,
                                 p3_note, p3_note2)
        self.clear_stage(self.prop_stage, run_time=0.5)

    # ------------------------------------------------------------ 08 收口
    def beat_summary(self):
        self.set_tag("⑧ 收口")

        def chip(color):
            return RoundedRectangle(width=0.09, height=0.40, corner_radius=0.04,
                                    fill_color=color, fill_opacity=1.0,
                                    stroke_width=0)

        def row(color, label, body):
            return VGroup(chip(color), cn(label, 24, MUTED), body).arrange(
                RIGHT, buff=0.30, aligned_edge=DOWN)

        r1 = row(KEY, "场强的定义",
                 VGroup(mth(r"E=\frac{F}{q}", 36),
                        cn("方向：正电荷受力方向", 21, DIM)).arrange(
                     RIGHT, buff=0.36, aligned_edge=DOWN))
        r2 = row(FIELD, "点电荷场强",
                 VGroup(mth(r"E=k\frac{Q}{r^{2}}", 36),
                        cn("r 是场点到点电荷的距离", 21, DIM)).arrange(
                     RIGHT, buff=0.36, aligned_edge=DOWN))
        r3 = row(ELEC, "场线的读法",
                 cn("从正到负 · 疏密表强弱 · 不相交不闭合 · 切线即场强", 23, INK))

        rows = VGroup(r1, r2, r3).arrange(DOWN, aligned_edge=LEFT, buff=0.52)
        rows.move_to([0, 0.90, 0])
        for r in rows:
            if r.width > 12.6:
                r.scale_to_fit_width(12.6)

        punch = cn("场线画的是空间各点的场方向，不是电荷的运动轨迹", 30, KEY, BOLD
                   ).move_to([0, -1.55, 0])
        fit(punch, max_w=12.6)
        tail = cn("下一节：用电势和等势面继续描述电场", 20, DIM).move_to([0, -2.35, 0])

        self.say("三句话收口：定义、点电荷、场线的读法")
        self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.18) for r in rows],
                              lag_ratio=0.30), run_time=1.15)
        self.say("E = F/q 是定义，E = kQ/r² 是点电荷的结果", 0.35)
        self.say("场线只是把每一点的场方向连起来，它本身不是轨迹", 0.4)
        self.play(Write(punch), run_time=0.9)
        self.play(FadeIn(tail, shift=UP * 0.06), run_time=0.5)
        self.say("记住：正电荷出发、负电荷终止，疏密看强弱，切线看方向", 2.0)

        self.play(FadeOut(VGroup(rows, punch, tail)), FadeOut(self.cap),
                  FadeOut(self.header), FadeOut(self.tag), run_time=0.9)
        self.cap = None
        self.tag = None


if __name__ == "__main__":
    # manim -qh electric_field_lines.py ElectricFieldLinesScene
    pass
