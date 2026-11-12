"""洛伦兹力与带电粒子在匀强磁场中的运动（人教版选择性必修第二册 第一章 1.1~1.3）。

分镜：
    1. 安培力的微观图像：大量定向移动电荷的洛伦兹力如何合成 F = BIL
    2. 单个电荷的洛伦兹力方向：左手定则，正负电荷对比
    3. 匀速圆周运动：r = mv/(qB)，改变 B 观察半径同步变化
    4. 周期与速率无关：T = 2πm/(qB)

渲染：
    manim -pql lorentz_force.py LorentzForceScene     # 快速预览
    manim -pqh lorentz_force.py LorentzForceScene     # 高清输出
"""

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
VEL = "#15803d"
FORCE = "#d97706"
POS = "#d64545"
NEG = "#3558ff"
ACCENT = "#6d28d9"


def cn(text, size=30, color=INK, weight="NORMAL"):
    return Text(text, font=FONT, font_size=size, color=color, weight=weight)


def title(text, subtitle=None):
    top = cn(text, 34, INK, "BOLD").to_edge(UP, buff=0.26)
    bar = Line(LEFT * 6.45, RIGHT * 6.45, color=LINE, stroke_width=2).next_to(top, DOWN, buff=0.14)
    group = VGroup(top, bar)
    if subtitle:
        sub = cn(subtitle, 21, MUTED).next_to(bar, DOWN, buff=0.12)
        group.add(sub)
    return group


def arrow(start, end, color=FORCE, width=3.5):
    return Arrow(
        start,
        end,
        buff=0,
        stroke_width=width,
        color=color,
        max_tip_length_to_length_ratio=0.28,
    )


def charge(sign=1, radius=0.17):
    color = POS if sign > 0 else NEG
    body = Circle(radius=radius, stroke_color="#ffffff", stroke_width=2.5, fill_color=color, fill_opacity=1)
    mark = cn("+" if sign > 0 else "−", int(radius * 96) + 6, "#ffffff", "BOLD").move_to(body)
    return VGroup(body, mark)


def b_field_symbols(width=12.4, height=6.2, spacing=1.15, into=True, color="#9aa7b8"):
    """匀强磁场符号：垂直纸面向里用 ×，向外用 ·。"""
    marks = VGroup()
    cols = int(width / spacing) + 1
    rows = int(height / spacing) + 1
    for i in range(cols):
        for j in range(rows):
            x = -width / 2 + i * spacing
            y = -height / 2 + j * spacing
            if into:
                cross = VGroup(
                    Line([-0.07, -0.07, 0], [0.07, 0.07, 0], color=color, stroke_width=1.6),
                    Line([-0.07, 0.07, 0], [0.07, -0.07, 0], color=color, stroke_width=1.6),
                )
                cross.move_to(np.array([x, y, 0]))
                marks.add(cross)
            else:
                ring = Circle(radius=0.075, color=color, stroke_width=1.5).move_to(np.array([x, y, 0]))
                dot = Dot(np.array([x, y, 0]), radius=0.022, color=color)
                marks.add(VGroup(ring, dot))
    return marks


class LorentzForceScene(Scene):
    """安培力、洛伦兹力与带电粒子在匀强磁场中的圆周运动。"""

    def construct(self):
        self.microscopic_ampere_force()
        self.single_charge_direction()
        self.circular_motion()
        self.period_independent_of_speed()
        self.summary()

    # ---------------------------------------------------------------- 分镜 1
    def microscopic_ampere_force(self):
        header = title("安培力与洛伦兹力", "通电导线受到的安培力，是导线中大量定向移动电荷所受洛伦兹力的合力")
        self.play(FadeIn(header, shift=DOWN), run_time=0.7)

        marks = b_field_symbols().shift(DOWN * 0.3)
        self.play(FadeIn(marks), run_time=0.9)

        wire = RoundedRectangle(
            width=7.6,
            height=1.0,
            corner_radius=0.10,
            stroke_color="#94a3b8",
            stroke_width=2,
            fill_color="#e2e8f0",
            fill_opacity=1,
        ).move_to(np.array([-2.1, -0.6, 0]))
        self.play(Create(wire), run_time=0.7)

        current = arrow(np.array([-5.6, -1.42, 0]), np.array([1.3, -1.42, 0]), FIELD, 3.5)
        current_label = cn("I  （正电荷定向移动方向）", 22, FIELD).next_to(current, DOWN, buff=0.10)
        self.play(GrowArrow(current), FadeIn(current_label), run_time=0.7)

        s = ValueTracker(0.0)
        s.add_updater(lambda m, dt: m.increment_value(dt * 0.16))
        self.add(s)

        def charge_x(k):
            return -5.6 + ((s.get_value() + k / 6.0) % 1.0) * 7.2

        charges = VGroup()
        for i in range(6):
            body = charge(1, 0.135).move_to(np.array([charge_x(i), -0.6, 0]))

            def upd(m, dt, k=i):
                m.move_to(np.array([charge_x(k), -0.6, 0]))

            body.add_updater(upd)
            charges.add(body)
        self.play(FadeIn(charges), run_time=0.8)

        def mini_force(k):
            x = charge_x(k)
            return arrow(np.array([x, -0.22, 0]), np.array([x, 0.40, 0]), FORCE, 3)

        mini_arrows = VGroup()
        for i in range(6):
            shaft = always_redraw(lambda k=i: mini_force(k))
            mini_arrows.add(shaft)
            self.add(shaft)

        each = VGroup(
            MathTex("f=qvB", font_size=40, color=FORCE),
            cn("每个定向移动电荷受到的洛伦兹力", 21, MUTED),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.14)
        each.move_to(np.array([4.55, 1.60, 0]))
        self.play(FadeIn(each, shift=LEFT), run_time=0.8)
        self.wait(1.2)

        big_force = arrow(np.array([-2.1, 0.02, 0]), np.array([-2.1, 1.55, 0]), FORCE, 5)
        big_label = cn("F安 = BIL", 32, FORCE, "BOLD").next_to(big_force, LEFT, buff=0.20)
        summ = VGroup(
            cn("F安 = NqvB = BIL", 36, ACCENT, "BOLD"),
            cn("N 个电荷受力方向相同，合力就是安培力", 21, MUTED),
            cn("I = nqvS，N = nSL  ->  NqvB = BIL", 20, MUTED),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
        summ.move_to(np.array([4.5, -0.85, 0]))

        self.play(GrowArrow(big_force), FadeIn(big_label), run_time=0.8)
        self.play(FadeIn(summ, shift=LEFT), run_time=0.9)
        self.wait(1.5)

        self.remove(*mini_arrows)
        self.play(
            FadeOut(VGroup(header, marks, wire, current, current_label, charges, each, summ, big_force, big_label)),
            run_time=0.8,
        )
        self.remove(s)

    # ---------------------------------------------------------------- 分镜 2
    def single_charge_direction(self):
        header = title("单个电荷的洛伦兹力方向", "左手定则：磁感线垂直穿入掌心，四指指向正电荷运动方向，拇指指向 F")
        self.play(FadeIn(header, shift=DOWN), run_time=0.6)

        marks = b_field_symbols().shift(DOWN * 0.25)
        self.play(FadeIn(marks), run_time=0.8)

        origin = np.array([-2.5, -0.55, 0])
        dot = charge(1).move_to(origin)
        v_arrow = arrow(origin, origin + RIGHT * 2.1, VEL, 4)
        v_label = MathTex("v", font_size=40, color=VEL).next_to(v_arrow.get_end(), RIGHT, buff=0.12)
        f_arrow = arrow(origin, origin + UP * 1.65, FORCE, 4)
        f_label = MathTex("F", font_size=40, color=FORCE).next_to(f_arrow.get_end(), UP, buff=0.10)
        field_note = cn("B 垂直纸面向里 ×", 24, FIELD, "BOLD").move_to(np.array([-2.5, 1.90, 0]))

        self.play(FadeIn(dot), FadeIn(field_note), run_time=0.5)
        self.play(GrowArrow(v_arrow), FadeIn(v_label), run_time=0.7)
        self.play(GrowArrow(f_arrow), FadeIn(f_label), run_time=0.8)

        rule = VGroup(
            cn("左手定则", 26, INK, "BOLD"),
            cn("① 让磁感线垂直穿入掌心", 22, MUTED),
            cn("② 四指指向正电荷运动方向", 22, MUTED),
            cn("③ 拇指所指就是洛伦兹力方向", 22, MUTED),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.16)
        rule.move_to(np.array([4.5, 1.40, 0]))
        self.play(FadeIn(rule, shift=LEFT), run_time=0.9)
        self.wait(1.0)

        neg_dot = charge(-1).move_to(origin)
        self.play(
            Rotate(f_arrow, PI, about_point=origin),
            f_label.animate.move_to(np.array([origin[0], origin[1] - 2.05, 0])),
            FadeOut(dot),
            FadeIn(neg_dot),
            run_time=1.1,
        )
        neg_note = cn("负电荷：洛伦兹力方向与正电荷相反", 24, NEG, "BOLD").move_to(np.array([4.5, -0.85, 0]))
        self.play(FadeIn(neg_note, shift=LEFT), run_time=0.7)

        formula = MathTex(r"F=qvB\sin\theta", r"\quad\Rightarrow\quad", r"F=qvB\ (\theta=90^\circ)", font_size=38, color=INK)
        formula.move_to(np.array([4.5, -2.0, 0]))
        self.play(Write(formula), run_time=1.0)
        self.wait(1.2)

        self.play(
            FadeOut(VGroup(header, marks, neg_dot, v_arrow, v_label, f_arrow, f_label, field_note, rule, neg_note, formula)),
            run_time=0.8,
        )

    # ---------------------------------------------------------------- 分镜 3
    def circular_motion(self):
        header = title("粒子为什么做圆周运动？", "洛伦兹力始终垂直于速度：只改变方向，不改变大小")
        self.play(FadeIn(header, shift=DOWN), run_time=0.6)

        marks = b_field_symbols(width=9.6, height=5.6).shift(LEFT * 2.2 + DOWN * 0.25)
        self.play(FadeIn(marks), run_time=0.8)

        center = np.array([-2.2, -0.35, 0])
        r0 = 1.40
        b0 = 100.0                      # 参考磁感应强度 / mT
        b_track = ValueTracker(1.0)     # B / B0
        ang = ValueTracker(0.0)
        ang.add_updater(lambda m, dt: m.increment_value(dt * 1.35))
        self.add(b_track, ang)

        def radius():
            return r0 / b_track.get_value()

        def theta():
            return -PI / 2 + ang.get_value()

        def pos():
            th = theta()
            return center + np.array([radius() * np.cos(th), radius() * np.sin(th), 0])

        def v_dir():
            th = theta()
            return np.array([-np.sin(th), np.cos(th), 0])

        def f_dir():
            th = theta()
            return np.array([-np.cos(th), -np.sin(th), 0])

        orbit = always_redraw(lambda: Circle(radius=radius(), color=VEL, stroke_width=3).move_to(center))
        radius_line = always_redraw(
            lambda: DashedLine(center, pos(), dash_length=0.10, color=LINE, stroke_width=2)
        )
        center_dot = Dot(center, radius=0.05, color=INK)
        center_label = MathTex("O", font_size=30, color=INK).next_to(center_dot, UR, buff=0.06)

        dot = charge(1).move_to(pos())
        dot.add_updater(lambda m: m.move_to(pos()))
        v_arrow = always_redraw(lambda: arrow(pos(), pos() + v_dir() * 0.80, VEL, 4))
        f_arrow = always_redraw(lambda: arrow(pos(), pos() + f_dir() * 0.60, FORCE, 4))

        self.add(orbit, radius_line)
        self.play(FadeIn(center_dot), FadeIn(center_label), run_time=0.5)
        self.add(dot, v_arrow, f_arrow)
        self.wait(1.0)

        formula = MathTex(r"qvB=\frac{mv^{2}}{r}", font_size=46, color=INK).move_to(np.array([4.55, 2.10, 0]))
        self.play(Write(formula), run_time=0.9)

        b_row = VGroup(
            cn("B =", 26, MUTED),
            DecimalNumber(100, num_decimal_places=0, color=FIELD).scale(0.62),
            cn("mT", 24, MUTED),
        ).arrange(RIGHT, buff=0.16).move_to(np.array([4.55, 1.10, 0]))
        r_row = VGroup(
            cn("r =", 26, MUTED),
            DecimalNumber(10.4, num_decimal_places=1, color=ACCENT).scale(0.62),
            cn("cm", 24, MUTED),
        ).arrange(RIGHT, buff=0.16).move_to(np.array([4.55, 0.50, 0]))
        b_num = b_row[1]
        r_num = r_row[1]
        b_num.add_updater(lambda m: m.set_value(b0 * b_track.get_value()))
        r_num.add_updater(lambda m: m.set_value(10.44 / b_track.get_value()))
        self.play(FadeIn(b_row), FadeIn(r_row), run_time=0.7)

        hint = cn("增大 B，半径 r 同步变小", 24, FIELD, "BOLD").move_to(np.array([4.55, -0.55, 0]))
        self.play(FadeIn(hint, shift=LEFT), run_time=0.6)

        self.play(b_track.animate.set_value(2.05), run_time=3.4, rate_func=smooth)
        self.wait(0.6)
        self.play(b_track.animate.set_value(0.72), run_time=3.0, rate_func=smooth)
        self.wait(0.4)

        result = MathTex(r"r=\frac{mv}{qB}", font_size=50, color=ACCENT).move_to(np.array([4.55, -1.55, 0]))
        self.play(FadeOut(formula, shift=UP * 0.2), FadeIn(result, shift=UP * 0.2), run_time=1.0)
        self.wait(0.9)

        self.remove(orbit, radius_line, v_arrow, f_arrow)
        dot.clear_updaters()
        self.play(
            FadeOut(VGroup(header, marks, center_dot, center_label, dot, b_row, r_row, hint, result)),
            run_time=0.8,
        )
        self.remove(b_track, ang)

    # ---------------------------------------------------------------- 分镜 4
    def period_independent_of_speed(self):
        header = title("半径不同，周期相同", "同一粒子在同一磁场中：T 与速率、半径都无关")
        self.play(FadeIn(header, shift=DOWN), run_time=0.6)

        center = np.array([-2.8, -0.35, 0])
        radii = [0.78, 1.28, 1.78]
        colors = [VEL, FIELD, ACCENT]
        speed_labels = ["v", "2v", "3v"]

        ang = ValueTracker(0.0)
        self.add(ang)

        circles = VGroup()
        labels = VGroup()
        dots = VGroup()
        for r, c, lab in zip(radii, colors, speed_labels):
            circles.add(Circle(radius=r, color=c, stroke_width=3, stroke_opacity=0.55).move_to(center))
            labels.add(cn(lab, 24, c, "BOLD").move_to(center + np.array([r + 0.36, 0.0, 0])))
            d = VGroup(Circle(radius=0.13, fill_color=c, fill_opacity=1, stroke_color="#ffffff", stroke_width=2))

            def upd(m, dt, rr=r):
                th = -PI / 2 + ang.get_value()
                m.move_to(center + np.array([rr * np.cos(th), rr * np.sin(th), 0]))

            d.add_updater(upd)
            dots.add(d)

        start_line = DashedLine(
            center + np.array([0, -1.95, 0]),
            center + np.array([0, 0.10, 0]),
            dash_length=0.08,
            color=LINE,
            stroke_width=2,
        )
        self.play(Create(circles), FadeIn(labels), FadeIn(start_line), run_time=1.0)
        self.play(FadeIn(dots), run_time=0.5)
        self.wait(0.4)

        self.play(ang.animate.set_value(TAU), run_time=3.6, rate_func=linear)
        self.wait(0.2)

        arrive = cn("同时回到出发点：周期相同", 25, ACCENT, "BOLD").move_to(np.array([2.9, -2.45, 0]))
        self.play(Indicate(dots, color=ACCENT), FadeIn(arrive, shift=LEFT), run_time=1.0)

        formula = MathTex(r"T=\frac{2\pi m}{qB}", font_size=54, color=INK)
        explain = VGroup(
            cn("T 只由 m、q、B 决定", 24, MUTED),
            cn("与速率 v、半径 r 无关", 24, MUTED),
            cn("回旋加速器可用固定频率加速", 21, FIELD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.16)
        panel = VGroup(formula, explain).arrange(DOWN, aligned_edge=LEFT, buff=0.32)
        panel.move_to(np.array([4.35, -0.30, 0]))
        self.play(Write(formula), FadeIn(explain, shift=LEFT), run_time=1.1)
        self.wait(1.3)

        self.play(
            FadeOut(VGroup(header, circles, labels, dots, start_line, arrive, formula, explain)),
            run_time=0.8,
        )
        self.remove(ang)

    # ---------------------------------------------------------------- 分镜 5
    def summary(self):
        head = cn("课堂归纳", 40, INK, "BOLD").to_edge(UP, buff=0.62)
        items = VGroup(
            cn("1  运动电荷受洛伦兹力 F = qvB sinθ，方向由左手定则判断。", 25, INK),
            cn("2  洛伦兹力始终垂直于速度，不做功：只改变方向，不改变速率。", 25, INK),
            cn("3  v 垂直于 B 时做匀速圆周运动：r = mv/(qB)，T = 2πm/(qB)。", 25, ACCENT, "BOLD"),
            cn("4  宏观的安培力 F = BIL，是大量电荷所受洛伦兹力的合力。", 25, INK),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.36)
        items.move_to(np.array([0, 0.30, 0]))

        footer = cn("模型假设：匀强磁场、忽略重力、非相对论（v 远小于 c）", 21, MUTED).to_edge(DOWN, buff=0.55)

        frame = RoundedRectangle(
            width=12.2,
            height=3.45,
            corner_radius=0.22,
            stroke_color=LINE,
            stroke_width=2,
            fill_color=PANEL,
            fill_opacity=1,
        ).move_to(items)

        self.play(FadeIn(head, shift=DOWN), FadeIn(frame), run_time=0.7)
        for item in items:
            self.play(FadeIn(item, shift=RIGHT), run_time=0.45)
        self.play(FadeIn(footer), run_time=0.6)
        self.wait(1.8)

        self.play(FadeOut(VGroup(head, frame, items, footer)), run_time=0.8)


if __name__ == "__main__":
    # manim -pql lorentz_force.py LorentzForceScene
    pass
