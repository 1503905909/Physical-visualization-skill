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
EQUIP = "#7c3aed"
PROBE = "#f59f00"


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


def charge(value, label="Q", radius=0.34):
    color = POSITIVE if value > 0 else NEGATIVE
    c = Circle(radius=radius, stroke_color="#ffffff", stroke_width=2)
    c.set_fill(color, opacity=1)
    sign = "+" if value > 0 else "-"
    sign_text = cn(sign, 31, "#ffffff", "BOLD").move_to(c.get_center() + UP * 0.03)
    label_text = cn(label, 18, "#ffffff", "BOLD").move_to(c.get_center() + DOWN * 0.16)
    return VGroup(c, sign_text, label_text)


def arrow(start, end, color=FIELD, width=3):
    return Arrow(start, end, buff=0, stroke_width=width, color=color, max_tip_length_to_length_ratio=0.35)


def equipotential_circles(center, radii):
    return VGroup(*[
        Circle(radius=r, color=EQUIP, stroke_width=2.5).move_to(center).set_opacity(0.82)
        for r in radii
    ])


def radial_field(center, count=12, inner=0.35, outer=2.35):
    lines = VGroup()
    for i in range(count):
        a = TAU * i / count
        d = np.array([np.cos(a), np.sin(a), 0])
        lines.add(arrow(center + d * inner, center + d * outer, FIELD, 2.8))
    return lines


def dipole_equipotentials(left, right):
    group = VGroup()
    for r in [0.55, 0.90, 1.25]:
        group.add(Circle(r, color="#ef4444", stroke_width=2.2).move_to(left).set_opacity(0.68))
        group.add(Circle(r, color="#3b82f6", stroke_width=2.2).move_to(right).set_opacity(0.68))
    midline = DashedLine(UP * 2.2, DOWN * 2.2, color=EQUIP, stroke_width=3).shift((left + right) / 2)
    group.add(midline)
    return group


def dipole_field_arrows(left, right):
    group = VGroup()
    samples = [
        (left + RIGHT * 0.55 + UP * 0.55, RIGHT * 0.9 + DOWN * 0.18),
        (left + RIGHT * 0.55 + DOWN * 0.55, RIGHT * 0.9 + UP * 0.18),
        ((left + right) / 2 + UP * 1.05, RIGHT * 1.0),
        ((left + right) / 2 + DOWN * 1.05, RIGHT * 1.0),
        (right + LEFT * 0.85, RIGHT * 0.7),
    ]
    for start, direction in samples:
        unit = direction / np.linalg.norm(direction)
        group.add(arrow(start, start + unit * 0.75, FIELD, 3.2))
    return group


class ElectricPotentialEquipotentialScene(Scene):
    """电势与等势面关系。"""

    def construct(self):
        self.scalar_vs_vector()
        self.equipotential_relation()
        self.uniform_field_relation()
        self.summary()

    def scalar_vs_vector(self):
        header = title("电势与等势面", "用颜色或高度理解电势，用箭头理解电场方向")
        self.play(FadeIn(header, shift=DOWN), run_time=0.7)

        center = LEFT * 2.9 + DOWN * 0.15
        q = charge(1).move_to(center)
        circles = equipotential_circles(center, [0.72, 1.15, 1.58, 2.02])
        field = radial_field(center, 12, outer=2.35)
        labels = VGroup(
            cn("等势线：电势相等的位置", 27, EQUIP, "BOLD"),
            cn("电场线：电场强度方向", 27, FIELD, "BOLD"),
            cn("越靠近正电荷，电势越高", 24, MUTED),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.24).to_edge(RIGHT, buff=0.95).shift(DOWN * 0.25)

        self.play(FadeIn(q, scale=0.75), run_time=0.5)
        self.play(Create(circles), run_time=1.1)
        self.play(LaggedStart(*[Create(a) for a in field], lag_ratio=0.04), FadeIn(labels, shift=LEFT), run_time=1.2)
        self.wait(0.8)
        self.play(FadeOut(VGroup(header, q, circles, field, labels)), run_time=0.8)

    def equipotential_relation(self):
        header = title("等势线与电场线垂直", "电场方向从高电势指向低电势")
        self.play(FadeIn(header, shift=DOWN), run_time=0.6)

        left = LEFT * 1.45 + DOWN * 0.25
        right = RIGHT * 1.45 + DOWN * 0.25
        charges = VGroup(charge(1).move_to(left), charge(-1).move_to(right))
        eq = dipole_equipotentials(left, right)
        fields = dipole_field_arrows(left, right)
        probe = VGroup(
            Circle(radius=0.16, stroke_color="#ffffff", stroke_width=2, fill_color=PROBE, fill_opacity=1),
            cn("V", 14, INK, "BOLD"),
        ).move_to(UP * 0.95 + LEFT * 0.25)
        probe_arrow = arrow(probe.get_center(), probe.get_center() + RIGHT * 0.9, PROBE, 4)

        note = VGroup(
            cn("沿同一等势线移动，静电力不做功。", 25, INK),
            cn("电场线穿过等势线时近似垂直。", 25, FIELD, "BOLD"),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).to_edge(DOWN, buff=0.52)

        self.play(FadeIn(charges, scale=0.75), run_time=0.5)
        self.play(Create(eq), run_time=1.2)
        self.play(LaggedStart(*[Create(a) for a in fields], lag_ratio=0.08), run_time=0.9)
        self.play(FadeIn(probe, scale=0.8), Create(probe_arrow), FadeIn(note, shift=UP), run_time=0.8)
        self.play(probe.animate.move_to(UP * 0.95 + RIGHT * 0.25), probe_arrow.animate.shift(RIGHT * 0.5), run_time=1.1)
        self.wait(0.8)
        self.play(FadeOut(VGroup(header, charges, eq, fields, probe, probe_arrow, note)), run_time=0.8)

    def uniform_field_relation(self):
        header = title("匀强电场中的等势线", "等势线间距相同；E = U / d")
        self.play(FadeIn(header, shift=DOWN), run_time=0.6)

        plate_l = Rectangle(width=0.22, height=4.5, color=POSITIVE, fill_color=POSITIVE, fill_opacity=0.20).shift(LEFT * 3.2 + DOWN * 0.1)
        plate_r = Rectangle(width=0.22, height=4.5, color=NEGATIVE, fill_color=NEGATIVE, fill_opacity=0.20).shift(RIGHT * 3.2 + DOWN * 0.1)
        plus = cn("+", 34, POSITIVE, "BOLD").next_to(plate_l, UP, buff=0.14)
        minus = cn("-", 38, NEGATIVE, "BOLD").next_to(plate_r, UP, buff=0.10)
        fields = VGroup(*[
            arrow(np.array([-2.65, y, 0]), np.array([2.65, y, 0]), FIELD, 3.2)
            for y in np.linspace(-1.8, 1.8, 5)
        ])
        equip = VGroup(*[
            DashedLine(np.array([x, -2.05, 0]), np.array([x, 2.05, 0]), color=EQUIP, stroke_width=2.6)
            for x in np.linspace(-2.2, 2.2, 6)
        ])
        formula = MathTex(r"E=\frac{U}{d}", font_size=54, color=INK).to_edge(DOWN, buff=0.58)
        note = cn("相邻等势线电势差相等时，间距越小，场强越大。", 24, MUTED).next_to(formula, UP, buff=0.28)

        self.play(FadeIn(VGroup(plate_l, plate_r, plus, minus)), run_time=0.6)
        self.play(LaggedStart(*[Create(a) for a in fields], lag_ratio=0.08), run_time=0.8)
        self.play(LaggedStart(*[Create(line) for line in equip], lag_ratio=0.06), FadeIn(note), Write(formula), run_time=1.1)
        self.wait(1.0)
        self.play(FadeOut(VGroup(header, plate_l, plate_r, plus, minus, fields, equip, formula, note)), run_time=0.8)

    def summary(self):
        header = cn("课堂归纳", 38, INK, "BOLD").to_edge(UP, buff=0.75)
        items = VGroup(
            cn("1  电势是标量，电场强度是矢量。", 29, INK),
            cn("2  等势面上移动电荷，静电力不做功。", 29, INK),
            cn("3  电场线与等势面垂直，并由高电势指向低电势。", 29, FIELD, "BOLD"),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.32).move_to(ORIGIN)
        panel = RoundedRectangle(width=10.4, height=3.2, corner_radius=0.22, stroke_color=LINE, stroke_width=2, fill_color=PANEL, fill_opacity=1).move_to(items)
        self.play(FadeIn(header, shift=DOWN), FadeIn(panel), run_time=0.7)
        for item in items:
            self.play(FadeIn(item, shift=RIGHT), run_time=0.35)
        self.wait(1.0)
        self.play(FadeOut(VGroup(header, panel, items)), run_time=0.8)


if __name__ == "__main__":
    # manim -pql electric_potential_equipotential.py ElectricPotentialEquipotentialScene
    pass
