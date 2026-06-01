"""
Manim 物理动画模板 - 基础公式推导
适用于: 定义、推导、定律演示
"""

from manim import *
from manim.utils.tex_templates import TexTemplateLibrary

# 如果需要中文支持，取消下面的注释
# config.tex_template = TexTemplateLibrary.ctex

class FormulaDerivationTemplate(Scene):
    """
    这是一个基础模板，展示如何用 Manim 推导和展示物理公式。
    
    典型步骤：
    1. 标题
    2. 显示基本定义或已知量
    3. 逐步推导，每次添加一个新的关系
    4. 显示最终结果
    5. 可视化结果（如曲线、矢量等）
    """
    
    def construct(self):
        # ========== 第一幕：标题 ==========
        title = Tex("公式推导示例")
        self.play(Write(title))
        self.wait(1)
        self.play(FadeOut(title))
        
        # ========== 第二幕：基本定义 ==========
        definition = Tex(r"定义: 物理量 $X = \frac{Y}{Z}$")
        self.play(Write(definition))
        self.wait(2)
        
        # ========== 第三幕：推导过程 ==========
        # 显示第一个等式
        eq1 = Tex(r"$Y = k \cdot A$")
        eq1.shift(UP * 2)
        self.play(Write(eq1))
        self.wait(1)
        
        # 显示第二个等式
        eq2 = Tex(r"$Z = B$")
        eq2.shift(DOWN * 1)
        self.play(Write(eq2))
        self.wait(1)
        
        # 显示推导结果
        eq3 = Tex(r"$\therefore X = \frac{k \cdot A}{B}$", color=YELLOW)
        eq3.shift(DOWN * 3)
        self.play(Write(eq3))
        self.wait(2)
        
        # ========== 第四幕：数值验证 ==========
        values = Tex(r"数值: $k = 9 \times 10^9$, $A = 2$, $B = 4$")
        values.shift(DOWN * 4.5)
        self.play(Write(values))
        self.wait(1)
        
        result = Tex(r"$X = \frac{9 \times 10^9 \times 2}{4} = 4.5 \times 10^9$", color=GREEN)
        result.shift(DOWN * 5.5)
        self.play(Write(result))
        self.wait(2)
        
        self.play(FadeOut(definition), FadeOut(eq1), FadeOut(eq2), 
                  FadeOut(eq3), FadeOut(values), FadeOut(result))


class VectorDemonstrationTemplate(Scene):
    """
    展示矢量和箭头的使用。
    适用于: 力、电场等矢量场的演示
    """
    
    def construct(self):
        # 创建坐标系
        axes = Axes(
            x_range=[-3, 3, 1],
            y_range=[-3, 3, 1],
            axis_config={"color": GREY_A},
            tips=False,
        )
        self.add(axes)
        
        # 创建矢量
        v1 = Arrow(ORIGIN, [2, 1, 0], color=BLUE)
        v2 = Arrow([2, 1, 0], [3, 2.5, 0], color=RED)
        v_resultant = Arrow(ORIGIN, [3, 2.5, 0], color=GREEN, stroke_width=3)
        
        # 标签
        label1 = MathTex(r"\vec{F}_1", color=BLUE).shift([1, 0.5, 0])
        label2 = MathTex(r"\vec{F}_2", color=RED).shift([2.5, 1.75, 0])
        label_result = MathTex(r"\vec{F}_{total}", color=GREEN).shift([1.5, 1.25, 0])
        
        # 演示
        self.play(Create(v1), Write(label1))
        self.wait(1)
        self.play(Create(v2), Write(label2))
        self.wait(1)
        self.play(Create(v_resultant), Write(label_result))
        self.wait(2)


class CurveTraceTemplate(Scene):
    """
    展示函数曲线。
    适用于: U-I 特性、电势分布等曲线演示
    """
    
    def construct(self):
        # 创建坐标系
        ax = Axes(
            x_range=[0, 5, 1],
            y_range=[0, 10, 2],
            axis_config={"color": GREY_A},
            tips=False,
        )
        labels = ax.get_axis_labels(x_label="x", y_label="y")
        
        # 绘制函数
        curve = ax.plot(lambda x: x**2, color=BLUE, stroke_width=2)
        
        # 标题
        title = MathTex("y = x^2", color=BLUE).to_corner(UP)
        
        self.add(ax, labels, title)
        self.play(Create(curve))
        self.wait(2)
        
        # 在曲线上标注几个点
        for x in [1, 2, 3]:
            y = x ** 2
            dot = Dot(ax.c2p(x, y), color=RED)
            self.play(Create(dot))
            self.wait(0.5)


if __name__ == "__main__":
    """
    运行命令示例：
    
    # 低质量快速预览
    manim -ql template_formula.py FormulaDerivationTemplate
    
    # 高质量最终版本
    manim -pqh template_formula.py FormulaDerivationTemplate
    
    # 其他场景
    manim -pqh template_formula.py VectorDemonstrationTemplate
    manim -pqh template_formula.py CurveTraceTemplate
    """
    pass
