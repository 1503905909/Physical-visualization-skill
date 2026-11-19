# 把 three.js + engine.js 内联进两个页面，生成单文件示例
import io
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent           # Physical-visualization-skill
SRC = ROOT / "tools" / "src"
OUT = ROOT / ".github" / "skills" / "physics-interactive-sim-lab" / "examples"

three = (SRC / "three.min.js").read_text("utf-8")
engine = (SRC / "engine.js").read_text("utf-8")
three = three.replace("//# sourceMappingURL=three.min.js.map", "")
engine = engine.replace("//# sourceMappingURL=engine.js.map", "")
assert "</script>" not in three.lower()
assert "</script>" not in engine.lower()

PAGES = {
    "potential.html": "electric_potential_equipotential_html.html",
    "field.html": "electric_field_lines_html.html",
}

for src_name, out_name in PAGES.items():
    html = (SRC / src_name).read_text("utf-8")
    html = html.replace(
        '<script src="three.min.js"></script>',
        "<script>\n/* three.js r160 · MIT */\n" + three + "\n</script>",
    )
    html = html.replace(
        '<script src="engine.js"></script>',
        "<script>\n" + engine + "\n</script>",
    )
    assert "<script src=" not in html
    dst = OUT / out_name
    io.open(dst, "w", encoding="utf-8", newline="\n").write(html)
    print(f"{out_name}: {dst.stat().st_size/1024:.0f} KB")
