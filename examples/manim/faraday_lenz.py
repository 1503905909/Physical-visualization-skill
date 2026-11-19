import numpy as np
from manim import *


config.frame_width = 14.222
config.frame_height = 8.0
config.pixel_width = 1280
config.pixel_height = 720
config.background_color = "#f7f8fb"
config.media_dir = r"build/videos/manim"


FONT = "Microsoft YaHei"
INK = "#172033"
MUTED = "#667085"
LINE = "#c9d2df"
PANEL = "#ffffff"
FIELD = "#0f766e"
ACCENT = "#7c3aed"
MAGNET_N = "#dc2626"
MAGNET_S = "#2563eb"
COPPER = "#b45309"
CURRENT = "#ca8a04"
INDUCED = "#ea580c"

COIL_X = 1.4
COIL_LEN = 3.4
COIL_R = 1.05
GALV_CENTER = np.array([COIL_X, 2.5, 0.0])


def cn(text, font_size=30, color=INK, weight="NORMAL"):
    return Text(text, font=FONT, font_size=font_size, color=color, weight=weight)


def title(text, subtitle=None):
    top = cn(text, 34, INK, "BOLD").to_edge(UP, buff=0.28)
    bar = Line(LEFT * 6.45, RIGHT * 6.45, color=LINE, stroke_width=2).next_to(top, DOWN, buff=0.16)
    group = VGroup(top, bar)
    if subtitle:
        sub = cn(subtitle, 21, MUTED).next_to(bar, DOWN, buff=0.14)
        group.add(sub)
    return group


def card(width, height, label=None):
    box = RoundedRectangle(width=width, height=height, corner_radius=0.18)
    box.set_fill(PANEL, opacity=1)
    box.set_stroke(LINE, width=2)
    group = VGroup(box)
    if label:
        tag = cn(label, 22, INK, "BOLD").next_to(box, UP, buff=0.16)
        group.add(tag)
    return group


def short_arrow(start, end, color=CURRENT, width=4):
    return Arrow(np.array(start), np.array(end), buff=0, stroke_width=width,
                 color=color, max_tip_length_to_length_ratio=0.35)


def magnet(width=1.5, height=0.6, left_pole="S"):
    """条形磁铁。默认左 S 右 N，即 N 极朝向线圈，线圈内磁场方向向右。"""
    half = width / 2
    left = Rectangle(width=half, height=height, stroke_color="#ffffff", stroke_width=2)
    left.set_fill(MAGNET_N if left_pole == "N" else MAGNET_S, opacity=1)
    right = Rectangle(width=half, height=height, stroke_color="#ffffff", stroke_width=2)
    right.set_fill(MAGNET_S if left_pole == "N" else MAGNET_N, opacity=1)
    right.next_to(left, RIGHT, buff=0)
    left_text = cn(left_pole, 23, "#ffffff", "BOLD").move_to(left.get_center())
    right_text = cn("S" if left_pole == "N" else "N", 23, "#ffffff", "BOLD").move_to(right.get_center())
    return VGroup(left, right, left_text, right_text)


def solenoid(turns=7, radius=COIL_R, length=COIL_LEN, color=COPPER, stroke=5):
    total = TAU * turns
    return ParametricFunction(
        lambda t: np.array([-length / 2 + length * t / total, radius * np.sin(t), 0.0]),
        t_range=[0, total, 0.02],
        color=color,
        stroke_width=stroke,
    )


def current_heads(turns=7, radius=COIL_R, length=COIL_LEN, direction=1, color=CURRENT, size=0.12):
    """线圈可见正面的电流方向：direction = 1 时电流沿 +t，螺线管内部磁场指向 -x。"""
    total = TAU * turns
    heads = VGroup()
    for k in range(turns):
        t = PI / 2 + TAU * k
        x = -length / 2 + length * t / total
        tip = Triangle(stroke_width=0).set_fill(color, 1)
        tip.scale(size)
        tip.rotate(-PI / 2 if direction > 0 else PI / 2)
        tip.move_to(np.array([x, radius, 0.0]))
        heads.add(tip)
    return heads


def galvanometer(radius=0.5):
    dial = Circle(radius=radius, stroke_color=INK, stroke_width=3).set_fill("#ffffff", 1)
    arc = Arc(radius=radius * 0.76, start_angle=PI * 0.2, angle=PI * 0.6,
              stroke_color=MUTED, stroke_width=2)
    letter = cn("G", 18, INK, "BOLD").move_to(dial.get_center() + DOWN * radius * 0.48)
    return VGroup(dial, arc, letter)


def needle(center, radius, tracker, scale=0.9, color=CURRENT):
    """指针：只更新端点，不重建对象，便于正常淡入淡出。"""
    line = Line(center, center + radius * 0.86 * UP, color=color, stroke_width=4, buff=0)

    def update(mobject):
        angle = float(np.clip(tracker.get_value() * scale, -0.95, 0.95))
        tip = center + radius * 0.86 * np.array([np.sin(angle), np.cos(angle), 0.0])
        mobject.put_start_and_end_on(center, tip)

    line.add_updater(update)
    return line


def flux_bar(origin, width=2.4, height=0.2, color=ACCENT):
    frame = Rectangle(width=width, height=height, stroke_color=LINE, stroke_width=2)
    frame.set_fill("#eef2f6", opacity=1)
    frame.move_to(np.array([origin[0] + width / 2, origin[1], 0.0]))
    return frame


def flux_fill(frame, value, color=ACCENT):
    width = max(0.02, frame.width * float(np.clip(value, 0.0, 1.0)))
    bar = Rectangle(width=width, height=frame.height * 0.72, stroke_width=0)
    bar.set_fill(color, opacity=1)
    bar.align_to(frame, LEFT)
    bar.set_y(frame.get_y())
    return bar


def flux_of(x):
    """磁铁越靠近线圈，穿过线圈的磁通量越大（0~1 的示意比例）。"""
    return 1.0 / (1.0 + np.exp(-(x + 2.6) / 0.5))


class FaradayLenzScene(Scene):
    """法拉第电磁感应定律与楞次定律。"""

    def construct(self):
        self.magnet_and_coil()
        self.quantitative_law()
        self.lenz_flux_increase()
        self.lenz_flux_decrease()
        self.summary()

    # ------------------------------------------------------------------
    # 分镜一：磁铁靠近、远离线圈
    # ------------------------------------------------------------------
    def magnet_and_coil(self):
        header = title("磁铁靠近线圈：磁通量变化产生感应电动势",
                       "磁铁不动时没有感应电流，只有磁通量发生变化才有")
        self.play(FadeIn(header, shift=DOWN), run_time=0.7)

        coil = solenoid().shift(RIGHT * COIL_X)
        coil_label = cn("线圈 n = 100 匝（画法示意）", 19, COPPER, "BOLD").next_to(coil, DOWN, buff=0.32)

        galv = galvanometer(0.5).move_to(GALV_CENTER)
        g_label = cn("电流计 G", 20, MUTED).next_to(galv, RIGHT, buff=0.22)
        wires = VGroup(
            Line([-0.3, 0, 0], [-0.3, 2.5, 0], color=MUTED, stroke_width=3),
            Line([-0.3, 2.5, 0], [0.9, 2.5, 0], color=MUTED, stroke_width=3),
            Line([3.1, 0, 0], [3.1, 2.5, 0], color=MUTED, stroke_width=3),
            Line([3.1, 2.5, 0], [1.9, 2.5, 0], color=MUTED, stroke_width=3),
        )

        mag_x = ValueTracker(-4.0)
        current = ValueTracker(0.0)

        mag = magnet()
        mag.add_updater(lambda m: m.move_to(np.array([mag_x.get_value(), 0.0, 0.0])))
        ndl = needle(np.array([COIL_X, 2.5, 0.0]), 0.5, current)

        bar_frame = flux_bar(np.array([-4.95, 1.75, 0.0]), width=2.4, height=0.22)
        bar_fill = always_redraw(lambda: flux_fill(bar_frame, flux_of(mag_x.get_value()), ACCENT))
        bar_label = cn("磁通量 Φ（示意 0–1）", 19, MUTED).next_to(bar_frame, UP, buff=0.12).align_to(bar_frame, LEFT)

        caption = cn("磁铁靠近线圈，穿过线圈的磁通量增大", 24, INK, "BOLD").to_edge(DOWN, buff=0.55)

        self.play(FadeIn(coil), FadeIn(coil_label), run_time=0.8)
        self.play(FadeIn(wires), FadeIn(galv), FadeIn(g_label), FadeIn(ndl), run_time=0.6)
        self.play(FadeIn(bar_frame), FadeIn(bar_label), run_time=0.5)
        self.add(bar_fill)
        self.play(FadeIn(mag), run_time=0.5)
        self.play(FadeIn(caption, shift=UP), run_time=0.5)

        # 靠近：磁通量增大，电流计偏转
        self.play(
            mag_x.animate.set_value(-1.15),
            current.animate.set_value(1.0),
            run_time=2.0,
            rate_func=smooth,
        )
        self.play(Transform(caption, cn("磁铁停止运动：磁通量不变，感应电流消失", 24, MUTED, "BOLD").to_edge(DOWN, buff=0.55)),
                  current.animate.set_value(0.0), run_time=0.9)

        # 远离：同样用 2.0 s，平均电动势大小相同，偏转方向相反
        self.play(
            mag_x.animate.set_value(-4.0),
            current.animate.set_value(-1.0),
            run_time=2.0,
            rate_func=smooth,
        )
        self.play(Transform(caption, cn("磁铁远离：磁通量减小，感应电流反向", 24, INK, "BOLD").to_edge(DOWN, buff=0.55)),
                  current.animate.set_value(0.0), run_time=0.8)
        self.wait(0.6)

        note = cn("结论：磁通量变化 → 感应电动势 → 感应电流", 22, FIELD, "BOLD").to_edge(DOWN, buff=0.24)
        self.play(FadeIn(note, shift=UP), run_time=0.5)
        self.wait(0.8)

        self.play(FadeOut(VGroup(header, coil, coil_label, wires, galv, g_label, ndl,
                                 bar_frame, bar_label, caption, note, mag)), run_time=0.7)
        self.remove(bar_fill)

    # ------------------------------------------------------------------
    # 分镜二：ε = n·ΔΦ/Δt 的定量关系
    # ------------------------------------------------------------------
    def quantitative_law(self):
        header = title("定量关系：ε = n·ΔΦ/Δt", "同样的磁通量变化，用时越短，平均感应电动势越大（线圈按示意绘制）")
        self.play(FadeIn(header, shift=DOWN), run_time=0.6)

        law = MathTex(r"\varepsilon = n\,\frac{\Delta \Phi}{\Delta t}", font_size=52, color=FIELD)
        law.move_to(np.array([0.0, -2.85, 0.0]))
        self.play(Write(law), run_time=1.0)

        left_card = card(5.9, 3.5, "慢速靠近：Δt = 2.0 s").shift(LEFT * 3.2 + UP * 0.35)
        right_card = card(5.9, 3.5, "快速靠近：Δt = 0.5 s").shift(RIGHT * 3.2 + UP * 0.35)
        self.play(FadeIn(left_card), FadeIn(right_card), run_time=0.6)

        def build_panel(center, turns=5, radius=0.58, length=1.9):
            coil = solenoid(turns=turns, radius=radius, length=length, stroke=4)
            coil.move_to(center)
            return coil

        left_center = left_card[0].get_center() + DOWN * 0.15
        right_center = right_card[0].get_center() + DOWN * 0.15
        left_coil = build_panel(left_center)
        right_coil = build_panel(right_center)

        lg_center = left_card[0].get_center() + np.array([1.85, 1.05, 0.0])
        rg_center = right_card[0].get_center() + np.array([1.85, 1.05, 0.0])
        left_galv = galvanometer(0.36).move_to(lg_center)
        right_galv = galvanometer(0.36).move_to(rg_center)

        left_x = ValueTracker(-1.25)
        right_x = ValueTracker(-1.25)
        left_cur = ValueTracker(0.0)
        right_cur = ValueTracker(0.0)

        left_mag = magnet(1.0, 0.44)
        left_mag.add_updater(lambda m: m.move_to(left_center + np.array([left_x.get_value(), 0.0, 0.0])))
        right_mag = magnet(1.0, 0.44)
        right_mag.add_updater(lambda m: m.move_to(right_center + np.array([right_x.get_value(), 0.0, 0.0])))
        left_ndl = needle(lg_center, 0.36, left_cur, scale=1.0)
        right_ndl = needle(rg_center, 0.36, right_cur, scale=1.0)

        left_txt = VGroup(
            cn("n = 100，ΔΦ = 0.02 Wb", 16, INK),
            cn("Δt = 2.0 s → 平均 ε = 100×0.02/2.0 = 1.0 V", 16, FIELD, "BOLD"),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.14)
        left_txt.move_to(left_card[0].get_center() + np.array([0.0, -1.05, 0.0]))

        right_txt = VGroup(
            cn("n = 100，ΔΦ = 0.02 Wb", 16, INK),
            cn("Δt = 0.5 s → 平均 ε = 100×0.02/0.5 = 4.0 V", 16, INDUCED, "BOLD"),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.14)
        right_txt.move_to(right_card[0].get_center() + np.array([0.0, -1.05, 0.0]))

        self.play(FadeIn(left_coil), FadeIn(right_coil), run_time=0.6)
        self.play(FadeIn(left_galv), FadeIn(right_galv), run_time=0.4)
        self.play(FadeIn(left_mag), FadeIn(right_mag), run_time=0.4)
        self.play(FadeIn(left_ndl), FadeIn(right_ndl), run_time=0.3)

        # 两个磁铁同时出发、速度不同；各自到位后停下，指针随即回零
        # 第一段 0.5 s：左磁铁走过 1/4，右磁铁前进到位，右指针满偏
        self.play(
            left_x.animate(run_time=0.5).set_value(-0.80),
            left_cur.animate(run_time=0.5).set_value(0.0625),
            right_x.animate(run_time=0.5).set_value(0.55),
            right_cur.animate(run_time=0.5).set_value(1.0),
            rate_func=linear,
        )
        # 第二段 0.5 s：右磁铁已静止 → 右指针回零；左磁铁继续缓慢前进
        self.play(
            left_x.animate(run_time=0.5).set_value(-0.35),
            left_cur.animate(run_time=0.5).set_value(0.125),
            right_cur.animate(run_time=0.5).set_value(0.0),
            rate_func=linear,
        )
        # 第三、四段：左磁铁继续走到位，左指针继续按比例增大
        self.play(
            left_x.animate(run_time=0.5).set_value(0.10),
            left_cur.animate(run_time=0.5).set_value(0.1875),
            rate_func=linear,
        )
        self.play(
            left_x.animate(run_time=0.5).set_value(0.55),
            left_cur.animate(run_time=0.5).set_value(0.25),
            rate_func=linear,
        )
        # 左磁铁也停下 → 指针回零
        self.play(left_cur.animate(run_time=0.5).set_value(0.0), rate_func=linear)
        self.play(FadeIn(left_txt, shift=UP), FadeIn(right_txt, shift=UP), run_time=0.7)
        self.wait(0.4)

        compare = cn("同样的 ΔΦ，Δt 越小，平均电动势越大：4.0 V 是 1.0 V 的 4 倍", 22, INDUCED, "BOLD")
        compare.to_edge(DOWN, buff=0.28)
        self.play(FadeIn(compare, shift=UP), run_time=0.6)
        self.wait(1.0)

        self.play(FadeOut(VGroup(header, law, left_card, right_card, left_coil, right_coil,
                                 left_galv, right_galv, left_mag, right_mag, left_ndl, right_ndl,
                                 left_txt, right_txt, compare)), run_time=0.7)
        self.remove(left_ndl, right_ndl)

    # ------------------------------------------------------------------
    # 分镜三：楞次定律——磁通量增大
    # ------------------------------------------------------------------
    def lenz_flux_increase(self):
        header = title("楞次定律（一）：磁通量增大", "感应电流的磁场要阻碍磁通量的增大")
        self.play(FadeIn(header, shift=DOWN), run_time=0.6)

        coil = solenoid().shift(RIGHT * COIL_X)

        mag_x = ValueTracker(-3.9)
        mag = magnet()
        mag.add_updater(lambda m: m.move_to(np.array([mag_x.get_value(), 0.0, 0.0])))

        # 线圈内的两种磁场：磁铁磁场向右，感应磁场向左（阻碍增大）
        b0_arrow = short_arrow([0.55, 0.42, 0], [3.0, 0.42, 0], "#94a3b8", 5)
        b0_label = cn("原磁场 B 向右", 20, "#64748b", "BOLD").move_to(np.array([COIL_X, 1.52, 0.0]))
        induced_b = short_arrow([3.0, -0.42, 0], [0.55, -0.42, 0], INDUCED, 7)
        induced_label = cn("感应磁场 B′ 向左", 20, INDUCED, "BOLD").move_to(np.array([COIL_X, -1.52, 0.0]))

        heads = current_heads(direction=1).shift(RIGHT * COIL_X)

        phi_up = cn("磁通量 Φ 增大", 22, INDUCED, "BOLD").move_to(np.array([-4.45, 1.72, 0.0]))
        phi_arrow = short_arrow([-5.4, 1.3, 0], [-3.5, 1.3, 0], INDUCED, 5)

        caption = cn("感应电流的磁场与原磁场方向相反，阻碍磁通量的增大", 23, INK, "BOLD")
        caption.to_edge(DOWN, buff=0.6)

        self.play(FadeIn(coil), run_time=0.7)
        self.play(FadeIn(mag), FadeIn(b0_arrow), FadeIn(b0_label), run_time=0.6)
        self.play(
            mag_x.animate.set_value(-1.15),
            FadeIn(heads, lag_ratio=0.1),
            Create(induced_b),
            run_time=2.0,
            rate_func=smooth,
        )
        self.play(FadeIn(induced_label, shift=UP), FadeIn(phi_up), Create(phi_arrow), run_time=0.6)
        self.play(FadeIn(caption, shift=UP), run_time=0.6)
        self.wait(1.0)

        # 磁铁停下 → 磁通量不再变化 → 感应电流、感应磁场随之消失
        stop_caption = cn("磁铁停止运动：磁通量不再变化，感应电流随之消失", 22, MUTED, "BOLD")
        stop_caption.to_edge(DOWN, buff=0.6)
        self.play(
            Transform(caption, stop_caption),
            FadeOut(heads),
            FadeOut(induced_b),
            FadeOut(induced_label),
            FadeOut(phi_up),
            FadeOut(phi_arrow),
            run_time=0.7,
        )
        self.wait(0.9)

        self.play(FadeOut(VGroup(header, coil, mag, b0_arrow, b0_label, caption)), run_time=0.7)
        self.remove(mag)

    # ------------------------------------------------------------------
    # 分镜四：楞次定律——磁通量减小
    # ------------------------------------------------------------------
    def lenz_flux_decrease(self):
        header = title("楞次定律（二）：磁通量减小", "感应电流的磁场要阻碍磁通量的减小")
        self.play(FadeIn(header, shift=DOWN), run_time=0.6)

        coil = solenoid().shift(RIGHT * COIL_X)

        mag_x = ValueTracker(-1.15)
        mag = magnet()
        mag.add_updater(lambda m: m.move_to(np.array([mag_x.get_value(), 0.0, 0.0])))

        b0_arrow = short_arrow([0.55, 0.42, 0], [3.0, 0.42, 0], "#94a3b8", 5)
        b0_label = cn("原磁场 B 向右", 20, "#64748b", "BOLD").move_to(np.array([COIL_X, 1.52, 0.0]))
        induced_b = short_arrow([0.55, -0.42, 0], [3.0, -0.42, 0], INDUCED, 7)
        induced_label = cn("感应磁场 B′ 向右", 20, INDUCED, "BOLD").move_to(np.array([COIL_X, -1.52, 0.0]))

        heads = current_heads(direction=-1).shift(RIGHT * COIL_X)

        phi_down = cn("磁通量 Φ 减小", 22, INDUCED, "BOLD").move_to(np.array([-4.45, 1.72, 0.0]))
        phi_arrow = short_arrow([-3.5, 1.3, 0], [-5.4, 1.3, 0], INDUCED, 5)

        caption = cn("感应电流的磁场与原磁场方向相同，阻碍磁通量的减小", 23, INK, "BOLD")
        caption.to_edge(DOWN, buff=0.6)

        self.play(FadeIn(coil), run_time=0.7)
        self.play(FadeIn(mag), FadeIn(b0_arrow), FadeIn(b0_label), run_time=0.6)
        self.play(
            mag_x.animate.set_value(-4.0),
            FadeIn(heads, lag_ratio=0.1),
            Create(induced_b),
            run_time=2.0,
            rate_func=smooth,
        )
        self.play(FadeIn(induced_label, shift=UP), FadeIn(phi_down), Create(phi_arrow), run_time=0.6)
        self.play(FadeIn(caption, shift=UP), run_time=0.6)
        self.wait(1.0)

        # 磁铁停下 → 磁通量不再变化 → 感应电流、感应磁场随之消失
        stop_caption = cn("磁铁停止运动：磁通量不再变化，感应电流随之消失", 22, MUTED, "BOLD")
        stop_caption.to_edge(DOWN, buff=0.6)
        self.play(
            Transform(caption, stop_caption),
            FadeOut(heads),
            FadeOut(induced_b),
            FadeOut(induced_label),
            FadeOut(phi_down),
            FadeOut(phi_arrow),
            run_time=0.7,
        )
        self.wait(0.9)

        self.play(FadeOut(VGroup(header, coil, mag, b0_arrow, b0_label, caption)), run_time=0.7)
        self.remove(mag)

    # ------------------------------------------------------------------
    # 分镜五：课堂小结
    # ------------------------------------------------------------------
    def summary(self):
        header = cn("课堂归纳", 38, INK, "BOLD").to_edge(UP, buff=0.55)
        self.play(FadeIn(header, shift=DOWN), run_time=0.6)

        items = VGroup(
            cn("1  磁通量变化是产生感应电动势的原因。", 27, INK),
            cn("2  ε = n·ΔΦ/Δt：变化越快，电动势越大。", 27, INK),
            cn("3  感应电流的磁场总要阻碍引起感应电流的磁通量的变化。", 27, INDUCED, "BOLD"),
            cn("4  “阻碍”不是“阻止”，磁通量仍在变化。", 27, MUTED),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.34).move_to(np.array([0.0, 0.15, 0.0]))

        panel = RoundedRectangle(width=10.4, height=3.5, corner_radius=0.22,
                                 stroke_color=LINE, stroke_width=2,
                                 fill_color=PANEL, fill_opacity=1)
        panel.move_to(items)

        law = MathTex(r"\varepsilon = n\,\frac{\Delta \Phi}{\Delta t}", font_size=40, color=FIELD)
        law.next_to(panel, DOWN, buff=0.35)

        self.play(FadeIn(panel, scale=0.98), run_time=0.5)
        for item in items:
            self.play(FadeIn(item, shift=RIGHT * 0.3), run_time=0.45)
        self.play(Write(law), run_time=0.8)
        self.wait(1.4)


if __name__ == "__main__":
    # 快速预览：manim -pql faraday_lenz.py FaradayLenzScene
    # 高清渲染：manim -pqh faraday_lenz.py FaradayLenzScene
    pass
