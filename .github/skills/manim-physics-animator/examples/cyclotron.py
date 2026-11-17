# -*- coding: utf-8 -*-
"""回旋加速器 · 50 秒讲解动画（16:9 / 1280×720）

分镜表（先有什么、再有什么；3D 搭结构 → 2D 讲场与运动）：

  01 装置   3D      两个中空的半圆金属盒 + 中间一条缝，镜头缓慢环绕
  02 缝隙   3D      缝里加交变电压 → 交变电场（绿色 E 箭头 + 左下角 U-t 方波）
  03 磁场   3D      整个装置处在与盒面垂直的匀强磁场里（蓝色 B 箭头竖直立起）
  04 俯视   3D→2D   镜头转到正上方：B 箭头变成圆点，立体的盒子压成平面 D 形
  05 第一圈 2D      粒子垂直进入磁场，洛伦兹力指向圆心，走一个半圆：r = mv/(qB)
  06 加速   2D      回到缝口时电场反向，缝里直线加速，半径按 n 的平方根变大
  07 周期   2D      半圈时间不变，U-t 的每次翻转正好对上粒子回到缝口：T = 2πm/(qB)
  08 收口   2D      三条式子 + 一句话

渲染：
  manim -qm cyclotron.py CyclotronScene      # 1280×720
"""

from __future__ import annotations

import math
from pathlib import Path

import numpy as np
from manim import *

ROOT = Path(__file__).resolve().parents[4]
config.media_dir = str(ROOT / "build" / "videos" / "manim")
config.frame_width = 14.222
config.frame_height = 8.0
config.pixel_width = 1280
config.pixel_height = 720
config.background_color = "#0a0f15"

# ---------------------------------------------------------------- 视觉常量
FONT = "Microsoft YaHei"
MATH_FONT = "Cambria"

INK = "#e8eef7"
MUTED = "#8ea3bd"
GRID = "#39424e"
METAL = "#9aa4b0"
METAL_DARK = "#12161b"
PATH_C = "#ffd166"
ACCEL = "#f59e0b"
FIELD = "#34d399"
MAG = "#4f6bff"
HOT = "#f472b6"
POS = "#ef4444"

# ---------------------------------------------------------------- 尺寸与物理
Z = 0.58                                 # 盒面高度：粒子、场都画在这一层上
R_BOX = 2.6                              # D 形盒半径
GAP = 0.70                               # 缝宽
R1 = 0.82                                # 第一次过缝后的半圆半径
N_PASS = 6                               # 穿缝次数


def cn(text, size=30, color=INK, weight=NORMAL):
    return Text(text, font=FONT, font_size=size, color=color, weight=weight)


def mth(markup, size=44, color=INK):
    return MarkupText(markup, font=MATH_FONT, font_size=size, color=color)


def frac(num, den, size=40, color=INK, pad=0.22, buff=0.10):
    a, b = mth(num, size, color), mth(den, size, color)
    w = max(a.width, b.width) + pad
    bar = Line(LEFT * w / 2, RIGHT * w / 2, color=color, stroke_width=2.4)
    a.next_to(bar, UP, buff=buff)
    b.next_to(bar, DOWN, buff=buff)
    return VGroup(a, bar, b)


# ---------------------------------------------------------------- 轨迹：缝内直线 + 盒内半圆
def build_pieces(n_pass=N_PASS, gap=GAP, r1=R1):
    half = gap / 2
    pieces, phase, y, side = [], 0.0, 0.0, 1

    for k in range(n_pass):
        r_prev = 0.0 if k == 0 else r1 * math.sqrt(k)
        r_next = r1 * math.sqrt(k + 1)

        dur = 2 * gap / (r_prev + r_next)            # 匀加速穿过缝宽的用时
        pieces.append(dict(kind="gap", t0=phase, dur=dur, y=y,
                           x0=-half if side > 0 else half,
                           x1=half if side > 0 else -half,
                           side=side, r_prev=r_prev, r_next=r_next, n=k))
        phase += dur

        is_right = side > 0
        cy = y + r_next if is_right else y - r_next
        pieces.append(dict(kind="arc", t0=phase, dur=math.pi, r=r_next,
                           cx=half if is_right else -half, cy=cy,
                           base=-math.pi / 2 if is_right else math.pi / 2,
                           right=is_right, n=k + 1))
        phase += math.pi

        y += 2 * r_next if is_right else -2 * r_next
        side = -side

    ys = [p["y"] for p in pieces if p["kind"] == "gap"]
    ys += [p["cy"] + p["r"] for p in pieces if p["kind"] == "arc"]
    ys += [p["cy"] - p["r"] for p in pieces if p["kind"] == "arc"]
    mid = (min(ys) + max(ys)) / 2

    for p in pieces:
        if p["kind"] == "gap":
            p["y"] -= mid
        else:
            p["cy"] -= mid
    return pieces, phase


def piece_at(pieces, t):
    piece = pieces[-1]
    for q in pieces:
        if t < q["t0"] + q["dur"]:
            piece = q
            break
    return piece


def track_pos(pieces, t):
    piece = piece_at(pieces, t)
    s = t - piece["t0"]

    if piece["kind"] == "gap":
        a = (piece["r_next"] ** 2 - piece["r_prev"] ** 2) / (2 * GAP)
        d = min(max(piece["r_prev"] * s + 0.5 * a * s * s, 0.0), GAP)
        x = piece["x0"] + (1 if piece["x1"] > piece["x0"] else -1) * d
        return np.array([x, piece["y"], Z])

    u = min(max(s / piece["dur"], 0.0), 1.0)
    ang = piece["base"] + u * math.pi
    return np.array([piece["cx"] + piece["r"] * math.cos(ang),
                     piece["cy"] + piece["r"] * math.sin(ang), Z])


def field_points_right(pieces, t):
    piece = piece_at(pieces, t)
    if piece["kind"] == "gap":
        return piece["side"] > 0
    return not piece["right"]


def sqrt_of(inner):
    """把 inner 套进一个手绘根号（自带横线），比 Unicode "√" 规整。"""
    w, hh = inner.width, inner.height
    H = hh + 0.20
    surd = VMobject(color=inner.get_color(), stroke_width=2.4)
    surd.set_points_as_corners([
        np.array([0.00, 0.12, 0]),
        np.array([0.08, 0.00, 0]),
        np.array([0.19, H, 0]),
        np.array([0.24 + w + 0.10, H, 0]),
    ])
    inner.move_to([0.24 + w / 2 + 0.05, H - hh / 2 - 0.07, 0])
    return VGroup(surd, inner)


# ---------------------------------------------------------------- 3D 零件
def half_cylinder(radius, height, right=False, color=METAL, opacity=0.42):
    """半圆柱（D 形盒）：侧曲面 + 剖面 + 上下两个半圆盖。"""
    a0, a1 = (-PI / 2, PI / 2) if right else (PI / 2, 3 * PI / 2)
    curved = Surface(
        lambda u, v: np.array([radius * np.cos(u), radius * np.sin(u), v]),
        u_range=[a0, a1], v_range=[0, height], resolution=(26, 2),
        fill_color=color, fill_opacity=opacity, stroke_width=0, checkerboard_colors=False)
    chord = Surface(
        lambda u, v: np.array([0.0, u, v]),
        u_range=[-radius, radius], v_range=[0, height], resolution=(2, 2),
        fill_color="#232a33", fill_opacity=0.78, stroke_width=0, checkerboard_colors=False)

    def cap(z, opa):
        return Surface(
            lambda u, v: np.array([v * np.cos(u), v * np.sin(u), z]),
            u_range=[a0, a1], v_range=[0, radius], resolution=(26, 7),
            fill_color=color, fill_opacity=opa, stroke_width=0, checkerboard_colors=False)

    return VGroup(curved, chord, cap(height, min(opacity + 0.18, 1.0)), cap(0.0, opacity))


def make_device():
    half = GAP / 2
    return VGroup(
        half_cylinder(R_BOX, Z, right=False).shift([-half, 0, 0]),
        half_cylinder(R_BOX, Z, right=True).shift([half, 0, 0]),
        device_outline(False),
        device_outline(True),
    )


def device_outline(right, radius=R_BOX, half=GAP / 2):
    """盒子的黑色轮廓：半圆弧 + 直边（画在盒面上，3D 里也清晰）。"""
    a0 = -PI / 2 if right else PI / 2
    arc = Arc(radius=radius, start_angle=a0, angle=PI, color="#0b0f14", stroke_width=3)
    chord = Line(-UP * radius, UP * radius, color="#0b0f14", stroke_width=3)
    return VGroup(arc, chord).shift([half if right else -half, 0, Z + 0.004])


def floor_grid():
    plane = NumberPlane(
        x_range=[-9, 9], y_range=[-6, 6],
        background_line_style={"stroke_color": GRID, "stroke_width": 1, "stroke_opacity": 0.55},
        axis_config={"stroke_opacity": 0},
    )
    plane.set_z(0)
    return plane


def e_arrows_3d(to_right, ys=(-1.6, -0.55, 0.55, 1.6)):
    half = GAP / 2 - 0.05
    grp = VGroup()
    for y in ys:
        start = np.array([-half if to_right else half, y, Z + 0.02])
        end = np.array([half if to_right else -half, y, Z + 0.02])
        grp.add(Arrow3D(start, end, thickness=0.022, height=0.13, color=FIELD))
    return grp


def b_arrows_3d(h=1.05):
    grp = VGroup()
    for x in np.linspace(-2.15, 2.15, 7):
        for y in np.linspace(-2.05, 2.05, 5):
            if abs(x) < GAP / 2 + 0.3:
                continue
            if math.hypot(x, y) > R_BOX - 0.42:
                continue
            grp.add(Arrow3D(np.array([x, y, Z + 0.02]), np.array([x, y, Z + 0.02 + h]),
                            thickness=0.013, height=0.10, color=MAG, resolution=8))
    return grp


def b_dots():
    dots = VGroup()
    for x in np.linspace(-2.15, 2.15, 7):
        for y in np.linspace(-2.05, 2.05, 5):
            if abs(x) < GAP / 2 + 0.3:
                continue
            if math.hypot(x, y) > R_BOX - 0.42:
                continue
            dots.add(Dot([x, y, Z + 0.02], radius=0.062, color=MAG, fill_opacity=0.85))
    return dots


def ac_source(y=-2.15, z=0.06):
    """交变电源符号：黄圈 + 正弦波，两条红线接到两个 D 形盒（不是电流球）。"""
    ball = Circle(radius=0.28, color="#facc15", stroke_width=4).move_to([0, y, z])
    wave = VMobject(color="#facc15", stroke_width=3)
    wave.set_points_smoothly([np.array([x, y + 0.11 * np.sin(x * 26), z])
                              for x in np.linspace(-0.16, 0.16, 40)])
    leads = VGroup(
        Line([-0.36, y, z], [-0.22, y, z], color="#ef4444", stroke_width=4),
        Line([0.36, y, z], [0.22, y, z], color="#ef4444", stroke_width=4),
    )
    label = cn("交变电源", 17, "#facc15").move_to([0.95, y, z])
    return VGroup(ball, wave, leads, label)


# ---------------------------------------------------------------- 场景
class CyclotronScene(ThreeDScene):
    def construct(self):
        self.cap = None
        self.cues = []
        self.pieces, self.total = build_pieces()

        self.beat_device()
        self.beat_gap_field()
        self.beat_magnetic()
        self.beat_top_down()
        self.beat_first_orbit()
        self.beat_accelerate()
        self.beat_period()
        self.beat_summary()
        self.write_srt()

    # ------------------------------------------------------------ 画面文字
    def caption_box(self, text, size=31):
        label = cn(text, size, "#f4f8fc")
        bg = RoundedRectangle(width=label.width + 0.7, height=label.height + 0.32,
                              corner_radius=0.14, fill_color="#070c12", fill_opacity=0.86,
                              stroke_width=0)
        return VGroup(bg, label).move_to([0.0, -3.42, 0.0])

    def say(self, text, hold=0.4):
        box = self.caption_box(text)
        self.add_fixed_in_frame_mobjects(box)
        if self.cap is not None:
            self.play(FadeOut(self.cap), run_time=0.1)
            self.remove_fixed_in_frame_mobjects(self.cap)
            self.remove(self.cap)
        self.play(FadeIn(box, shift=UP * 0.08), run_time=0.18)
        self.cap = box
        self.cues.append((self.renderer.time, text))
        self.wait(hold)

    def set_step(self, title_text, kicker="回旋加速器 · 选必二"):
        new = VGroup(cn(kicker, 19, MUTED), cn(title_text, 38, INK, BOLD)) \
            .arrange(DOWN, aligned_edge=LEFT, buff=0.05).to_corner(UL, buff=0.5)
        self.add_fixed_in_frame_mobjects(new)
        if getattr(self, "step", None) is not None:
            self.play(FadeOut(self.step), run_time=0.1)
            self.remove_fixed_in_frame_mobjects(self.step)
            self.remove(self.step)
        self.play(FadeIn(new, shift=DOWN * 0.08), run_time=0.18)
        self.step = new

    # ------------------------------------------------------------ 01 装置（3D）
    def beat_device(self):
        self.set_camera_orientation(phi=62 * DEGREES, theta=-48 * DEGREES, zoom=1.22)

        grid = floor_grid()
        self.play(FadeIn(grid), run_time=0.6)

        dev = make_device()
        self.play(FadeIn(dev), run_time=0.7)
        self.begin_ambient_camera_rotation(rate=0.05)

        self.say("回旋加速器 = 两个中空的半圆金属盒", 0.6)
        self.say("中间留一条缝，粒子就在缝里被加速", 0.9)
        self.stop_ambient_camera_rotation()

        self.grid, self.device = grid, dev

    # ------------------------------------------------------------ 02 缝隙电场
    def beat_gap_field(self):
        e_arrows = e_arrows_3d(True)
        source = ac_source()
        self.play(FadeIn(e_arrows), FadeIn(source), run_time=0.8)
        self.say("缝里加交变电压，就得到交变电场", 0.4)

        ut, x_of = self.ut_panel()
        self.add_fixed_in_frame_mobjects(ut)
        self.play(FadeIn(ut, shift=UP * 0.12), run_time=0.6)
        self.say("电压每半个周期翻一次向", 0.5)

        flipped = e_arrows_3d(False)
        self.play(FadeOut(e_arrows), FadeIn(flipped), run_time=0.5)
        self.play(FadeOut(flipped), FadeIn(e_arrows), run_time=0.3)

        self.e_arrows, self.ut, self.x_of, self.source = e_arrows, ut, x_of, source
        self.wait(0.2)

    # ------------------------------------------------------------ 03 磁场
    def beat_magnetic(self):
        bs = b_arrows_3d()
        self.play(FadeIn(bs), run_time=1.2)
        self.say("整个装置处在与盒面垂直的匀强磁场中", 0.9)
        self.b_arrows = bs

    # ------------------------------------------------------------ 04 俯视（3D → 2D）
    def beat_top_down(self):
        self.say("从上往下看：盒里只有磁场，缝里只有电场", 0.2)

        dots = b_dots()
        # 硬切到俯视：参考视频也是 3D 一镜、2D 一镜的切法，比连续转相机稳且快
        self.play(FadeOut(self.b_arrows), FadeOut(self.device), FadeOut(self.grid),
                  run_time=0.5)
        self.set_camera_orientation(phi=0, theta=-90 * DEGREES, zoom=1.12)
        self.play(FadeIn(self.device), FadeIn(self.grid), FadeIn(dots), run_time=0.6)
        self.b_dots = dots
        self.wait(0.2)

        labels = VGroup(
            cn("D₁", 28, INK, BOLD).move_to([-1.95, 1.95, Z + 0.02]),
            cn("D₂", 28, INK, BOLD).move_to([1.95, 1.95, Z + 0.02]),
        )
        self.play(FadeIn(labels), run_time=0.4)
        self.labels = labels

    # ------------------------------------------------------------ 05 第一圈
    def beat_first_orbit(self):
        self.say("粒子从缝口静止出发，先被电场加速", 0.2)

        mover = Dot(track_pos(self.pieces, 0.0), radius=0.12, color=POS).set_stroke("#ffffff", 2)
        trail = TracedPath(mover.get_center, stroke_color=PATH_C, stroke_width=5)
        phase = ValueTracker(0.0)
        mover.add_updater(lambda m: m.move_to(track_pos(self.pieces, phase.get_value())))
        self.add(trail, mover)
        self.play(FadeIn(mover), run_time=0.2)

        gap0 = self.pieces[0]
        self.play(phase.animate.set_value(gap0["t0"] + gap0["dur"]),
                  run_time=0.8, rate_func=linear)

        self.say("垂直进入磁场后，洛伦兹力始终指向圆心", 0.3)
        f = VGroup(mth("<i>r</i> =", 44), frac("<i>mv</i>", "<i>qB</i>", 40)) \
            .arrange(RIGHT, buff=0.16).move_to([4.55, 1.25, 0.0])
        hint = VGroup(mth("<i>r</i> ∝", 30, MUTED), sqrt_of(mth("<i>n</i>", 30, MUTED))) \
            .arrange(RIGHT, buff=0.12).move_to([4.55, 0.32, 0.0])
        self.add_fixed_in_frame_mobjects(f, hint)
        self.play(FadeIn(f, shift=LEFT * 0.2), FadeIn(hint, shift=UP * 0.1), run_time=0.6)

        arc0 = self.pieces[1]
        self.play(phase.animate.set_value(arc0["t0"] + arc0["dur"]),
                  run_time=1.7, rate_func=linear)
        self.say("qvB = mv²/r → 半径只由速度决定", 0.7)

        self.mover, self.trail, self.phase, self.f_r, self.hint = mover, trail, phase, f, hint

    # ------------------------------------------------------------ 06 加速
    def beat_accelerate(self):
        self.say("回到缝口时电场刚好反向，再加速一次", 0.3)

        gaps = [q for q in self.pieces if q["kind"] == "gap"]
        marks = VGroup()
        marked = set()

        def live_marks(m):
            now = self.phase.get_value()
            for i, p in enumerate(gaps):
                if i in marked or now < p["t0"] + p["dur"] - 1e-9:
                    continue
                m.add(Line([p["x0"], p["y"], Z + 0.01], [p["x1"], p["y"], Z + 0.01],
                           color=ACCEL, stroke_width=6))
                marked.add(i)

        marks.add_updater(live_marks)
        self.add(marks)
        self.play(self.phase.animate.set_value(self.total),
                  run_time=(self.total - self.phase.get_value()) * 0.62 / math.pi,
                  rate_func=linear)
        marks.clear_updaters()
        self.say("每过一次缝，动能 +qU，半径按 n 的平方根变大", 0.7)
        self.marks = marks

    # ------------------------------------------------------------ 07 周期
    def beat_period(self):
        self.say("半径一次比一次大，但每半圈的时间没变", 0.4)

        f = VGroup(mth("<i>T</i> =", 44), frac("2π<i>m</i>", "<i>qB</i>", 40)) \
            .arrange(RIGHT, buff=0.16).move_to([4.55, -0.78, 0.0])
        self.add_fixed_in_frame_mobjects(f)
        self.play(FadeIn(f, shift=LEFT * 0.2), run_time=0.5)

        cursor = Line([0, 0, 0], [0, 0, 0], color=HOT, stroke_width=3)

        def move_cursor(m):
            x = self.x_of(self.phase.get_value() / math.pi)
            m.become(Line([x, -2.5, 0], [x, -1.4, 0], color=HOT, stroke_width=3))

        cursor.add_updater(move_cursor)
        self.add_fixed_in_frame_mobjects(cursor)
        self.add(cursor)
        self.say("所以电压的翻转，总能卡在粒子到缝口的时刻", 0.9)

        self.cursor, self.f_t = cursor, f

    # ------------------------------------------------------------ 08 收口
    def beat_summary(self):
        # 先把 3D 场景收掉，收口页只留字，读起来才干净
        self.play(FadeOut(VGroup(self.device, self.grid, self.b_dots, self.labels,
                                 self.e_arrows, self.source, self.marks, self.trail, self.mover,
                                 self.f_r, self.f_t, self.hint)), run_time=0.6)
        self.play(FadeOut(self.ut), run_time=0.3)
        self.remove_fixed_in_frame_mobjects(self.ut, self.f_r, self.f_t)
        self.cursor.clear_updaters()
        self.remove_fixed_in_frame_mobjects(self.cursor)
        self.remove(self.cursor)
        self.say("一句话：电场管加速，磁场管转弯", 0.3)

        def row(color, label, markup):
            chip = RoundedRectangle(width=0.09, height=0.4, corner_radius=0.04,
                                    fill_color=color, fill_opacity=1, stroke_width=0)
            return VGroup(chip, cn(label, 25, MUTED), mth(markup, 40, INK)) \
                .arrange(RIGHT, buff=0.26, aligned_edge=DOWN)

        rows = VGroup(
            row(ACCEL, "电场加速", "Δ<i>E</i><sub>k</sub> = <i>qU</i>"),
            row(MAG, "磁场偏转", "<i>r</i> = <i>mv</i>/(<i>qB</i>)"),
            row(FIELD, "周期固定", "<i>T</i> = 2π<i>m</i>/(<i>qB</i>)"),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).move_to(UP * 0.3)
        self.add_fixed_in_frame_mobjects(rows)

        punch = cn("电加速 · 磁偏转 · 一圈一圈越转越快", 33, INK, BOLD) \
            .next_to(rows, DOWN, buff=0.55)
        self.add_fixed_in_frame_mobjects(punch)

        self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.2) for r in rows], lag_ratio=0.25),
                  run_time=1.0)
        self.play(Write(punch), run_time=0.9)
        self.wait(2.0)

    # ------------------------------------------------------------ U-t 面板
    def ut_panel(self, periods=6, w=3.3, h=1.2, x0=-5.95, y0=-1.95):
        step = w / periods
        segs = VGroup()
        for k in range(periods):
            y = h / 2 if k % 2 == 0 else -h / 2
            segs.add(Line([x0 + k * step, y0 + y, 0], [x0 + (k + 1) * step, y0 + y, 0],
                          color=ACCEL, stroke_width=3.5))
            if k:
                prev = h / 2 if k % 2 else -h / 2
                segs.add(Line([x0 + k * step, y0 + prev, 0], [x0 + k * step, y0 + y, 0],
                              color=ACCEL, stroke_width=3.5))
        axis = VGroup(
            Line([x0 - 0.1, y0, 0], [x0 + w + 0.25, y0, 0], color=MUTED, stroke_width=2),
            Line([x0, y0 - h / 2 - 0.2, 0], [x0, y0 + h / 2 + 0.3, 0], color=MUTED, stroke_width=2),
        )
        lab = VGroup(
            mth("<i>U</i>", 26, MUTED).next_to(axis[1], UP, buff=0.06),
            mth("<i>t</i>", 26, MUTED).next_to(axis[0], RIGHT, buff=0.08),
            cn("交变电压", 18, MUTED).next_to(axis[1], UP, buff=0.45),
        )
        return VGroup(axis, segs, lab), (lambda k: x0 + k * step)

    # ------------------------------------------------------------ SRT
    def write_srt(self):
        def ts(sec):
            ms = int(round(sec * 1000))
            h, ms = divmod(ms, 3600_000)
            m, ms = divmod(ms, 60_000)
            s, ms = divmod(ms, 1000)
            return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"

        path = ROOT / "build" / "videos" / "manim" / "cyclotron.srt"
        path.parent.mkdir(parents=True, exist_ok=True)
        blocks = []
        for i, (t0, text) in enumerate(self.cues):
            t1 = self.cues[i + 1][0] if i + 1 < len(self.cues) else self.renderer.time
            blocks.append(f"{i + 1}\n{ts(t0)} --> {ts(t1)}\n{text}\n")
        path.write_text("\n".join(blocks), encoding="utf-8")
