"""Render data/contributions.json as an animated contribution heatmap SVG."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data" / "contributions.json"
OUT = ROOT / "contrib-heatmap.svg"

PALETTE = ["#161b22", "#0e4429", "#006d32", "#26a641", "#39d353"]
CELL = 11
GAP = 3
STEP = CELL + GAP
MARGIN_LEFT = 10
MARGIN_TOP = 10
LEGEND_H = 26
FOOTER_H = 22


def main():
    data = json.loads(DATA.read_text())
    days = data["days"]
    stats = data["stats"]

    weeks = max(d["week"] for d in days) + 1

    grid_w = weeks * STEP - GAP
    grid_h = 7 * STEP - GAP
    width = MARGIN_LEFT * 2 + grid_w
    height = MARGIN_TOP + grid_h + LEGEND_H + FOOTER_H

    rects = []
    for d in days:
        x = MARGIN_LEFT + d["week"] * STEP
        y = MARGIN_TOP + d["day"] * STEP
        delay = (d["week"] + d["day"]) * 6
        color = PALETTE[d["level"]]
        title = f"{d['count']} contribution{'s' if d['count'] != 1 else ''} on {d['date']}"
        rects.append(
            f'<rect x="{x}" y="{y - 6}" width="{CELL}" height="{CELL}" rx="2" ry="2" '
            f'fill="{color}" class="box" style="animation-delay:{delay}ms"><title>{title}</title></rect>'
        )

    legend_y = MARGIN_TOP + grid_h + 14
    legend_x = width - MARGIN_LEFT - (len(PALETTE) * (CELL + 4) + 60)
    legend_boxes = []
    for i, color in enumerate(PALETTE):
        lx = legend_x + 40 + i * (CELL + 4)
        legend_boxes.append(f'<rect x="{lx}" y="{legend_y - 9}" width="{CELL}" height="{CELL}" rx="2" fill="{color}"/>')

    footer_y = MARGIN_TOP + grid_h + LEGEND_H + 16
    streak = stats["current_streak"]
    longest = stats["longest_streak"]
    footer = (
        f"{stats['total']} contributions in the last year &#183; "
        f"current streak {streak}d &#183; longest streak {longest}d"
    )

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
<style>
  text {{ font-family: 'SFMono-Regular', Consolas, 'Fira Code', monospace; fill: #8b949e; }}
  .box {{ opacity: 0; transform-box: fill-box; transform-origin: center; animation: reveal 0.5s ease-out forwards; }}
  @keyframes reveal {{
    0% {{ opacity: 0; transform: translateY(-6px); }}
    100% {{ opacity: 1; transform: translateY(0); }}
  }}
</style>
<rect width="{width}" height="{height}" fill="#0d1117"/>
{''.join(rects)}
<text x="{legend_x}" y="{legend_y}" font-size="11">Less</text>
{''.join(legend_boxes)}
<text x="{legend_x + 40 + len(PALETTE) * (CELL + 4) + 6}" y="{legend_y}" font-size="11">More</text>
<text x="{MARGIN_LEFT}" y="{footer_y}" font-size="12">{footer}</text>
</svg>
'''
    OUT.write_text(svg)
    print(f"wrote {OUT} ({width}x{height})")


if __name__ == "__main__":
    main()
