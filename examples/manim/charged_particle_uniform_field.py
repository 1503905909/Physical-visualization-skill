# -*- coding: utf-8 -*-
"""带电粒子的加速与偏转 · 45 秒分步解题动画（16:9 / 1280×720）

题目（参考短视频里那道）：
  A、B 两板间有加速电场 E₀，板距 L，粒子由静止从 A 出发；
  出来后水平进入 C、D 两板间的偏转电场 E（板长也是 L），
  飞出时速度与水平方向成 θ = 30°。求偏转场强 E。

分镜（读图 → 判断受力 → 建立模型 → 推导 → 检验）：
  01 读图    画两段场：左边加速（A、B），右边偏转（C、D），标 E₀、E、L、θ
  02 受力    加速段只有 qE₀ 做功；偏转段只有 qE，方向与 v₀ 垂直
  03 建模    加速段匀加速直线；偏转段类平抛（水平匀速 + 竖直匀加速）
  04 加速    qE₀L = ½mv₀²  →  v₀² = 2qE₀L/m
  05 偏转    v_y = at = (qE/m)(L/v₀)
  06 出射角  tanθ = v_y/v₀ = qEL/(mv₀²)
  07 代入    把 v₀² 代进去：tanθ = E/(2E₀)  →  E = 2E₀tanθ
  08 检验    tan30° = √3/3  →  E = (2√3/3)E₀（精确值，不取近似）；量纲、极限都对

渲染：manim -qm charged_particle_uniform_field.py ChargedParticleUniformFieldScene
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
from manim import *

ROOT = Path(__file__).resolve().parents[4]
config.media_dir = str(ROOT / "build" / "videos" / "manim")
config.frame_width = 14.222
config.frame_height = 8.0
config.pixel_width = 1280
config.pixel_height = 720
config.background_color = "#0a0f15"

FONT = "Microsoft YaHei"
MATH_FONT = "Cambria"

INK = "#e8eef7"
MUTED = "#8ea3bd"
POS = "#e0566a"
NEG = "#5b8def"
PLATE = "#8d959e"
FIELD = "#34d399"
PATH_C = "#ffd166"
HOT = "#f472b6"

# ---------------- 版面（示意图坐标）
ACC_X0, ACC_X1 = -6.35, -5.15      # 加速区两板
ACC_H = 1.30                       # 加速板半高
DEF_X0, DEF_X1 = -4.55, -0.55      # 偏转板起止（板长 = DEF_X1-DEF_X0）
DEF_Y = 0.88                       # 偏转板半距
THETA = 30 * DEGREES

FX = 3.55                          # 右栏公式中心


def cn(text, size=30, color=INK, weight=NORMAL):
    return Text(text, font=FONT, font_size=size, color=color, weight=weight)


def mth(markup, size=40, color=INK):
    return MarkupText(markup, font=MATH_FONT, font_size=size, color=color)


def frac(num, den, size=36, color=INK, pad=0.20, buff=0.08):
    a, b = mth(num, size, color), mth(den, size, color)
    w = max(a.width, b.width) + pad
    bar = Line(LEFT * w / 2, RIGHT * w / 2, color=color, stroke_width=2.2)
    a.next_to(bar, UP, buff=buff)
    b.next_to(bar, DOWN, buff=buff)
    return VGroup(a, bar, b)


def sqrt_of(inner, color=INK):
    w, hh = inner.width, inner.height
    H = hh + 0.16
    surd = VMobject(color=color, stroke_width=2.2)
    surd.set_points_as_corners([
        np.array([0.00, 0.10, 0]),
        np.array([0.07, 0.00, 0]),
        np.array([0.17, H, 0]),
        np.array([0.21 + w + 0.08, H, 0]),
    ])
    inner.move_to([0.21 + w / 2 + 0.04, H - hh / 2 - 0.05, 0])
    return VGroup(surd, inner)


# ---------------------------------------------------------------- 场景
class ChargedParticleUniformFieldScene(Scene):
    # 播放速度：0.4 = 原速的 0.4 倍（所有 play / wait 的时长统一 ×2.5）
    SPEED = 0.56

    def play(self, *args, **kwargs):
        kwargs["run_time"] = kwargs.get("run_time", 1.0) / self.SPEED
        return super().play(*args, **kwargs)

    def construct(self):
        self.cap = None
        self.cues = []

        self.beat_read()
        self.beat_force()
        self.beat_model()
        self.beat_accel()
        self.beat_deflect()
        self.beat_angle()
        self.beat_substitute()
        self.beat_check()
        self.write_srt()

    # ------------------------------------------------------------ 字幕
    def caption_box(self, text, size=30):
        label = cn(text, size, "#f4f8fc")
        bg = RoundedRectangle(width=label.width + 0.7, height=label.height + 0.32,
                              corner_radius=0.14, fill_color="#070c12", fill_opacity=0.86,
                              stroke_width=0)
        return VGroup(bg, label).move_to([0.0, -3.42, 0.0])

    def say(self, text, hold=0.4):
        box = self.caption_box(text)
        if self.cap is not None:
            self.play(FadeOut(self.cap), run_time=0.1)
            self.remove(self.cap)
        self.play(FadeIn(box, shift=UP * 0.08), run_time=0.18)
        self.cap = box
        self.cues.append((self.renderer.time, text))
        self.wait(hold)

    # ------------------------------------------------------------ 01 读图
    def beat_read(self):
        self.say("先把图读清楚：两段场，一段加速、一段偏转", 0.3)

        acc = VGroup(
            Rectangle(width=0.16, height=2 * ACC_H, fill_color=PLATE, fill_opacity=0.6,
                      stroke_color="#0b0f14", stroke_width=2).move_to([ACC_X0, 0, 0]),
            Rectangle(width=0.16, height=2 * ACC_H, fill_color=PLATE, fill_opacity=0.6,
                      stroke_color="#0b0f14", stroke_width=2).move_to([ACC_X1, 0, 0]),
        )
        acc_marks = VGroup(
            cn("+", 26, POS, BOLD).move_to([ACC_X0, ACC_H + 0.28, 0]),
            cn("−", 26, NEG, BOLD).move_to([ACC_X1, ACC_H + 0.28, 0]),
            cn("A", 22, MUTED).move_to([ACC_X0, -ACC_H - 0.32, 0]),
            cn("B", 22, MUTED).move_to([ACC_X1, -ACC_H - 0.32, 0]),
        )
        e0 = VGroup(*[
            Arrow([ACC_X0 + 0.16, y, 0], [ACC_X1 - 0.16, y, 0], buff=0, color=FIELD,
                  stroke_width=3, max_tip_length_to_length_ratio=0.35)
            for y in (-0.8, -0.25, 0.3, 0.85)
        ])
        lab_e0 = mth("<i>E</i><sub>0</sub>", 28, FIELD).move_to([(ACC_X0 + ACC_X1) / 2, -1.78, 0])

        dfl = VGroup(
            Rectangle(width=DEF_X1 - DEF_X0, height=0.14, fill_color=PLATE, fill_opacity=0.6,
                      stroke_color="#0b0f14", stroke_width=2).move_to([(DEF_X0 + DEF_X1) / 2, DEF_Y, 0]),
            Rectangle(width=DEF_X1 - DEF_X0, height=0.14, fill_color=PLATE, fill_opacity=0.6,
                      stroke_color="#0b0f14", stroke_width=2).move_to([(DEF_X0 + DEF_X1) / 2, -DEF_Y, 0]),
        )
        dfl_marks = VGroup(
            cn("C", 22, MUTED).move_to([DEF_X0 - 0.25, DEF_Y, 0]),
            cn("D", 22, MUTED).move_to([DEF_X0 - 0.25, -DEF_Y, 0]),
            cn("+", 24, POS, BOLD).move_to([DEF_X1 - 0.2, DEF_Y + 0.28, 0]),
            cn("−", 24, NEG, BOLD).move_to([DEF_X1 - 0.2, -DEF_Y - 0.28, 0]),
        )
        e_arrows = VGroup(*[
            Arrow([x, DEF_Y - 0.12, 0], [x, -DEF_Y + 0.12, 0], buff=0, color=FIELD,
                  stroke_width=3, max_tip_length_to_length_ratio=0.25)
            for x in np.linspace(DEF_X0 + 0.55, DEF_X1 - 0.55, 5)
        ])
        lab_e = mth("<i>E</i>", 28, FIELD).move_to([DEF_X1 + 0.42, 0, 0])

        # 轨迹：加速直线 → 漂移 → 抛物线
        exit_y = -DEF_Y + 0.2
        pts = [np.array([ACC_X0, 0.0, 0]), np.array([ACC_X1, 0.0, 0]),
               np.array([DEF_X0, 0.0, 0])]
        for k in range(1, 25):
            t = k / 24
            pts.append(np.array([DEF_X0 + (DEF_X1 - DEF_X0) * t, exit_y * (t ** 2), 0]))
        path = VMobject(color=PATH_C, stroke_width=4).set_points_smoothly(pts)

        self.play(FadeIn(acc), FadeIn(acc_marks), run_time=0.6)
        self.play(FadeIn(e0), FadeIn(lab_e0), run_time=0.5)
        self.say("左边 A、B 两板：加速电场 E₀，粒子由静止出发", 0.4)
        self.play(FadeIn(dfl), FadeIn(dfl_marks), FadeIn(e_arrows), FadeIn(lab_e), run_time=0.6)
        self.say("右边 C、D 两板：偏转电场 E，粒子水平射入", 0.3)

        l1 = DoubleArrow([ACC_X0, ACC_H + 0.62, 0], [ACC_X1, ACC_H + 0.62, 0], buff=0,
                         color=MUTED, stroke_width=2, max_tip_length_to_length_ratio=0.22)
        l2 = DoubleArrow([DEF_X0, -DEF_Y - 0.45, 0], [DEF_X1, -DEF_Y - 0.45, 0], buff=0,
                         color=MUTED, stroke_width=2, max_tip_length_to_length_ratio=0.05)
        lab_l1 = mth("<i>L</i>", 24, MUTED).next_to(l1, UP, buff=0.06)
        lab_l2 = mth("<i>L</i>", 24, MUTED).next_to(l2, DOWN, buff=0.06)
        self.play(GrowArrow(l1), FadeIn(lab_l1), GrowArrow(l2), FadeIn(lab_l2), run_time=0.6)

        p_exit = np.array([DEF_X1, exit_y, 0])
        v_dir = np.array([np.cos(-THETA), np.sin(-THETA), 0])
        v_out = Arrow(p_exit, p_exit + v_dir * 1.15, buff=0, color=INK, stroke_width=3.5,
                      max_tip_length_to_length_ratio=0.22)
        ang = Arc(radius=0.62, start_angle=0, angle=-THETA, color=INK,
                  stroke_width=2).move_to(p_exit)
        th_lab = mth("θ", 24, INK).move_to(p_exit + v_dir * 0.95)
        self.play(Create(path), run_time=1.1)
        self.play(GrowArrow(v_out), Create(ang), FadeIn(th_lab), run_time=0.5)
        self.say("飞出时速度方向偏了 θ = 30° —— 要求的就是 E", 0.4)

        self.wait(0.8)
        self.diagram = VGroup(acc, acc_marks, e0, lab_e0, dfl, dfl_marks, e_arrows, lab_e,
                              l1, lab_l1, l2, lab_l2, path, v_out, ang, th_lab)

    # ------------------------------------------------------------ 02 受力
    def beat_force(self):
        self.say("判断受力：加速段只有 qE₀，偏转段只有 qE", 0.2)

        f0 = Arrow([ACC_X0 + 0.28, 0.75, 0], [ACC_X0 + 0.88, 0.75, 0], buff=0,
                   color=HOT, stroke_width=4, max_tip_length_to_length_ratio=0.3)
        lab_f0 = mth("<i>qE</i><sub>0</sub>", 24, HOT).next_to(f0, UP, buff=0.06)

        p_in = np.array([DEF_X0 + 0.7, 0.0, 0])
        f1 = Arrow(p_in, p_in + DOWN * 0.6, buff=0, color=HOT, stroke_width=4,
                   max_tip_length_to_length_ratio=0.3)
        lab_f1 = mth("<i>qE</i>", 24, HOT).next_to(f1, RIGHT, buff=0.08)

        self.play(GrowArrow(f0), FadeIn(lab_f0), run_time=0.5)
        self.play(GrowArrow(f1), FadeIn(lab_f1), run_time=0.5)
        self.say("qE₀ 与运动方向相同 → 一直加速；qE 与 v₀ 垂直 → 只改方向", 0.6)

        self.forces = VGroup(f0, lab_f0, f1, lab_f1)
        self.wait(0.6)

    # ------------------------------------------------------------ 03 建模
    def beat_model(self):
        self.say("建立模型：一段匀加速直线，一段类平抛", 0.2)

        m1 = cn("加速段：匀加速直线", 22, PATH_C, BOLD).move_to([ACC_X0 + 0.95, -2.35, 0])
        m2 = cn("偏转段：类平抛", 22, PATH_C, BOLD).move_to([(DEF_X0 + DEF_X1) / 2, -2.35, 0])
        self.play(FadeIn(m1), FadeIn(m2), run_time=0.5)
        self.say("类平抛 = 水平匀速 + 竖直匀加速，两段互不影响", 0.5)
        self.models = VGroup(m1, m2)
        self.wait(0.6)

    # ------------------------------------------------------------ 04 加速
    def beat_accel(self):
        self.say("第一步：加速段用动能定理", 0.2)

        f1 = mth("<i>qE</i><sub>0</sub><i>L</i> = ½<i>mv</i><sub>0</sub>²", 38).move_to([FX, 2.0, 0])
        f2 = VGroup(mth("<i>v</i><sub>0</sub>² =", 38),
                    frac("2<i>qE</i><sub>0</sub><i>L</i>", "<i>m</i>", 32)) \
            .arrange(RIGHT, buff=0.16).move_to([FX, 1.05, 0])
        self.play(FadeIn(f1, shift=LEFT * 0.15), run_time=0.5)
        self.play(FadeIn(f2, shift=LEFT * 0.15), run_time=0.5)
        self.say("v₀² = 2qE₀L/m —— 先存着，后面要用", 0.5)
        self.f_acc = VGroup(f1, f2)
        self.wait(0.9)

    # ------------------------------------------------------------ 05 偏转
    def beat_deflect(self):
        self.say("第二步：偏转段，竖直方向 v_y = at", 0.2)

        f3 = VGroup(mth("<i>v</i><sub>y</sub> = <i>at</i> =", 36),
                    frac("<i>qE</i>", "<i>m</i>", 30), mth("·", 36),
                    frac("<i>L</i>", "<i>v</i><sub>0</sub>", 30)) \
            .arrange(RIGHT, buff=0.14).move_to([FX, 0.05, 0])
        self.play(FadeIn(f3, shift=LEFT * 0.15), run_time=0.5)
        self.say("水平方向走完板长要用 L/v₀，这就是时间 t", 0.5)
        self.f_def = f3
        self.wait(0.9)

    # ------------------------------------------------------------ 06 出射角
    def beat_angle(self):
        self.say("第三步：出射角 tanθ = v_y / v₀", 0.2)

        f4 = VGroup(mth("tan<i>θ</i> =", 36),
                    frac("<i>v</i><sub>y</sub>", "<i>v</i><sub>0</sub>", 32),
                    mth("=", 36), frac("<i>qEL</i>", "<i>mv</i><sub>0</sub>²", 32)) \
            .arrange(RIGHT, buff=0.12).move_to([FX, -1.15, 0])
        self.play(FadeIn(f4, shift=LEFT * 0.15), run_time=0.5)
        self.say("分母是 v₀² —— 正好和第 4 步那条接上", 0.6)
        self.f_tan = f4
        self.wait(0.9)

    # ------------------------------------------------------------ 07 代入
    def beat_substitute(self):
        self.say("第四步：把 v₀² 代进去，q、L、m 全部约掉", 0.2)

        self.play(FadeOut(self.f_def), FadeOut(self.f_tan), run_time=0.3)
        f5 = mth("tan<i>θ</i> = <i>qEL</i> / (2<i>qE</i><sub>0</sub><i>L</i>) = <i>E</i> / (2<i>E</i><sub>0</sub>)", 34) \
            .move_to([FX, -0.15, 0])
        f6 = mth("<i>E</i> = 2<i>E</i><sub>0</sub> tan<i>θ</i>", 40, HOT).move_to([FX, -1.15, 0])
        self.play(FadeIn(f5, shift=LEFT * 0.15), run_time=0.6)
        self.play(FadeIn(f6, shift=LEFT * 0.15), run_time=0.5)
        self.say("只剩两段场强和角度 —— 与粒子的 q、m 完全无关", 0.7)
        self.f_sub = VGroup(f5, f6)
        self.wait(1.2)

    # ------------------------------------------------------------ 08 检验
    def beat_check(self):
        self.say("最后代数据、做检验", 0.2)
        self.play(FadeOut(self.f_acc), FadeOut(self.f_sub), run_time=0.3)

        tan30 = VGroup(mth("tan30° =", 32), sqrt_of(mth("3", 28), INK),
                       mth("/ 3", 32)).arrange(RIGHT, buff=0.10).move_to([FX, 1.25, 0])

        num = VGroup(mth("2", 34), sqrt_of(mth("3", 28), INK)).arrange(RIGHT, buff=0.05)
        den = mth("3", 34)
        barW = max(num.width, den.width) + 0.20
        bar = Line(LEFT * barW / 2, RIGHT * barW / 2, color=HOT, stroke_width=2.4)
        num.next_to(bar, UP, buff=0.07)
        den.next_to(bar, DOWN, buff=0.07)
        result = VGroup(mth("<i>E</i> =", 40, HOT), VGroup(num, bar, den),
                        mth("<i>E</i><sub>0</sub>", 40, HOT)) \
            .arrange(RIGHT, buff=0.14).move_to([FX, 0.25, 0])
        self.play(FadeIn(tan30, shift=LEFT * 0.15), run_time=0.5)
        self.play(FadeIn(result, shift=LEFT * 0.15), run_time=0.5)
        self.say("检验：两边单位都是 V/m；θ→0 时 E→0，极限也对", 0.8)

        bar = VGroup(
            cn("加速 qE₀L = ½mv₀²", 22, MUTED),
            mth("<i>E</i> = 2<i>E</i><sub>0</sub>tan<i>θ</i>", 32, HOT),
            cn("与 q、m 无关", 22, FIELD),
        ).arrange(RIGHT, buff=0.42).move_to([0, 2.75, 0])
        self.play(FadeIn(bar, shift=DOWN * 0.1), run_time=0.6)

        self.say("一句话：加速定 v₀²，偏转定 tanθ，两式一联立就解出 E", 1.0)

    # ------------------------------------------------------------ SRT
    def write_srt(self):
        def ts(sec):
            ms = int(round(sec * 1000))
            h, ms = divmod(ms, 3600_000)
            m, ms = divmod(ms, 60_000)
            s, ms = divmod(ms, 1000)
            return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"

        path = ROOT / "build" / "videos" / "manim" / "charged_particle_uniform_field.srt"
        path.parent.mkdir(parents=True, exist_ok=True)
        blocks = []
        for i, (t0, text) in enumerate(self.cues):
            t1 = self.cues[i + 1][0] if i + 1 < len(self.cues) else self.renderer.time
            blocks.append(f"{i + 1}\n{ts(t0)} --> {ts(t1)}\n{text}\n")
        path.write_text("\n".join(blocks), encoding="utf-8")
