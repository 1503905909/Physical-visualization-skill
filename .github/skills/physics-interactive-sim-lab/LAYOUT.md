# 界面规范（浅色外壳 · 画面优先）

适用于 `physics-interactive-sim-lab` 生成的全部 HTML 交互仿真。核心是一句话：**白底页面里嵌一块黑色画布窗口，参数与读数都在白卡里，画布内的字越少越好。**

## 一、整体版式

```
┌────────────────────────────────────────────────────┐  页面底色 #f4f6f8
│ 标题（16px，#16232b）        [读数条 白底 ≤4 项]   [?] │  顶栏白底，高 56px
├─────────────────────────────────┬──────────────────┤
│                                 │  参数白卡         │  宽 280（≤1200px 时 240）
│      黑色画布窗口 16:9            │  分组：场景/参数  │  圆角 12、边框 #e3e8ec
│      圆角 14、轻阴影、内嵌         │  滑块/开关/重置   │
│                                 │                  │
├─────────────────────────────────┴──────────────────┤
│ 图例：一行 12px 灰字（#5d7480）                        │
└────────────────────────────────────────────────────┘
```

| 元素 | 规格 |
|---|---|
| 页面底色 | `#f4f6f8`；正文色 `#16232b`；次要文字 `#5d7480` |
| 顶栏 | 白底、高 56px、底部 1px 边框 `#e3e8ec`；左侧标题 16px（不要副标题段落） |
| 读数条 | 顶栏右侧，白底小卡，≤4 项，`标签 12.5px 灰 + 数值 13.5px 深色加粗` |
| 画布窗口 | 黑色卡片 `#0b141a`、圆角 14px、`box-shadow: 0 10px 30px rgba(16,42,52,.12)`；宽度 `min(72vw, calc(177.78vh - 266.67px))`，居中；比例严格 16:9 |
| 参数白卡 | `#fff`、圆角 12px、边框 `#e3e8ec`、内边距 14px、宽 280px（≤1200px 视口 240px）；分组标题 12px 灰色 |
| 图例 | 画布下方一行，12px、`#5d7480`，与画布左缘对齐 |
| 「?」抽屉 | 白卡覆盖在参数卡位置或从右侧滑出，圆角 12px、阴影；装结论、模型假设、课堂观察问题 |
| ≤900px 视口 | 画布与参数卡改为上下堆叠 |

```css
:root{
  --bg:#f4f6f8; --ink:#16232b; --muted:#5d7480; --line:#e3e8ec;
  --accent:#2f7f8f; --card:#fff; --stage:#0b141a;
}
body{ margin:0; background:var(--bg); color:var(--ink);
      font:14px/1.6 -apple-system,"Microsoft YaHei","PingFang SC",sans-serif; }
.topbar{ display:flex; align-items:center; gap:16px; height:56px; padding:0 20px;
         background:#fff; border-bottom:1px solid var(--line); }
.topbar h1{ margin:0; font-size:16px; font-weight:600; }
.readouts{ margin-left:auto; display:flex; gap:14px; padding:6px 12px;
           background:#fff; border:1px solid var(--line); border-radius:10px; }
.readouts b{ font-size:13.5px; }
.main{ display:flex; gap:18px; padding:16px 20px 0; align-items:flex-start; }
.stage-card{ background:var(--stage); border-radius:14px; overflow:hidden;
             box-shadow:0 10px 30px rgba(16,42,52,.12);
             width:min(72vw, calc(177.78vh - 266.67px)); aspect-ratio:16/9; }
.stage-card canvas{ display:block; width:100%; height:100%; }
.panel{ width:280px; flex:0 0 auto; background:var(--card); border:1px solid var(--line);
        border-radius:12px; padding:14px; }
.panel h2{ margin:2px 0 8px; font-size:12px; color:var(--muted); font-weight:600; }
.legend{ margin:10px 20px 18px; font-size:12px; color:var(--muted); }
@media (max-width:1200px){ .panel{ width:240px; } }
@media (max-width:900px){ .main{ flex-direction:column; } .stage-card{ width:100%; } .panel{ width:100%; } }
```

## 二、文字预算

- 页面上**不出现**整段说明、结论卡、课堂问题卡；这些一律进「?」抽屉。
- 画布内除物理标注外 ≤3 行文字；物理量数值只在顶栏读数条与抽屉里出现，画布上不重复写数。
- 按钮、分组标题用 12–13px；不要为了塞字缩小字号到 11px 以下。

## 三、交互与可用性

- 所有滑块、按钮、拖拽、播放/暂停/重置必须保持原有行为。
- 指针映射一律按逻辑坐标换算：`(clientX - rect.left) * (LW / rect.width)`，**不得**用 `canvas.width / rect.width`（位图会随 DPR 变）。
- 键盘：`空格` 播放/暂停、`R` 重置、`?` 打开抽屉、`Esc` 关闭抽屉。
- 鼠标点过按钮后按空格不应被按钮吃掉（`event.detail > 0` 时 `blur()`）。
- 折叠/开关状态用 `aria-expanded` / `aria-pressed`，抽屉用 `hidden`。
- 画布卡片宽度改变时（窗口缩放），指针映射与 HiDPI 位图都要重新同步。

## 四、高清渲染（HiDPI）

画布**不允许**固定位图尺寸后靠 CSS 拉伸。位图 = CSS 尺寸 × 设备像素比（上限 3），绘制统一映射回逻辑坐标：

```js
const LW = 960, LH = 540;          // 该页原有逻辑坐标系，保持不变
function syncBackingStore(){
  const r = canvas.getBoundingClientRect();
  const dpr = Math.min(window.devicePixelRatio || 1, 3);
  const w = Math.max(1, Math.round(r.width * dpr));
  const h = Math.max(1, Math.round(r.height * dpr));
  if (canvas.width !== w || canvas.height !== h){ canvas.width = w; canvas.height = h; }
}
function beginFrame(){
  syncBackingStore();
  ctx.setTransform(canvas.width / LW, 0, 0, canvas.height / LH, 0, 0);
}
```

- 每帧绘制前调用 `beginFrame()`；`resize` 后重绘。
- 逻辑坐标、图形、字号全部不变，变的只是位图密度。

## 五、自检清单

- [ ] 1366×768 下无滚动条；黑色画布窗口四角都在视口内；画布占视口宽约 72%
- [ ] 参数卡不被截断，滑块全部可达
- [ ] 画布内除物理标注外 ≤3 行文字；首屏无结论段落与课堂问题
- [ ] 所有交互实测可用；console 0 报错
- [ ] DPR=2 时位图 = CSS 尺寸 × 2，画面不发虚
- [ ] `node --check`（抽出内联脚本）通过
