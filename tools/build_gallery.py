# -*- coding: utf-8 -*-
"""生成资源画廊 index.html（单文件、可离线打开、可直接用 GitHub Pages）。

用法：
    python tools/build_gallery.py           # 重新生成 index.html
    python tools/build_gallery.py --check   # 只检查：列出已注册/未注册的示例文件

新增资源：在 gallery/resources.json 里加一条，然后重跑本脚本。
"""
from __future__ import annotations

import argparse
import html
import json
import os
import shutil
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REGISTRY = os.path.join(ROOT, "gallery", "resources.json")
OUT = os.path.join(ROOT, "index.html")

EXAMPLE_DIRS = [
    ".github/skills/physics-interactive-sim-lab/examples",
    ".github/skills/manim-physics-animator/examples",
]

# GitHub Pages 不发布 .github 目录，因此把示例镜像到站点根下的 examples/ 供线上访问。
# 源文件仍以 .github/skills/ 为准，镜像由本脚本自动生成。
MIRROR = [
    (".github/skills/physics-interactive-sim-lab/examples", "examples/interactive", (".html",)),
    (".github/skills/manim-physics-animator/examples", "examples/manim", (".py", ".mp4", ".srt")),
]
TEMPLATE_EXCLUDE = {
    "template_streamlit.py",
    "template_formula.py",
    "test_chinese.py",
    "coulombs_law_sim.py",
}

CHAPTER_ORDER = [
    "必修三 · 第九章",
    "必修三 · 第十章",
    "必修三 · 第十三章",
    "选必二 · 第一章",
    "选必二 · 第二章",
    "选必二 · 第三章",
]


def load_registry() -> dict:
    with open(REGISTRY, encoding="utf-8") as f:
        return json.load(f)


def posix(p: str) -> str:
    return p.replace("\\", "/")


VIDEO_DIR = ".github/skills/manim-physics-animator/examples/videos"


def served_path(src_rel: str) -> str:
    """把 .github 下的源文件路径映射为站点可访问的镜像路径。"""
    rel = posix(src_rel)
    for src_dir, dst_dir, _exts in MIRROR:
        if rel.startswith(src_dir + "/"):
            return dst_dir + "/" + rel[len(src_dir) + 1:]
    return rel


def mirror_examples() -> int:
    """把示例复制到站点根下的 examples/（Pages 不发布 .github），并清理已失效的镜像文件。"""
    copied = 0
    for src_dir, dst_dir, exts in MIRROR:
        src_root = os.path.join(ROOT, src_dir)
        dst_root = os.path.join(ROOT, dst_dir)
        live = set()
        for dirpath, _dirnames, filenames in os.walk(src_root):
            for fn in filenames:
                if not fn.lower().endswith(tuple(e.lower() for e in exts)):
                    continue
                src = os.path.join(dirpath, fn)
                rel = os.path.relpath(src, src_root)
                dst = os.path.join(dst_root, rel)
                live.add(os.path.normcase(dst))
                os.makedirs(os.path.dirname(dst), exist_ok=True)
                if not os.path.exists(dst) or os.path.getmtime(src) > os.path.getmtime(dst):
                    shutil.copy2(src, dst)
                    copied += 1
        # 删除源里已经不存在的镜像文件
        for dirpath, _dirnames, filenames in os.walk(dst_root):
            for fn in filenames:
                dst = os.path.normcase(os.path.join(dirpath, fn))
                if dst not in live:
                    os.remove(dst)
    return copied


def video_for(rid: str) -> str | None:
    """找已渲染的 MP4：优先 skill 的 examples/videos，其次 build/videos/manim（本地渲染产物，被 gitignore）。"""
    for rel in (f"{VIDEO_DIR}/{rid}.mp4", f"build/videos/manim/{rid}.mp4"):
        if os.path.exists(os.path.join(ROOT, rel)):
            served = served_path(rel)
            return served if os.path.exists(os.path.join(ROOT, served)) else rel
    return None


def thumb_url(rel: str) -> str:
    """给缩略图加上基于修改时间的版本号，避免换图后浏览器仍用旧缓存。"""
    full = os.path.join(ROOT, rel)
    try:
        stamp = int(os.path.getmtime(full))
    except OSError:
        stamp = 0
    return f"{rel}?v={stamp}"


def esc(s: str) -> str:
    return html.escape(s, quote=True)


def card_html(r: dict, video: str | None) -> str:
    typ = r["type"]
    path = served_path(posix(r["path"]))
    search = " ".join(
        [r["title"], r.get("topic", ""), r["chapter"], r.get("chapterName", "")] + r.get("tags", [])
    )
    tags = "".join(f'<span class="tag">{esc(t)}</span>' for t in r.get("tags", []))
    badge = (
        '<span class="badge badge-html">交互仿真</span>'
        if typ == "html"
        else '<span class="badge badge-manim">讲解动画</span>'
    )

    if typ == "html":
        thumb = thumb_url(r.get("thumb", ""))
        media = (
            f'<a class="thumb" href="{esc(path)}" target="_blank" rel="noopener">'
            f'<img src="{esc(thumb)}" alt="{esc(r["title"])}" loading="lazy">{badge}</a>'
        )
        foot = (
            f'<a class="btn" href="{esc(path)}" target="_blank" rel="noopener">打开仿真 ↗</a>'
            f'<span class="hint">单文件，双击即可离线运行</span>'
        )
    else:
        scene = r.get("scene", "")
        fname = os.path.basename(path)
        if video:
            media = (
                f'<div class="thumb vid">{badge}'
                f'<video controls preload="none" src="{esc(video)}"></video></div>'
            )
            foot = (
                f'<a class="btn" href="{esc(video)}" target="_blank" rel="noopener">播放视频 ↗</a>'
                f'<a class="btn btn-ghost" href="{esc(path)}" target="_blank" rel="noopener">查看脚本</a>'
            )
        else:
            media = (
                f'<a class="thumb poster" href="{esc(path)}" target="_blank" rel="noopener">'
                f'{badge}<span class="poster-scene">{esc(scene)}</span>'
                f'<span class="poster-note">尚未渲染视频</span></a>'
            )
            cmd = f"manim -pqh {fname} {scene}"
            foot = (
                f'<button class="btn btn-ghost" data-copy="{esc(cmd)}">复制渲染命令</button>'
                f'<a class="btn btn-ghost" href="{esc(path)}" target="_blank" rel="noopener">查看脚本</a>'
            )

    return (
        f'<article class="card" data-type="{typ}" data-chapter="{esc(r["chapter"])}" '
        f'data-search="{esc(search)}">'
        f"{media}"
        f'<div class="body">'
        f'<div class="kicker">{esc(r["chapter"])} · {esc(r.get("chapterName", ""))}</div>'
        f'<h2><a href="{esc(path)}" target="_blank" rel="noopener">{esc(r["title"])}</a></h2>'
        f'<p class="desc">{esc(r["desc"])}</p>'
        f'<div class="tags">{tags}</div>'
        f"</div>"
        f'<div class="foot">{foot}</div>'
        f"</article>"
    )


CSS = """
:root{
  --bg:#f6f8fa; --card:#fff; --ink:#16232b; --muted:#5d7480;
  --teal:#2f7f8f; --teal-d:#246a78; --teal-l:#e6f2f4;
  --amber:#b7791f; --line:#dde5e9; --shadow:0 1px 2px rgba(16,42,52,.06),0 8px 24px rgba(16,42,52,.06);
}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);
  font:15px/1.65 -apple-system,BlinkMacSystemFont,"Segoe UI","Microsoft YaHei","PingFang SC",sans-serif}
a{color:inherit;text-decoration:none}
.hero{background:linear-gradient(135deg,#1f5c68 0%,#2f7f8f 55%,#4a9aa8 100%);color:#fff;padding:44px 24px 38px}
.wrap{max-width:1320px;margin:0 auto;padding:0 24px}
.hero h1{margin:0 0 8px;font-size:30px;letter-spacing:.5px}
.hero p{margin:0;opacity:.9;font-size:15px}
.hero .stats{margin-top:18px;display:flex;gap:10px;flex-wrap:wrap}
.stat{background:rgba(255,255,255,.14);border:1px solid rgba(255,255,255,.22);
  border-radius:999px;padding:5px 14px;font-size:13px}
.bar{position:sticky;top:0;z-index:5;background:rgba(246,248,250,.94);
  backdrop-filter:blur(8px);border-bottom:1px solid var(--line);padding:14px 0}
.bar .wrap{display:flex;gap:14px;align-items:center;flex-wrap:wrap}
input[type=search]{flex:1 1 300px;min-width:220px;padding:10px 14px;border:1px solid var(--line);
  border-radius:10px;background:#fff;font-size:14px;outline:none}
input[type=search]:focus{border-color:var(--teal);box-shadow:0 0 0 3px var(--teal-l)}
.chips{display:flex;gap:8px;flex-wrap:wrap}
.chip{border:1px solid var(--line);background:#fff;color:var(--muted);border-radius:999px;
  padding:7px 14px;font-size:13px;cursor:pointer;transition:.15s}
.chip:hover{border-color:var(--teal);color:var(--teal)}
.chip[aria-pressed=true]{background:var(--teal);border-color:var(--teal);color:#fff}
.count{color:var(--muted);font-size:13px;margin:18px 0 6px}
.group{margin-top:30px}
.group[hidden]{display:none}
.group-head{display:flex;align-items:baseline;gap:12px;flex-wrap:wrap;
  margin:0 0 16px;padding-bottom:10px;border-bottom:1px solid var(--line)}
.group-title{margin:0;font-size:19px;letter-spacing:.4px;font-weight:700}
.group-title::before{content:"";display:inline-block;width:4px;height:15px;border-radius:2px;
  background:var(--teal);margin-right:9px;vertical-align:-1px}
.group[data-group="manim"] .group-title::before{background:var(--amber)}
.group-sub{margin:0;color:var(--muted);font-size:13px}
main.wrap{padding-bottom:48px}
.grid{display:grid;grid-template-columns:repeat(5,minmax(0,1fr));gap:18px;padding-bottom:8px}
.card{background:var(--card);border:1px solid var(--line);border-radius:14px;overflow:hidden;
  box-shadow:var(--shadow);display:flex;flex-direction:column;transition:.18s}
.card:hover{transform:translateY(-2px);box-shadow:0 10px 28px rgba(16,42,52,.12)}
.thumb{position:relative;display:block;aspect-ratio:16/9;background:#0d1b21;overflow:hidden}
.thumb img{width:100%;height:100%;object-fit:cover;display:block}
.thumb.vid video{width:100%;height:100%;object-fit:cover;display:block}
.thumb.poster{display:flex;flex-direction:column;justify-content:center;align-items:center;gap:8px;
  background:linear-gradient(135deg,#123b45,#256a7a 60%,#3f8b9a)}
.poster-scene{color:#eaf6f8;font:600 clamp(10px,0.95vw,13.5px)/1.4 ui-monospace,SFMono-Regular,Consolas,monospace;
  opacity:.95;padding:0 10px;max-width:100%;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.poster-note{color:#a9cfd7;font-size:12px}
.badge{position:absolute;left:10px;top:10px;border-radius:999px;padding:3px 10px;font-size:11.5px;
  font-weight:600;letter-spacing:.3px;color:#fff}
.badge-html{background:var(--teal)}
.badge-manim{background:#8a5a12}
.body{padding:12px 14px 5px;flex:1}
.kicker{font-size:12px;color:var(--teal);font-weight:600;letter-spacing:.2px}
.body h2{margin:6px 0 6px;font-size:15.5px;line-height:1.4}
.body h2 a:hover{color:var(--teal)}
.desc{margin:0 0 10px;color:var(--muted);font-size:13px;line-height:1.6}
.tags{display:flex;gap:6px;flex-wrap:wrap;margin-bottom:10px}
.tag{background:var(--teal-l);color:var(--teal-d);border-radius:6px;padding:2px 8px;font-size:11.5px}
.foot{padding:10px 14px 12px;border-top:1px solid var(--line);display:flex;gap:8px;
  align-items:center;flex-wrap:wrap}
.btn{background:var(--teal);color:#fff;border:none;border-radius:8px;padding:7px 13px;
  font-size:13px;cursor:pointer;font-family:inherit}
.btn:hover{background:var(--teal-d)}
.btn-ghost{background:#fff;color:var(--teal);border:1px solid var(--line)}
.btn-ghost:hover{border-color:var(--teal);background:var(--teal-l)}
.hint{color:var(--muted);font-size:12px}
.empty{padding:60px 0;text-align:center;color:var(--muted)}
.toast{position:fixed;left:50%;bottom:28px;transform:translateX(-50%) translateY(12px);
  background:#16232b;color:#fff;padding:9px 16px;border-radius:10px;font-size:13px;opacity:0;
  pointer-events:none;transition:.2s}
.toast.on{opacity:1;transform:translateX(-50%) translateY(0)}
@media(max-width:1200px){
  .grid{grid-template-columns:repeat(4,minmax(0,1fr))}
}
@media(max-width:980px){
  .grid{grid-template-columns:repeat(3,minmax(0,1fr))}
}
@media(max-width:760px){
  .grid{grid-template-columns:repeat(2,minmax(0,1fr))}
}
@media(max-width:640px){
  .hero h1{font-size:23px}
}
@media(max-width:560px){
  .grid{grid-template-columns:1fr}
}
"""

JS = """
(function(){
  const cards=[...document.querySelectorAll('.card')];
  const q=document.getElementById('q');
  const typeChips=[...document.querySelectorAll('#typeChips .chip')];
  const chapChips=[...document.querySelectorAll('#chapChips .chip')];
  const countEl=document.getElementById('count');
  const empty=document.getElementById('empty');
  const groups=[...document.querySelectorAll('.group')];
  let type='all', chap='all';

  function apply(){
    const kw=q.value.trim().toLowerCase();
    let shown=0;
    for(const c of cards){
      const okType = type==='all' || c.dataset.type===type;
      const okChap = chap==='all' || c.dataset.chapter===chap;
      const okKw = !kw || c.dataset.search.toLowerCase().includes(kw);
      const on = okType && okChap && okKw;
      c.style.display = on ? '' : 'none';
      if(on) shown++;
    }
    for(const g of groups){
      const vis=[...g.querySelectorAll('.card')].filter(c=>c.style.display!=='none').length;
      g.hidden = vis===0;
      const n=g.querySelector('[data-count]');
      if(n) n.textContent=vis;
    }
    countEl.textContent = '显示 ' + shown + ' / ' + cards.length + ' 个资源';
    empty.hidden = shown !== 0;
  }

  q.addEventListener('input', apply);
  typeChips.forEach(ch=>ch.addEventListener('click',()=>{
    type=ch.dataset.type;
    typeChips.forEach(o=>o.setAttribute('aria-pressed', String(o===ch)));
    apply();
  }));
  chapChips.forEach(ch=>ch.addEventListener('click',()=>{
    chap=ch.dataset.chapter;
    chapChips.forEach(o=>o.setAttribute('aria-pressed', String(o===ch)));
    apply();
  }));

  const toast=document.getElementById('toast');
  let tid;
  function say(msg){
    toast.textContent=msg; toast.classList.add('on');
    clearTimeout(tid); tid=setTimeout(()=>toast.classList.remove('on'),1600);
  }
  document.addEventListener('click',e=>{
    const b=e.target.closest('[data-copy]');
    if(!b) return;
    const txt=b.getAttribute('data-copy');
    const done=()=>say('已复制：'+txt);
    if(navigator.clipboard&&window.isSecureContext){
      navigator.clipboard.writeText(txt).then(done).catch(()=>fallback());
    }else{ fallback(); }
    function fallback(){
      const ta=document.createElement('textarea');
      ta.value=txt; ta.style.position='fixed'; ta.style.opacity='0';
      document.body.appendChild(ta); ta.select();
      try{document.execCommand('copy'); done();}catch(_){ say('复制失败，请手动选择'); }
      ta.remove();
    }
  });

  document.addEventListener('keydown',e=>{
    if(e.key==='/'&&document.activeElement!==q){ e.preventDefault(); q.focus(); }
    if(e.key==='Escape'&&document.activeElement===q){ q.value=''; apply(); q.blur(); }
  });

  apply();
})();
"""


def build_page(reg: dict) -> str:
    site = reg["site"]
    res = sorted(
        reg["resources"],
        key=lambda r: (
            CHAPTER_ORDER.index(r["chapter"]) if r["chapter"] in CHAPTER_ORDER else 99,
            0 if r["type"] == "html" else 1,
            r["title"],
        ),
    )

    chapters = []
    for r in res:
        if r["chapter"] not in chapters:
            chapters.append(r["chapter"])

    books = []
    for c in chapters:
        book = c.split("·")[0].strip()
        if book and book not in books:
            books.append(book)

    n_html = sum(1 for r in res if r["type"] == "html")
    n_manim = len(res) - n_html

    cards_html = "\n".join(card_html(r, video_for(r["id"])) for r in res if r["type"] == "html")
    cards_manim = "\n".join(card_html(r, video_for(r["id"])) for r in res if r["type"] != "html")

    type_chips = (
        '<button class="chip" data-type="all" aria-pressed="true">全部</button>'
        f'<button class="chip" data-type="html" aria-pressed="false">交互仿真（{n_html}）</button>'
        f'<button class="chip" data-type="manim" aria-pressed="false">讲解动画（{n_manim}）</button>'
    )
    chap_chips = '<button class="chip" data-chapter="all" aria-pressed="true">全部章节</button>' + "".join(
        f'<button class="chip" data-chapter="{esc(c)}" aria-pressed="false">{esc(c)}</button>'
        for c in chapters
    )

    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(site['title'])}</title>
<meta name="description" content="{esc(site['subtitle'])}">
<style>{CSS}</style>
</head>
<body>

<header class="hero">
  <div class="wrap">
    <h1>{esc(site['title'])}</h1>
    <p>{esc(site['subtitle'])}</p>
    <div class="stats">
      <span class="stat">共 {len(res)} 个资源</span>
      <span class="stat">交互仿真 {n_html}</span>
      <span class="stat">讲解动画 {n_manim}</span>
      <span class="stat">覆盖 {len(books)} 册 · {len(chapters)} 章</span>
    </div>
  </div>
</header>

<div class="bar">
  <div class="wrap">
    <input type="search" id="q" placeholder="搜索知识点、章节或关键词（按 / 聚焦）" aria-label="搜索资源">
    <div class="chips" id="typeChips">{type_chips}</div>
    <div class="chips" id="chapChips">{chap_chips}</div>
  </div>
</div>

<main class="wrap">
  <p class="count" id="count"></p>

  <section class="group" data-group="html">
    <div class="group-head">
      <h2 class="group-title">交互仿真</h2>
      <p class="group-sub">单文件 HTML，双击即可离线运行 · 共 <span data-count="html">{n_html}</span> 个</p>
    </div>
    <div class="grid">
{cards_html}
    </div>
  </section>

  <section class="group" data-group="manim">
    <div class="group-head">
      <h2 class="group-title">讲解动画</h2>
      <p class="group-sub">Manim 脚本渲染的课堂动画 · 共 <span data-count="manim">{n_manim}</span> 个</p>
    </div>
    <div class="grid">
{cards_manim}
    </div>
  </section>

  <div class="empty" id="empty" hidden>没有匹配的资源，试试换个关键词或清除筛选。</div>
</main>

<div class="toast" id="toast" role="status" aria-live="polite"></div>

<script>{JS}</script>
</body>
</html>
"""


def check(reg: dict) -> int:
    registered = {posix(r["path"]): r for r in reg["resources"]}
    problems = 0

    for r in reg["resources"]:
        p = posix(r["path"])
        if not os.path.exists(os.path.join(ROOT, p)):
            print(f"[缺失文件] {r['id']}: {p}")
            problems += 1
        thumb = r.get("thumb")
        if r["type"] == "html" and thumb and not os.path.exists(os.path.join(ROOT, thumb)):
            print(f"[缺少缩略图] {r['id']}: {thumb}")
            problems += 1

    for d in EXAMPLE_DIRS:
        full = os.path.join(ROOT, d)
        if not os.path.isdir(full):
            continue
        for fn in sorted(os.listdir(full)):
            if fn in TEMPLATE_EXCLUDE:
                continue
            if not (fn.endswith(".html") or fn.endswith(".py")):
                continue
            rel = posix(os.path.join(d, fn))
            if rel not in registered:
                print(f"[未登记] {rel}")
                problems += 1

    print(f"\n共 {len(reg['resources'])} 条登记，发现 {problems} 个问题。")
    return 1 if problems else 0


def main() -> int:
    ap = argparse.ArgumentParser(description="生成资源画廊 index.html")
    ap.add_argument("--check", action="store_true", help="只做一致性检查，不生成")
    args = ap.parse_args()

    reg = load_registry()
    if args.check:
        return check(reg)

    n = mirror_examples()
    print(f'镜像示例文件：{n} 个 -> examples/')
    page = build_page(reg)
    with open(OUT, "w", encoding="utf-8", newline="\n") as f:
        f.write(page)
    print(f"已生成 {posix(os.path.relpath(OUT, ROOT))}（{len(page) // 1024} KB，{len(reg['resources'])} 个资源）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
