---
name: manim-physics-animator
description: Generate classroom-ready Python Manim animations for high school physics teaching, especially electromagnetism topics such as Coulomb's law, electric fields, electric potential, capacitors, circuits, electromagnetic induction, and charged-particle motion. Use when the user asks for Manim physics animation, formula derivation animation, concept visualization, teaching video, physics process animation, or PPT-ready MP4 resources.
---

# Manim Physics Animator

Use this skill to create Manim Community Edition animations that serve classroom teaching, not just decorative formula videos.

## Output Goal

Produce a complete Manim `.py` scene that can be rendered as a 16:9 teaching video. The animation should help high school students understand one physical concept, law, process, or graph relationship.

Default audience: high school physics teachers and students.

Default style: clean blackboard or dark-stage visual language, clear Chinese labels, readable formulas, restrained colors, and visible motion.

## Workflow

1. Clarify the teaching target.
   - Identify the exact concept, law, formula, graph relationship, or physical process.
   - State the textbook-level learning goal in one sentence.
   - If the user does not specify a grade or chapter, assume high school physics and keep the model simple.

2. Design a storyboard before coding.
   - Use 4 to 6 short scenes.
   - Each scene must have a teaching purpose, visible objects, animation action, and expected student takeaway.
   - Avoid long paragraphs on screen. Prefer short labels, arrows, color emphasis, and one key formula at a time.

3. Check the physics model.
   - Confirm formula, units, direction, sign convention, and model assumptions.
   - For vector quantities, explicitly show direction with arrows.
   - For inverse-square or proportional relations, include a dynamic comparison or graph.
   - If a generated visual might be misleading, simplify or add an assumption label.

4. Write Manim code.
   - Use Manim Community Edition APIs.
   - Use `Text(..., font="Microsoft YaHei")` for Chinese labels by default.
   - Use `MathTex` for formulas and symbols only.
   - Use helper functions for repeated objects such as charges, arrows, axes, labels, and callouts.
   - Prefer `ValueTracker` and `always_redraw` when showing variable changes.
   - Avoid external images, audio, custom fonts, or network assets unless the user provides them.

5. Provide render commands and classroom use notes.
   - Quick preview: `manim -pql file.py SceneClass`
   - Final render: `manim -pqh file.py SceneClass`
   - Explain how the teacher can use the animation in导入、讲解、对比、总结 or课后预习.

## Required Animation Quality

- The output must include real motion or transformation. A sequence of static formulas is not enough.
- The first screen should show the topic and core question.
- The main screen should show a physical model: objects, distance, direction, trajectory, field line, circuit path, coordinate axes, or graph.
- Important physical quantities must have labels and units.
- Use color consistently:
  - positive charge: red
  - negative charge: blue
  - force/vector arrows: yellow or white
  - distance/trajectory: green
  - formulas/key conclusions: yellow
- Keep text inside the safe area. Do not place dense Chinese text near the frame edge.
- Do not overcrowd the frame with more than one complex idea at once.

## Physics Guardrails

- Coulomb force: use magnitude `F = k |q1 q2| / r^2`; direction depends on charge signs.
- Electric field of a positive charge points outward; electric field of a negative charge points inward.
- Field lines do not cross.
- For electric potential and equipotential lines, distinguish scalar potential from vector electric field.
- For circuit topics, clearly distinguish current direction, conventional current, electron motion, voltage, resistance, and power.
- For particle motion in electric or magnetic fields, state assumptions such as uniform field, neglecting gravity, or non-relativistic motion.

## Response Format

When using this skill, respond with:

1. `动画目标`
2. `分镜脚本`
3. `物理模型与假设`
4. `Manim代码`
5. `运行命令`
6. `课堂使用建议`

If the user asks you to edit files directly, write or update the `.py` file and then run at least a syntax check. Render a preview when the local Manim environment is available.

## Useful Examples

- `examples/coulombs_law.py`: classroom animation for Coulomb's law with charge signs, force arrows, distance comparison, and inverse-square relation.
- `examples/template_formula.py`: reusable templates for formula derivation, vector demonstration, and curve tracing.
- `examples/test_chinese.py`: quick Chinese text rendering test.
