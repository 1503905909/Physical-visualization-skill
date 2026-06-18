import numpy as np
from manim import *


config.frame_width = 14.222
config.frame_height = 8.0
config.pixel_width = 1280
config.pixel_height = 720
config.background_color = "#f7f8fb"
config.media_dir = r"d:\PycharmProjects1\Physical-visualization-skill\build\videos\manim"


FONT = "Microsoft YaHei"
INK = "#172033"
MUTED = "#667085"
LINE = "#c9d2df"
PANEL = "#ffffff"
POSITIVE = "#d9480f"
NEGATIVE = "#2563eb"
FIELD = "#0f766e"
PATH = "#f59f00"
ACCENT = "#7c3aed"


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


def arrow(start, end, color=FIELD, width=3):
    return Arrow(start, end, buff=0, stroke_width=width, color=color, max_tip_length_to_length_ratio=0.35)


def particle(label="+", radius=0.19, color=POSITIVE):
    dot = Circle(radius=radius, stroke_color="#ffffff", stroke_width=2, fill_color=color, fill_opacity=1)
    sign = cn(label, 18, "#ffffff", "BOLD").move_to(dot)
    return VGroup(dot, sign)


def trajectory_points(x0=-4.4, x1=4.1, y0=0.85, curvature=0.18, samples=90):
    pts = []
    for i in range(samples + 1):
        t = i / samples
        x = x0 + (x1 - x0) * t
        y = y0 - curvature * (t ** 2) * 9.0
        pts.append(np.array([x, y, 0]))
    return pts


class ChargedParticleUniformFieldScene(Scene):
    """带电粒子垂直进入匀强电场后的偏转。"""

    def construct(self):
        self.field_and_force()
        self.decompose_motion()
        self.parameter_comparison()
        self.summary()

    def field_and_force(self):
        header = title("带电粒子在匀强电场中的运动", "初速度垂直于电场时，轨迹发生偏转")
        self.play(FadeIn(header, shift=DOWN), run_time=0.7)

        top_plate = Rectangle(width=9.4, height=0.22, color=POSITIVE, fill_color=POSITIVE, fill_opacity=0.18).shift(UP * 2.05)
        bottom_plate = Rectangle(width=9.4, height=0.22, color=NEGATIVE, fill_color=NEGATIVE, fill_opacity=0.18).shift(DOWN * 2.05)
        plus = cn("+ 极板", 24, POSITIVE, "BOLD").next_to(top_plate, LEFT, buff=0.18)
        minus = cn("- 极板", 24, NEGATIVE, "BOLD").next_to(bottom_plate, LEFT, buff=0.18)
        field_arrows = VGroup(*[
            arrow(np.array([x, 1.72, 0]), np.array([x, -1.72, 0]), FIELD, 3)
            for x in np.linspace(-3.7, 3.7, 7)
        ])
        p = particle("+").move_to(np.array([-4.15, 0.95, 0]))
        v0 = arrow(p.get_center(), p.get_center() + RIGHT * 1.05, "#64748b", 4)
        force = arrow(p.get_center(), p.get_center() + DOWN * 0.95, PATH, 4.5)
        labels = VGroup(
            cn("正电荷：F = qE，方向与电场方向相同", 25, INK, "BOLD"),
            cn("水平方向没有电场力，竖直方向受恒力", 24, MUTED),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).to_edge(DOWN, buff=0.55)

        self.play(FadeIn(VGroup(top_plate, bottom_plate, plus, minus)), run_time=0.6)
        self.play(LaggedStart(*[Create(a) for a in field_arrows], lag_ratio=0.06), run_time=0.8)
        self.play(FadeIn(p, scale=0.8), Create(v0), Create(force), FadeIn(labels, shift=UP), run_time=0.9)
        self.wait(0.8)
        self.play(FadeOut(VGroup(header, top_plate, bottom_plate, plus, minus, field_arrows, p, v0, force, labels)), run_time=0.8)

    def decompose_motion(self):
        header = title("运动分解", "水平方向匀速，竖直方向匀加速")
        self.play(FadeIn(header, shift=DOWN), run_time=0.6)

        axes = Axes(
            x_range=[0, 8, 1],
            y_range=[-3, 1.5, 1],
            x_length=8.8,
            y_length=4.6,
            tips=False,
            axis_config={"color": LINE, "stroke_width": 2},
        ).shift(DOWN * 0.2)
        x_label = cn("x", 22, MUTED).next_to(axes.x_axis, RIGHT, buff=0.1)
        y_label = cn("y", 22, MUTED).next_to(axes.y_axis, UP, buff=0.1)
        pts = trajectory_points(x0=-4.4, x1=4.1, y0=0.85, curvature=0.18)
        path = VMobject(color=PATH, stroke_width=4)
        path.set_points_smoothly(pts)
        mover = particle("+").move_to(pts[0])
        guide_x = DashedLine(pts[0], np.array([pts[-1][0], pts[0][1], 0]), color="#94a3b8", stroke_width=2)
        guide_y = DashedLine(np.array([pts[-1][0], pts[0][1], 0]), pts[-1], color=ACCENT, stroke_width=2)
        formula = VGroup(
            MathTex(r"x=v_0t", font_size=42, color=INK),
            MathTex(r"y=\frac12at^2,\quad a=\frac{qE}{m}", font_size=42, color=INK),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.24).to_edge(RIGHT, buff=0.7).shift(UP * 0.45)

        self.play(Create(axes), FadeIn(VGroup(x_label, y_label)), FadeIn(mover, scale=0.8), run_time=0.7)
        self.play(Create(path), MoveAlongPath(mover, path), run_time=2.2, rate_func=linear)
        self.play(Create(guide_x), Create(guide_y), FadeIn(formula, shift=LEFT), run_time=1.0)
        self.wait(1.0)
        self.play(FadeOut(VGroup(header, axes, x_label, y_label, path, mover, guide_x, guide_y, formula)), run_time=0.8)

    def parameter_comparison(self):
        header = title("参数改变时，偏转怎样变化？")
        self.play(FadeIn(header, shift=DOWN), run_time=0.6)

        labels = VGroup(
            cn("E 较小", 24, FIELD, "BOLD").shift(LEFT * 4.35 + UP * 1.65),
            cn("E 较大", 24, POSITIVE, "BOLD").shift(LEFT * 4.35 + UP * 0.35),
            cn("v₀ 较大", 24, ACCENT, "BOLD").shift(LEFT * 4.35 + DOWN * 0.95),
        )
        curves = VGroup()
        settings = [(0.10, FIELD, 1.75), (0.22, POSITIVE, 0.45), (0.08, ACCENT, -0.85)]
        for curvature, color, offset in settings:
            pts = trajectory_points(x0=-3.6, x1=4.5, y0=offset, curvature=curvature)
            vm = VMobject(color=color, stroke_width=4)
            vm.set_points_smoothly(pts)
            curves.add(vm)
        formula = MathTex(r"y=\frac{qE}{2m}\left(\frac{x}{v_0}\right)^2", font_size=52, color=INK)
        formula.to_edge(DOWN, buff=0.65)
        note = cn("偏转量随 E 增大而增大，随 v₀ 增大而减小。", 27, INK, "BOLD").next_to(formula, UP, buff=0.24)

        self.play(FadeIn(labels), run_time=0.5)
        self.play(LaggedStart(*[Create(c) for c in curves], lag_ratio=0.25), run_time=1.8)
        self.play(FadeIn(note, shift=UP), Write(formula), run_time=1.0)
        self.wait(1.1)
        self.play(FadeOut(VGroup(header, labels, curves, note, formula)), run_time=0.8)

    def summary(self):
        header = cn("课堂归纳", 38, INK, "BOLD").to_edge(UP, buff=0.75)
        items = VGroup(
            cn("1  电场力 F = qE，方向由电荷正负决定。", 29, INK),
            cn("2  垂直进入匀强电场时，可按平抛运动类比分析。", 29, INK),
            cn("3  偏转轨迹为抛物线；E 越大、m 越小、v₀ 越小，偏转越明显。", 29, FIELD, "BOLD"),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.32).move_to(ORIGIN)
        panel = RoundedRectangle(width=11.0, height=3.2, corner_radius=0.22, stroke_color=LINE, stroke_width=2, fill_color=PANEL, fill_opacity=1).move_to(items)
        self.play(FadeIn(header, shift=DOWN), FadeIn(panel), run_time=0.7)
        for item in items:
            self.play(FadeIn(item, shift=RIGHT), run_time=0.35)
        self.wait(1.0)
        self.play(FadeOut(VGroup(header, panel, items)), run_time=0.8)


if __name__ == "__main__":
    # manim -pql charged_particle_uniform_field.py ChargedParticleUniformFieldScene
    pass
