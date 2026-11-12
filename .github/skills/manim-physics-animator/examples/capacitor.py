"""平行板电容器课堂动画（人教版必修第三册 10.4 电容器的电容）。

渲染命令：
    manim -pql capacitor.py CapacitorScene    # 快速预览
    manim -pqh capacitor.py CapacitorScene    # 高清
"""

import numpy as np
from manim import *

config.frame_width = 14.222
config.frame_height = 8.0
config.pixel_width = 1280
config.pixel_height = 720
config.background_color = "#f7f8fb"
config.media_dir = r"build/videos/manim"

FONT = "Microsoft YaHei"
INK = "#172033"
MUTED = "#667085"
LINE = "#c9d2df"
PANEL = "#ffffff"
FIELD = "#0f766e"
VECTOR = "#d97706"
PATH_C = "#2f9e44"
POSITIVE = "#d92b2b"
NEGATIVE = "#3558ff"
ACCENT = "#7c3aed"
WIRE = "#94a3b8"

EPS0 = 8.8541878128e-12
S_CM2 = 300.0
U_VOLT = 300.0


def cn(text, font_size=30, color=INK, weight="NORMAL"):
    return Text(text, font=FONT, font_size=font_size, color=color, weight=weight)


def title(text, subtitle=None):
    top = cn(text, 34, INK, "BOLD").to_edge(UP, buff=0.28)
    bar = Line(LEFT * 6.45, RIGHT * 6.45, color=LINE, stroke_width=2).next_to(top, DOWN, buff=0.16)
    group = VGroup(top, bar)
    if subtitle:
        sub = cn(subtitle, 22, MUTED).next_to(bar, DOWN, buff=0.16)
        group.add(sub)
    return group


def arrow(start, end, color=VECTOR, width=3.2):
    return Arrow(start, end, buff=0, stroke_width=width, color=color,
                 max_tip_length_to_length_ratio=0.22)


def plates(gap, height, center, depth=0.2):
    """两块竖直极板：左正右负，内表面分别在中心两侧 gap/2 处。"""
    left = Rectangle(width=depth, height=height, stroke_color=POSITIVE,
                     stroke_width=3, fill_color=POSITIVE, fill_opacity=0.12)
    left.move_to(center + LEFT * (gap / 2 + depth / 2))
    right = Rectangle(width=depth, height=height, stroke_color=NEGATIVE,
                      stroke_width=3, fill_color=NEGATIVE, fill_opacity=0.12)
    right.move_to(center + RIGHT * (gap / 2 + depth / 2))
    return VGroup(left, right)


def battery(center, scale=1.0):
    long_bar = Line(LEFT * 0.13 + UP * 0.30, LEFT * 0.13 + DOWN * 0.30,
                    color=POSITIVE, stroke_width=7)
    short_bar = Line(RIGHT * 0.13 + UP * 0.16, RIGHT * 0.13 + DOWN * 0.16,
                     color=NEGATIVE, stroke_width=7)
    return VGroup(long_bar, short_bar).scale(scale).move_to(center)


def circuit(gap, height, center, y_batt, bx=None):
    """把两块极板接到下方电源（bx 为电源所在横坐标）。"""
    bx = center[0] if bx is None else bx
    lx = center[0] - gap / 2 - 0.1
    rx = center[0] + gap / 2 + 0.1
    bottom = center[1] - height / 2
    return VGroup(
        Line([lx, bottom, 0], [lx, y_batt, 0], color=WIRE, stroke_width=2.5),
        Line([rx, bottom, 0], [rx, y_batt, 0], color=WIRE, stroke_width=2.5),
        Line([lx, y_batt, 0], [bx - 0.13, y_batt, 0], color=WIRE, stroke_width=2.5),
        Line([bx + 0.13, y_batt, 0], [rx, y_batt, 0], color=WIRE, stroke_width=2.5),
    )


def field_arrows(center, gap, height, count, color=VECTOR, width=3.0, inset=0.12, span=0.78):
    """板间匀强电场：方向一律由正极板指向负极板。"""
    if count < 1:
        return VGroup()
    ys = np.linspace(-height * span / 2, height * span / 2, count) if count > 1 else [0.0]
    return VGroup(*[
        arrow([center[0] - gap / 2 + inset, center[1] + y, 0],
              [center[0] + gap / 2 - inset, center[1] + y, 0], color, width)
        for y in ys
    ])


def charges(center, gap, height, count, size=26, span=0.70):
    ys = np.linspace(-height * span / 2, height * span / 2, count) if count > 1 else [0.0]
    plus = VGroup(*[cn("+", size, POSITIVE, "BOLD").move_to([center[0] - gap / 2, center[1] + y, 0])
                    for y in ys])
    minus = VGroup(*[cn("−", size, NEGATIVE, "BOLD").move_to([center[0] + gap / 2, center[1] + y, 0])
                     for y in ys])
    return VGroup(plus, minus)


def capacity_farad(d_mm, er=1.0, s_cm2=S_CM2):
    """C = ε0·εr·S/d，返回法拉。"""
    return EPS0 * er * (s_cm2 * 1e-4) / (d_mm * 1e-3)


def state_u_const(d_mm, u_volt=U_VOLT):
    c = capacity_farad(d_mm)
    return {
        "C": c,
        "U": u_volt,
        "Q": c * u_volt,
        "E": u_volt / (d_mm * 1e-3),
        "W": 0.5 * c * u_volt ** 2,
    }


def state_q_const(d_mm, q_coulomb):
    """断开电源：Q 不变，U = Q/C，E = U/d = Q/(ε0 εr S)，与 d 无关。"""
    c = capacity_farad(d_mm)
    u = q_coulomb / c
    return {
        "C": c,
        "U": u,
        "Q": q_coulomb,
        "E": u / (d_mm * 1e-3),
        "W": 0.5 * q_coulomb * q_coulomb / c,
    }


Q_FROZEN = state_u_const(3.0)["Q"]


def arrow_count(e_v_per_m):
    """场线箭头的条数随场强增大而增多，只用于示意疏密。"""
    kv = e_v_per_m / 1e3
    return int(np.clip(round(2 + 4 * np.log10(max(kv, 1.0) / 20.0)), 3, 7))


class CapacitorScene(Scene):
    """平行板电容器：充电、电容的决定因素、两种电源状态、储能。"""

    def construct(self):
        self.charging()
        self.factors()
        self.modes()
        self.energy()
        self.summary()

    def _chip(self, text, color, font_size=20):
        label = cn(text, font_size, color, "BOLD")
        box = RoundedRectangle(width=label.width + 0.44, height=0.54, corner_radius=0.12,
                               stroke_color=color, stroke_width=1.6,
                               fill_color=color, fill_opacity=0.08)
        return VGroup(box, label)

    @staticmethod
    def _stop(*mobjects):
        """停止所有更新器，之后才能正常淡出。"""
        for mob in mobjects:
            mob.clear_updaters()

    # ---------------------------------------------------------------- 分镜 1
    def charging(self):
        header = title("电容器是怎样储电的？", "两极板带上等量异种电荷，板间出现匀强电场")
        self.play(FadeIn(header, shift=DOWN), run_time=0.7)

        gap, height = 3.2, 3.0
        center = np.array([0.0, 0.30, 0.0])
        y_batt = -2.45

        body = plates(gap, height, center)
        wires = circuit(gap, height, center, y_batt)
        batt = battery(np.array([0.0, y_batt, 0.0]))
        u_label = cn("U = 300 V", 20, MUTED).next_to(batt, DOWN, buff=0.22)
        plate_labels = VGroup(
            cn("正极板", 23, POSITIVE, "BOLD").move_to(
                [center[0] - gap / 2 - 0.1, center[1] + height / 2 + 0.34, 0]),
            cn("负极板", 23, NEGATIVE, "BOLD").move_to(
                [center[0] + gap / 2 + 0.1, center[1] + height / 2 + 0.34, 0]),
        )

        self.play(FadeIn(VGroup(body, plate_labels)), run_time=0.7)
        self.play(Create(wires), FadeIn(batt), FadeIn(u_label), run_time=0.9)

        charge_group = charges(center, gap, height, 6, size=28)
        pairs = VGroup(*[VGroup(charge_group[0][i], charge_group[1][i]) for i in range(6)])
        self.play(LaggedStart(*[FadeIn(p, shift=RIGHT * 0.1) for p in pairs], lag_ratio=0.18),
                  run_time=2.0)

        arrows = field_arrows(center, gap, height, 5)
        self.play(LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=0.16), run_time=1.6)

        left_note = VGroup(
            cn("板间为匀强电场", 22, FIELD, "BOLD"),
            cn("方向：正极板 → 负极板", 20, INK),
            MathTex(r"E=\frac{U}{d}", font_size=40, color=INK),
            cn("E = 100 kV/m", 20, MUTED),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.24).move_to([-5.15, 0.35, 0])

        right_note = VGroup(
            cn("充电完成后", 21, MUTED),
            cn("U = 300 V", 21, INK, "BOLD"),
            cn("Q = 26.6 nC", 21, POSITIVE, "BOLD"),
            cn("C = 88.5 pF", 21, NEGATIVE, "BOLD"),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.24).move_to([5.15, 0.35, 0])

        self.play(FadeIn(left_note, shift=LEFT), FadeIn(right_note, shift=RIGHT), run_time=1.0)
        self.wait(1.2)

        self.play(FadeOut(VGroup(header, body, wires, batt, u_label, plate_labels,
                                 charge_group, arrows, left_note, right_note)), run_time=0.8)

    # ---------------------------------------------------------------- 分镜 2
    def factors(self):
        header = title("电容 C 由什么决定？", "只由结构与介质决定，与 U、Q 无关")
        self.play(FadeIn(header, shift=DOWN), run_time=0.6)

        d_tr = ValueTracker(3.0)
        er_tr = ValueTracker(1.0)
        s_tr = ValueTracker(300.0)

        center = np.array([-3.45, 0.05, 0.0])

        def gap_of(d):
            return 0.85 + (d - 1.2) * 0.42

        def height_of(s):
            return 1.45 + (s - 300.0) / 300.0 * 0.85

        def build():
            g = gap_of(d_tr.get_value())
            h = height_of(s_tr.get_value())
            medium = Rectangle(width=g, height=h, stroke_width=0, fill_color="#38bdf8",
                               fill_opacity=0.04 + 0.20 * (er_tr.get_value() - 1.0) / 3.2)
            medium.move_to(center)
            body = plates(g, h, center, depth=0.16)
            arrows = field_arrows(center, g, h, 5, inset=0.10, width=2.8)
            top, y_dim = center[1] + h / 2, center[1] + h / 2 + 0.34
            dim = VGroup(
                DoubleArrow([center[0] - g / 2, y_dim, 0], [center[0] + g / 2, y_dim, 0],
                            buff=0, stroke_width=2.4, color=PATH_C, tip_length=0.12),
                Line([center[0] - g / 2, top, 0], [center[0] - g / 2, y_dim - 0.06, 0],
                     color=PATH_C, stroke_width=1.4),
                Line([center[0] + g / 2, top, 0], [center[0] + g / 2, y_dim - 0.06, 0],
                     color=PATH_C, stroke_width=1.4),
            )
            return VGroup(medium, body, arrows, dim)

        scene_group = always_redraw(build)

        panel = RoundedRectangle(width=5.3, height=4.5, corner_radius=0.16,
                                 stroke_color=LINE, stroke_width=2,
                                 fill_color=PANEL, fill_opacity=1).move_to([3.75, 0.05, 0])
        formula = MathTex(r"C=\varepsilon_0\varepsilon_r\frac{S}{d}", font_size=56, color=INK)
        formula.move_to([3.75, 1.62, 0])
        rule = Line([1.55, 0.98, 0], [5.95, 0.98, 0], color=LINE, stroke_width=1.5)

        s_num = DecimalNumber(300, num_decimal_places=0, font_size=26, color=INK)
        er_num = DecimalNumber(1.0, num_decimal_places=1, font_size=26, color=INK)
        d_num = DecimalNumber(3.0, num_decimal_places=1, font_size=26, color=INK)
        c_num = DecimalNumber(capacity_farad(3.0) * 1e12, num_decimal_places=1,
                              font_size=44, color=FIELD)

        rows = VGroup(
            VGroup(cn("S = ", 24, MUTED, "BOLD"), s_num, cn(" cm²", 24, MUTED)
                   ).arrange(RIGHT, buff=0.06, aligned_edge=DOWN),
            VGroup(cn("εr = ", 24, MUTED, "BOLD"), er_num
                   ).arrange(RIGHT, buff=0.06, aligned_edge=DOWN),
            VGroup(cn("d = ", 24, MUTED, "BOLD"), d_num, cn(" mm", 24, MUTED)
                   ).arrange(RIGHT, buff=0.06, aligned_edge=DOWN),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.16).move_to([2.55, 0.22, 0])
        rows.shift(RIGHT * (2.05 - rows.get_left()[0]))

        c_row = VGroup(cn("C = ", 30, INK, "BOLD"), c_num, cn(" pF", 30, MUTED)
                       ).arrange(RIGHT, buff=0.08, aligned_edge=DOWN)
        c_row.move_to([3.75, -0.85, 0])
        c_note = cn("只由 εr、S、d 决定", 20, MUTED).move_to([3.75, -1.45, 0])

        s_num.add_updater(lambda m: m.set_value(s_tr.get_value()))
        er_num.add_updater(lambda m: m.set_value(er_tr.get_value()))
        d_num.add_updater(lambda m: m.set_value(d_tr.get_value()))
        c_num.add_updater(lambda m: m.set_value(
            capacity_farad(d_tr.get_value(), er_tr.get_value(), s_tr.get_value()) * 1e12))

        self.play(FadeIn(VGroup(panel, formula, rule, c_note)), run_time=0.7)
        self.add(scene_group)
        self.play(FadeIn(rows), FadeIn(c_row), run_time=0.7)

        chip_d = self._chip("d 减小 → C 增大", PATH_C)
        chip_er = self._chip("εr 增大 → C 增大", ACCENT)
        chip_s = self._chip("S 增大 → C 增大", FIELD)
        chips = VGroup(chip_d, chip_er, chip_s).arrange(RIGHT, buff=0.28).move_to([-1.1, -3.3, 0])

        self.play(d_tr.animate.set_value(1.2), run_time=1.8)
        self.play(d_tr.animate.set_value(5.6), run_time=2.0)
        self.play(FadeIn(chip_d, shift=UP), run_time=0.5)

        self.play(d_tr.animate.set_value(2.4), run_time=1.0)
        self.play(er_tr.animate.set_value(4.2), run_time=1.6)
        self.play(FadeIn(chip_er, shift=UP), run_time=0.5)

        self.play(s_tr.animate.set_value(620), run_time=1.6)
        self.play(FadeIn(chip_s, shift=UP), run_time=0.5)
        self.wait(0.8)

        self._stop(scene_group, s_num, er_num, d_num, c_num)
        self.play(FadeOut(VGroup(header, panel, formula, rule, rows, c_row, c_note,
                                 scene_group, chips)), run_time=0.8)

    # ---------------------------------------------------------------- 分镜 3
    def modes(self):
        header = title("两种情形，结论完全不同", "接通电源 U 不变；断开电源 Q 不变")
        self.play(FadeIn(header, shift=DOWN), run_time=0.6)

        d_tr = ValueTracker(3.0)
        left_static, left_cap, left_nums = self._mode_panel("u", -3.55, d_tr)
        right_static, right_cap, right_nums = self._mode_panel("q", 3.55, d_tr)

        d_label = VGroup(
            cn("两图同步改变 d：", 20, MUTED),
            DecimalNumber(3.0, num_decimal_places=1, font_size=24, color=PATH_C),
            cn(" mm", 20, MUTED),
        ).arrange(RIGHT, buff=0.08, aligned_edge=DOWN).move_to([0.0, -3.5, 0])
        d_label[1].add_updater(lambda m: m.set_value(d_tr.get_value()))

        chip_l = self._chip("d 增大 → Q 减小、E 减小", FIELD).move_to([-3.55, -2.82, 0])
        chip_r = self._chip("d 增大 → U 增大、E 不变", ACCENT).move_to([3.55, -2.82, 0])

        self.add(left_cap, right_cap)
        self.play(FadeIn(VGroup(left_static, right_static)), FadeIn(d_label), run_time=0.9)

        self.play(d_tr.animate.set_value(6.0), run_time=2.4)
        self.wait(0.3)
        self.play(d_tr.animate.set_value(1.2), run_time=2.4)
        self.wait(0.3)

        self.play(FadeIn(chip_l, shift=UP), FadeIn(chip_r, shift=UP), run_time=0.7)
        self.wait(1.0)

        self._stop(left_cap, right_cap, d_label[1], *left_nums, *right_nums)
        self.play(FadeOut(VGroup(header, left_static, right_static, left_cap, right_cap,
                                 d_label, chip_l, chip_r)), run_time=0.8)

    def _mode_panel(self, kind, cx, d_tr):
        box = RoundedRectangle(width=6.3, height=5.1, corner_radius=0.16,
                               stroke_color=LINE, stroke_width=2,
                               fill_color=PANEL, fill_opacity=1).move_to([cx, -0.6, 0])

        if kind == "u":
            head = cn("接通电源：U 不变", 24, FIELD, "BOLD")
            sub = cn("Q 随 C 变化", 18, MUTED)
        else:
            head = cn("断开电源：Q 不变", 24, ACCENT, "BOLD")
            sub = cn("U 随 C 变化", 18, MUTED)
        head.move_to([cx, 1.6, 0])
        sub.next_to(head, DOWN, buff=0.10)

        cap_center = np.array([cx, 0.32, 0.0])
        cap_height = 1.45

        def build():
            g = 0.70 + (d_tr.get_value() - 1.0) * 0.30
            body = plates(g, cap_height, cap_center, depth=0.14)
            e = (state_u_const(d_tr.get_value())["E"] if kind == "u"
                 else state_q_const(d_tr.get_value(), Q_FROZEN)["E"])
            arrows = field_arrows(cap_center, g, cap_height, arrow_count(e), inset=0.08, width=2.6)
            return VGroup(body, arrows)

        cap_group = always_redraw(build)

        rows = VGroup()
        dynamic_numbers = []
        if kind == "u":
            q_num = DecimalNumber(26.6, num_decimal_places=1, font_size=26, color=POSITIVE)
            e_num = DecimalNumber(100, num_decimal_places=0, font_size=26, color=VECTOR)
            w_num = DecimalNumber(4.0, num_decimal_places=1, font_size=26, color=FIELD)
            q_num.add_updater(lambda m: m.set_value(state_u_const(d_tr.get_value())["Q"] * 1e9))
            e_num.add_updater(lambda m: m.set_value(state_u_const(d_tr.get_value())["E"] / 1e3))
            w_num.add_updater(lambda m: m.set_value(state_u_const(d_tr.get_value())["W"] * 1e6))
            dynamic_numbers = [q_num, e_num, w_num]
            rows.add(self._row("U = ", cn("300", 26, INK, "BOLD"), " V"))
            rows.add(self._row("Q = ", q_num, " nC"))
            rows.add(self._row("E = ", e_num, " kV/m"))
            rows.add(self._row("W = ", w_num, " μJ"))
        else:
            u_num = DecimalNumber(300, num_decimal_places=0, font_size=26, color=NEGATIVE)
            w_num = DecimalNumber(4.0, num_decimal_places=1, font_size=26, color=FIELD)
            u_num.add_updater(lambda m: m.set_value(state_q_const(d_tr.get_value(), Q_FROZEN)["U"]))
            w_num.add_updater(lambda m: m.set_value(state_q_const(d_tr.get_value(), Q_FROZEN)["W"] * 1e6))
            dynamic_numbers = [u_num, w_num]
            rows.add(self._row("U = ", u_num, " V"))
            rows.add(self._row("Q = ", cn("26.6", 26, POSITIVE, "BOLD"), " nC"))
            rows.add(self._row("E = ", cn("100", 26, VECTOR, "BOLD"), " kV/m"))
            rows.add(self._row("W = ", w_num, " μJ"))

        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.16)
        rows.move_to([cx, -1.55, 0])

        static = VGroup(box, head, sub, rows)
        return static, cap_group, dynamic_numbers

    def _row(self, label, num, unit):
        return VGroup(cn(label, 22, MUTED, "BOLD"), num, cn(unit, 20, MUTED)
                      ).arrange(RIGHT, buff=0.06, aligned_edge=DOWN)

    # ---------------------------------------------------------------- 分镜 4
    def energy(self):
        header = title("电容器储存了多少能量？", "W = ½CU² = ½QU：电压加倍，能量变为 4 倍")
        self.play(FadeIn(header, shift=DOWN), run_time=0.6)

        u_tr = ValueTracker(100.0)
        center = np.array([-4.2, 0.25, 0.0])
        gap, height, y_batt = 1.7, 2.4, -2.15

        def energy_joule():
            return 0.5 * capacity_farad(3.0) * u_tr.get_value() ** 2

        body = plates(gap, height, center)
        wires = circuit(gap, height, center, y_batt)
        batt = battery(np.array([center[0], y_batt, 0.0]))
        u_num = DecimalNumber(100, num_decimal_places=0, font_size=24, color=INK)
        u_num.add_updater(lambda m: m.set_value(u_tr.get_value()))
        u_label = VGroup(cn("U = ", 22, MUTED, "BOLD"), u_num, cn(" V", 22, MUTED)
                         ).arrange(RIGHT, buff=0.06, aligned_edge=DOWN)
        u_label.next_to(batt, DOWN, buff=0.26)

        fields = always_redraw(lambda: field_arrows(
            center, gap, height,
            arrow_count(state_u_const(3.0, u_tr.get_value())["E"]),
            inset=0.10, width=2.8))

        formula = MathTex(r"W=\frac{1}{2}CU^2=\frac{1}{2}QU", font_size=52, color=INK)
        formula.move_to([2.6, 2.05, 0])

        w_num = DecimalNumber(0.44, num_decimal_places=2, font_size=46, color=FIELD)
        w_num.add_updater(lambda m: m.set_value(energy_joule() * 1e6))
        w_row = VGroup(cn("W = ", 30, INK, "BOLD"), w_num, cn(" μJ", 28, MUTED)
                       ).arrange(RIGHT, buff=0.08, aligned_edge=DOWN)
        w_row.move_to([2.6, 1.0, 0])

        base_y = -1.95
        base = Line([1.8, base_y, 0], [3.6, base_y, 0], color=LINE, stroke_width=2.5)
        bar = always_redraw(lambda: Rectangle(
            width=0.7,
            height=max(0.02, 2.3 * energy_joule() / 1.59e-5),
            stroke_color=FIELD, stroke_width=2, fill_color=FIELD, fill_opacity=0.18,
        ).move_to([2.7, base_y + max(0.02, 2.3 * energy_joule() / 1.59e-5) / 2, 0]))
        bar_caption = cn("电场能 W", 18, MUTED).next_to(base, DOWN, buff=0.16)

        note = cn("U 增大到 3 倍，W 变为 9 倍；U 再增大到 2 倍，W 又变为 4 倍", 20, MUTED)
        note.move_to([2.6, -2.75, 0])

        self.play(FadeIn(VGroup(body, wires, batt, u_label)), run_time=0.9)
        self.add(fields)
        self.play(FadeIn(formula), FadeIn(w_row), Create(base), FadeIn(bar_caption), run_time=0.8)
        self.add(bar)

        self.play(u_tr.animate.set_value(300.0), run_time=2.0)
        self.wait(0.4)
        self.play(u_tr.animate.set_value(600.0), run_time=2.0)
        self.play(FadeIn(note, shift=UP), run_time=0.7)
        self.wait(1.2)

        self._stop(bar, fields, u_num, w_num)
        self.play(FadeOut(VGroup(header, body, wires, batt, u_label, fields, formula,
                                 w_row, base, bar, bar_caption, note)), run_time=0.8)

    # ---------------------------------------------------------------- 分镜 5
    def summary(self):
        header = cn("课堂归纳", 38, INK, "BOLD").to_edge(UP, buff=0.55)

        items = VGroup(
            cn("1  充电后两极板带等量异种电荷，板间出现匀强电场。", 24, INK),
            cn("2  电容只由结构、介质决定，与电压、电荷量无关。", 24, INK),
            cn("3  接通电源（U 不变）：改变 d 时，E 与 Q 都随之改变。", 24, FIELD, "BOLD"),
            cn("4  断开电源（Q 不变）：E 与 d 无关，U 与 d 成正比。", 24, ACCENT, "BOLD"),
            cn("5  储存的电场能与电压的平方成正比。", 24, INK),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.26).move_to([-0.55, 0.55, 0])

        formula_row = VGroup(
            MathTex(r"C=\varepsilon_0\varepsilon_r\frac{S}{d}", font_size=38, color=INK),
            MathTex(r"E=\frac{U}{d}", font_size=38, color=INK),
            MathTex(r"W=\frac{1}{2}CU^2=\frac{1}{2}QU", font_size=38, color=INK),
        ).arrange(RIGHT, buff=0.8).move_to([0.0, -1.95, 0])

        panel = RoundedRectangle(width=12.6, height=5.2, corner_radius=0.2,
                                 stroke_color=LINE, stroke_width=2,
                                 fill_color=PANEL, fill_opacity=1).move_to([0.0, 0.05, 0])

        self.play(FadeIn(header, shift=DOWN), FadeIn(panel), run_time=0.7)
        for item in items:
            self.play(FadeIn(item, shift=RIGHT), run_time=0.3)
        self.play(FadeIn(formula_row, shift=UP), run_time=0.8)
        self.wait(1.6)
        self.play(FadeOut(VGroup(header, panel, items, formula_row)), run_time=0.8)


if __name__ == "__main__":
    # manim -pql capacitor.py CapacitorScene
    pass
