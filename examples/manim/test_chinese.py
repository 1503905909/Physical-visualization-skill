from manim import *


config.frame_width = 14.222
config.frame_height = 8.0
config.pixel_width = 1280
config.pixel_height = 720
config.background_color = "#0b1020"


class TestChinese(Scene):
    """Quick check for Chinese text and formula rendering."""

    def construct(self):
        title = Text("库仑定律", font="Microsoft YaHei", font_size=82, weight="BOLD")
        formula = MathTex(r"F = k \frac{|q_1 q_2|}{r^2}", font_size=56, color=YELLOW)
        note = Text("同号相斥，异号相吸", font="Microsoft YaHei", font_size=36)
        group = VGroup(title, formula, note).arrange(DOWN, buff=0.55).move_to(ORIGIN)

        self.play(FadeIn(title, shift=DOWN), run_time=0.7)
        self.play(Write(formula), run_time=0.8)
        self.play(FadeIn(note, shift=UP), run_time=0.7)
        self.wait(1.5)


if __name__ == "__main__":
    # manim -pql test_chinese.py TestChinese
    pass
