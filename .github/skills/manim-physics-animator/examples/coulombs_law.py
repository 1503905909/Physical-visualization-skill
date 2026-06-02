import numpy as np
from manim import *


config.frame_width = 14.222
config.frame_height = 8.0
config.pixel_width = 1280
config.pixel_height = 720
config.background_color = "#0b1020"
config.media_dir = r"d:\PycharmProjects1\Physical-visualization-skill\build\videos\manim"


FONT = "Microsoft YaHei"
POSITIVE = "#ff4d4f"
NEGATIVE = "#4f6dff"
FORCE = "#ffd166"
DISTANCE = "#33d17a"
PANEL = "#111827"


def cn(text, font_size=30, color=WHITE, weight="NORMAL"):
    return Text(text, font=FONT, font_size=font_size, color=color, weight=weight)


def charge_mobject(value, label, radius=0.45):
    color = POSITIVE if value >= 0 else NEGATIVE
    circle = Circle(radius=radius, stroke_color=WHITE, stroke_width=2)
    circle.set_fill(color, opacity=0.95)
    sign = "+" if value > 0 else "-" if value < 0 else "0"
    sign_text = cn(sign, font_size=36, weight="BOLD").move_to(circle.get_center() + UP * 0.12)
    label_text = MathTex(label, font_size=34, color=WHITE).move_to(circle.get_center() + DOWN * 0.18)
    return VGroup(circle, sign_text, label_text)


def force_arrow(start, direction, length=1.2, label=None, color=FORCE):
    arrow = Arrow(
        start=start,
        end=start + direction * length,
        buff=0,
        stroke_width=7,
        max_tip_length_to_length_ratio=0.22,
        color=color,
    )
    if label is None:
        return arrow
    text = MathTex(label, font_size=30, color=color).next_to(arrow, UP, buff=0.12)
    return VGroup(arrow, text)


class CoulombsLawScene(Scene):
    """高中物理：库仑定律课堂演示动画。"""

    def construct(self):
        self.opening_question()
        self.same_and_opposite_charges()
        self.distance_changes_force()
        self.inverse_square_graph()
        self.summary()

    def scene_title(self, text):
        title = cn(text, font_size=34, weight="BOLD")
        title.to_edge(UP, buff=0.28)
        line = Line(LEFT * 6.4, RIGHT * 6.4, color="#334155", stroke_width=2)
        line.next_to(title, DOWN, buff=0.18)
        return VGroup(title, line)

    def opening_question(self):
        title = cn("库仑定律：电荷之间的相互作用", font_size=42, weight="BOLD")
        title.to_edge(UP, buff=0.55)

        q1 = charge_mobject(1, "q_1").shift(LEFT * 2.2)
        q2 = charge_mobject(-1, "q_2").shift(RIGHT * 2.2)
        connector = DashedLine(q1.get_center(), q2.get_center(), color=GREY_B, stroke_width=3)
        distance = BraceBetweenPoints(q1.get_center(), q2.get_center(), DOWN, color=DISTANCE)
        distance_label = MathTex("r", font_size=36, color=DISTANCE).next_to(distance, DOWN, buff=0.15)

        question = cn("两个电荷之间的力由什么决定？", font_size=34, color=YELLOW, weight="BOLD")
        question.next_to(connector, DOWN, buff=1.2)

        formula = MathTex(
            r"F = k\frac{|q_1q_2|}{r^2}",
            font_size=50,
            color=WHITE,
        ).next_to(question, DOWN, buff=0.45)
        formula.set_color_by_tex("F", FORCE)
        formula.set_color_by_tex("q_1", POSITIVE)
        formula.set_color_by_tex("q_2", NEGATIVE)
        formula.set_color_by_tex("r", DISTANCE)

        self.play(FadeIn(title, shift=DOWN), run_time=0.8)
        self.play(FadeIn(q1, shift=LEFT), FadeIn(q2, shift=RIGHT), Create(connector), run_time=1.0)
        self.play(GrowFromCenter(distance), Write(distance_label), run_time=0.8)
        self.play(Write(question), run_time=0.9)
        self.play(Write(formula), run_time=1.0)
        self.wait(1.2)
        self.play(FadeOut(VGroup(title, q1, q2, connector, distance, distance_label, question, formula)))

    def same_and_opposite_charges(self):
        header = self.scene_title("一、力的方向：同号相斥，异号相吸")
        self.play(FadeIn(header))

        left_panel = RoundedRectangle(width=5.7, height=4.2, corner_radius=0.18)
        right_panel = RoundedRectangle(width=5.7, height=4.2, corner_radius=0.18)
        for panel in (left_panel, right_panel):
            panel.set_stroke("#475569", width=2)
            panel.set_fill(PANEL, opacity=0.55)
        left_panel.shift(LEFT * 3.05 + DOWN * 0.25)
        right_panel.shift(RIGHT * 3.05 + DOWN * 0.25)

        same_label = cn("同号电荷", font_size=28, weight="BOLD").next_to(left_panel, UP, buff=0.18)
        opposite_label = cn("异号电荷", font_size=28, weight="BOLD").next_to(right_panel, UP, buff=0.18)

        same_q1 = charge_mobject(1, "q_1").move_to(left_panel.get_center() + LEFT * 1.05)
        same_q2 = charge_mobject(1, "q_2").move_to(left_panel.get_center() + RIGHT * 1.05)
        opp_q1 = charge_mobject(1, "q_1").move_to(right_panel.get_center() + LEFT * 1.05)
        opp_q2 = charge_mobject(-1, "q_2").move_to(right_panel.get_center() + RIGHT * 1.05)

        same_line = Line(same_q1.get_center(), same_q2.get_center(), color=GREY_B, stroke_width=3)
        opp_line = Line(opp_q1.get_center(), opp_q2.get_center(), color=GREY_B, stroke_width=3)

        same_arrows = VGroup(
            force_arrow(same_q1.get_left() + LEFT * 0.05, LEFT, 1.05, r"\vec F_{12}"),
            force_arrow(same_q2.get_right() + RIGHT * 0.05, RIGHT, 1.05, r"\vec F_{21}"),
        )
        opp_arrows = VGroup(
            force_arrow(opp_q1.get_right() + RIGHT * 0.05, RIGHT, 1.05, r"\vec F_{12}"),
            force_arrow(opp_q2.get_left() + LEFT * 0.05, LEFT, 1.05, r"\vec F_{21}"),
        )
        same_conclusion = cn("排斥：受力方向相互远离", font_size=24, color=FORCE)
        same_conclusion.next_to(left_panel, DOWN, buff=0.24)
        opp_conclusion = cn("吸引：受力方向相互靠近", font_size=24, color=FORCE)
        opp_conclusion.next_to(right_panel, DOWN, buff=0.24)

        self.play(
            FadeIn(left_panel),
            FadeIn(right_panel),
            Write(same_label),
            Write(opposite_label),
            run_time=0.8,
        )
        self.play(
            FadeIn(VGroup(same_q1, same_q2, opp_q1, opp_q2)),
            Create(same_line),
            Create(opp_line),
            run_time=0.9,
        )
        self.play(Create(same_arrows), Write(same_conclusion), run_time=1.1)
        self.play(Create(opp_arrows), Write(opp_conclusion), run_time=1.1)
        self.wait(1.2)
        self.play(FadeOut(VGroup(header, left_panel, right_panel, same_label, opposite_label,
                                 same_q1, same_q2, opp_q1, opp_q2, same_line, opp_line,
                                 same_arrows, opp_arrows, same_conclusion, opp_conclusion)))

    def distance_changes_force(self):
        header = self.scene_title("二、力的大小：距离越大，静电力越小")
        self.play(FadeIn(header))

        q1_tracker = ValueTracker(-2.0)
        q2_tracker = ValueTracker(2.0)

        def q1_group():
            return charge_mobject(1, "q_1").move_to([q1_tracker.get_value(), 0.15, 0])

        def q2_group():
            return charge_mobject(-1, "q_2").move_to([q2_tracker.get_value(), 0.15, 0])

        q1 = always_redraw(q1_group)
        q2 = always_redraw(q2_group)

        line = always_redraw(lambda: Line(
            [q1_tracker.get_value(), 0.15, 0],
            [q2_tracker.get_value(), 0.15, 0],
            color=GREY_B,
            stroke_width=3,
        ))
        brace = always_redraw(lambda: BraceBetweenPoints(
            [q1_tracker.get_value(), 0.15, 0],
            [q2_tracker.get_value(), 0.15, 0],
            DOWN,
            color=DISTANCE,
        ))

        def distance_text():
            distance = q2_tracker.get_value() - q1_tracker.get_value()
            return MathTex(
                rf"r = {distance:.1f}\,\mathrm{{cm}}",
                font_size=32,
                color=DISTANCE,
            ).next_to(brace, DOWN, buff=0.15)

        r_label = always_redraw(distance_text)

        def force_text():
            distance = q2_tracker.get_value() - q1_tracker.get_value()
            relative_force = 16 / (distance ** 2)
            return MathTex(
                rf"F \propto \frac{{1}}{{r^2}} = {relative_force:.2f}",
                font_size=42,
                color=FORCE,
            ).to_edge(DOWN, buff=0.55)

        formula = always_redraw(force_text)

        def arrows():
            distance = q2_tracker.get_value() - q1_tracker.get_value()
            length = min(1.65, max(0.42, 2.5 / distance))
            left_start = np.array([q1_tracker.get_value() + 0.48, 1.05, 0.0])
            right_start = np.array([q2_tracker.get_value() - 0.48, 1.05, 0.0])
            return VGroup(
                force_arrow(left_start, RIGHT, length),
                force_arrow(right_start, LEFT, length),
            )

        force_arrows = always_redraw(arrows)
        note = cn("保持电荷量不变，只改变距离 r", font_size=28, color=YELLOW)
        note.to_edge(LEFT, buff=0.85).shift(UP * 2.0)

        self.play(Write(note), FadeIn(q1), FadeIn(q2), Create(line), GrowFromCenter(brace), Write(r_label))
        self.play(Create(force_arrows), Write(formula), run_time=0.8)
        self.wait(0.8)
        self.play(q1_tracker.animate.set_value(-3.1), q2_tracker.animate.set_value(3.1), run_time=2.4)
        self.wait(0.8)
        self.play(q1_tracker.animate.set_value(-1.5), q2_tracker.animate.set_value(1.5), run_time=2.0)
        self.wait(1.0)
        self.play(FadeOut(VGroup(header, q1, q2, line, brace, r_label, formula, force_arrows, note)))

    def inverse_square_graph(self):
        header = self.scene_title("三、图像表达：反平方关系")
        self.play(FadeIn(header))

        axes = Axes(
            x_range=[0, 5.5, 1],
            y_range=[0, 5.5, 1],
            x_length=7.0,
            y_length=4.3,
            tips=False,
            axis_config={"color": GREY_B, "stroke_width": 2},
        ).shift(LEFT * 1.0 + DOWN * 0.2)
        x_label = axes.get_x_axis_label(MathTex("r", font_size=30), edge=RIGHT, direction=DOWN)
        y_label = axes.get_y_axis_label(MathTex("F", font_size=30), edge=UP, direction=LEFT)
        graph = axes.plot(lambda x: 4 / (x ** 2 + 0.25), x_range=[0.55, 5.2], color=FORCE, stroke_width=5)

        moving_x = ValueTracker(1.0)

        dot = always_redraw(lambda: Dot(
            axes.c2p(moving_x.get_value(), 4 / (moving_x.get_value() ** 2 + 0.25)),
            color=YELLOW,
            radius=0.07,
        ))
        v_line = always_redraw(lambda: DashedLine(
            axes.c2p(moving_x.get_value(), 0),
            axes.c2p(moving_x.get_value(), 4 / (moving_x.get_value() ** 2 + 0.25)),
            color=DISTANCE,
        ))
        h_line = always_redraw(lambda: DashedLine(
            axes.c2p(0, 4 / (moving_x.get_value() ** 2 + 0.25)),
            axes.c2p(moving_x.get_value(), 4 / (moving_x.get_value() ** 2 + 0.25)),
            color=DISTANCE,
        ))
        readout = always_redraw(lambda: MathTex(
            rf"r={moving_x.get_value():.1f},\quad F\approx{4 / (moving_x.get_value() ** 2 + 0.25):.2f}",
            font_size=32,
            color=WHITE,
        ).next_to(axes, RIGHT, buff=0.65).shift(UP * 0.8))

        conclusion = VGroup(
            cn("距离变为 2 倍", font_size=30),
            MathTex(r"F \rightarrow \frac{1}{4}F", font_size=44, color=FORCE),
            cn("这就是反平方关系", font_size=28, color=YELLOW),
        ).arrange(DOWN, buff=0.35).next_to(axes, RIGHT, buff=0.9).shift(DOWN * 0.65)

        self.play(Create(axes), Write(x_label), Write(y_label), run_time=1.0)
        self.play(Create(graph), run_time=1.2)
        self.play(Create(dot), Create(v_line), Create(h_line), Write(readout), run_time=0.8)
        self.play(moving_x.animate.set_value(2.0), run_time=1.7)
        self.play(FadeIn(conclusion, shift=UP), run_time=0.9)
        self.play(moving_x.animate.set_value(4.0), run_time=1.8)
        self.wait(1.0)
        self.play(FadeOut(VGroup(header, axes, x_label, y_label, graph, dot, v_line, h_line, readout, conclusion)))

    def summary(self):
        title = cn("课堂小结", font_size=42, weight="BOLD").to_edge(UP, buff=0.6)
        items = VGroup(
            VGroup(cn("1.", 30, FORCE), cn("同号电荷相斥，异号电荷相吸。", 30)),
            VGroup(cn("2.", 30, FORCE), cn("库仑力沿两电荷连线方向。", 30)),
            VGroup(cn("3.", 30, FORCE), cn("力的大小与电荷量乘积成正比，与距离平方成反比。", 30)),
        )
        for item in items:
            item.arrange(RIGHT, buff=0.18)
        items.arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to(ORIGIN + DOWN * 0.3)

        formula = MathTex(r"F = k\frac{|q_1q_2|}{r^2}", font_size=54, color=YELLOW)
        formula.next_to(items, DOWN, buff=0.55)

        self.play(FadeIn(title, shift=DOWN))
        for item in items:
            self.play(FadeIn(item, shift=RIGHT), run_time=0.45)
        self.play(Write(formula))
        self.wait(1.6)
        self.play(FadeOut(VGroup(title, items, formula)))


if __name__ == "__main__":
    # Quick preview:
    # manim -pql coulombs_law.py CoulombsLawScene
    #
    # Final render:
    # manim -pqh coulombs_law.py CoulombsLawScene
    pass
