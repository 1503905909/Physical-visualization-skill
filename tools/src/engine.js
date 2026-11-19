/* 电场/电势 3D 演示共用引擎（three.js r160）
 * 场景：正点电荷 / 负点电荷 / 等量异种 / 等量同种 / 匀强电场
 * 两种视角：2D（正交，看向 z 轴）/ 3D（透视，可旋转）
 * 层：电势色图（z=0 截面）、等势面（绕 x 轴旋转体）、电场线、探针
 */
(function () {
  const SOFT2 = 0.08;                 // 软化半径²，避免电荷中心发散
  const BOUND = { x: 5.6, y: 3.15 };
  const UNIFORM_E = 0.72;

  const SCENES = {
    singlePositive: {
      name: "正点电荷",
      charges: [{ q: 1, x: 0, label: "+Q" }],
      tip: "正点电荷周围电势由内向外降低；三维里等势面是一层层同心球面。"
    },
    singleNegative: {
      name: "负点电荷",
      charges: [{ q: -1, x: 0, label: "-Q" }],
      tip: "负点电荷周围电势为负，越靠近越低；等势面同样是同心球面，只是颜色与箭头方向相反。"
    },
    dipole: {
      name: "等量异种",
      charges: [{ q: 1, x: -1.4, label: "+Q" }, { q: -1, x: 1.4, label: "-Q" }],
      tip: "等量异种电荷：中垂面上电势恒为零；电场线从正电荷出发终止于负电荷。"
    },
    samePositive: {
      name: "等量同种",
      charges: [{ q: 1, x: -1.4, label: "+Q" }, { q: 1, x: 1.4, label: "+Q" }],
      tip: "等量同种电荷：中点处场强为零但电势不为零；等势面在两个电荷处各自成壳并向外合并。"
    },
    uniform: {
      name: "匀强电场",
      uniform: true,
      tip: "两板之间电场处处相同（大小方向都不变），等势面是一组平行平面。"
    }
  };

  const COLOR = {
    bg: 0x070a0e,
    pos: 0xff4d5a,
    neg: 0x4d6bff,
    field: 0x7fd8ea,
    warm: 0xff8a5c,
    cool: 0x5b8cff,
    plane: 0x1d3a4a,
    grid: 0x14222c
  };

  // ---------- 场与电势 ----------
  function makeField(sceneKey) {
    const sc = SCENES[sceneKey];
    const cs = sc.charges || [];
    return {
      sc,
      charges: cs,
      potential(x, y, z) {
        if (sc.uniform) return -UNIFORM_E * x;
        let v = 0;
        for (const c of cs) {
          const dx = x - c.x;
          v += c.q / Math.sqrt(dx * dx + y * y + z * z + SOFT2);
        }
        return v;
      },
      // 子午面（z=0，y=rho）上的分量
      meridional(x, rho) {
        if (sc.uniform) return { ex: UNIFORM_E, er: 0 };
        let ex = 0, er = 0;
        for (const c of cs) {
          const dx = x - c.x;
          const r2 = dx * dx + rho * rho + SOFT2;
          const inv = c.q / (r2 * Math.sqrt(r2));
          ex += inv * dx;
          er += inv * rho;
        }
        return { ex, er };
      },
      field(x, y, z) {
        if (sc.uniform) return { x: UNIFORM_E, y: 0, z: 0 };
        let ex = 0, ey = 0, ez = 0;
        for (const c of cs) {
          const dx = x - c.x;
          const r2 = dx * dx + y * y + z * z + SOFT2;
          const inv = c.q / (r2 * Math.sqrt(r2));
          ex += inv * dx; ey += inv * y; ez += inv * z;
        }
        return { x: ex, y: ey, z: ez };
      }
    };
  }

  // ---------- 等势线（子午面 marching squares，按边编号串联） ----------
  function contourPolys(field, level, nx, nr) {
    const xmin = -BOUND.x, xmax = BOUND.x, rmax = BOUND.y;
    const dx = (xmax - xmin) / nx, dr = rmax / nr;
    const val = new Float32Array((nx + 1) * (nr + 1));
    for (let j = 0; j <= nr; j++) {
      for (let i = 0; i <= nx; i++) {
        val[j * (nx + 1) + i] = field.potential(xmin + i * dx, j * dr, 0);
      }
    }

    const pt = new Map(), adj = new Map();
    const kH = (i, j) => "H" + i + "_" + j;
    const kV = (i, j) => "V" + i + "_" + j;

    function pointH(i, j) {
      const k = kH(i, j);
      if (!pt.has(k)) {
        const a = val[j * (nx + 1) + i], b = val[j * (nx + 1) + i + 1];
        const t = (level - a) / ((b - a) || 1e-9);
        pt.set(k, [xmin + (i + t) * dx, j * dr]);
      }
      return k;
    }
    function pointV(i, j) {
      const k = kV(i, j);
      if (!pt.has(k)) {
        const a = val[j * (nx + 1) + i], b = val[(j + 1) * (nx + 1) + i];
        const t = (level - a) / ((b - a) || 1e-9);
        pt.set(k, [xmin + i * dx, (j + t) * dr]);
      }
      return k;
    }
    function link(a, b) {
      if (!adj.has(a)) adj.set(a, []);
      if (!adj.has(b)) adj.set(b, []);
      adj.get(a).push(b); adj.get(b).push(a);
    }

    for (let j = 0; j < nr; j++) {
      for (let i = 0; i < nx; i++) {
        const v00 = val[j * (nx + 1) + i], v10 = val[j * (nx + 1) + i + 1];
        const v01 = val[(j + 1) * (nx + 1) + i], v11 = val[(j + 1) * (nx + 1) + i + 1];
        let code = 0;
        if (v00 > level) code |= 1;
        if (v10 > level) code |= 2;
        if (v11 > level) code |= 4;
        if (v01 > level) code |= 8;
        if (code === 0 || code === 15) continue;
        const B_ = () => pointH(i, j), R_ = () => pointV(i + 1, j);
        const T_ = () => pointH(i, j + 1), L_ = () => pointV(i, j);
        switch (code) {
          case 1: case 14: link(L_(), B_()); break;
          case 2: case 13: link(B_(), R_()); break;
          case 3: case 12: link(L_(), R_()); break;
          case 4: case 11: link(R_(), T_()); break;
          case 6: case 9: link(B_(), T_()); break;
          case 7: case 8: link(L_(), T_()); break;
          case 5: link(L_(), B_()); link(R_(), T_()); break;
          case 10: link(L_(), T_()); link(B_(), R_()); break;
        }
      }
    }

    const used = new Set(), polys = [];
    function walk(start, closed) {
      const poly = [];
      let cur = start, prev = null;
      while (cur && !used.has(cur)) {
        used.add(cur);
        poly.push(pt.get(cur));
        const nxt = adj.get(cur).find(k => k !== prev && !used.has(k));
        prev = cur; cur = nxt;
      }
      if (poly.length > 2) {
        if (closed) poly.push(poly[0]);
        polys.push(poly);
      } else if (poly.length === 2) {
        polys.push(poly);
      }
    }
    for (const start of adj.keys()) if (adj.get(start).length === 1) walk(start, false);
    for (const start of adj.keys()) if (!used.has(start)) walk(start, true);
    return polys;
  }

  // 把子午线旋转成回转面
  function revolve(points, segs) {
    const rings = segs + 1;
    const n = points.length;
    const pos = [];
    for (let k = 0; k < rings; k++) {
      const th = (k / segs) * Math.PI * 2;
      const c = Math.cos(th), s = Math.sin(th);
      for (const p of points) {
        pos.push(p[0], p[1] * c, p[1] * s);
      }
    }
    const idx = [];
    for (let k = 0; k < segs; k++) {
      const a = k * n, b = ((k + 1) % rings) * n;
      for (let i = 0; i < n - 1; i++) {
        idx.push(a + i, b + i, a + i + 1);
        idx.push(a + i + 1, b + i, b + i + 1);
      }
    }
    const g = new THREE.BufferGeometry();
    g.setAttribute("position", new THREE.Float32BufferAttribute(pos, 3));
    g.setIndex(idx);
    g.computeVertexNormals();
    return g;
  }

  // ---------- 电场线（子午面 RK4，再旋转成多条） ----------
  function traceLine(field, x0, r0, dir, maxSteps) {
    const pts = [];
    let x = x0, r = r0;
    const h = 0.045;
    for (let i = 0; i < maxSteps; i++) {
      pts.push([x, Math.abs(r)]);
      const f1 = field.meridional(x, r);
      const m1 = Math.hypot(f1.ex, f1.er) || 1;
      const f2 = field.meridional(x + (dir * h / 2) * f1.ex / m1, r + (dir * h / 2) * f1.er / m1);
      const m2 = Math.hypot(f2.ex, f2.er) || 1;
      const f3 = field.meridional(x + (dir * h / 2) * f2.ex / m2, r + (dir * h / 2) * f2.er / m2);
      const m3 = Math.hypot(f3.ex, f3.er) || 1;
      const f4 = field.meridional(x + dir * h * f3.ex / m3, r + dir * h * f3.er / m3);
      const m4 = Math.hypot(f4.ex, f4.er) || 1;
      x += dir * h * (f1.ex / m1 + 2 * f2.ex / m2 + 2 * f3.ex / m3 + f4.ex / m4) / 6;
      r += dir * h * (f1.er / m1 + 2 * f2.er / m2 + 2 * f3.er / m3 + f4.er / m4) / 6;
      if (!isFinite(x) || !isFinite(r)) break;
      if (Math.abs(x) > BOUND.x + 1.6 || r > BOUND.y + 1.4) break;
      if (r < 0.02) { r = Math.abs(r); }
      let near = false;
      for (const c of field.charges) if (Math.hypot(x - c.x, r) < 0.12) near = true;
      if (near) break;
    }
    return pts;
  }

  function seedLines(field, density) {
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

  // ---------- 主程序 ----------
  function init(mount, opts) {
    const cfg = Object.assign({ mode: "potential", title: "" }, opts || {});
    const sceneKey0 = cfg.scene || "singlePositive";
    const qs = new URLSearchParams(location.search);
    let state = {
      scene: (cfg.mode === "potential" && (qs.get("scene") === "uniform" || qs.get("scene") === "samePositive")) ? sceneKey0
        : (SCENES[qs.get("scene")] ? qs.get("scene") : sceneKey0),
      levels: (function () { const v = parseInt(qs.get("levels"), 10); return v >= 3 && v <= 13 ? v : 7; })(),
      density: 12,
      scale: (function () { const v = parseFloat(qs.get("scale")); return v >= 0.5 && v <= 2.5 ? v : 1; })(),
      view: qs.get("view") === "3d" ? "3d" : "2d"
    };

    const scene = new THREE.Scene();
    scene.background = new THREE.Color(COLOR.bg);
    scene.fog = new THREE.Fog(COLOR.bg, 26, 60);

    const renderer = new THREE.WebGLRenderer({ antialias: true });
    renderer.setPixelRatio(Math.min(devicePixelRatio || 1, 2));
    renderer.setSize(mount.clientWidth || 800, mount.clientHeight || 480, false);
    renderer.setClearColor(COLOR.bg, 1);
    mount.appendChild(renderer.domElement);

    // 相机
    const persp = new THREE.PerspectiveCamera(40, 1, 0.1, 200);
    const ortho = new THREE.OrthographicCamera(-1, 1, 1, -1, 0.1, 200);
    let cam = { theta: 0.62, phi: 1.14, dist: 16 };

    const upAxis = cfg.mode === "potential" ? new THREE.Vector3(0, 0, 1) : new THREE.Vector3(0, 1, 0);
    persp.up.copy(upAxis);
    ortho.up.set(0, 1, 0);   // 俯视图：屏幕 y 就是世界 y

    function applyCamera() {
      const w = mount.clientWidth, h = mount.clientHeight;
      const aspect = w / h;
      persp.aspect = aspect; persp.updateProjectionMatrix();
      persp.position.set(
        cam.dist * Math.sin(cam.phi) * Math.sin(cam.theta),
        cam.dist * Math.cos(cam.phi),
        cam.dist * Math.sin(cam.phi) * Math.cos(cam.theta)
      );
      persp.lookAt(0, 0, 0);

      const half = 3.35;
      ortho.left = -half * aspect; ortho.right = half * aspect;
      ortho.top = half; ortho.bottom = -half;
      ortho.position.set(0, 0, 30); ortho.lookAt(0, 0, 0);
      ortho.updateProjectionMatrix();
    }

    // 灯光
    scene.add(new THREE.AmbientLight(0xffffff, 0.95));
    const key = new THREE.DirectionalLight(0xbfe9ff, 1.5); key.position.set(5, 9, 12); scene.add(key);
    const fill = new THREE.DirectionalLight(0x88aacc, 0.6); fill.position.set(-6, -4, 6); scene.add(fill);

    // 组
    const gSlice = new THREE.Group();
    const gEquipSurface = new THREE.Group();
    const gEquipLine = new THREE.Group();
    const gFieldSpace = new THREE.Group();
    const gFieldPlane = new THREE.Group();
    const gArrows = new THREE.Group();
    const gCharges = new THREE.Group();
    const gProbe = new THREE.Group();
    const gTerrain = new THREE.Group();
    const gTerrainArrows = new THREE.Group();
    scene.add(gSlice, gEquipSurface, gEquipLine, gFieldSpace, gFieldPlane, gArrows, gCharges, gProbe,
      gTerrain, gTerrainArrows);

    const ZMAX = 3.2;
    const ZS = 0.62;                       // 电势 -> 高度 的比例
    // 地形图专用：软化半径更大，山包/山谷才圆润（真电势在电荷处发散）
    function softPotential(x, y) {
      let v = 0;
      for (const c of field.charges) {
        const dx = x - c.x;
        v += c.q / Math.sqrt(dx * dx + y * y + 0.36);
      }
      return v;
    }
    function hgt(x, y) {
      return ZMAX * Math.tanh(softPotential(x, y) * 1.55);
    }

    let field = makeField(state.scene);
    let probe = { x: 1.6, y: 1.0 };

    // ---------- 电势色图（z=0 截面） ----------
    function buildSlice() {
      gSlice.clear();
      const W = 512, H = 288;
      const cv = document.createElement("canvas");
      cv.width = W; cv.height = H;
      const g = cv.getContext("2d");
      const img = g.createImageData(W, H);
      for (let j = 0; j < H; j++) {
        for (let i = 0; i < W; i++) {
          const x = -BOUND.x + (i / (W - 1)) * BOUND.x * 2;
          const y = BOUND.y - (j / (H - 1)) * BOUND.y * 2;
          const v = field.potential(x, y, 0);
          const t = Math.tanh(v * state.scale * 0.9);
          const idx = (j * W + i) * 4;
          if (t >= 0) {
            img.data[idx] = 40 + 200 * t;
            img.data[idx + 1] = 90 - 70 * t;
            img.data[idx + 2] = 130 - 100 * t;
          } else {
            const a = -t;
            img.data[idx] = 40 - 10 * a;
            img.data[idx + 1] = 90 - 20 * a;
            img.data[idx + 2] = 130 + 110 * a;
          }
          img.data[idx + 3] = 255;
        }
      }
      g.putImageData(img, 0, 0);
      const tex = new THREE.CanvasTexture(cv);
      tex.colorSpace = THREE.SRGBColorSpace;
      const plane = new THREE.Mesh(
        new THREE.PlaneGeometry(BOUND.x * 2, BOUND.y * 2),
        new THREE.MeshBasicMaterial({ map: tex, transparent: true, opacity: state.view === "2d" ? 1 : 0.12, depthWrite: false })
      );
      plane.position.z = -0.02;
      gSlice.add(plane);

      // 坐标网格
      const grid = new THREE.GridHelper(BOUND.x * 2, 14, 0x1b3340, 0x14232c);
      grid.rotation.x = Math.PI / 2;
      grid.material.transparent = true; grid.material.opacity = 0.5;
      gSlice.add(grid);
    }

    // ---------- 等势面 ----------
    function levelList() {
      const n = state.levels;
      const out = [];
      if (field.sc.uniform) {
        const xs = [];
        for (let i = 0; i < n; i++) xs.push(-2.8 + (5.6 * i) / (n - 1));
        return xs.map(x => ({ kind: "plane", x }));
      }
      if (field.charges.length === 1) {
        const q = field.charges[0].q;
        for (let i = 0; i < n; i++) {
          const r = 0.55 + (3.2 * i) / (n - 1);
          out.push({ kind: "surface", level: q / Math.sqrt(r * r + SOFT2), sign: q });
        }
        return out;
      }
      // 双电荷：正负各一半
      const hasNeg = field.charges.some(c => c.q < 0);
      const vmax = 1.15;
      if (hasNeg) {
        const half = Math.floor(n / 2);
        for (let i = 0; i < half; i++) out.push({ kind: "surface", level: vmax * (i + 1) / half, sign: 1 });
        for (let i = 0; i < half; i++) out.push({ kind: "surface", level: -vmax * (i + 1) / half, sign: -1 });
      } else {
        for (let i = 0; i < n; i++) out.push({ kind: "surface", level: 0.18 + (vmax - 0.18) * i / (n - 1), sign: 1 });
      }
      return out;
    }

    function buildEquipotential() {
      gEquipSurface.clear(); gEquipLine.clear();
      const levels = levelList();

      for (const lv of levels) {
        if (lv.kind === "plane") {
          const geo = new THREE.PlaneGeometry(BOUND.y * 2, BOUND.y * 2);
          const mesh = new THREE.Mesh(geo, new THREE.MeshBasicMaterial({
            color: COLOR.plane, transparent: true, opacity: 0.16, side: THREE.DoubleSide, depthWrite: false
          }));
          mesh.position.x = lv.x;
          mesh.rotation.y = Math.PI / 2;
          gEquipSurface.add(mesh);
          const ring = new THREE.LineLoop(
            new THREE.BufferGeometry().setFromPoints([
              new THREE.Vector3(lv.x, -BOUND.y, -BOUND.y),
              new THREE.Vector3(lv.x, BOUND.y, -BOUND.y),
              new THREE.Vector3(lv.x, BOUND.y, BOUND.y),
              new THREE.Vector3(lv.x, -BOUND.y, BOUND.y)
            ]),
            new THREE.LineBasicMaterial({ color: 0x5f87a8, transparent: true, opacity: 0.5 })
          );
          gEquipLine.add(ring);
          continue;
        }

        const polys = contourPolys(field, lv.level, 180, 96);
        for (const poly of polys) {
          if (poly.length < 3) continue;
          if (Math.max(...poly.map(p => p[1])) < 0.02) continue;

          const colr = lv.sign > 0 ? COLOR.warm : COLOR.cool;

          // 2D：只画子午线（z=0 平面上的轮廓）
          const pts = poly.map(p => new THREE.Vector3(p[0], p[1], 0.01));
          const mir = poly.map(p => new THREE.Vector3(p[0], -p[1], 0.01));
          const lineMat = new THREE.LineBasicMaterial({ color: colr, transparent: true, opacity: 0.85 });
          gEquipLine.add(new THREE.Line(new THREE.BufferGeometry().setFromPoints(pts), lineMat));
          gEquipLine.add(new THREE.Line(new THREE.BufferGeometry().setFromPoints(mir), lineMat.clone()));

          // 3D：回转面
          const geo = revolve(poly, 48);
          const mesh = new THREE.Mesh(geo, new THREE.MeshBasicMaterial({
            color: colr, transparent: true, opacity: 0.07, side: THREE.DoubleSide, depthWrite: false
          }));
          gEquipSurface.add(mesh);

        }
      }
    }


    // ---------- 电势地形图：z = φ(x,y) ----------
    function contourPolysXY(field, level, sampler) {
      const nx = 150, ny = 86;
      const xmin = -BOUND.x, xmax = BOUND.x, ymin = -BOUND.y, ymax = BOUND.y;
      const dx = (xmax - xmin) / nx, dy = (ymax - ymin) / ny;
      const val = new Float32Array((nx + 1) * (ny + 1));
      for (let j = 0; j <= ny; j++) {
        for (let i = 0; i <= nx; i++) {
          val[j * (nx + 1) + i] = (sampler || ((a, b) => field.potential(a, b, 0)))(xmin + i * dx, ymin + j * dy);
        }
      }
      const pt = new Map(), adj = new Map();
      const kH = (i, j) => "H" + i + "_" + j;
      const kV = (i, j) => "V" + i + "_" + j;
      function pointH(i, j) {
        const k = kH(i, j);
        if (!pt.has(k)) {
          const a = val[j * (nx + 1) + i], b = val[j * (nx + 1) + i + 1];
          const t = (level - a) / ((b - a) || 1e-9);
          pt.set(k, [xmin + (i + t) * dx, ymin + j * dy]);
        }
        return k;
      }
      function pointV(i, j) {
        const k = kV(i, j);
        if (!pt.has(k)) {
          const a = val[j * (nx + 1) + i], b = val[(j + 1) * (nx + 1) + i];
          const t = (level - a) / ((b - a) || 1e-9);
          pt.set(k, [xmin + i * dx, ymin + (j + t) * dy]);
        }
        return k;
      }
      function link(a, b) {
        if (!adj.has(a)) adj.set(a, []);
        if (!adj.has(b)) adj.set(b, []);
        adj.get(a).push(b); adj.get(b).push(a);
      }
      for (let j = 0; j < ny; j++) {
        for (let i = 0; i < nx; i++) {
          const v00 = val[j * (nx + 1) + i], v10 = val[j * (nx + 1) + i + 1];
          const v01 = val[(j + 1) * (nx + 1) + i], v11 = val[(j + 1) * (nx + 1) + i + 1];
          let code = 0;
          if (v00 > level) code |= 1;
          if (v10 > level) code |= 2;
          if (v11 > level) code |= 4;
          if (v01 > level) code |= 8;
          if (code === 0 || code === 15) continue;
          const B_ = () => pointH(i, j), R_ = () => pointV(i + 1, j);
          const T_ = () => pointH(i, j + 1), L_ = () => pointV(i, j);
          switch (code) {
            case 1: case 14: link(L_(), B_()); break;
            case 2: case 13: link(B_(), R_()); break;
            case 3: case 12: link(L_(), R_()); break;
            case 4: case 11: link(R_(), T_()); break;
            case 6: case 9: link(B_(), T_()); break;
            case 7: case 8: link(L_(), T_()); break;
            case 5: link(L_(), B_()); link(R_(), T_()); break;
            case 10: link(L_(), T_()); link(B_(), R_()); break;
          }
        }
      }
      const used = new Set(), polys = [];
      function walk(start, closed) {
        const poly = [];
        let cur = start, prev = null;
        while (cur && !used.has(cur)) {
          used.add(cur);
          poly.push(pt.get(cur));
          const nxt = adj.get(cur).find(k => k !== prev && !used.has(k));
          prev = cur; cur = nxt;
        }
        if (poly.length > 2) { if (closed) poly.push(poly[0]); polys.push(poly); }
      }
      for (const k of adj.keys()) if (adj.get(k).length === 1) walk(k, false);
      for (const k of adj.keys()) if (!used.has(k)) walk(k, true);
      return polys;
    }

    function buildTerrain() {
      gTerrain.clear(); gTerrainArrows.clear();
      if (cfg.mode !== "potential") return;

      const NX = 72, NY = 46;
      const pos = [], col = [], idx = [];
      const cPos = new THREE.Color(0xff6a52), cMid = new THREE.Color(0x22303d), cNeg = new THREE.Color(0x4f7dff);
      for (let j = 0; j <= NY; j++) {
        for (let i = 0; i <= NX; i++) {
          const x = -BOUND.x + (2 * BOUND.x * i) / NX;
          const y = -BOUND.y + (2 * BOUND.y * j) / NY;
          const v = softPotential(x, y);
          pos.push(x, y, ZMAX * Math.tanh(v * 1.55));
          const t = Math.tanh(v * 1.4 * state.scale);
          const c = t >= 0
            ? cMid.clone().lerp(cPos, Math.min(1, t))
            : cMid.clone().lerp(cNeg, Math.min(1, -t));
          col.push(c.r, c.g, c.b);
        }
      }
      for (let j = 0; j < NY; j++) {
        for (let i = 0; i < NX; i++) {
          const a = j * (NX + 1) + i, b = a + 1, c = a + NX + 1, d = c + 1;
          idx.push(a, c, b, b, c, d);
        }
      }
      const geo = new THREE.BufferGeometry();
      geo.setAttribute("position", new THREE.Float32BufferAttribute(pos, 3));
      geo.setAttribute("color", new THREE.Float32BufferAttribute(col, 3));
      geo.setIndex(idx);
      geo.computeVertexNormals();

      gTerrain.add(new THREE.Mesh(geo, new THREE.MeshStandardMaterial({
        vertexColors: true, side: THREE.DoubleSide, roughness: 0.9, metalness: 0.02,
        transparent: true, opacity: 0.55
      })));
      gTerrain.add(new THREE.Mesh(geo, new THREE.MeshBasicMaterial({
        color: 0xa8cfe0, wireframe: true, transparent: true, opacity: 0.08
      })));

      // 等高线 = 等势线（都按软化后的地形算，保证和曲面一致）
      if (layers.equip) {
        const n = state.levels;
        const levels = [];
        const single = field.charges.length === 1;
        const neg = field.charges.some(c => c.q < 0);
        if (single) {
          const q = Math.sign(field.charges[0].q);
          for (let i = 0; i < n; i++) {
            const r = 0.55 + (2.9 * i) / (n - 1);
            levels.push({ level: q / Math.sqrt(r * r + 0.36), sign: q });
          }
        } else {
          const half = Math.max(2, Math.floor(n / 2));
          for (let i = 0; i < half; i++) {
            const r = 0.55 + (1.9 * i) / (half - 1);
            levels.push({ level: 1 / Math.sqrt(r * r + 0.36), sign: 1 });
            if (neg) levels.push({ level: -1 / Math.sqrt(r * r + 0.36), sign: -1 });
          }
        }
        for (const lv of levels) {
          const polys = contourPolysXY(field, lv.level, softPotential);
          for (const poly of polys) {
            if (poly.length < 3) continue;
            const pts = poly.map(q => new THREE.Vector3(q[0], q[1], hgt(q[0], q[1]) + 0.02));
            gTerrain.add(new THREE.Line(
              new THREE.BufferGeometry().setFromPoints(pts),
              new THREE.LineBasicMaterial({
                color: lv.sign > 0 ? 0xffd9b0 : 0xc3d6ff, transparent: true, opacity: 0.95
              })));
          }
        }
      }

      // 场线贴着地形走 + 箭头（参考视频那种）
      if (layers.field) {
        const lines = seedLines(field, Math.max(7, Math.round(state.density * 0.7)));
        for (const ln of lines) {
          for (const mir of [1, -1]) {
            // 场线画在底面（z≈0），不要"贴"到起伏上：贴上去会在山顶绕成一团
            const pts = ln.pts
              .filter(p => (p[1] > 1e-3 || mir > 0) &&
                Math.abs(p[0]) < BOUND.x - 0.15 && Math.abs(p[1]) < BOUND.y - 0.15)
              .map(p => new THREE.Vector3(p[0], p[1] * mir, 0.05));
            if (pts.length < 4) continue;
            gTerrainArrows.add(new THREE.Line(
              new THREE.BufferGeometry().setFromPoints(pts),
              new THREE.LineBasicMaterial({ color: 0xffd84d, transparent: true, opacity: 0.55 })
            ));
            for (const f of [0.35, 0.7]) {
              const i = Math.floor(pts.length * f);
              if (i < 2 || i >= pts.length - 1) continue;
              const dir = pts[i + 1].clone().sub(pts[i - 1]).normalize();
              const cone = new THREE.Mesh(
                new THREE.ConeGeometry(0.05, 0.15, 8),
                new THREE.MeshBasicMaterial({ color: 0xffd84d })
              );
              cone.position.copy(pts[i]);
              cone.quaternion.setFromUnitVectors(new THREE.Vector3(0, 1, 0), dir);
              gTerrainArrows.add(cone);
            }
          }
        }
      }
    }

    // ---------- 电场线 ----------
    function buildFieldLines() {
      gFieldSpace.clear(); gFieldPlane.clear(); gArrows.clear();
      const lines = seedLines(field, state.density);
      const AZ = 8;

      for (const ln of lines) {
        if (ln.pts.length < 3) continue;
        const col = field.sc.uniform ? 0x9fd8e8 : COLOR.field;

        // z=0 平面上的那条（2D 与 3D 都显示）
        const flat = ln.pts.map(p => new THREE.Vector3(p[0], p[1], 0.02));
        const flatM = ln.pts.map(p => new THREE.Vector3(p[0], -p[1], 0.02));
        const lineMatF = new THREE.LineBasicMaterial({ color: col, transparent: true, opacity: 0.8 });
        gFieldPlane.add(new THREE.Line(new THREE.BufferGeometry().setFromPoints(flat), lineMatF));
        gFieldPlane.add(new THREE.Line(new THREE.BufferGeometry().setFromPoints(flatM), lineMatF.clone()));
        addArrowheads(ln.pts, col, gArrows, 1);
        addArrowheads(ln.pts, col, gArrows, -1);

        // 绕 x 轴旋转出空间场线
        for (let k = 1; k < AZ; k++) {
          const th = (k / AZ) * Math.PI * 2;
          const c = Math.cos(th), s = Math.sin(th);
          const pts3 = ln.pts.map(p => new THREE.Vector3(p[0], p[1] * c, p[1] * s));
          gFieldSpace.add(new THREE.Line(
            new THREE.BufferGeometry().setFromPoints(pts3),
            new THREE.LineBasicMaterial({ color: col, transparent: true, opacity: 0.16 })
          ));
        }
      }

      // 匀强电场：整片平行箭头
      if (field.sc.uniform) {
        for (let y = -2.4; y <= 2.4; y += 1.2) {
          for (let z = -1.2; z <= 1.2; z += 1.2) {
            const a = new THREE.ArrowHelper(new THREE.Vector3(1, 0, 0),
              new THREE.Vector3(-2.6, y, z), 1.2, 0xa9e2f0, 0.2, 0.12);
            gArrows.add(a);
          }
        }
      }
    }

    function addArrowheads(pts, color, group, mir) {
      const n = pts.length;
      for (const f of [0.45, 0.75]) {
        const i = Math.floor(n * f);
        if (i < 2 || i >= n - 1) continue;
        const a = pts[i - 1], b = pts[i + 1];
        const dir = new THREE.Vector3(b[0] - a[0], (b[1] - a[1]) * mir, 0).normalize();
        const pos = new THREE.Vector3(pts[i][0], pts[i][1] * mir, 0.03);
        const cone = new THREE.Mesh(
          new THREE.ConeGeometry(0.045, 0.16, 8),
          new THREE.MeshBasicMaterial({ color })
        );
        cone.position.copy(pos);
        cone.quaternion.setFromUnitVectors(new THREE.Vector3(0, 1, 0), dir);
        group.add(cone);
      }
    }

    // ---------- 电荷 ----------
    function buildCharges() {
      gCharges.clear();
      if (field.sc.uniform) {
        for (const sx of [-3.6, 3.6]) {
          const plate = new THREE.Mesh(
            new THREE.BoxGeometry(0.08, BOUND.y * 1.6, BOUND.y * 1.6),
            new THREE.MeshStandardMaterial({
              color: sx < 0 ? COLOR.pos : COLOR.neg, transparent: true, opacity: 0.45, roughness: 0.5
            })
          );
          plate.position.x = sx;
          gCharges.add(plate);
          const lab = makeLabel(sx < 0 ? "＋" : "－", sx < 0 ? "#ffd3d6" : "#d3dcff", 1.0);
          lab.position.set(sx, 0, 0);
          gCharges.add(lab);
        }
        const eArrow = new THREE.ArrowHelper(new THREE.Vector3(1, 0, 0),
          new THREE.Vector3(-1.6, BOUND.y * 0.86, 0), 2.4, 0xffd84d, 0.3, 0.16);
        gCharges.add(eArrow);
        const eLab = makeLabel("E", "#ffd84d", 0.7);
        eLab.position.set(1.0, BOUND.y * 0.86 + 0.3, 0);
        gCharges.add(eLab);
        return;
      }
      for (const c of field.charges) {
        const col = c.q > 0 ? COLOR.pos : COLOR.neg;
        const ball = new THREE.Mesh(
          new THREE.SphereGeometry(0.22, 24, 18),
          new THREE.MeshStandardMaterial({ color: col, emissive: col, emissiveIntensity: 0.65, roughness: 0.35 })
        );
        const cz = cfg.mode === "potential" ? hgt(c.x, 0) : 0;
        ball.position.set(c.x, 0, cz);
        gCharges.add(ball);

        const halo = new THREE.Sprite(new THREE.SpriteMaterial({
          map: haloTex(col), transparent: true, opacity: 0.75,
          blending: THREE.AdditiveBlending, depthWrite: false
        }));
        halo.scale.set(1.0, 1.0, 1);
        halo.position.copy(ball.position);
        gCharges.add(halo);

        const lab = makeLabel(c.label, c.q > 0 ? "#ffd0d4" : "#c7d2ff", 0.72);
        lab.position.set(c.x, cfg.mode === "potential" ? 0 : 0.52, cz + (c.q > 0 ? 0.55 : -0.55));
        gCharges.add(lab);
      }
    }

    function haloTex(col) {
      const cv = document.createElement("canvas"); cv.width = cv.height = 128;
      const g = cv.getContext("2d");
      const grd = g.createRadialGradient(64, 64, 0, 64, 64, 64);
      const c = new THREE.Color(col);
      grd.addColorStop(0, `rgba(${c.r * 255 | 0},${c.g * 255 | 0},${c.b * 255 | 0},0.9)`);
      grd.addColorStop(1, `rgba(${c.r * 255 | 0},${c.g * 255 | 0},${c.b * 255 | 0},0)`);
      g.fillStyle = grd; g.fillRect(0, 0, 128, 128);
      return new THREE.CanvasTexture(cv);
    }

    function makeLabel(text, color, size) {
      const cv = document.createElement("canvas"); cv.width = 256; cv.height = 128;
      const g = cv.getContext("2d");
      g.font = 'bold 76px "Microsoft YaHei", sans-serif';
      g.fillStyle = color; g.textAlign = "center"; g.textBaseline = "middle";
      g.fillText(text, 128, 66);
      const tex = new THREE.CanvasTexture(cv);
      tex.colorSpace = THREE.SRGBColorSpace;
      const sp = new THREE.Sprite(new THREE.SpriteMaterial({ map: tex, transparent: true, depthWrite: false, depthTest: false }));
      sp.renderOrder = 20;
      sp.scale.set(size, size * 0.5, 1);
      return sp;
    }

    // ---------- 探针 ----------
    const probeMesh = new THREE.Mesh(
      new THREE.SphereGeometry(0.09, 16, 12),
      new THREE.MeshStandardMaterial({ color: 0xffd84d, emissive: 0xffb020, emissiveIntensity: 0.8 })
    );
    const probeRing = new THREE.Mesh(
      new THREE.RingGeometry(0.16, 0.2, 32),
      new THREE.MeshBasicMaterial({ color: 0xffd84d, transparent: true, opacity: 0.55, side: THREE.DoubleSide })
    );
    gProbe.add(probeMesh, probeRing);

    function updateProbe() {
      const pz = cfg.mode === "potential" && state.view !== "2d" ? hgt(probe.x, probe.y) + 0.03 : 0.06;
      probeMesh.position.set(probe.x, probe.y, pz);
      probeRing.position.set(probe.x, probe.y, pz);
      const v = field.potential(probe.x, probe.y, 0);
      const e = field.field(probe.x, probe.y, 0);
      if (cfg.onProbe) cfg.onProbe({ phi: v, e, scene: field.sc });
    }

    // ---------- 显示规则 ----------
    function applyView() {
      const is2d = state.view === "2d";
      const terrain = cfg.mode === "potential" && !is2d;
      gTerrain.visible = terrain && layers.equip;
      gTerrainArrows.visible = terrain && layers.field;
      gEquipSurface.visible = !is2d && !terrain && layers.equip;
      gFieldSpace.visible = !is2d && !terrain && layers.field;
      gFieldPlane.visible = !terrain && layers.field;
      gEquipLine.visible = layers.equip && (!terrain || is2d);
      gArrows.visible = !terrain && layers.field;
      gSlice.visible = layers.heat && !terrain;
      gSlice.children.forEach(ch => {
        if (ch.material && ch.material.map) ch.material.opacity = is2d ? 1 : 0.12;
      });
      applyCamera();
    }

    const layers = { heat: true, equip: true, field: true };

    // ---------- 交互 ----------
    let dragging = false, last = { x: 0, y: 0 };
    renderer.domElement.addEventListener("pointerdown", e => {
      if (state.view === "3d") {
        dragging = true; last = { x: e.clientX, y: e.clientY };
        renderer.domElement.style.cursor = "grabbing";
      } else if (cfg.mode === "potential") {
        const p = pickOnPlane(e);
        if (p) { probe = p; updateProbe(); }
        draggingProbe = true;
      }
    });
    let draggingProbe = false;
    addEventListener("pointerup", () => { dragging = false; draggingProbe = false; renderer.domElement.style.cursor = "grab"; });
    addEventListener("pointermove", e => {
      if (dragging) {
        cam.theta -= (e.clientX - last.x) * 0.008;
        cam.phi = Math.min(Math.PI - 0.12, Math.max(0.12, cam.phi - (e.clientY - last.y) * 0.008));
        last = { x: e.clientX, y: e.clientY };
        applyCamera();
      } else if (draggingProbe) {
        const p = pickOnPlane(e);
        if (p) { probe = p; updateProbe(); }
      }
    });
    renderer.domElement.addEventListener("wheel", e => {
      if (state.view !== "3d") return;
      e.preventDefault();
      cam.dist = Math.min(34, Math.max(8, cam.dist * (1 + e.deltaY * 0.0012)));
      applyCamera();
    }, { passive: false });

    function pickOnPlane(e) {
      const rect = renderer.domElement.getBoundingClientRect();
      const ndc = new THREE.Vector2(
        ((e.clientX - rect.left) / rect.width) * 2 - 1,
        -((e.clientY - rect.top) / rect.height) * 2 + 1
      );
      const ray = new THREE.Raycaster();
      ray.setFromCamera(ndc, state.view === "2d" ? ortho : persp);
      const plane = new THREE.Plane(new THREE.Vector3(0, 0, 1), 0);
      const hit = new THREE.Vector3();
      if (!ray.ray.intersectPlane(plane, hit)) return null;
      return {
        x: Math.max(-BOUND.x + 0.1, Math.min(BOUND.x - 0.1, hit.x)),
        y: Math.max(-BOUND.y + 0.1, Math.min(BOUND.y - 0.1, hit.y))
      };
    }

    // ---------- 重建 ----------
    function rebuildAll() {
      field = makeField(state.scene);
      buildSlice();
      buildEquipotential();
      buildFieldLines();
      buildTerrain();
      buildCharges();
      updateProbe();
      applyView();
      if (cfg.onScene) cfg.onScene({ scene: field.sc, charges: field.charges });
    }

    function setScene(k) { state.scene = k; rebuildAll(); }
    function setView(v) { state.view = v; applyView(); }
    function setLevels(n) { state.levels = n; buildEquipotential(); buildTerrain(); applyView(); }
    function setDensity(n) { state.density = n; buildFieldLines(); applyView(); }
    function setScale(s) { state.scale = s; buildSlice(); buildTerrain(); applyView(); }
    function setLayer(k, on) { layers[k] = on; applyView(); }

    function onResize() {
      const w = mount.clientWidth || 800, h = mount.clientHeight || 480;
      renderer.setSize(w, h, false);
      applyCamera();
    }
    addEventListener("resize", onResize);
    if (window.ResizeObserver) new ResizeObserver(onResize).observe(mount);
    requestAnimationFrame(onResize);

    rebuildAll();

    const clock = new THREE.Clock();
    (function loop() {
      requestAnimationFrame(loop);
      if (cfg.mode === "potential") {
        const t = clock.getElapsedTime();
        probeRing.scale.setScalar(1 + 0.12 * Math.sin(t * 3));
      }
      renderer.render(scene, state.view === "2d" ? ortho : persp);
    })();

    return { setScene, setView, setLevels, setDensity, setScale, setLayer, state };
  }

  window.ElectricLab = { init, SCENES };
})();
