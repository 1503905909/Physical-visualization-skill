from manim import *
from manim.utils.tex_templates import TexTemplateLibrary

# 启用中文 LaTeX 模板
config.tex_template = TexTemplateLibrary.ctex

class CoulombsLawScene(Scene):
    """高中物理：库仑定律动画演示"""

    def construct(self):
        self.show_title()
        self.show_physical_background()
        self.show_force_equation()
        self.show_repulsion_and_attraction()
        self.show_distance_effect_graph()
        self.summary_scene()

    def show_title(self):
        title = Title("库仑定律：电荷间的相互作用力")
        subtitle = VGroup(
            Text("同号相斥，异号相吸；", font="Microsoft YaHei", font_size=36),
            MathTex(r"F = k \frac{q_1 q_2}{r^2}")
        )
        subtitle.arrange(DOWN)
        subtitle.next_to(title, DOWN)

        self.play(Write(title), FadeIn(subtitle, shift=DOWN))
        self.wait(2)
        self.play(FadeOut(title), FadeOut(subtitle))

    def show_physical_background(self):
        items = VGroup(
            Text("两个点电荷之间存在相互作用力", font="Microsoft YaHei", font_size=36),
            Text("力的大小与电荷量成正比，与距离的平方成反比", font="Microsoft YaHei", font_size=36),
            Text("力的方向沿连线，且具有吸引或排斥性质", font="Microsoft YaHei", font_size=36),
        )
        items.arrange(DOWN, aligned_edge=LEFT)
        items.scale(0.8)
        self.play(Create(items))
        self.wait(3)
        self.play(FadeOut(items))

    def show_force_equation(self):
        equation = MathTex(r"F = k \frac{q_1 q_2}{r^2}")
        equation.set_color_by_tex("F", YELLOW)
        equation.set_color_by_tex("k", BLUE)
        equation.set_color_by_tex("q_1", RED)
        equation.set_color_by_tex("q_2", RED)
        equation.set_color_by_tex("r", GREEN)

        definitions = VGroup(
            Text("F：电荷间相互作用力，单位 N", font="Microsoft YaHei", font_size=28),
            Text("k：库仑常数，8.99 × 10^9 N·m^2/C^2", font="Microsoft YaHei", font_size=28),
            Text("q_1, q_2：电荷量，单位 C", font="Microsoft YaHei", font_size=28),
            Text("r：电荷间距离，单位 m", font="Microsoft YaHei", font_size=28),
        )
        definitions.arrange(DOWN, aligned_edge=LEFT)
        definitions.next_to(equation, DOWN, buff=0.8)

        self.play(Write(equation))
        self.wait(1.5)
        self.play(FadeIn(definitions, shift=UP))
        self.wait(3)
        self.play(FadeOut(equation), FadeOut(definitions))

    def create_charge_pair(self, sign1, sign2, color1, color2, distance=3.5):
        charge_1 = Circle(radius=0.35, color=color1, fill_opacity=1)
        charge_2 = Circle(radius=0.35, color=color2, fill_opacity=1)
        charge_1.move_to(LEFT * distance / 2)
        charge_2.move_to(RIGHT * distance / 2)

        label_1 = MathTex(sign1, font_size=48).move_to(charge_1.get_center())
        label_2 = MathTex(sign2, font_size=48).move_to(charge_2.get_center())

        return VGroup(charge_1, charge_2, label_1, label_2)

    def show_repulsion_and_attraction(self):
        repulsion = self.create_charge_pair(
            "+", "+", RED, RED, distance=3.5
        )
        repulsion_text = Text("同号电荷相互排斥", font="Microsoft YaHei", font_size=36, color=RED)
        repulsion_text.next_to(repulsion, DOWN, buff=0.8)

        arrow1 = Arrow(repulsion[0].get_right(), repulsion[0].get_right() + LEFT * 1.2, buff=0.05, color=YELLOW)
        arrow2 = Arrow(repulsion[1].get_left(), repulsion[1].get_left() + RIGHT * 1.2, buff=0.05, color=YELLOW)
        arrow1_label = MathTex(r"\vec{F}_{12}", color=YELLOW).next_to(arrow1, UP)
        arrow2_label = MathTex(r"\vec{F}_{21}", color=YELLOW).next_to(arrow2, UP)

        attraction = self.create_charge_pair(
            "+", "-", RED, BLUE, distance=3.5
        )
        attraction_text = Text("异号电荷相互吸引", font="Microsoft YaHei", font_size=36, color=BLUE)
        attraction_text.next_to(attraction, DOWN, buff=0.8)

        arrow3 = Arrow(attraction[0].get_right(), attraction[0].get_right() + RIGHT * 1.0, buff=0.05, color=GREEN)
        arrow4 = Arrow(attraction[1].get_left(), attraction[1].get_left() + LEFT * 1.0, buff=0.05, color=GREEN)
        arrow3_label = MathTex(r"\vec{F}_{12}", color=GREEN).next_to(arrow3, UP)
        arrow4_label = MathTex(r"\vec{F}_{21}", color=GREEN).next_to(arrow4, UP)

        self.play(FadeIn(repulsion), Write(repulsion_text))
        self.wait(1)
        self.play(Create(arrow1), Create(arrow2), Write(arrow1_label), Write(arrow2_label))
        self.wait(2)
        self.play(FadeOut(repulsion), FadeOut(repulsion_text), FadeOut(arrow1), FadeOut(arrow2), FadeOut(arrow1_label), FadeOut(arrow2_label))

        self.play(FadeIn(attraction), Write(attraction_text))
        self.wait(1)
        self.play(Create(arrow3), Create(arrow4), Write(arrow3_label), Write(arrow4_label))
        self.wait(2)
        self.play(FadeOut(attraction), FadeOut(attraction_text), FadeOut(arrow3), FadeOut(arrow4), FadeOut(arrow3_label), FadeOut(arrow4_label))

    def show_distance_effect_graph(self):
        axes = Axes(
            x_range=[0, 5.5, 1],
            y_range=[0, 8, 2],
            x_length=6,
            y_length=4,
            axis_config={"include_tip": True}
        )
        axes.to_edge(LEFT, buff=1)

        x_label = axes.get_x_axis_label(r"r\, (m)")
        y_label = axes.get_y_axis_label(r"F\, (N)")
        graph = axes.plot(lambda x: 8 / (x**2 + 0.5), color=BLUE)
        graph_label = axes.get_graph_label(graph, label="F(r)", x_val=4.5, direction=UR)

        point = Dot(axes.c2p(1.5, 3.0), color=YELLOW)
        point_label = MathTex("(r, F)", font_size=28).next_to(point, UR)
        explanation = Text("距离越大，力的大小迅速减小，符合反平方规律", font="Microsoft YaHei", font_size=28).scale(0.8)
        explanation.next_to(axes, RIGHT, buff=0.8)

        self.play(Create(axes), Write(x_label), Write(y_label))
        self.wait(1)
        self.play(Create(graph), Write(graph_label))
        self.wait(1)
        self.play(Create(point), Write(point_label), Write(explanation))
        self.wait(3)
        self.play(FadeOut(axes), FadeOut(x_label), FadeOut(y_label), FadeOut(graph), FadeOut(graph_label), FadeOut(point), FadeOut(point_label), FadeOut(explanation))

    def summary_scene(self):
        summary = VGroup(
            Text("库仑定律表达为：F = k q_1 q_2 / r^2", font="Microsoft YaHei", font_size=32),
            Text("同号电荷排斥，异号电荷吸引", font="Microsoft YaHei", font_size=32),
            Text("力的大小与电荷量成正比，与距离的平方成反比", font="Microsoft YaHei", font_size=32),
        )
        summary.arrange(DOWN, aligned_edge=LEFT)
        summary.scale(0.8)
        self.play(Create(summary))
        self.wait(4)
        self.play(FadeOut(summary))


if __name__ == "__main__":
    """运行命令示例：
    manim -pqh coulombs_law.py CoulombsLawScene
    """
    pass
