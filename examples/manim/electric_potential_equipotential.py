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



def fixed_title(scene, text, subtitle):
    group = title(text, subtitle)
    scene.add_fixed_in_frame_mobjects(group)
    return group


def sphere_dirs_for_potential():
    directions = []
    for z, count, offset in [(-0.70, 5, 18), (0.0, 8, 0), (0.70, 5, 45)]:
        radius = np.sqrt(max(0.0, 1 - z * z))
        for i in range(count):
            angle = TAU * i / count + np.deg2rad(offset)
            directions.append(np.array([radius * np.cos(angle), radius * np.sin(angle), z]))
    return directions


def field_lines_3d_for_point(inner=0.42, outer=2.15):
    return VGroup(*[
        Line3D(start=d * inner, end=d * outer, thickness=0.012, color=FIELD, resolution=4)
        for d in sphere_dirs_for_potential()
    ])


def potential_height(x, y, charges):
    value = 0.0
    for q, cx, cy in charges:
        r = np.sqrt((x - cx) ** 2 + (y - cy) ** 2 + 0.16)
        value += q / r
    return float(np.clip(0.92 * value, -1.85, 2.10))


def potential_surface(axes, charges, color="#20c7c9"):
    surface = Surface(
        lambda u, v: axes.c2p(u, v, potential_height(u, v, charges)),
        u_range=[-3.0, 3.0],
        v_range=[-2.1, 2.1],
        resolution=(24, 16),
        fill_opacity=0.54,
        stroke_color="#14868a",
        stroke_width=0.28,
    )
    surface.set_fill(color, opacity=0.50)
    return surface


def contour_ring_on_surface(axes, center, radius, charges, color=EQUIP, width=3.2):
    cx, cy = center
    return ParametricFunction(
        lambda t: axes.c2p(
            cx + radius * np.cos(t),
            cy + radius * np.sin(t),
            potential_height(cx + radius * np.cos(t), cy + radius * np.sin(t), charges) + 0.035,
        ),
        t_range=[0, TAU],
        color=color,
        stroke_width=width,
    )


def base_grid(axes):
    grid = VGroup()
    for x in np.linspace(-3, 3, 7):
        grid.add(Line3D(axes.c2p(x, -2.1, 0), axes.c2p(x, 2.1, 0), thickness=0.004, color="#94a3b8"))
    for y in np.linspace(-2, 2, 5):
        grid.add(Line3D(axes.c2p(-3.0, y, 0), axes.c2p(3.0, y, 0), thickness=0.004, color="#94a3b8"))
    grid.set_opacity(0.45)
    return grid


class ElectricPotential3DSurfaceScene(ThreeDScene):
    """电势与等势面：三维空间模型和电势高度图。"""

    def construct(self):
        self.equipotential_line_to_surface()
        self.potential_surface_compare()

    def equipotential_line_to_surface(self):
        self.set_camera_orientation(phi=0 * DEGREES, theta=-90 * DEGREES, zoom=0.90)
        header = fixed_title(self, "电势与等势面：由等势线到等势面", "平面等势线是空间等势面的一个截面")
        self.play(FadeIn(header, shift=DOWN), run_time=0.6)

        source = charge(1, "Q", 0.30).move_to(ORIGIN)
        circles = equipotential_circles(ORIGIN, [0.75, 1.18, 1.62, 2.05])
        field = radial_field(ORIGIN, count=12, inner=0.35, outer=2.28)
        step1 = cn("二维图示：同一圆周上电势相等", 24, INK, "BOLD").to_edge(DOWN, buff=0.55)
        self.add_fixed_in_frame_mobjects(step1)

        self.play(FadeIn(source, scale=0.85), Create(circles), run_time=1.0)
        self.play(LaggedStart(*[Create(a) for a in field], lag_ratio=0.04), FadeIn(step1, shift=UP), run_time=1.0)
        self.wait(0.45)

        self.play(FadeOut(step1), FadeOut(field), run_time=0.35)
        self.move_camera(phi=64 * DEGREES, theta=-42 * DEGREES, zoom=0.86, run_time=1.3)

        sphere = Sphere(radius=0.25, resolution=(16, 8)).set_color(POSITIVE).set_opacity(0.95)
        shells = VGroup()
        for r, opacity in [(0.75, 0.20), (1.18, 0.15), (1.62, 0.11), (2.05, 0.08)]:
            shell = Sphere(radius=r, resolution=(24, 12))
            shell.set_color(EQUIP)
            shell.set_opacity(opacity)
            shell.set_stroke(EQUIP, width=0.8, opacity=0.28)
            shells.add(shell)
        spatial_field = field_lines_3d_for_point()
        step2 = cn("三维模型：等势线对应空间中的等势面", 24, EQUIP, "BOLD").to_edge(DOWN, buff=0.55)
        self.add_fixed_in_frame_mobjects(step2)

        self.play(FadeOut(source), FadeOut(circles), FadeIn(sphere), FadeIn(shells), FadeIn(spatial_field), FadeIn(step2, shift=UP), run_time=1.2)
        self.move_camera(phi=70 * DEGREES, theta=-10 * DEGREES, zoom=0.84, run_time=1.0)
        self.wait(0.8)
        self.play(FadeOut(VGroup(header, sphere, shells, spatial_field, step2)), run_time=0.7)

    def potential_surface_compare(self):
        self.set_camera_orientation(phi=58 * DEGREES, theta=-50 * DEGREES, zoom=0.92)
        header = fixed_title(self, "三维电势高度图", "用高度辅助理解电势大小，用曲线标出典型等势线")
        self.play(FadeIn(header, shift=DOWN), run_time=0.6)

        axes = ThreeDAxes(
            x_range=[-3.2, 3.2, 1],
            y_range=[-2.2, 2.2, 1],
            z_range=[-2.0, 2.2, 1],
            x_length=6.2,
            y_length=4.2,
            z_length=3.5,
        ).shift(DOWN * 0.08)
        grid = base_grid(axes)

        like_charges = [(1, -1.25, 0.0), (1, 1.25, 0.0)]
        like_surface = potential_surface(axes, like_charges)
        like_contours = VGroup(
            contour_ring_on_surface(axes, (-1.25, 0.0), 0.55, like_charges, EQUIP),
            contour_ring_on_surface(axes, (1.25, 0.0), 0.55, like_charges, EQUIP),
            contour_ring_on_surface(axes, (-1.25, 0.0), 0.95, like_charges, "#2563eb", 2.6),
            contour_ring_on_surface(axes, (1.25, 0.0), 0.95, like_charges, "#2563eb", 2.6),
        )
        like_points = VGroup(
            Sphere(radius=0.08, resolution=(10, 5)).set_color(POSITIVE).move_to(axes.c2p(-1.25, 0, 1.78)),
            Sphere(radius=0.08, resolution=(10, 5)).set_color(POSITIVE).move_to(axes.c2p(1.25, 0, 1.78)),
        )
        label_like = cn("等量同种点电荷：两个高电势区域", 23, INK, "BOLD").to_edge(DOWN, buff=0.55)
        self.add_fixed_in_frame_mobjects(label_like)
        self.play(FadeIn(grid), FadeIn(label_like, shift=UP), run_time=0.6)
        self.play(FadeIn(like_surface), FadeIn(like_contours), FadeIn(like_points), run_time=1.3)
        self.move_camera(phi=60 * DEGREES, theta=-30 * DEGREES, zoom=0.98, run_time=1.0)
        self.wait(0.7)

        dipole_charges = [(1, -1.25, 0.0), (-1, 1.25, 0.0)]
        dipole_surface = potential_surface(axes, dipole_charges)
        dipole_zero = Line3D(axes.c2p(0, -2.0, 0.04), axes.c2p(0, 2.0, 0.04), thickness=0.018, color=EQUIP)
        dipole_contours = VGroup(
            contour_ring_on_surface(axes, (-1.25, 0.0), 0.55, dipole_charges, "#ef4444"),
            contour_ring_on_surface(axes, (1.25, 0.0), 0.55, dipole_charges, "#2563eb"),
            dipole_zero,
        )
        dipole_points = VGroup(
            Sphere(radius=0.08, resolution=(10, 5)).set_color(POSITIVE).move_to(axes.c2p(-1.25, 0, 1.70)),
            Sphere(radius=0.08, resolution=(10, 5)).set_color(NEGATIVE).move_to(axes.c2p(1.25, 0, -1.45)),
        )
        label_dipole = cn("等量异种点电荷：高电势与低电势相对分布", 23, INK, "BOLD").to_edge(DOWN, buff=0.55)
        self.add_fixed_in_frame_mobjects(label_dipole)
        self.play(
            FadeOut(like_surface),
            FadeOut(like_contours),
            FadeOut(like_points),
            FadeOut(label_like),
            FadeIn(dipole_surface),
            FadeIn(dipole_contours),
            FadeIn(dipole_points),
            FadeIn(label_dipole, shift=UP),
            run_time=1.2,
        )
        self.move_camera(phi=60 * DEGREES, theta=-42 * DEGREES, zoom=0.98, run_time=1.0)
        self.wait(1.4)


if __name__ == "__main__":
    # manim -pql electric_potential_equipotential.py ElectricPotentialEquipotentialScene
    # manim -pql electric_potential_equipotential.py ElectricPotential3DSurfaceScene
    pass
