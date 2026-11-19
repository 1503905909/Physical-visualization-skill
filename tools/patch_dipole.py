import io
from pathlib import Path

p = Path(r"D:\DeepSeekHarness\zdn工作区\Physical-visualization-skill\tools\src\engine.js")
s = io.open(p, encoding="utf-8").read()

# 1) 追踪范围放宽，让绕远的场线能收回负电荷
s = s.replace("if (Math.abs(x) > BOUND.x + 0.6 || r > BOUND.y + 0.6) break;",
              "if (Math.abs(x) > BOUND.x + 1.6 || r > BOUND.y + 1.4) break;")

# 2) 双电荷场景：负电荷也补“外侧”那一半的场线
start = s.index("  function seedLines(field, density) {")
end = s.index("  // ---------- 主程序 ----------")
new_seed = '''  function seedLines(field, density) {
    const out = [];
    const sc = field.sc;
    if (sc.uniform) {
      const ys = [0];
      for (let k = 1; k <= 2; k++) { ys.push(k * 0.85, -k * 0.85); }
      for (const y of ys) {
        const pts = [];
        for (let x = -3.6; x <= 3.6; x += 0.18) pts.push([x, Math.abs(y)]);
        out.push({ pts, sign: 1 });
      }
      return out;
    }

    const charges = field.charges;
    const hasPos = charges.some(c => c.q > 0);

    for (const c of charges) {
      const isPos = c.q > 0;

      if (isPos) {
        // 正电荷：向各个方向发出
        for (let i = 0; i < density; i++) {
          const ang = (i + 0.5) / density * Math.PI;
          const x0 = c.x + 0.16 * Math.cos(ang), r0 = 0.16 * Math.sin(ang);
          const pts = traceLine(field, x0, r0, 1, 900);
          if (pts.length > 6) out.push({ pts, sign: 1 });
        }
      } else if (hasPos) {
        // 负电荷：只补“背离正电荷”的那一侧，否则会和正电荷发出的线重复
        const other = charges.filter(o => o.q > 0)
          .sort((a, b) => Math.abs(a.x - c.x) - Math.abs(b.x - c.x))[0];
        const outward = other ? (Math.sign(c.x - other.x) || 1) : 1;
        for (let i = 0; i < density; i++) {
          const ang = (i + 0.5) / density * Math.PI;
          if (Math.cos(ang) * outward < -0.25) continue;   // 指向正电荷的方向跳过
          const x0 = c.x + 0.16 * Math.cos(ang), r0 = 0.16 * Math.sin(ang);
          let pts = traceLine(field, x0, r0, -1, 900);      // 逆着场强往回追
          pts = pts.reverse();                              // 箭头指向负电荷
          if (pts.length > 6) out.push({ pts, sign: -1 });
        }
      } else {
        // 只有负电荷的场景
        for (let i = 0; i < density; i++) {
          const ang = (i + 0.5) / density * Math.PI;
          const x0 = c.x + 0.16 * Math.cos(ang), r0 = 0.16 * Math.sin(ang);
          let pts = traceLine(field, x0, r0, -1, 900);
          pts = pts.reverse();
          if (pts.length > 6) out.push({ pts, sign: -1 });
        }
      }
    }
    return out;
  }

'''
s = s[:start] + new_seed + s[end:]
io.open(p, "w", encoding="utf-8", newline="\n").write(s)
print("ok", len(s))
