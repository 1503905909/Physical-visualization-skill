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
FIELD = "#0f766e"
PATH = "#f59f00"
FORCE = "#0ea5e9"
POSITIVE = "#d9480f"
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


def particle(radius=0.16):
    dot = Circle(radius=radius, stroke_color="#ffffff", stroke_width=2, fill_color=POSITIVE, fill_opacity=1)
    sign = cn("+", 17, "#ffffff", "BOLD").move_to(dot)
    return VGroup(dot, sign)


def cyclotron_body():
    left = Arc(radius=2.0, start_angle=PI / 2, angle=PI, color=LINE, stroke_width=3)
    left.add(Line(UP * 2, DOWN * 2, color=LINE, stroke_width=3))
    left.shift(LEFT * 0.22)
    right = Arc(radius=2.0, start_angle=-PI / 2, angle=PI, color=LINE, stroke_width=3)
    right.add(Line(DOWN * 2, UP * 2, color=LINE, stroke_width=3))
    right.shift(RIGHT * 0.22)
    fill_l = AnnularSector(inner_radius=0.0, outer_radius=2.0, angle=PI, start_angle=PI / 2, fill_color="#dbeafe", fill_opacity=0.48, stroke_width=0).shift(LEFT * 0.22)
    fill_r = AnnularSector(inner_radius=0.0, outer_radius=2.0, angle=PI, start_angle=-PI / 2, fill_color="#e0f2fe", fill_opacity=0.48, stroke_width=0).shift(RIGHT * 0.22)
    gap = DashedLine(UP * 2.0, DOWN * 2.0, color=PATH, stroke_width=3)
    labels = VGroup(cn("D₁", 24, INK, "BOLD").shift(LEFT * 1.2 + UP * 1.55), cn("D₂", 24, INK, "BOLD").shift(RIGHT * 1.2 + UP * 1.55))
    return VGroup(fill_l, fill_r, left, right, gap, labels)


def b_field_symbols():
    marks = VGroup()
    for x in np.linspace(-2.2, 2.2, 6):
        for y in np.linspace(-1.55, 1.55, 4):
            if abs(x) < 0.22:
                continue
            dot = Dot(np.array([x, y, 0]), radius=0.028, color=MUTED)
            ring = Circle(radius=0.08, color=MUTED, stroke_width=1.2).move_to(dot)
            marks.add(VGroup(ring, dot))
    return marks


def spiral_points(turns=3.35, samples=260):
    pts = []
    start = -PI / 2
    end = start + turns * TAU
    for i in range(samples + 1):
        t = i / samples
        theta = start + (end - start) * t
        r = 0.22 + 1.72 * (t ** 0.72)
        pts.append(np.array([r * np.cos(theta), r * np.sin(theta), 0]))
    return pts


class CyclotronScene(Scene):
    """回旋加速器原理。"""

    def construct(self):
        self.structure()
        self.acceleration_and_bending()
        self.period_relation()
        self.summary()

    def structure(self):
        header = title("回旋加速器", "D 形盒内磁场偏转，盒间缝隙电场加速")
        self.play(FadeIn(header, shift=DOWN), run_time=0.7)
        body = cyclotron_body().scale(1.25).shift(DOWN * 0.2)
        bmarks = b_field_symbols().scale(1.25).shift(DOWN * 0.2)
        e_arrows = VGroup(*[
            arrow(np.array([-0.22, y, 0]), np.array([0.22, y, 0]), PATH, 4)
            for y in [-1.15, 0, 1.15]
        ]).scale(1.25).shift(DOWN * 0.2)
        note = VGroup(
            cn("磁场 B 垂直纸面向外", 25, FIELD, "BOLD"),
            cn("缝隙电场每半个周期反向一次", 24, MUTED),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).to_edge(RIGHT, buff=0.9).shift(DOWN * 0.1)

        self.play(FadeIn(body), run_time=0.7)
        self.play(FadeIn(bmarks), FadeIn(note[0], shift=LEFT), run_time=0.7)
        self.play(LaggedStart(*[Create(a) for a in e_arrows], lag_ratio=0.12), FadeIn(note[1], shift=LEFT), run_time=0.9)
        self.wait(0.8)
        self.play(FadeOut(VGroup(header, body, bmarks, e_arrows, note)), run_time=0.8)

    def acceleration_and_bending(self):
        header = title("粒子怎样越转越快？", "盒内速度大小近似不变；过缝隙时电场做功")
        self.play(FadeIn(header, shift=DOWN), run_time=0.6)

        body = cyclotron_body().scale(1.18).shift(LEFT * 1.0 + DOWN * 0.18)
        bmarks = b_field_symbols().scale(1.18).shift(LEFT * 1.0 + DOWN * 0.18)
        pts = [p * 1.18 + LEFT * 1.0 + DOWN * 0.18 for p in spiral_points()]
        path = VMobject(color=PATH, stroke_width=4)
        path.set_points_smoothly(pts)
        mover = particle().move_to(pts[0])
        formula = VGroup(
            MathTex(r"qvB=\frac{mv^2}{r}", font_size=42, color=INK),
            MathTex(r"\Delta E_k=qU", font_size=42, color=INK),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28).to_edge(RIGHT, buff=0.9).shift(UP * 0.45)
        note = cn("每次通过缝隙，动能增加；速度增大后半径也增大。", 24, MUTED).next_to(formula, DOWN, buff=0.32)

        self.play(FadeIn(VGroup(body, bmarks, mover)), run_time=0.6)
        self.play(Create(path), MoveAlongPath(mover, path), run_time=3.0, rate_func=linear)
        self.play(FadeIn(formula, shift=LEFT), FadeIn(note, shift=LEFT), run_time=1.0)
        self.wait(0.9)
        self.play(FadeOut(VGroup(header, body, bmarks, path, mover, formula, note)), run_time=0.8)

    def period_relation(self):
        header = title("为什么每次到缝隙时电场方向刚好反向？")
        self.play(FadeIn(header, shift=DOWN), run_time=0.6)

        circles = VGroup()
        labels = VGroup()
        for r, label, color in [(0.82, "低速", FIELD), (1.38, "中速", PATH), (1.94, "高速", ACCENT)]:
            c = Circle(radius=r, color=color, stroke_width=3).shift(LEFT * 2.65 + DOWN * 0.12)
            circles.add(c)
            labels.add(cn(label, 22, color, "BOLD").next_to(c, RIGHT, buff=0.16))
        formula = MathTex(r"T=\frac{2\pi m}{qB}", font_size=58, color=INK).to_edge(RIGHT, buff=1.0).shift(UP * 0.6)
        explanation = VGroup(
            cn("非相对论条件下，同一粒子在同一 B 中", 25, INK),
            cn("周期与速度无关", 30, FIELD, "BOLD"),
            cn("所以交流电压可按固定频率反向。", 24, MUTED),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).next_to(formula, DOWN, buff=0.4)

        dots = VGroup(*[
            Dot(c.point_at_angle(-PI / 2), radius=0.06, color=c.get_color())
            for c in circles
        ])
        self.play(Create(circles), FadeIn(labels), run_time=0.9)
        self.play(FadeIn(dots), run_time=0.4)
        self.play(
            *[MoveAlongPath(dot, circle) for dot, circle in zip(dots, circles)],
            run_time=2.2,
            rate_func=linear,
        )
        self.play(Write(formula), FadeIn(explanation, shift=LEFT), run_time=1.0)
        self.wait(1.0)
        self.play(FadeOut(VGroup(header, circles, labels, dots, formula, explanation)), run_time=0.8)

    def summary(self):
        header = cn("课堂归纳", 38, INK, "BOLD").to_edge(UP, buff=0.75)
        items = VGroup(
            cn("1  D 形盒内磁场提供向心力，粒子做圆周运动。", 28, INK),
            cn("2  缝隙中电场做功，粒子动能逐次增加。", 28, INK),
            cn("3  半径 r = mv/qB 随速度增大；周期 T = 2πm/qB。", 28, FIELD, "BOLD"),
            cn("4  模型适用于非相对论近似，实际能量存在上限。", 27, MUTED),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.30).move_to(ORIGIN)
        panel = RoundedRectangle(width=11.0, height=3.75, corner_radius=0.22, stroke_color=LINE, stroke_width=2, fill_color=PANEL, fill_opacity=1).move_to(items)
        self.play(FadeIn(header, shift=DOWN), FadeIn(panel), run_time=0.7)
        for item in items:
            self.play(FadeIn(item, shift=RIGHT), run_time=0.35)
        self.wait(1.0)
        self.play(FadeOut(VGroup(header, panel, items)), run_time=0.8)


if __name__ == "__main__":
    # manim -pql cyclotron.py CyclotronScene
    pass
