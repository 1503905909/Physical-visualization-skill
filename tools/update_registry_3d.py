import io
import json
from pathlib import Path

p = Path(r"D:\DeepSeekHarness\zdn工作区\Physical-visualization-skill\gallery\resources.json")
data = json.loads(io.open(p, encoding="utf-8").read())

DESC = {
    "electric_field_lines_html":
        "支持 2D 剖面 / 3D 立体的电场线演示：正电荷、负电荷、等量异种、等量同种、匀强电场五种场景，可拖动旋转看空间分布，场线密度与等势面可调。",
    "electric_potential_equipotential_html":
        "2D / 3D 可切换的电势与等势面演示：三种场景外新增负点电荷与等量同种，探针可拖动读电势；3D 下等势面是绕轴的回转面，能直观看出「等势面 ⊥ 电场线」。",
}

for r in data["resources"]:
    if r["id"] in DESC:
        r["desc"] = DESC[r["id"]]
        r.setdefault("tags", [])
        if "3D" not in r["tags"]:
            r["tags"] = ["2D/3D"] + r["tags"][:3]

io.open(p, "w", encoding="utf-8", newline="\n").write(
    json.dumps(data, ensure_ascii=False, indent=2) + "\n")
print("registry updated")
