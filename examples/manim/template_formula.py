from manim import *


config.frame_width = 14.222
config.frame_height = 8.0
config.pixel_width = 1280
config.pixel_height = 720
config.background_color = "#0b1020"


FONT = "Microsoft YaHei"
ACCENT = "#ffd166"
BLUE = "#5aa9ff"
GREEN = "#33d17a"
RED = "#ff4d4f"


def cn(text, font_size=30, color=WHITE, weight="NORMAL"):
    return Text(text, font=FONT, font_size=font_size, color=color, weight=weight)


class FormulaDerivationTemplate(Scene):
    """公式推导类动画模板：适合定义、定律、比例关系和推导过程。"""

    def construct(self):
        self.show_title()
        self.show_known_relations()
        self.derive_formula()
        self.apply_formula()

    def show_title(self):
        title = cn("公式推导动画模板", font_size=44, weight="BOLD")
        subtitle = cn("一屏只讲一个关系，让学生跟得上推导过程", font_size=28, color=GREY_A)
        subtitle.next_to(title, DOWN, buff=0.35)
        self.play(FadeIn(title, shift=DOWN), FadeIn(subtitle, shift=DOWN), run_time=0.8)
        self.wait(0.8)
        self.play(FadeOut(VGroup(title, subtitle)))

    def show_known_relations(self):
        heading = cn("第一步：写出已知关系", font_size=34, color=ACCENT, weight="BOLD")
        heading.to_edge(UP, buff=0.55)

        relation_1 = MathTex(r"X = \frac{Y}{Z}", font_size=48)
        relation_2 = MathTex(r"Y = kA,\quad Z = B", font_size=48)
        relations = VGroup(relation_1, relation_2).arrange(DOWN, buff=0.55).move_to(ORIGIN)

        labels = VGroup(
            cn("先出现定义式", font_size=25, color=GREY_A).next_to(relation_1, LEFT, buff=0.55),
            cn("再补充可替换关系", font_size=25, color=GREY_A).next_to(relation_2, LEFT, buff=0.55),
        )

        self.play(FadeIn(heading))
        self.play(Write(relation_1), FadeIn(labels[0], shift=RIGHT), run_time=0.8)
        self.play(Write(relation_2), FadeIn(labels[1], shift=RIGHT), run_time=0.8)
        self.wait(0.8)
        self.play(FadeOut(VGroup(heading, relations, labels)))

    def derive_formula(self):
        heading = cn("第二步：代入并得到结论", font_size=34, color=ACCENT, weight="BOLD")
        heading.to_edge(UP, buff=0.55)

        eq1 = MathTex(r"X = \frac{Y}{Z}", font_size=46)
        eq2 = MathTex(r"X = \frac{kA}{B}", font_size=50, color=ACCENT)
        eq3 = MathTex(r"\therefore\quad X \propto A,\quad X \propto \frac{1}{B}", font_size=42, color=GREEN)
        equations = VGroup(eq1, eq2, eq3).arrange(DOWN, buff=0.55).move_to(ORIGIN)

        arrow_1 = Arrow(eq1.get_bottom(), eq2.get_top(), color=GREY_B, buff=0.15)
        arrow_2 = Arrow(eq2.get_bottom(), eq3.get_top(), color=GREY_B, buff=0.15)

        self.play(FadeIn(heading))
        self.play(Write(eq1))
        self.play(Create(arrow_1), TransformFromCopy(eq1, eq2), run_time=0.9)
        self.play(Create(arrow_2), Write(eq3), run_time=0.9)
        self.wait(1.0)
        self.play(FadeOut(VGroup(heading, equations, arrow_1, arrow_2)))

    def apply_formula(self):
        heading = cn("第三步：用数值检验公式含义", font_size=34, color=ACCENT, weight="BOLD")
        heading.to_edge(UP, buff=0.55)

        axes = Axes(
            x_range=[0, 5, 1],
            y_range=[0, 6, 1],
            x_length=6,
            y_length=3.8,
            tips=False,
            axis_config={"color": GREY_B},
        ).shift(LEFT * 1.0 + DOWN * 0.3)
        labels = axes.get_axis_labels(MathTex("B"), MathTex("X"))
        curve = axes.plot(lambda x: 5 / (x + 0.4), x_range=[0.4, 5], color=BLUE, stroke_width=5)

        note = VGroup(
            cn("当 B 增大时", font_size=30),
            MathTex(r"X=\frac{kA}{B}", font_size=46, color=ACCENT),
            cn("对应的 X 逐渐减小", font_size=30, color=GREEN),
        ).arrange(DOWN, buff=0.25).next_to(axes, RIGHT, buff=0.75)

        dot_tracker = ValueTracker(0.8)
        dot = always_redraw(lambda: Dot(
            axes.c2p(dot_tracker.get_value(), 5 / (dot_tracker.get_value() + 0.4)),
            color=ACCENT,
            radius=0.08,
        ))

        self.play(FadeIn(heading), Create(axes), Write(labels), run_time=0.9)
        self.play(Create(curve), FadeIn(note, shift=LEFT), run_time=1.0)
        self.play(FadeIn(dot))
        self.play(dot_tracker.animate.set_value(4.2), run_time=2.2)
        self.wait(0.8)
        self.play(FadeOut(VGroup(heading, axes, labels, curve, note, dot)))


class VectorDemonstrationTemplate(Scene):
    """矢量演示模板：适合力、电场强度、速度、加速度等方向性物理量。"""

    def construct(self):
        title = cn("矢量合成演示模板", font_size=40, weight="BOLD").to_edge(UP, buff=0.55)
        axes = NumberPlane(
            x_range=[-4, 4, 1],
            y_range=[-2.5, 2.5, 1],
            background_line_style={"stroke_color": "#334155", "stroke_width": 1},
            axis_config={"color": GREY_B},
        )

        vector_1 = Arrow(ORIGIN, RIGHT * 2.3 + UP * 0.8, color=BLUE, stroke_width=7, buff=0)
        vector_2 = Arrow(vector_1.get_end(), vector_1.get_end() + RIGHT * 1.2 + UP * 1.0, color=RED, stroke_width=7, buff=0)
        resultant = Arrow(ORIGIN, vector_2.get_end(), color=GREEN, stroke_width=8, buff=0)

        labels = VGroup(
            MathTex(r"\vec F_1", color=BLUE, font_size=34).next_to(vector_1, DOWN, buff=0.12),
            MathTex(r"\vec F_2", color=RED, font_size=34).next_to(vector_2, RIGHT, buff=0.12),
            MathTex(r"\vec F", color=GREEN, font_size=38).next_to(resultant, UP, buff=0.12),
        )

        self.play(FadeIn(title), Create(axes))
        self.play(Create(vector_1), Write(labels[0]))
        self.play(Create(vector_2), Write(labels[1]))
        self.play(Create(resultant), Write(labels[2]))
        self.wait(1.2)


class CurveTraceTemplate(Scene):
    """曲线追踪模板：适合 U-I 图像、F-r 图像、轨迹和变量关系。"""

    def construct(self):
        title = cn("变量关系曲线模板", font_size=40, weight="BOLD").to_edge(UP, buff=0.55)
        axes = Axes(
            x_range=[0, 5.5, 1],
            y_range=[0, 5.5, 1],
            x_length=7,
            y_length=4,
            tips=False,
            axis_config={"color": GREY_B},
        ).shift(DOWN * 0.25)
        labels = axes.get_axis_labels(MathTex("x"), MathTex("y"))
        curve = axes.plot(lambda x: 0.22 * x ** 2 + 0.5, x_range=[0, 5], color=BLUE, stroke_width=5)

        tracker = ValueTracker(0.5)
        dot = always_redraw(lambda: Dot(
            axes.c2p(tracker.get_value(), 0.22 * tracker.get_value() ** 2 + 0.5),
            color=ACCENT,
            radius=0.08,
        ))
        value_label = always_redraw(lambda: MathTex(
            rf"x={tracker.get_value():.1f}",
            font_size=32,
            color=ACCENT,
        ).next_to(dot, UP, buff=0.18))

        self.play(FadeIn(title), Create(axes), Write(labels))
        self.play(Create(curve))
        self.play(FadeIn(dot), Write(value_label))
        self.play(tracker.animate.set_value(5.0), run_time=2.5)
        self.wait(0.8)


if __name__ == "__main__":
    # Quick preview:
    # manim -pql template_formula.py FormulaDerivationTemplate
    #
    # Other scenes:
    # manim -pql template_formula.py VectorDemonstrationTemplate
    # manim -pql template_formula.py CurveTraceTemplate
    pass
