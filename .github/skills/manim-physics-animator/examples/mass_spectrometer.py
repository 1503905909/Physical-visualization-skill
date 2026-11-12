import numpy as np
from manim import *


config.frame_width = 14.222
config.frame_height = 8.0
config.pixel_width = 1280
config.pixel_height = 720
config.background_color = "#f7f8fb"
config.media_dir = "build/videos/manim"


FONT = "Microsoft YaHei"
INK = "#172033"
MUTED = "#667085"
LINE = "#c9d2df"
PANEL = "#ffffff"
FIELD = "#0f766e"
TRACK = "#2f9e44"
TRACK2 = "#66a80f"
FORCE_E = "#f08c00"
FORCE_B = "#1971c2"
POSITIVE = "#e03131"
ACCENT = "#6741d9"
WARN = "#e8590c"


def cn(text, font_size=28, color=INK, weight="NORMAL"):
    return Text(text, font=FONT, font_size=font_size, color=color, weight=weight)


def title(text, subtitle=None):
    top = cn(text, 34, INK, "BOLD").to_edge(UP, buff=0.28)
    bar = Line(LEFT * 6.45, RIGHT * 6.45, color=LINE, stroke_width=2).next_to(top, DOWN, buff=0.16)
    group = VGroup(top, bar)
    if subtitle:
        sub = cn(subtitle, 21, MUTED).next_to(bar, DOWN, buff=0.14)
        group.add(sub)
    return group


def arrow(start, end, color=FORCE_B, width=4):
    return Arrow(start, end, buff=0, stroke_width=width, color=color, max_tip_length_to_length_ratio=0.28)


def field_dot(point, radius=0.055, color=MUTED):
    ring = Circle(radius=radius, color=color, stroke_width=1.2).move_to(point)
    dot = Dot(point, radius=radius * 0.30, color=color)
    return VGroup(ring, dot)


# ---------------------------------------------------------------------------
# 统一几何：底片在 BOUND_X，入射点高度 ENTRY_Y，半圆向下方偏转
# （正离子、B 垂直纸面向外：v × B 指向下方，所以圆心在入射点下方）
# ---------------------------------------------------------------------------
BOUND_X = -1.60
ENTRY_Y = 1.10
SRC_X = -5.95
SEL_X0, SEL_X1 = -4.95, -3.05
R_A = 1.85                      # 20Ne+：约 8.3 cm
R_B = R_A * 22.0 / 20.0         # 22Ne+：约 9.1 cm
CM_PER_UNIT = 4.5               # 底片刻度：1 单位 ≈ 4.5 cm


def ion_source():
    box = RoundedRectangle(
        width=0.95, height=0.66, corner_radius=0.12,
        stroke_color=LINE, stroke_width=2.5, fill_color=PANEL, fill_opacity=1,
    ).move_to([SRC_X, ENTRY_Y, 0])
    plus = cn("+", 26, POSITIVE, "BOLD").move_to(box.get_center())
    label = cn("离子源", 20, MUTED).next_to(box, DOWN, buff=0.12)
    return VGroup(box, plus, label)


def velocity_selector_zone():
    top = Line([SEL_X0, ENTRY_Y + 0.62, 0], [SEL_X1, ENTRY_Y + 0.62, 0], color="#9aa7b8", stroke_width=9)
    bottom = Line([SEL_X0, ENTRY_Y - 0.62, 0], [SEL_X1, ENTRY_Y - 0.62, 0], color="#9aa7b8", stroke_width=9)
    e_arrows = VGroup(*[
        arrow([x, ENTRY_Y - 0.40, 0], [x, ENTRY_Y + 0.40, 0], FORCE_E, 4)
        for x in [-4.62, -4.00, -3.38]
    ])
    marks = VGroup(
        field_dot([-4.80, ENTRY_Y + 0.26, 0], 0.045),
        field_dot([-3.22, ENTRY_Y + 0.26, 0], 0.045),
        field_dot([-3.22, ENTRY_Y - 0.26, 0], 0.045),
    )
    minus = cn("−", 26, "#1d4ed8", "BOLD").move_to([-4.00, ENTRY_Y + 0.92, 0])
    plus = cn("+", 26, POSITIVE, "BOLD").move_to([-4.00, ENTRY_Y - 0.92, 0])
    label = cn("① 速度选择器 E ⊥ B₁", 19, INK, "BOLD").move_to([-4.00, ENTRY_Y + 1.24, 0])
    return VGroup(top, bottom, e_arrows, marks, minus, plus, label)


def deflection_chamber(label_text="② 偏转磁场 B₂"):
    rect = Rectangle(width=2.15, height=5.15, stroke_color=LINE, stroke_width=1.6)
    rect.move_to([-0.525, -0.725, 0])
    dashed = DashedVMobject(rect, num_dashes=60)
    marks = VGroup()
    for x in np.linspace(-1.35, 0.30, 4):
        for y in np.linspace(-3.05, 1.55, 6):
            marks.add(field_dot([x, y, 0], 0.048))
    label = cn(label_text, 19, INK, "BOLD").move_to([-0.30, 2.05, 0])
    return VGroup(dashed, marks, label)


def photographic_plate(with_label=True):
    plate = Line([BOUND_X, 1.62, 0], [BOUND_X, -3.34, 0], color="#8d99ac", stroke_width=7)
    ticks = VGroup()
    labels = VGroup()
    for i in range(5):
        y = ENTRY_Y - i * (5.0 / CM_PER_UNIT)
        ticks.add(Line([BOUND_X - 0.13, y, 0], [BOUND_X, y, 0], color="#8d99ac", stroke_width=2))
        labels.add(cn(str(i * 5), 15, MUTED).move_to([BOUND_X - 0.30, y, 0]))
    unit = cn("x / cm", 15, MUTED).move_to([BOUND_X - 0.95, -3.62, 0])
    group = VGroup(plate, ticks, labels, unit)
    if with_label:
        group.add(cn("③ 照相底片", 18, INK, "BOLD").move_to([-1.86, 1.98, 0]))
    return group


def path_arc(radius, color=TRACK, width=4):
    return Arc(radius=radius, start_angle=PI / 2, angle=-PI, color=color, stroke_width=width).move_arc_center_to(
        [BOUND_X, ENTRY_Y - radius, 0]
    )


def ion_dot(color=POSITIVE, radius=0.13, sign="+"):
    body = Circle(radius=radius, fill_color=color, fill_opacity=1, stroke_color="#ffffff", stroke_width=2)
    mark = cn(sign, 16, "#ffffff", "BOLD").move_to(body.get_center())
    return VGroup(body, mark)


def landing_mark(radius, color=TRACK):
    y = ENTRY_Y - 2 * radius
    dot = Dot([BOUND_X, y, 0], radius=0.075, color=color)
    tick = Line([BOUND_X - 0.16, y, 0], [BOUND_X + 0.10, y, 0], color=color, stroke_width=3)
    return VGroup(dot, tick)


class MassSpectrometerScene(Scene):
    """质谱仪：速度选择 + 磁场偏转 + 底片记录。"""

    def construct(self):
        self.structure()
        self.velocity_selector()
        self.deflection()
        self.isotope_separation()
        self.summary()

    # ---------------------------------------------------------------- 分镜 1
    def structure(self):
        header = title("质谱仪", "选择速度 → 磁场偏转 → 底片记录，用落点比较质量")
        self.play(FadeIn(header, shift=DOWN), run_time=0.7)

        source = ion_source()
        selector = velocity_selector_zone()
        chamber = deflection_chamber()
        plate = photographic_plate()

        beam = Line([SRC_X + 0.48, ENTRY_Y, 0], [BOUND_X, ENTRY_Y, 0], color=TRACK, stroke_width=4)
        arc = path_arc(R_A)

        note = VGroup(
            cn("离子以同一速度 v = E/B₁", 22, INK),
            cn("垂直进入匀强磁场 B₂", 22, INK),
            cn("⊙ 表示 B₂ 垂直纸面向外", 20, MUTED),
            cn("质量不同 → 半径不同 → 落点不同", 22, FIELD, "BOLD"),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).move_to([3.90, -1.20, 0])

        self.play(FadeIn(source), run_time=0.5)
        self.play(FadeIn(selector), run_time=0.7)
        self.play(FadeIn(chamber), run_time=0.7)
        self.play(FadeIn(plate), run_time=0.6)
        self.play(Create(beam), Create(arc), run_time=1.8, rate_func=linear)
        self.play(FadeIn(note, shift=UP), run_time=0.7)
        self.wait(0.9)
        self.play(
            FadeOut(VGroup(header, source, selector, chamber, plate, beam, arc, note)),
            run_time=0.8,
        )

    # ---------------------------------------------------------------- 分镜 2
    def velocity_selector(self):
        header = title("为什么只有 v = E / B₁ 的离子能通过？", "电场力与洛伦兹力方向相反，大小相等时合力为零")
        self.play(FadeIn(header, shift=DOWN), run_time=0.6)

        top = Line([-5.20, 1.30, 0], [-0.20, 1.30, 0], color="#9aa7b8", stroke_width=9)
        bottom = Line([-5.20, -0.90, 0], [-0.20, -0.90, 0], color="#9aa7b8", stroke_width=9)
        e_arrows = VGroup(*[
            arrow([x, -0.70, 0], [x, 1.10, 0], FORCE_E, 4)
            for x in [-4.55, -3.65, -2.75, -1.85, -0.95]
        ])
        marks = VGroup(
            field_dot([-5.02, 0.20, 0], 0.05),
            field_dot([-3.10, 0.20, 0], 0.05),
            field_dot([-0.55, 0.20, 0], 0.05),
        )
        plate_labels = VGroup(
            cn("−", 32, "#1d4ed8", "BOLD").move_to([-4.55, 1.54, 0]),
            cn("+", 32, POSITIVE, "BOLD").move_to([-4.55, -1.14, 0]),
        )
        chamber_label = cn("速度选择器（E ⊥ B₁）", 20, INK, "BOLD").move_to([-2.70, 1.86, 0])

        p_slow = CubicBezier(
            [-5.55, 0.20, 0], [-4.75, 0.20, 0], [-3.85, 0.62, 0], [-3.35, 1.28, 0]
        )
        p_fast = CubicBezier(
            [-5.55, 0.20, 0], [-4.75, 0.20, 0], [-3.85, -0.22, 0], [-3.35, -0.88, 0]
        )
        p_ok = Line([-5.55, 0.20, 0], [0.35, 0.20, 0])

        dot_slow = ion_dot(radius=0.11).move_to(p_slow.get_start())
        dot_ok = ion_dot(radius=0.13).move_to(p_ok.get_start())
        dot_fast = ion_dot(radius=0.11).move_to(p_fast.get_start())

        formula = VGroup(
            MathTex(r"qE = qvB_1", font_size=46, color=INK),
            MathTex(r"v = \frac{E}{B_1}", font_size=58, color=FIELD),
        ).arrange(DOWN, buff=0.35).move_to([4.15, 0.70, 0])
        formula_note = cn("只有这一速度的离子", 21, MUTED).next_to(formula, DOWN, buff=0.30)
        formula_note2 = cn("合力为零，沿直线通过", 21, MUTED).next_to(formula_note, DOWN, buff=0.10)

        self.play(FadeIn(VGroup(top, bottom, chamber_label)), run_time=0.7)
        self.play(LaggedStart(*[Create(a) for a in e_arrows], lag_ratio=0.10), FadeIn(marks), run_time=0.7)
        self.play(FadeIn(plate_labels), run_time=0.5)

        # 受力分析：两个力等大反向
        f_e = arrow([-2.30, 0.20, 0], [-2.30, 1.00, 0], FORCE_E, 5)
        f_b = arrow([-2.30, 0.20, 0], [-2.30, -0.60, 0], FORCE_B, 5)
        f_e_label = cn("qE：电场力（向上）", 18, FORCE_E).move_to([-2.30, 1.17, 0])
        f_b_label = cn("qvB₁：洛伦兹力（向下）", 18, FORCE_B).move_to([-2.30, -0.77, 0])
        balance = cn("等大反向 → 合力为零", 21, FIELD, "BOLD").move_to([-2.30, 1.56, 0])

        self.play(FadeIn(dot_ok), run_time=0.3)
        self.play(GrowArrow(f_e), GrowArrow(f_b), run_time=0.9)
        self.play(FadeIn(f_e_label), FadeIn(f_b_label), run_time=0.5)
        self.play(Write(formula[0]), run_time=0.8)
        self.play(FadeIn(formula[1], shift=LEFT), FadeIn(balance), run_time=0.8)
        self.play(FadeIn(formula_note), FadeIn(formula_note2), run_time=0.5)
        self.wait(0.6)

        # 三种速度的离子：偏小、正好、偏大
        self.play(FadeOut(VGroup(f_e, f_b, f_e_label, f_b_label, balance)), run_time=0.5)
        slow_label = cn("v 偏小：打在上板", 19, WARN).move_to([-3.10, 1.48, 0])
        ok_label = cn("v = E/B₁ 的离子通过", 19, FIELD, "BOLD").move_to([0.85, 0.62, 0])
        fast_label = cn("v 偏大：打在下板", 19, WARN).move_to([-3.10, -1.10, 0])

        self.play(
            MoveAlongPath(dot_slow, p_slow),
            MoveAlongPath(dot_ok, p_ok),
            MoveAlongPath(dot_fast, p_fast),
            run_time=2.6,
            rate_func=linear,
        )
        self.play(FadeIn(slow_label), FadeIn(fast_label), FadeIn(ok_label), run_time=0.6)
        self.wait(1.0)

        self.play(
            FadeOut(VGroup(
                header, top, bottom, e_arrows, marks, plate_labels, chamber_label,
                dot_slow, dot_ok, dot_fast,
                formula, formula_note, formula_note2, slow_label, fast_label, ok_label,
            )),
            run_time=0.8,
        )

    # ---------------------------------------------------------------- 分镜 3
    def deflection(self):
        header = title("进入 B₂：半个圆周，半径 r = mv / (qB₂)", "洛伦兹力提供向心力，速度大小不变")
        self.play(FadeIn(header, shift=DOWN), run_time=0.6)

        chamber = deflection_chamber()
        plate = photographic_plate(with_label=False)
        beam = Line([-3.20, ENTRY_Y, 0], [BOUND_X, ENTRY_Y, 0], color=TRACK, stroke_width=4)
        arc = path_arc(R_A)
        dot = ion_dot(radius=0.13)

        center_dot = Dot([BOUND_X, ENTRY_Y - R_A, 0], radius=0.06, color=MUTED)
        radius_line = DashedLine(
            [BOUND_X, ENTRY_Y - R_A, 0], [BOUND_X + R_A, ENTRY_Y - R_A, 0],
            color=FORCE_E, stroke_width=2.4, dash_length=0.10,
        )
        r_label = cn("r", 24, FORCE_E, "BOLD").move_to([BOUND_X + R_A * 0.55, ENTRY_Y - R_A + 0.22, 0])
        mark = landing_mark(R_A)
        chord = DoubleArrow(
            [BOUND_X + 0.16, ENTRY_Y, 0], [BOUND_X + 0.16, ENTRY_Y - 2 * R_A, 0],
            buff=0, color=ACCENT, stroke_width=3, tip_length=0.14,
        )
        chord_label = cn("x = 2r", 21, ACCENT, "BOLD").move_to([BOUND_X + 0.62, ENTRY_Y - 0.42, 0])

        formula = VGroup(
            MathTex(r"qvB_2 = \frac{mv^2}{r}", font_size=42, color=INK),
            MathTex(r"r = \frac{mv}{qB_2}", font_size=46, color=FIELD),
            MathTex(r"x = 2r", font_size=44, color=ACCENT),
        ).arrange(DOWN, buff=0.34).move_to([4.20, 0.55, 0])

        self.play(FadeIn(VGroup(chamber, plate, beam)), run_time=0.8)
        dot.move_to(arc.get_start())
        self.play(FadeIn(dot), run_time=0.3)
        self.play(Create(arc), MoveAlongPath(dot, arc), run_time=2.6, rate_func=linear)
        self.play(FadeIn(center_dot), Create(radius_line), FadeIn(r_label), run_time=0.8)
        self.play(FadeIn(mark), Create(chord), FadeIn(chord_label), run_time=0.8)
        self.play(Write(formula[0]), run_time=0.8)
        self.play(FadeIn(formula[1], shift=LEFT), run_time=0.6)
        self.play(FadeIn(formula[2], shift=LEFT), run_time=0.5)
        self.wait(0.8)
        self.play(
            FadeOut(VGroup(formula, center_dot, radius_line, r_label, mark, chord, chord_label, arc, dot)),
            run_time=0.6,
        )

        # 用 ValueTracker 连续改变 B₂，看半径与落点怎样变化
        k_radius = R_A * 0.5
        bt = ValueTracker(0.5)

        def live_deflection():
            radius = k_radius / bt.get_value()
            live_arc = path_arc(radius)
            live_center = Dot([BOUND_X, ENTRY_Y - radius, 0], radius=0.05, color=MUTED)
            live_radius = Line(
                [BOUND_X, ENTRY_Y - radius, 0], [BOUND_X + radius, ENTRY_Y - radius, 0],
                color=FORCE_E, stroke_width=2,
            )
            live_mark = landing_mark(radius)
            return VGroup(live_arc, live_center, live_radius, live_mark)

        live = always_redraw(live_deflection)

        def readout_for(b_value):
            r_cm = k_radius / b_value * CM_PER_UNIT
            return cn("B₂ = %.2f T      r = %.1f cm" % (b_value, r_cm), 26, INK).move_to([3.95, 0.55, 0])

        readout = readout_for(0.50)
        hint = cn("B₂ 增大 → r 减小 → 落点靠近入射点", 20, MUTED).move_to([3.95, 0.02, 0])
        v_note = cn("v = 2.0×10⁵ m/s（进入 B₂ 后大小不变）", 19, MUTED).move_to([3.95, -0.52, 0])

        self.add(live)
        self.play(FadeIn(readout), FadeIn(hint), FadeIn(v_note), run_time=0.6)
        for b_value in [0.60, 0.75, 0.90]:
            self.play(
                Transform(readout, readout_for(b_value)),
                bt.animate.set_value(b_value),
                run_time=0.95,
                rate_func=smooth,
            )
        self.wait(0.8)
        live.clear_updaters()
        self.play(
            FadeOut(VGroup(header, chamber, plate, beam, live, readout, hint, v_note)),
            run_time=0.8,
        )

    # ---------------------------------------------------------------- 分镜 4
    def isotope_separation(self):
        header = title("质量不同 → 落点不同：把同位素分开", "速度相同、电荷相同，半径只由质量决定")
        self.play(FadeIn(header, shift=DOWN), run_time=0.6)

        chamber = deflection_chamber()
        plate = photographic_plate(with_label=False)
        beam = Line([-3.20, ENTRY_Y, 0], [BOUND_X, ENTRY_Y, 0], color=TRACK, stroke_width=4)

        arc_a = path_arc(R_A, TRACK, 4)
        arc_b = path_arc(R_B, TRACK2, 3)
        dot_a = ion_dot(radius=0.13)
        dot_b = ion_dot(radius=0.115)

        mark_a = landing_mark(R_A, TRACK)
        mark_b = landing_mark(R_B, TRACK2)
        label_a = cn("²⁰Ne⁺  x₁", 20, TRACK, "BOLD").move_to([BOUND_X + 1.05, ENTRY_Y - 2 * R_A - 0.30, 0])
        label_b = cn("²²Ne⁺  x₂", 20, TRACK2, "BOLD").move_to([BOUND_X + 1.05, ENTRY_Y - 2 * R_B - 0.30, 0])

        brace = Brace(
            Line([BOUND_X, ENTRY_Y - 2 * R_A, 0], [BOUND_X, ENTRY_Y - 2 * R_B, 0]),
            direction=LEFT, buff=0.05, color=ACCENT,
        )
        brace_label = cn("Δx", 21, ACCENT, "BOLD").next_to(brace, LEFT, buff=0.10)

        mass_formula = VGroup(
            MathTex(r"m = \frac{q B_1 B_2 x}{2E}", font_size=44, color=FIELD),
            cn("由落点反推质量", 21, MUTED),
        ).arrange(DOWN, buff=0.20).move_to([4.35, 0.60, 0])
        apps = VGroup(
            cn("应用：同位素分析", 21, INK),
            cn("有机物分子量测定", 21, INK),
            cn("¹⁴C 考古测年", 21, INK),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.16).next_to(mass_formula, DOWN, buff=0.55)

        self.play(FadeIn(VGroup(chamber, plate, beam)), run_time=0.7)
        dot_a.move_to(arc_a.get_start())
        dot_b.move_to(arc_b.get_start())
        self.play(FadeIn(VGroup(dot_a, dot_b)), run_time=0.3)
        self.play(
            Create(arc_a), Create(arc_b),
            MoveAlongPath(dot_a, arc_a, run_time=2.4, rate_func=linear),
            MoveAlongPath(dot_b, arc_b, run_time=2.4 * R_B / R_A, rate_func=linear),
        )
        self.play(FadeIn(VGroup(mark_a, mark_b, label_a, label_b)), run_time=0.7)
        self.play(GrowFromCenter(brace), FadeIn(brace_label), run_time=0.7)
        self.play(Write(mass_formula[0]), run_time=0.9)
        self.play(FadeIn(mass_formula[1]), run_time=0.4)
        self.play(LaggedStart(*[FadeIn(a, shift=LEFT) for a in apps], lag_ratio=0.25), run_time=1.0)
        self.wait(1.2)

        self.play(
            FadeOut(VGroup(
                header, chamber, plate, beam, arc_a, arc_b, dot_a, dot_b,
                mark_a, mark_b, label_a, label_b, brace, brace_label,
                mass_formula, apps,
            )),
            run_time=0.8,
        )

    # ---------------------------------------------------------------- 分镜 5
    def summary(self):
        header = cn("课堂归纳", 38, INK, "BOLD").to_edge(UP, buff=0.72)
        items = VGroup(
            cn("1  速度选择器：电场力与洛伦兹力等大反向，只放行 v = E/B₁。", 26, INK),
            cn("2  偏转磁场：洛伦兹力提供向心力，离子做半圆运动。", 26, INK),
            cn("3  半径 r = mv/(qB₂)，落点 x = 2r，质量越大落点越远。", 26, FIELD, "BOLD"),
            cn("4  由 x 反推质量 m = qB₁B₂x/(2E)，这是质谱仪测质量的依据。", 26, INK),
            cn("简化假设：忽略重力、非相对论、忽略边缘场。", 22, WARN),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.30).move_to([0, 0.05, 0])
        panel = RoundedRectangle(
            width=12.1, height=4.15, corner_radius=0.22,
            stroke_color=LINE, stroke_width=2, fill_color=PANEL, fill_opacity=1,
        ).move_to(items)
        self.play(FadeIn(header, shift=DOWN), FadeIn(panel), run_time=0.7)
        for item in items:
            self.play(FadeIn(item, shift=RIGHT), run_time=0.35)
        self.wait(1.2)
        self.play(FadeOut(VGroup(header, panel, items)), run_time=0.8)


if __name__ == "__main__":
    # 快速预览：manim -pql mass_spectrometer.py MassSpectrometerScene
    # 高清渲染：manim -pqh mass_spectrometer.py MassSpectrometerScene
    pass
