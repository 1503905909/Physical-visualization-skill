---
name: physics-interactive-sim-lab
description: Build classroom-ready interactive physics simulations for high school physics, especially electromagnetism topics such as Coulomb's law, electric fields, Ohm's law, capacitors, circuits, induction, and charged-particle motion. Use when the user asks for physics simulation, interactive experiment, adjustable parameter demo, HTML/JavaScript browser simulation, Streamlit physics app, classroom lab tool, or visualization resource with sliders, drag controls, live graphs, or real-time physical calculations.
---

# Physics Interactive Sim Lab

Use this skill to create interactive physics simulations that are useful in a real classroom. Prioritize conceptual clarity, direct manipulation, correct physics, and easy deployment.

## Default Output Choice

Choose the output format based on teaching use:

- **HTML/JavaScript single file**: default for classroom demonstration, PPT embedding, student self-study, or situations where Python is inconvenient. It should run by double-clicking the `.html` file in a browser.
- **Streamlit Python app**: use when the user needs data export, more complex numeric computation, multi-tab analysis, or integration with Python plots.
- **Both**: use when the user asks for a polished classroom demo plus a data-analysis version.

For the user's current project, prefer HTML/JavaScript for interactive classroom tools unless they explicitly request Streamlit.

## Workflow

1. Define the teaching goal.
   - State the physical law or concept to explore.
   - Identify what students should observe, compare, or conclude.
   - Keep the model at high school level unless the user requests more depth.

2. Build the physics model before the UI.
   - Write formulas, variables, units, conversion rules, assumptions, and valid ranges.
   - Use SI units internally even if UI uses cm, nC, uC, V, ohm, or mm.
   - Handle impossible values such as zero distance, zero resistance, or out-of-range inputs.

3. Design the interaction.
   - Prefer direct manipulation when possible: draggable charges, movable sliders, switches, checkboxes, or graph cursors.
   - Limit controls to the variables students need to explore.
   - Put the main physical scene first; put settings and numeric details beside or below it.
   - Include one to three classroom observation prompts.

4. Implement the simulation.
   - For HTML output, use vanilla HTML/CSS/JavaScript by default. Avoid external CDN dependencies unless truly needed.
   - For Streamlit output, use `st.slider`, `st.number_input`, `st.checkbox`, `st.metric`, `st.tabs`, and Matplotlib/Plotly only when useful.
   - Use clear Chinese UI labels and units.
   - Keep the layout stable on a classroom projector and on a laptop screen.

5. Validate before delivery.
   - Check that the file opens without console-breaking syntax errors.
   - Verify at least one known numerical example by hand or in code.
   - Verify that changes in parameters update the visualization.
   - For HTML, render or screenshot when possible; for Streamlit, run a syntax/import check if the environment is available.

## Classroom Design Rules

- The first screen should be the usable simulation, not a long explanation.
- The physical object or process should be visible: charges, field vectors, circuit diagram, trajectory, ruler, graph, or meter.
- Numbers should support the visual scene, not replace it.
- Avoid overloading students with too many sliders.
- Use familiar classroom colors:
  - positive charge: red
  - negative charge: blue
  - force/vector arrows: white or yellow
  - distance/trajectory: green
  - warning/model limits: orange
- Include model assumptions when they matter, but keep them short.

## Physics Guardrails

- Use correct unit conversion. Example: `1 uC = 1e-6 C`, `1 nC = 1e-9 C`, `1 cm = 1e-2 m`.
- Coulomb force magnitude: `F = k |q1 q2| / r^2`; interaction is attractive for unlike charges and repulsive for like charges.
- Electric field direction: outward from positive charge, inward toward negative charge.
- Ohm's law: clearly distinguish voltage `U`, current `I`, and resistance `R`.
- Capacitor simulations should state ideal parallel-plate assumptions when using `C = epsilon S / d`.
- If a simplified model is used, label it as a simplified model.

## HTML Simulation Requirements

When generating a browser-based simulation:

- Create one complete `.html` file with embedded CSS and JavaScript.
- Use `<canvas>` or SVG for the main physical scene when dynamic drawing is needed.
- Do not rely on online libraries for core behavior.
- Provide sliders, number inputs, checkboxes, or drag interaction as appropriate.
- Show live computed values with units.
- Include a reset button.
- Include 1 to 3 classroom observation questions.
- Make text readable on a 1366px projector screen.

## Streamlit Simulation Requirements

When generating a Streamlit app:

- Create a complete `app.py`.
- Use functions for physical calculations and plotting.
- Use `st.set_page_config(layout="wide")`.
- Set Chinese fonts for Matplotlib:

```python
from matplotlib import rcParams
rcParams["font.sans-serif"] = ["SimHei", "Microsoft YaHei", "DejaVu Sans"]
rcParams["axes.unicode_minus"] = False
```

- Include export only when useful; otherwise keep the app simple.

## Response Format

When using this skill, respond with:

1. `实验目标`
2. `物理模型与单位`
3. `交互设计`
4. `完整代码`
5. `运行方式`
6. `课堂使用建议`
7. `校验说明`

If the user asks you to edit files directly, update the files and run a syntax or rendering check whenever possible.

## Useful Examples

- `examples/coulombs_law_html.html`: single-file browser simulation for Coulomb's law with draggable charges, ruler, force arrows, and live force values.
- `examples/coulombs_law_sim.py`: Streamlit version for Coulomb's law data exploration.
- `examples/template_streamlit.py`: basic Streamlit template for physics sliders, metrics, plots, and optional data export.
