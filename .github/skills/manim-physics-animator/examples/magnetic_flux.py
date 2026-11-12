import math

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
COIL = "#0f766e"
FIELD = "#3b6ea5"
NORMAL = "#1f2937"
WARN = "#c2410c"
LAMP = "#f59f00"
ACCENT = "#6d28d9"

DEG = math.pi / 180.0
B0 = 0.15                     # 磁感应强度，单位 T
S0 = 1.5e-2                   # 线圈面积，单位 m^2
PHI_MAX = B0 * S0 * 1000.0    # 最大磁通量，单位 mWb


# ---------- 基础绘图工具 ----------

def cn(text, size=30, color=INK, weight="NORMAL"):
    return Text(text, font=FONT, font_size=size, color=color, weight=weight)


def title(text, subtitle=None):
    top = cn(text, 34, INK, "BOLD").to_edge(UP, buff=0.28)
    bar = Line(LEFT * 6.45, RIGHT * 6.45, color=LINE, stroke_width=2).next_to(top, DOWN, buff=0.16)
    group = VGroup(top, bar)
    if subtitle:
        sub = cn(subtitle, 22, MUTED).next_to(bar, DOWN, buff=0.16)
        group.add(sub)
    return group


def cross_mark(center, size=0.07, color=FIELD, width=2.2):
    a = np.array([center[0], center[1], 0.0])
    return VGroup(
        Line(a + np.array([-size, -size, 0]), a + np.array([size, size, 0]), color=color, stroke_width=width),
        Line(a + np.array([size, -size, 0]), a + np.array([-size, size, 0]), color=color, stroke_width=width),
    )


def dot_mark(center, radius=0.04, color=FIELD, width=2.4):
    a = np.array([center[0], center[1], 0.0])
    return VGroup(
        Circle(radius=radius * 2.0, color=color, stroke_width=width).move_to(a),
        Dot(a, radius=radius * 0.55, color=color),
    )


def field_marks(width, height, cols, rows, center=ORIGIN, into=True):
    group = VGroup()
    for i in range(cols):
        for j in range(rows):
            x = center[0] - width / 2 + (i + 0.5) * width / cols
            y = center[1] - height / 2 + (j + 0.5) * height / rows
            group.add(cross_mark((x, y)) if into else dot_mark((x, y)))
    return group


def field_panel(width, height, cols, rows, center=ORIGIN, into=True):
    rect = Rectangle(
        width=width,
        height=height,
        stroke_color=LINE,
        stroke_width=2.2,
        fill_color="#e8f0fb",
        fill_opacity=0.85,
    ).move_to(center)
    return VGroup(rect, field_marks(width, height, cols, rows, center, into))


def coil_ellipse(rx, ry, center, color=COIL, width=5, fill_opacity=0.08):
    rx = max(rx, 0.03)
    ry = max(ry, 0.03)
    e = Ellipse(width=2 * rx, height=2 * ry, color=color, stroke_width=width)
    e.set_fill(color, opacity=fill_opacity)
    return e.move_to(center)


def lamp(center, radius=0.16, on=False):
    glow = Circle(radius=radius * 2.4, stroke_width=0, fill_color=LAMP, fill_opacity=0.38 if on else 0.0)
    glow.move_to(center)
    body = Circle(
        radius=radius,
        color="#b45309" if on else MUTED,
        stroke_width=2.6,
        fill_color=LAMP if on else "#ffffff",
        fill_opacity=0.95 if on else 1.0,
    ).move_to(center)
    filament = VGroup(
        Line(center + LEFT * 0.05 + UP * 0.05, center + LEFT * 0.015 + DOWN * 0.05, color="#b45309", stroke_width=2),
        Line(center + LEFT * 0.015 + DOWN * 0.05, center + RIGHT * 0.015 + UP * 0.05, color="#b45309", stroke_width=2),
        Line(center + RIGHT * 0.015 + UP * 0.05, center + RIGHT * 0.05 + DOWN * 0.05, color="#b45309", stroke_width=2),
    )
    return VGroup(glow, body, filament)


def panel_box(width, height, center):
    return RoundedRectangle(
        width=width,
        height=height,
        corner_radius=0.18,
        stroke_color=LINE,
        stroke_width=2,
        fill_color=PANEL,
        fill_opacity=1.0,
    ).move_to(center)


def _g(u):
    """椭圆（或圆）在 x = u·a 右侧的面积系数。"""
    if u >= 1:
        return 0.0
    if u <= -1:
        return math.pi
    return math.acos(u) - u * math.sqrt(1 - u * u)


def overlap_fraction(radius, center_x, half_width):
    """圆与竖直条带（匀强磁场区域）重叠面积占圆面积的比例。"""
    a = radius
    u1 = (-half_width - center_x) / a
    u2 = (half_width - center_x) / a
    area = a * a * (_g(u1) - _g(u2))
    full = math.pi * a * a
    return max(0.0, min(1.0, area / full))


# ---------- 场景 ----------

class MagneticFluxScene(Scene):
    """磁通量与电磁感应现象的产生条件（人教版必修第三册 第十三章）。"""

    def construct(self):
        self.field_image()
        self.flux_definition()
        self.coil_translate()
        self.three_cases()
        self.summary()

    # 分镜 1：磁场与磁感线的空间图像
    def field_image(self):
        header = title("磁场与磁感线", "匀强磁场：空间各点的磁感应强度 B 大小相等、方向相同")
        self.play(FadeIn(header, shift=DOWN), run_time=0.6)

        lines = VGroup()
        for i in range(5):
            start = np.array([-5.35, -1.5 + i * 0.62, 0.0])
            end = start + np.array([1.5, 0.85, 0.0])
            lines.add(
                Arrow(start, end, buff=0, color=FIELD, stroke_width=3.4,
                      max_tip_length_to_length_ratio=0.18)
            )
        left_text = VGroup(
            cn("磁感线：一组平行直线", 24, INK, "BOLD"),
            cn("方向相同、间距相同", 22, MUTED),
        ).arrange(DOWN, buff=0.1).move_to([-3.4, -2.55, 0])

        self.play(LaggedStart(*[GrowArrow(a) for a in lines], lag_ratio=0.14), run_time=1.5)
        self.play(FadeIn(left_text, shift=UP), run_time=0.6)

        right_center = np.array([3.5, 0.05, 0.0])
        right = field_panel(3.2, 2.5, 5, 4, right_center, into=True)
        sight = CurvedArrow(
            start_point=np.array([-1.15, 1.55, 0.0]),
            end_point=np.array([1.55, 1.55, 0.0]),
            angle=-0.55,
            color=WARN,
            stroke_width=3,
        )
        sight_text = cn("沿 B 方向观察", 20, WARN).next_to(sight, UP, buff=0.05)
        right_text = VGroup(
            cn("看到的是 ×：B 垂直纸面向里", 23, INK, "BOLD"),
            cn("若 B 向外，则画成 ·", 22, MUTED),
        ).arrange(DOWN, buff=0.1).move_to([3.5, -2.1, 0])

        legend = VGroup(
            VGroup(cross_mark((0, 0)), cn("向里", 21, MUTED)).arrange(RIGHT, buff=0.14),
            VGroup(dot_mark((0, 0)), cn("向外", 21, MUTED)).arrange(RIGHT, buff=0.14),
        ).arrange(RIGHT, buff=0.75).move_to([3.5, -3.15, 0])

        self.play(FadeIn(right), run_time=0.8)
        self.play(Create(sight), FadeIn(sight_text), run_time=0.9)
        self.play(FadeIn(right_text, shift=UP), FadeIn(legend, shift=UP), run_time=0.7)
        self.wait(0.8)
        self.play(
            FadeOut(VGroup(header, lines, left_text, right, right_text, legend, sight, sight_text)),
            run_time=0.7,
        )

    # 分镜 2：磁通量 Φ = B·S·cosθ
    def flux_definition(self):
        header = title("磁通量：穿过线圈的磁感线有多少", "Φ = B·S·cosθ，θ 为线圈法线 n 与 B 的夹角")
        self.play(FadeIn(header, shift=DOWN), run_time=0.6)

        field_center = np.array([-3.7, -0.3, 0.0])
        field = field_panel(3.4, 2.9, 5, 4, field_center, into=True)
        axis_line = DashedLine(
            field_center + DOWN * 1.12,
            field_center + UP * 1.12,
            color=MUTED,
            stroke_width=2,
        )
        axis_text = cn("转轴", 18, MUTED).next_to(axis_line, UP, buff=0.06)

        theta = ValueTracker(0.0)
        radius = 0.9

        def coil_shape():
            th = theta.get_value()
            return coil_ellipse(radius * abs(math.cos(th)), radius, field_center)

        coil = always_redraw(coil_shape)

        def normal_shape():
            th = theta.get_value()
            length = 1.15 * abs(math.sin(th))
            if length < 0.15:
                return VGroup()
            return VGroup(
                Arrow(
                    field_center,
                    field_center + RIGHT * length,
                    buff=0,
                    color=NORMAL,
                    stroke_width=4,
                    max_tip_length_to_length_ratio=0.26,
                )
            )

        normal = always_redraw(normal_shape)
        n_label = MathTex("n", font_size=34, color=NORMAL)
        n_label.add_updater(
            lambda m: m.move_to(field_center + RIGHT * (1.15 * abs(math.sin(theta.get_value())) + 0.26))
        )

        self.play(FadeIn(field), FadeIn(axis_line), FadeIn(axis_text), run_time=0.9)
        self.add(coil, normal, n_label)

        formula = MathTex(r"\Phi = B\,S\cos\theta", font_size=54, color=INK).move_to([3.5, 1.5, 0])
        given = cn("B = 0.15 T，S = 150 cm²", 19, MUTED).move_to([3.5, 1.02, 0])
        phi_label = cn("Φ =", 26, INK).move_to([2.35, 0.62, 0])
        phi_num = DecimalNumber(PHI_MAX, num_decimal_places=2, font_size=44, color=WARN)
        phi_num.move_to([3.35, 0.62, 0])
        phi_unit = cn("mWb", 24, MUTED).move_to([4.35, 0.62, 0])

        theta_label = cn("θ =", 26, INK).move_to([2.55, -0.1, 0])
        theta_num = DecimalNumber(0, num_decimal_places=0, font_size=38, color=INK)
        theta_num.move_to([3.3, -0.1, 0])
        theta_unit = cn("°", 30, INK).move_to([3.85, -0.1, 0])

        axes = Axes(
            x_range=[0, 90, 30],
            y_range=[0, 2.5, 1],
            x_length=3.3,
            y_length=1.5,
            tips=False,
            axis_config={"stroke_color": MUTED, "stroke_width": 2, "font_size": 18},
        ).move_to([3.5, -2.0, 0])
        curve = axes.plot(
            lambda d: PHI_MAX * math.cos(d * DEG),
            x_range=[0, 90],
            color=ACCENT,
            stroke_width=3.4,
        )
        curve_text = cn("Φ 随 θ 的曲线", 19, MUTED).next_to(axes, DOWN, buff=0.12)

        def dot_pos():
            d = theta.get_value()
            return Dot(axes.c2p(d / DEG, PHI_MAX * math.cos(d)), color=WARN, radius=0.065)

        moving_dot = always_redraw(dot_pos)

        phi_num.add_updater(lambda m: m.set_value(PHI_MAX * math.cos(theta.get_value())))
        theta_num.add_updater(lambda m: m.set_value(theta.get_value() / DEG))

        self.play(Write(formula), run_time=0.9)
        self.play(FadeIn(given), run_time=0.4)
        self.play(FadeIn(phi_label), FadeIn(phi_num), FadeIn(phi_unit), run_time=0.4)
        self.play(FadeIn(theta_label), FadeIn(theta_num), FadeIn(theta_unit), run_time=0.4)
        self.play(FadeIn(axes), Create(curve), run_time=1.0)
        self.play(FadeIn(moving_dot), run_time=0.4)
        self.wait(0.5)

        self.play(theta.animate.set_value(60 * DEG), run_time=3.0, rate_func=smooth)
        self.play(theta.animate.set_value(90 * DEG), run_time=2.2, rate_func=smooth)

        end_text = VGroup(
            cn("θ = 0°：Φ 最大", 22, INK),
            cn("θ = 90°：Φ = 0（线圈平面与 B 平行）", 22, WARN, "BOLD"),
        ).arrange(DOWN, buff=0.12).move_to([-3.7, -3.2, 0])
        self.play(FadeIn(end_text, shift=UP), run_time=0.8)
        self.wait(1.0)

        phi_num.clear_updaters()
        theta_num.clear_updaters()
        coil.clear_updaters()
        normal.clear_updaters()
        n_label.clear_updaters()
        moving_dot.clear_updaters()
        self.play(
            FadeOut(VGroup(header, field, axis_line, axis_text, coil, normal, n_label,
                           formula, given, phi_label, phi_num, phi_unit, theta_label,
                           theta_num, theta_unit, axes, curve, curve_text, moving_dot,
                           end_text)),
            run_time=0.8,
        )

    # 分镜 3：线圈平移进出磁场
    def coil_translate(self):
        header = title("线圈平移进出磁场", "完全在磁场内平移时 Φ 不变；跨过边界时 Φ 变化")
        self.play(FadeIn(header, shift=DOWN), run_time=0.6)

        field_center = np.array([-0.25, 0.2, 0.0])
        half_width = 1.8
        radius = 0.8
        field = field_panel(2 * half_width, 2.7, 6, 5, field_center, into=True)
        field_text = cn("匀强磁场区域", 20, MUTED).move_to([field_center[0], 1.82, 0])
        self.play(FadeIn(field), FadeIn(field_text, shift=UP), run_time=0.9)

        xc = ValueTracker(-4.7)

        coil = coil_ellipse(radius, radius, ORIGIN)
        coil.add_updater(lambda m: m.move_to(np.array([xc.get_value(), field_center[1], 0.0])))

        v_arrow = Arrow(ORIGIN, RIGHT * 0.7, buff=0, color=WARN, stroke_width=3.4,
                        max_tip_length_to_length_ratio=0.32)
        v_arrow.add_updater(lambda m: m.move_to(np.array([xc.get_value(), field_center[1], 0.0]) + RIGHT * 1.28))

        v_text = cn("v", 24, WARN, "BOLD")
        v_text.add_updater(
            lambda m: m.move_to(np.array([xc.get_value(), field_center[1], 0.0]) + RIGHT * 1.28 + UP * 0.48)
        )

        def fraction():
            return overlap_fraction(radius, xc.get_value() - field_center[0], half_width)

        phi_label = cn("Φ =", 26, INK).move_to([-1.8, -3.15, 0])
        phi_num = DecimalNumber(0.0, num_decimal_places=2, font_size=44, color=WARN)
        phi_num.move_to([-0.4, -3.15, 0])
        phi_unit = cn("mWb", 24, MUTED).move_to([0.75, -3.15, 0])
        phi_num.add_updater(lambda m: m.set_value(PHI_MAX * fraction()))

        changing = cn("Φ 正在变化", 26, WARN, "BOLD").move_to([3.3, -3.15, 0])
        steady = cn("Φ 保持不变", 26, MUTED, "BOLD").move_to([3.3, -3.15, 0])
        changing.set_opacity(0)
        steady.set_opacity(0)

        def status_updater(dt):
            f = fraction()
            moving = 0.001 < f < 0.999
            changing.set_opacity(1.0 if moving else 0.0)
            steady.set_opacity(0.0 if moving else 1.0)
            changing.move_to([3.3, -3.15, 0])
            steady.move_to([3.3, -3.15, 0])

        status_updater(0)
        status_group = VGroup(changing, steady)
        status_group.add_updater(status_updater)

        self.add(coil, v_arrow, v_text, phi_label, phi_num, phi_unit, status_group)
        self.wait(0.5)

        self.play(xc.animate.set_value(4.7), run_time=9.0, rate_func=linear)

        self.wait(0.6)
        for mobject in (coil, v_arrow, v_text, phi_num, status_group):
            mobject.clear_updaters()
        self.play(
            FadeOut(VGroup(header, field, field_text, coil, v_arrow, v_text, phi_label,
                           phi_num, phi_unit, status_group)),
            run_time=0.8,
        )

    # 分镜 4：三种情形的对比
    def three_cases(self):
        header = title("三种情形：Φ 变了没有？", "线圈静止、平移进出、绕轴转动")
        self.play(FadeIn(header, shift=DOWN), run_time=0.6)

        def mini_panel(center, name, coil_rx, coil_ry, lit, coil_shift=0.0):
            box = panel_box(4.0, 3.9, center)
            patch_center = np.array([center[0], center[1] + 0.4, 0.0])
            patch = field_panel(2.2, 1.2, 4, 3, patch_center, into=True)
            coil = coil_ellipse(coil_rx, coil_ry, patch_center + RIGHT * coil_shift)
            bulb = lamp(np.array([center[0], center[1] - 0.62, 0.0]), 0.13, lit)
            name_text = cn(name, 22, INK, "BOLD").move_to([center[0], center[1] + 1.42, 0])
            result_text = cn("Φ 变化" if lit else "Φ 不变", 24, WARN if lit else MUTED, "BOLD")
            result_text.move_to([center[0], center[1] - 1.35, 0])
            status_text = cn("有感应电流" if lit else "无感应电流", 21, WARN if lit else MUTED)
            status_text.move_to([center[0], center[1] - 1.72, 0])
            return VGroup(box, patch, coil, bulb, name_text, result_text, status_text)

        left = mini_panel(np.array([-4.55, -0.3, 0.0]), "静止在磁场中", 0.5, 0.5, False)
        mid = mini_panel(np.array([0.0, -0.3, 0.0]), "平移进出磁场", 0.5, 0.5, True, 0.78)
        right = mini_panel(np.array([4.55, -0.3, 0.0]), "绕轴转动", 0.3, 0.5, True)

        self.play(FadeIn(left, shift=UP), run_time=0.7)
        self.play(FadeIn(mid, shift=UP), run_time=0.7)
        self.play(FadeIn(right, shift=UP), run_time=0.7)

        for panel in (mid, right):
            glow = panel[3][0]
            self.play(glow.animate.set_fill(LAMP, opacity=0.55), run_time=0.35)
            self.play(glow.animate.set_fill(LAMP, opacity=0.28), run_time=0.35)

        motion_note = VGroup(
            Arrow(np.array([1.35, 0.02, 0.0]), np.array([2.15, 0.02, 0.0]), buff=0,
                  color=WARN, stroke_width=3.2, max_tip_length_to_length_ratio=0.3),
            cn("线圈在此位置来回运动", 19, MUTED),
        ).arrange(RIGHT, buff=0.16).move_to([0.0, -2.55, 0])

        rotate_note = VGroup(
            Arc(radius=0.3, start_angle=-PI / 2, angle=2.2, color=WARN, stroke_width=3),
            cn("转动", 19, MUTED),
        ).arrange(RIGHT, buff=0.16).move_to([4.55, -2.55, 0])

        self.play(FadeIn(motion_note), FadeIn(rotate_note), run_time=0.6)
        self.wait(1.2)
        self.play(
            FadeOut(VGroup(header, left, mid, right, motion_note, rotate_note)),
            run_time=0.8,
        )

    # 分镜 5：归纳产生感应电流的条件
    def summary(self):
        header = cn("产生感应电流的条件", 38, INK, "BOLD").to_edge(UP, buff=0.55)
        self.play(FadeIn(header, shift=DOWN), run_time=0.6)

        items = VGroup(
            cn("1  Φ = B·S·cosθ：B 越大、有效面积越大，Φ 越大。", 25, INK),
            cn("2  B、S、θ 任一个改变，或线圈进出磁场，Φ 都会变化。", 25, INK),
            cn("3  Φ 不变时，闭合回路中没有感应电流。", 25, MUTED),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.26).move_to([0.0, 0.7, 0])

        key_box = RoundedRectangle(
            width=9.8,
            height=1.15,
            corner_radius=0.16,
            stroke_color=WARN,
            stroke_width=2.4,
            fill_color="#fff4e8",
            fill_opacity=1.0,
        ).move_to([0.0, -1.65, 0])
        key_text = cn("穿过闭合回路的磁通量发生变化 → 产生感应电流", 26, WARN, "BOLD")
        key_text.move_to(key_box)

        self.play(FadeIn(items, shift=RIGHT), run_time=1.0)
        self.play(FadeIn(key_box), Write(key_text), run_time=1.0)
        self.wait(1.6)
        self.play(FadeOut(VGroup(header, items, key_box, key_text)), run_time=0.8)


if __name__ == "__main__":
    # manim -pql magnetic_flux.py MagneticFluxScene
    pass
