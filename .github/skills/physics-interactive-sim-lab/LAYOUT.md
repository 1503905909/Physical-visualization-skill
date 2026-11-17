# 画面优先的布局规范（PhET 式）

本规范约束**交互仿真**（`physics-interactive-sim-lab`）的界面形态。目标：学生打开就看见物理现象，而不是先看见一堆字。

## 三条硬规则

1. **画布是布局主干。** 1366×768 屏幕上，画布至少占 70% 宽度，不被侧栏挤压；页面不出纵向滚动条。画布按 16:9 等比铺满可用区域，超出部分留白，不得拉伸变形（内部坐标系不变，指针映射才不会错位）。
2. **参数与读数是叠加层。** 参数面板浮在画布右上角（半透明、圆角、可折叠）；实时读数浮在左上角（不超过 4 个 chips）；图例浮在左下角，默认一行，点开才展开。
3. **文字预算。** 画布内除物理标注外，最多 3 行短文字。所有解释性内容——结论、模型假设、课堂观察问题——默认折叠，收进右下角的「?」抽屉，不得占据首屏。

## DOM 骨架

```html
<body>
  <main class="app">
    <div class="stage">
      <div class="stage-frame">
        <canvas id="..."></canvas>

        <div class="hud hud-readout"><!-- ≤4 个 chips --></div>
        <div class="hud hud-legend" id="legend"><!-- 一行 --></div>

        <aside class="hud hud-panel" id="ctrlPanel"><!-- 参数与开关 --></aside>
        <button class="hud-toggle" id="ctrlToggle" aria-expanded="true">参数</button>

        <button class="hud-more" id="moreBtn" aria-expanded="false">?</button>
        <section class="drawer" id="drawer" hidden><!-- 结论 / 模型假设 / 课堂问题 --></section>
      </div>
    </div>
  </main>
</body>
```

## 必需 CSS（照抄，只允许改强调色与宽度常量）

```css
html, body { height: 100%; }
body { margin: 0; background: #070d11; overflow: hidden;
       font: 14px/1.5 -apple-system, "Microsoft YaHei", sans-serif; color: #eaf2f5; }

.app  { height: 100vh; display: flex; align-items: center; justify-content: center; }

.stage { width: 100%; height: 100%; display: flex; align-items: center; justify-content: center; padding: 8px; box-sizing: border-box; }

/* 16:9 等比舞台：同时受宽高约束 */
.stage-frame { position: relative; aspect-ratio: 16 / 9;
               width: min(100%, calc((100vh - 16px) * 16 / 9));
               border-radius: 12px; overflow: hidden; background: #0b141a; }

.stage-frame > canvas { display: block; width: 100%; height: 100%; }

.hud { position: absolute; z-index: 3; backdrop-filter: blur(6px);
       border-radius: 10px; border: 1px solid rgba(255,255,255,.14);
       background: rgba(12, 24, 30, .72); color: #eaf2f5; }

.hud-readout { left: 12px; top: 12px; display: flex; gap: 8px; flex-wrap: wrap;
               padding: 6px 10px; font-size: 12.5px; }
.hud-readout b { font-size: 14px; color: #7fd6e4; }

.hud-legend { left: 12px; bottom: 12px; max-width: 62%; padding: 6px 10px; font-size: 12px;
              color: #cfe3e9; }

.hud-panel { right: 12px; top: 12px; width: 258px; max-height: calc(100% - 24px);
             overflow-y: auto; padding: 12px; font-size: 12.5px; }
.hud-panel[hidden] { display: none; }

.hud-toggle { position: absolute; right: 12px; top: 12px; z-index: 4;
              padding: 6px 12px; border-radius: 8px; cursor: pointer;
              border: 1px solid rgba(255,255,255,.2); background: rgba(12,24,30,.8); color: #eaf2f5; }
.hud-toggle[aria-expanded="true"] { right: 286px; }   /* 面板展开时让到面板左边 */

.hud-more { position: absolute; right: 12px; bottom: 12px; z-index: 4;
            width: 34px; height: 34px; border-radius: 50%; cursor: pointer; font-weight: 700;
            border: 1px solid rgba(255,255,255,.2); background: rgba(12,24,30,.8); color: #eaf2f5; }

.drawer { position: absolute; z-index: 5; right: 12px; bottom: 56px; width: min(420px, 72%);
          max-height: 60%; overflow-y: auto; padding: 14px 16px; border-radius: 12px;
          background: rgba(10, 20, 26, .95); border: 1px solid rgba(255,255,255,.16); font-size: 13px; }
.drawer h3 { margin: 10px 0 4px; font-size: 13px; color: #7fd6e4; }
.drawer p, .drawer li { color: #cfe3e9; margin: 4px 0; }

@media (max-width: 900px) {
  .hud-panel { width: 210px; font-size: 12px; }
  .hud-toggle[aria-expanded="true"] { right: 232px; }
}
```

## 内容改写规则

- **删掉页面级大标题与副标题段落。** 画布左上角最多留一行 12px 小字（如「平行板电容器」），或干脆不留——浏览器标签页已有标题。
- **结论压缩成一句。** 原来的结论卡、公式块、说明段合并为「一句结论 + 一个关键式」，放进抽屉，首屏不显示。
- **课堂观察问题进抽屉**，默认折叠；不要三个大卡片并排。
- **模型假设**：画布右下角 11px 灰字一行，或进抽屉。禁止整段说明。
- **单位换算表、有效数字说明**之类，全部进抽屉或删除。
- 画布内的物理标注（极板、电荷、方向、数值）保留，但字号不得小于 11px（按 1600×900 画布坐标）。

## 交互规则

- 所有滑块、按钮、拖拽功能**必须保持原有行为**，只改外观与位置。
- 指针映射不得错位：如果原代码用 `canvas.getBoundingClientRect()` 换算，改造后画布 CSS 尺寸变化，必须仍按 `canvas.width / rect.width` 缩放。
- 键盘：`空格` 播放/暂停、`R` 重置、`P` 折叠/展开参数、`?` 打开抽屉。
- 折叠用 `aria-expanded`，抽屉用 `hidden` 属性。
- 1024×768 与 1920×1080 下都要完整可用：面板不遮挡主要物理对象，滑块不被截断。

## 参数面板必须可拖动（防遮挡）

叠加式布局的固有矛盾是：面板一定会压住画布的一角，而不同参数下物理对象会跑到那一角。解决办法不是把面板做小，而是让它**能被拖走、并记住位置**。

```css
.hud-panel { cursor: default; }
.hud-panel .panel-grip { cursor: grab; user-select: none; display: flex; align-items: center;
                         justify-content: space-between; margin: -2px 0 8px; }
.hud-panel .panel-grip:active { cursor: grabbing; }
.hud-panel.dragging { opacity: .96; box-shadow: 0 12px 32px rgba(0,0,0,.45); }
```

```js
// 面板拖动 + 位置记忆：所有仿真页面共用同一份实现
(function initDraggablePanel(){
  const panel = document.getElementById('ctrlPanel');
  const grip  = panel && panel.querySelector('.panel-grip');
  if (!panel || !grip) return;
  const KEY = 'hud-panel-pos:' + location.pathname.split('/').pop();

  function clampToFrame(x, y){
    const f = panel.parentElement.getBoundingClientRect();
    const r = panel.getBoundingClientRect();
    return {
      x: Math.min(Math.max(8, x), f.width  - r.width  - 8),
      y: Math.min(Math.max(8, y), f.height - r.height - 8)
    };
  }
  function place(x, y){
    const p = clampToFrame(x, y);
    panel.style.left = p.x + 'px';
    panel.style.top  = p.y + 'px';
    panel.style.right = 'auto';
  }
  const saved = JSON.parse(localStorage.getItem(KEY) || 'null');
  if (saved) place(saved.x, saved.y);        // 恢复上次位置；无记录则用 CSS 默认角落

  let dx = 0, dy = 0, dragging = false;
  grip.addEventListener('pointerdown', e => {
    const f = panel.parentElement.getBoundingClientRect();
    const r = panel.getBoundingClientRect();
    dx = e.clientX - r.left; dy = e.clientY - r.top;
    dragging = true; panel.classList.add('dragging');
    grip.setPointerCapture(e.pointerId);
    panel.style.left = (r.left - f.left) + 'px';
    panel.style.top  = (r.top  - f.top ) + 'px';
    panel.style.right = 'auto';
  });
  grip.addEventListener('pointermove', e => {
    if (!dragging) return;
    const f = panel.parentElement.getBoundingClientRect();
    place(e.clientX - f.left - dx, e.clientY - f.top - dy);
  });
  grip.addEventListener('pointerup', e => {
    if (!dragging) return;
    dragging = false; panel.classList.remove('dragging');
    grip.releasePointerCapture(e.pointerId);
    localStorage.setItem(KEY, JSON.stringify({
      x: parseFloat(panel.style.left), y: parseFloat(panel.style.top)
    }));
  });
  grip.addEventListener('dblclick', () => document.getElementById('ctrlToggle').click());
})();
```

面板首行必须是 `.panel-grip`，内含标题（如「参数」）与折叠按钮；双击标题行等同于点「参数」按钮。

**默认位置**：按页面内容选一个空角（哪一角物理对象最少就放哪一角），不要一律放右上。若默认位置仍压住主体，说明该页应把面板改成更扁的两列布局，而不是继续缩小。

## 自检清单

- [ ] 1366×768 下页面无滚动条，画布宽度 ≥ 70%
- [ ] 画布内除物理标注外 ≤ 3 行文字
- [ ] 首屏看不到结论段落与课堂问题
- [ ] 参数面板可折叠，折叠后画布无遮挡
- [ ] 所有滑块、按钮、拖拽均正常，读数随操作更新
- [ ] 浏览器 console 无报错
