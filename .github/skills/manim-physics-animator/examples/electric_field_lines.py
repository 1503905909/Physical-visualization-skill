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


def card(width, height, label):
    box = RoundedRectangle(width=width, height=height, corner_radius=0.18)
    box.set_fill(PANEL, opacity=1)
    box.set_stroke(LINE, width=2)
    tag = cn(label, 24, INK, "BOLD").next_to(box, UP, buff=0.18)
    return VGroup(box, tag)


def charge(value, label="Q", radius=0.34):
    color = POSITIVE if value > 0 else NEGATIVE
    c = Circle(radius=radius, stroke_color="#ffffff", stroke_width=2)
    c.set_fill(color, opacity=1)
    sign = "+" if value > 0 else "-"
    sign_text = cn(sign, 31, "#ffffff", "BOLD").move_to(c.get_center() + UP * 0.03)
    label_text = cn(label, 18, "#ffffff", "BOLD").move_to(c.get_center() + DOWN * 0.16)
    return VGroup(c, sign_text, label_text)


def short_arrow(start, end, color=FIELD, width=3):
    return Arrow(start, end, buff=0, stroke_width=width, color=color, max_tip_length_to_length_ratio=0.45)


def curve(points, color=FIELD, width=3):
    if len(points) < 2:
        return VMobject()
    vm = VMobject(color=color, stroke_width=width)
    vm.set_points_smoothly([np.array(p) for p in points])
    return vm


def arrow_on(points, color=FIELD, ratio=0.58):
    if len(points) < 8:
        return VGroup()
    i = min(len(points) - 7, max(6, int(len(points) * ratio)))
    return short_arrow(points[i - 5], points[i + 5], color=color, width=4.2)


def radial_lines(center, sign=1, count=16, inner=0.44, outer=1.95):
    group = VGroup()
    for i in range(count):
        a = TAU * i / count
        direction = np.array([np.cos(a), np.sin(a), 0])
        if sign > 0:
            start = center + direction * inner
            end = center + direction * outer
        else:
            start = center + direction * outer
            end = center + direction * inner
        group.add(short_arrow(start, end, width=2.8))
    return group


def bezier_points(p0, p1, p2, p3, samples=56):
    result = []
    for i in range(samples + 1):
        t = i / samples
        u = 1 - t
        result.append((u ** 3) * p0 + 3 * (u ** 2) * t * p1 + 3 * u * (t ** 2) * p2 + (t ** 3) * p3)
    return result


def electric_field(point, charges):
    field = np.array([0.0, 0.0, 0.0])
    for q, source in charges:
        r = point - source
        r2 = float(np.dot(r[:2], r[:2])) + 0.018
        field += q * r / (r2 * np.sqrt(r2))
    return field


def in_bounds(point, bounds):
    xmin, xmax, ymin, ymax = bounds
    return xmin <= point[0] <= xmax and ymin <= point[1] <= ymax


def trace_field_line(seed, charges, bounds, step=0.035, max_steps=520, stop_at_negative=True):
    points = [np.array(seed, dtype=float)]
    point = np.array(seed, dtype=float)
    for _ in range(max_steps):
        field = electric_field(point, charges)
        norm = np.linalg.norm(field)
        if norm < 0.006:
            break
        point = point + field / norm * step
        points.append(np.array(point))

        if not in_bounds(point, bounds):
            break
        if stop_at_negative:
            for q, source in charges:
                if q < 0 and np.linalg.norm(point - source) < 0.42:
                    return points
    return points


def field_line_group(seeds, charges, bounds, arrow_ratio=0.58, stop_at_negative=True):
    lines = VGroup()
    arrows = VGroup()
    for seed in seeds:
        points = trace_field_line(seed, charges, bounds, stop_at_negative=stop_at_negative)
        if len(points) < 8:
            continue
        lines.add(curve(points))
        arrows.add(arrow_on(points, ratio=arrow_ratio))
    return VGroup(lines, arrows)


def dipole_field_lines(pos, neg):
    center = (pos + neg) / 2
    bounds = (center[0] - 2.55, center[0] + 2.55, center[1] - 1.72, center[1] + 1.72)
    charges = [(1, pos), (-1, neg)]
    angles = np.deg2rad([-70, -52, -34, -16, 0, 16, 34, 52, 70])
    seeds = [pos + np.array([np.cos(a), np.sin(a), 0]) * 0.43 for a in angles]
    return field_line_group(seeds, charges, bounds, arrow_ratio=0.62, stop_at_negative=True)


def like_charge_lines(left, right):
    center = (left + right) / 2
    bounds = (center[0] - 2.55, center[0] + 2.55, center[1] - 1.72, center[1] + 1.72)
    charges = [(1, left), (1, right)]
    left_angles = np.deg2rad([118, 150, 190, 242, 66, -66])
    right_angles = np.deg2rad([62, 30, -30, -62, 114, -114])
    seeds = [left + np.array([np.cos(a), np.sin(a), 0]) * 0.43 for a in left_angles]
    seeds += [right + np.array([np.cos(a), np.sin(a), 0]) * 0.43 for a in right_angles]
    return field_line_group(seeds, charges, bounds, arrow_ratio=0.55, stop_at_negative=False)


class ElectricFieldLinesScene(Scene):
    """点电荷与两点电荷电场线方向。"""

    def construct(self):
        self.compare_single_charges()
        self.test_charge_direction()
        self.compare_two_charges()
        self.wrap_up()

    def compare_single_charges(self):
        header = title("点电荷电场线", "箭头方向表示正试探电荷在该点的受力方向")
        self.play(FadeIn(header, shift=DOWN), run_time=0.8)

        left = card(5.6, 4.25, "正点电荷：向外发散").shift(LEFT * 3.05 + DOWN * 0.25)
        right = card(5.6, 4.25, "负点电荷：由外指向电荷").shift(RIGHT * 3.05 + DOWN * 0.25)
        q1 = charge(1).move_to(left[0].get_center())
        q2 = charge(-1).move_to(right[0].get_center())
        l1 = radial_lines(q1.get_center(), sign=1, count=16, outer=1.65)
        l2 = radial_lines(q2.get_center(), sign=-1, count=16, outer=1.65)

        self.play(FadeIn(left), FadeIn(right), run_time=0.7)
        self.play(FadeIn(q1, scale=0.75), FadeIn(q2, scale=0.75), run_time=0.6)
        self.play(
            LaggedStart(*[Create(line) for line in l1], lag_ratio=0.035),
            LaggedStart(*[Create(line) for line in l2], lag_ratio=0.035),
            run_time=1.7,
        )
        note = cn("同一电场中，电场线不相交；疏密反映场强大小。", 25, ACCENT, "BOLD").to_edge(DOWN, buff=0.48)
        self.play(FadeIn(note, shift=UP), run_time=0.6)
        self.wait(0.8)
        self.play(FadeOut(VGroup(header, left, right, q1, q2, l1, l2, note)), run_time=0.8)

    def test_charge_direction(self):
        header = title("为什么用正试探电荷规定方向？")
        self.play(FadeIn(header, shift=DOWN), run_time=0.6)

        source = charge(1, "Q", 0.42).shift(LEFT * 2.5 + DOWN * 0.15)
        lines = radial_lines(source.get_center(), 1, 14, outer=2.25)
        probe = charge(1, "q", 0.22).move_to(source.get_center() + RIGHT * 2.25 + UP * 0.75)
        field_vec = short_arrow(probe.get_center(), probe.get_center() + RIGHT * 1.35 + UP * 0.42, FIELD, 5)
        tangent = DashedLine(probe.get_center() + LEFT * 0.8 + DOWN * 0.25, probe.get_center() + RIGHT * 1.0 + UP * 0.32, color=ACCENT, stroke_width=3)

        labels = VGroup(
            cn("电场线某点的切线方向", 27, INK, "BOLD"),
            cn("就是该点电场强度 E 的方向", 27, FIELD, "BOLD"),
            cn("也就是正试探电荷受力方向", 24, MUTED),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).to_edge(RIGHT, buff=0.85).shift(DOWN * 0.35)

        self.play(FadeIn(source), LaggedStart(*[Create(line) for line in lines], lag_ratio=0.03), run_time=1.5)
        self.play(FadeIn(probe, scale=0.7), Create(tangent), run_time=0.7)
        self.play(Create(field_vec), FadeIn(labels, shift=LEFT), run_time=0.8)
        self.wait(0.9)
        self.play(FadeOut(VGroup(header, source, lines, probe, field_vec, tangent, labels)), run_time=0.8)

    def compare_two_charges(self):
        header = title("两点电荷电场线比较", "等量异种从正到负；等量同种向外分开，不相交")
        self.play(FadeIn(header, shift=DOWN), run_time=0.6)

        left_card = card(6.0, 4.4, "等量异种点电荷").shift(LEFT * 3.15 + DOWN * 0.28)
        right_card = card(6.0, 4.4, "等量同种点电荷").shift(RIGHT * 3.15 + DOWN * 0.28)
        self.play(FadeIn(left_card), FadeIn(right_card), run_time=0.6)

        dip_pos = left_card[0].get_center() + LEFT * 1.15
        dip_neg = left_card[0].get_center() + RIGHT * 1.15
        same_l = right_card[0].get_center() + LEFT * 1.05
        same_r = right_card[0].get_center() + RIGHT * 1.05
        charges = VGroup(
            charge(1).move_to(dip_pos),
            charge(-1).move_to(dip_neg),
            charge(1).move_to(same_l),
            charge(1).move_to(same_r),
        )
        dip = dipole_field_lines(dip_pos, dip_neg)
        same = like_charge_lines(same_l, same_r)
        note1 = cn("场线从正电荷出发，终止于负电荷", 21, FIELD, "BOLD").next_to(left_card[0], DOWN, buff=0.2)
        note2 = cn("两电荷之间场线分开，不能相交", 21, FIELD, "BOLD").next_to(right_card[0], DOWN, buff=0.2)

        self.play(FadeIn(charges, scale=0.8), run_time=0.6)
        self.play(
            Create(dip[0]),
            Create(same[0]),
            FadeIn(dip[1]),
            FadeIn(same[1]),
            run_time=1.9,
        )
        self.play(FadeIn(note1), FadeIn(note2), run_time=0.6)
        self.wait(1.0)
        self.play(FadeOut(VGroup(header, left_card, right_card, charges, dip, same, note1, note2)), run_time=0.8)

    def wrap_up(self):
        header = cn("课堂归纳", 38, INK, "BOLD").to_edge(UP, buff=0.7)
        items = VGroup(
            cn("1  正电荷向外，负电荷向内。", 29, INK),
            cn("2  电场线方向就是电场强度方向。", 29, INK),
            cn("3  疏密表示场强大小，电场线不相交。", 29, INK),
            cn("4  典型图像要和受力方向、场强方向一起理解。", 29, FIELD, "BOLD"),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.30).move_to(ORIGIN + DOWN * 0.1)
        panel = RoundedRectangle(width=9.8, height=3.7, corner_radius=0.22, stroke_color=LINE, stroke_width=2, fill_color=PANEL, fill_opacity=1)
        panel.move_to(items)
        self.play(FadeIn(header, shift=DOWN), FadeIn(panel, scale=0.98), run_time=0.7)
        for item in items:
            self.play(FadeIn(item, shift=RIGHT), run_time=0.35)
        self.wait(1.1)
        self.play(FadeOut(VGroup(header, panel, items)), run_time=0.8)



def sphere_directions():
    directions = []
    for z, count, offset in [(-0.62, 4, 18), (0.0, 8, 0), (0.62, 4, 45)]:
        radius = np.sqrt(max(0.0, 1 - z * z))
        for i in range(count):
            angle = TAU * i / count + np.deg2rad(offset)
            directions.append(np.array([radius * np.cos(angle), radius * np.sin(angle), z]))
    directions.append(np.array([0.0, 0.0, 1.0]))
    directions.append(np.array([0.0, 0.0, -1.0]))
    return directions


def radial_lines_3d(inner=0.48, outer=2.28, sign=1):
    lines = VGroup()
    for direction in sphere_directions():
        start = direction * inner if sign > 0 else direction * outer
        end = direction * outer if sign > 0 else direction * inner
        lines.add(Line3D(start=start, end=end, thickness=0.010, color=FIELD, resolution=4))
    return lines


class ElectricFieldLines2D3DScene(ThreeDScene):
    """点电荷电场线：由教材二维图示过渡到三维空间分布。"""

    def construct(self):
        self.set_camera_orientation(phi=0 * DEGREES, theta=-90 * DEGREES, zoom=0.88)
        header = title("点电荷电场线：由二维图示到三维图示", "教材平面图可看作空间电场分布的一个截面")
        self.add_fixed_in_frame_mobjects(header)
        self.play(FadeIn(header, shift=DOWN), run_time=0.7)

        source = charge(1, "Q", 0.30).move_to(ORIGIN)
        flat_lines = radial_lines(ORIGIN, sign=1, count=16, inner=0.43, outer=2.12)
        step1 = cn("第一步：观察教材中的平面电场线", 25, INK, "BOLD").to_edge(DOWN, buff=0.55)
        self.add_fixed_in_frame_mobjects(step1)

        self.play(FadeIn(source, scale=0.85), run_time=0.35)
        self.play(LaggedStart(*[Create(line) for line in flat_lines], lag_ratio=0.025), run_time=1.35)
        self.play(FadeIn(step1, shift=UP), run_time=0.4)
        self.wait(0.55)

        plane = Square(side_length=4.95, stroke_color="#94a3b8", stroke_width=1.2)
        plane.set_fill("#dbeafe", opacity=0.14)
        step2 = cn("第二步：把平面图理解为空间分布的一个截面", 25, ACCENT, "BOLD").to_edge(DOWN, buff=0.55)
        self.add_fixed_in_frame_mobjects(step2)
        self.play(FadeOut(step1), FadeIn(plane), FadeIn(step2, shift=UP), run_time=0.55)

        self.move_camera(phi=62 * DEGREES, theta=-43 * DEGREES, zoom=0.88, run_time=1.5)

        sphere = Sphere(radius=0.27, resolution=(18, 9))
        sphere.set_color(POSITIVE)
        sphere.set_opacity(0.96)
        sphere.set_shade_in_3d(True)

        spatial_lines = radial_lines_3d(sign=1)

        step3 = cn("第三步：正点电荷电场线向空间各方向发散", 24, INK, "BOLD").to_edge(DOWN, buff=0.55)
        self.add_fixed_in_frame_mobjects(step3)
        self.play(
            FadeOut(source),
            flat_lines.animate.set_opacity(0.18),
            FadeIn(sphere, scale=0.9),
            FadeIn(spatial_lines),
            FadeOut(step2),
            FadeIn(step3, shift=UP),
            run_time=1.35,
        )
        self.move_camera(phi=68 * DEGREES, theta=-18 * DEGREES, zoom=0.86, run_time=1.0)
        self.wait(0.8)
        self.play(FadeOut(step3), run_time=0.3)

        conclusion = VGroup(
            cn("正点电荷：电场线向外发散", 24, FIELD, "BOLD"),
            cn("平面电场线图只是空间模型的一个观察截面", 21, MUTED),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).to_corner(DR, buff=0.55)
        self.add_fixed_in_frame_mobjects(conclusion)
        self.play(FadeIn(conclusion, shift=LEFT), run_time=0.65)
        self.wait(1.0)


if __name__ == "__main__":
    # manim -pql electric_field_lines.py ElectricFieldLinesScene
    # manim -pql electric_field_lines.py ElectricFieldLines2D3DScene
    pass
