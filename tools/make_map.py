#!/usr/bin/env python3
"""Genera data/pr_map.svg (78 municipios) desde un GeoJSON de condados de EE.UU. (FIPS 72 = Puerto Rico).
Uso: python3 tools/make_map.py ruta/al/geojson-counties-fips.json"""
import json, math, sys, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
d = json.load(open(sys.argv[1], encoding="utf-8"))
feats = [f for f in d["features"] if f["id"].startswith("72")]
LAT0 = 18.2; K = math.cos(math.radians(LAT0))
W = 1000

def polys(g):
    return [g["coordinates"]] if g["type"] == "Polygon" else g["coordinates"]

def keep(ring):  # descarta Mona, Monito y Desecheo
    lon = sum(p[0] for p in ring) / len(ring)
    return lon > -67.3

allpts = [p for f in feats for poly in polys(f["geometry"]) for ring in poly if keep(ring) for p in ring]
minx = min(p[0] for p in allpts) * K; maxx = max(p[0] for p in allpts) * K
maxy = max(p[1] for p in allpts); miny = min(p[1] for p in allpts)
S = W / (maxx - minx); H = (maxy - miny) * S
def proj(p): return ((p[0] * K - minx) * S, (maxy - p[1]) * S)

def dp(pts, eps):
    if len(pts) < 3: return pts
    (x1, y1), (x2, y2) = pts[0], pts[-1]
    dx, dy = x2 - x1, y2 - y1; n = math.hypot(dx, dy) or 1e-9
    idx, dmax = 0, 0
    for i in range(1, len(pts) - 1):
        x, y = pts[i]; dd = abs(dy * x - dx * y + x2 * y1 - y2 * x1) / n
        if dd > dmax: idx, dmax = i, dd
    if dmax > eps: return dp(pts[:idx + 1], eps)[:-1] + dp(pts[idx:], eps)
    return [pts[0], pts[-1]]

out = []
for f in sorted(feats, key=lambda f: f["properties"]["NAME"]):
    name = f["properties"]["NAME"]; parts = []; cx = cy = area = 0
    for poly in polys(f["geometry"]):
        for ri, ring in enumerate(poly):
            if not keep(ring): continue
            raw = [proj(p) for p in ring]; h = len(raw) // 2
            pts = dp(raw[:h + 1], 0.6)[:-1] + dp(raw[h:], 0.6)
            if len(pts) < 4: continue
            parts.append("M" + "L".join(f"{x:.1f},{y:.1f}" for x, y in pts) + "Z")
            if ri == 0 or area == 0:
                a = abs(sum(pts[i][0] * pts[i + 1][1] - pts[i + 1][0] * pts[i][1] for i in range(len(pts) - 1))) / 2
                cx += sum(p[0] for p in pts) / len(pts) * a; cy += sum(p[1] for p in pts) / len(pts) * a; area += a
    if not parts: continue
    cx, cy = cx / area, cy / area
    out.append(f'<path class="muni" data-name="{name}" data-cx="{cx:.0f}" data-cy="{cy:.0f}" d="{"".join(parts)}"><title>{name}</title></path>')

svg = f'<svg class="prmap" viewBox="0 0 {W} {H:.0f}" role="img" aria-label="Mapa de los 78 municipios de Puerto Rico">' + "".join(out) + "</svg>"
open(os.path.join(ROOT, "data", "pr_map.svg"), "w", encoding="utf-8").write(svg)
print(len(out), "municipios ·", f"{len(svg)/1024:.0f} KB · viewBox 0 0 {W} {H:.0f}")
