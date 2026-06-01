from manim import *


class TestChinese(Scene):
    def construct(self):
        title = Text("库仑定律", font="Microsoft YaHei", font_size=96)
        formula = MathTex(r"F = k \dfrac{q_1 q_2}{r^2}")
        formula.next_to(title, DOWN, buff=0.6)
        note = Text("同号相斥，异号相吸", font="Microsoft YaHei", font_size=36)
        note.next_to(formula, DOWN, buff=0.6)

        self.play(FadeIn(title))
        self.wait(0.6)
        self.play(Write(formula))
        self.wait(0.6)
        self.play(FadeIn(note))
        self.wait(1.5)


if __name__ == '__main__':
    pass
