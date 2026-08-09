"""Hand-authored neofetch-style info card SVG. Static, regenerate only when details change."""
import os
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "info-card.svg"
STATIC = os.environ.get("STATIC") == "1"

WIDTH = 490
PAD = 20
LINE_H = 24
TITLE_H = 34

ROWS = [
    ("Now", "Software Engineer I @ project44"),
    ("Prev", "xAI (Specialist), GSoC 2025 @ SugarLabs"),
    ("Stack", "Go, Java, Python, Spring Boot, PostgreSQL, Kafka"),
    ("AI/LLM", "RAG, LangChain, LangGraph, MCP"),
    ("Notes", "LeetCode top 3.28% (463) - 600+ DSA solved"),
]

LABEL_COLOR = "#7ee787"
VALUE_COLOR = "#c9d1d9"


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def main():
    height = TITLE_H + PAD * 2 + LINE_H * len(ROWS)

    rows = []
    for i, (label, value) in enumerate(ROWS):
        y = TITLE_H + PAD + i * LINE_H + 16
        delay = i * 90
        anim = "" if STATIC else f' class="line" style="animation-delay:{delay}ms"'
        rows.append(
            f'<g{anim} opacity="{1 if STATIC else 0}">'
            f'<text x="{PAD}" y="{y}" font-size="14" font-weight="700" fill="{LABEL_COLOR}">{label}</text>'
            f'<text x="{PAD + 74}" y="{y}" font-size="14" fill="{VALUE_COLOR}">{esc(value)}</text>'
            f'</g>'
        )

    style = "" if STATIC else '''
  .line { animation: typeIn 0.4s ease-out forwards; }
  @keyframes typeIn {
    0% { opacity: 0; transform: translateX(-8px); }
    100% { opacity: 1; transform: translateX(0); }
  }
'''

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{height}" viewBox="0 0 {WIDTH} {height}">
<style>
  text {{ font-family: 'SFMono-Regular', Consolas, 'Fira Code', monospace; }}
  {style}
</style>
<rect width="{WIDTH}" height="{height}" rx="8" fill="#0d1117" stroke="#30363d"/>
<rect width="{WIDTH}" height="{TITLE_H}" rx="8" fill="#161b22"/>
<rect y="{TITLE_H - 8}" width="{WIDTH}" height="8" fill="#161b22"/>
<circle cx="18" cy="{TITLE_H / 2}" r="6" fill="#ff5f56"/>
<circle cx="38" cy="{TITLE_H / 2}" r="6" fill="#ffbd2e"/>
<circle cx="58" cy="{TITLE_H / 2}" r="6" fill="#27c93f"/>
<text x="{WIDTH / 2}" y="{TITLE_H / 2 + 5}" font-size="13" fill="#8b949e" text-anchor="middle">aditya@github</text>
{''.join(rows)}
</svg>
'''
    OUT.write_text(svg)
    print(f"wrote {OUT} ({WIDTH}x{height})")


if __name__ == "__main__":
    main()
