"""The building plan of the agency, drawn the same way in every episode (production-guide.md, The building plan).

draw_plan(lit) draws the plan at 1920 by 1080 with the rooms named in lit in full colour and the rest faded; lit=None
draws every room in full colour. Run as a script it writes the full plan and one plan for each episode into out/.
"""

from __future__ import annotations

import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

W, H = 1920, 1080
BG = (247, 246, 242)
INK = (31, 31, 31)
MUTED = (110, 110, 105)
DROP = (192, 57, 43)

# Border and fill for each kind of step, as in flow.png.
KIND = {
    "model": ((224, 150, 47), (253, 241, 220)),
    "code": ((61, 111, 168), (230, 238, 249)),
    "person": ((138, 91, 179), (242, 232, 248)),
    "stored": ((143, 143, 138), (236, 235, 230)),
}

FONT_DIRS = [Path("/usr/share/fonts/truetype/liberation"), Path("/Library/Fonts"), Path("/System/Library/Fonts/Supplemental")]
FONT_FILES = {
    "serif-bold": ["LiberationSerif-Bold.ttf", "Georgia Bold.ttf"],
    "sans": ["LiberationSans-Regular.ttf", "Arial.ttf"],
    "sans-bold": ["LiberationSans-Bold.ttf", "Arial Bold.ttf"],
}


def font(face: str, size: int) -> ImageFont.FreeTypeFont:
    for d in FONT_DIRS:
        for name in FONT_FILES[face]:
            if (d / name).exists():
                return ImageFont.truetype(str(d / name), size)
    return ImageFont.load_default(size)


# Each room: its id, name, a line on what it does, its kind, and its box (left, top, right, bottom).
ROOMS = [
    ("wire", "Wire room", "nine collectors,\none shape for every item", "code", (250, 330, 520, 700)),
    ("barrier", "Barrier", "is this\non topic?", "model", (550, 440, 670, 590)),
    ("prebook", "Filing room", "the Pre-Book,\nkept 21 days", "stored", (700, 400, 900, 630)),
    ("ai", "AI newsroom", "choose, check,\nwrite, tag", "model", (940, 300, 1180, 500)),
    ("et", "Ethiopia newsroom", "choose, check,\nwrite, tag", "model", (940, 530, 1180, 730)),
    ("book", "The Book", "every note,\nkept for good", "stored", (1220, 400, 1420, 630)),
    ("print", "Print room", "issues on\na timetable", "model", (1460, 400, 1660, 630)),
    ("readers", "Readers' room", "questions answered from the Book", "model", (1220, 820, 1660, 940)),
    ("server", "Server room", "one MacBook Air runs it all", "code", (250, 820, 670, 940)),
    ("chief", "Editor-in-chief", "the rules, versioned", "person", (250, 150, 580, 240)),
    ("finance", "Finance", "budgets and costs", "person", (620, 150, 950, 240)),
    ("lab", "Model lab", "benchmarks", "person", (990, 150, 1320, 240)),
    ("health", "Health desk", "alerts at 06:30", "person", (1330, 150, 1660, 240)),
]
SOURCES = ["feeds", "X posts", "newsletters", "Telegram", "podcasts", "papers", "WeChat"]
OUTLETS = ["email", "LinkedIn", "Telegram", "the site", "YouTube"]

# Which rooms each episode lights (production-guide.md); "sources" and "outlets" are the two edges of the plan.
EPISODES = {
    1: None, 2: {"wire", "sources"}, 3: {"barrier", "prebook"}, 4: {"ai", "et"}, 5: {"book"},
    6: {"print", "outlets"}, 7: {"readers"}, 8: {"server"}, 9: {"lab", "finance"}, 10: None,
}


def _fade(c: tuple[int, int, int], on: bool, amount: float = 0.78) -> tuple[int, int, int]:
    if on:
        return c
    return tuple(round(v + (b - v) * amount) for v, b in zip(c, BG))


def _arrow(d: ImageDraw.ImageDraw, a: tuple[int, int], b: tuple[int, int], colour, width: int = 3) -> None:
    d.line([a, b], fill=colour, width=width)
    (x1, y1), (x2, y2) = a, b
    if x1 == x2:
        s = 1 if y2 > y1 else -1
        d.polygon([(x2, y2), (x2 - 8, y2 - 14 * s), (x2 + 8, y2 - 14 * s)], fill=colour)
    else:
        s = 1 if x2 > x1 else -1
        d.polygon([(x2, y2), (x2 - 14 * s, y2 - 8), (x2 - 14 * s, y2 + 8)], fill=colour)


def _centred(d: ImageDraw.ImageDraw, box, lines: list[tuple[str, ImageFont.FreeTypeFont, tuple]], gap: int = 8) -> None:
    left, top, right, bottom = box
    heights = [f.getbbox(t)[3] - f.getbbox(t)[1] for t, f, _ in lines]
    y = (top + bottom - sum(heights) - gap * (len(lines) - 1)) / 2
    for (t, f, c), h in zip(lines, heights):
        w = d.textlength(t, font=f)
        d.text(((left + right - w) / 2, y - f.getbbox(t)[1]), t, font=f, fill=c)
        y += h + gap


def draw_plan(lit: set[str] | None = None, title: str | None = None) -> Image.Image:
    on = (lambda r: True) if lit is None else (lambda r: r in lit)
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    name_f, line_f, small_f = font("serif-bold", 28), font("sans", 19), font("sans", 18)
    box = {r[0]: r[4] for r in ROOMS}

    if title:
        d.text((250, 60), title, font=font("serif-bold", 40), fill=INK)
    else:
        d.text((250, 70), "The Observatory", font=font("serif-bold", 40), fill=INK)
        d.text((610, 86), "a news agency in one laptop", font=font("sans", 22), fill=MUTED)
    d.line([(250, 125), (1660, 125)], fill=_fade(MUTED, True, 0.5), width=1)

    # The flow of copy, drawn under the rooms.
    flow = _fade(MUTED, lit is None or bool(lit - {"chief", "finance", "lab", "health", "server"}), 0.6)
    mid = 515
    for a, b in [("wire", "barrier"), ("barrier", "prebook")]:
        _arrow(d, (box[a][2], mid), (box[b][0], mid), flow)
    for room in ("ai", "et"):
        y = (box[room][1] + box[room][3]) // 2
        d.line([(box["prebook"][2], mid), (915, mid), (915, y)], fill=flow, width=3)
        _arrow(d, (915, y), (box[room][0], y), flow)
        d.line([(box[room][2], y), (1200, y), (1200, mid)], fill=flow, width=3)
    _arrow(d, (1200, mid), (box["book"][0], mid), flow)
    _arrow(d, (box["book"][2], mid), (box["print"][0], mid), flow)
    _arrow(d, (1320, box["book"][3]), (1320, box["readers"][1]), flow)
    dropped = _fade(DROP, lit is None or "barrier" in lit, 0.7)
    x = (box["barrier"][0] + box["barrier"][2]) // 2
    for y in range(box["barrier"][3], box["barrier"][3] + 60, 12):
        d.line([(x, y), (x, y + 6)], fill=dropped, width=3)
    d.polygon([(x, box["barrier"][3] + 72), (x - 8, box["barrier"][3] + 58), (x + 8, box["barrier"][3] + 58)], fill=dropped)
    d.text((x + 14, box["barrier"][3] + 50), "dropped", font=small_f, fill=dropped)

    # Sources on the left edge and destinations on the right.
    src_on = lit is None or "sources" in lit or "wire" in lit
    for k, s in enumerate(SOURCES):
        y = 350 + k * 50
        d.text((70, y - 11), s, font=small_f, fill=_fade(INK, src_on))
        _arrow(d, (190, y), (box["wire"][0], y), _fade(MUTED, src_on, 0.7), 2)
    out_on = lit is None or "outlets" in lit or "print" in lit
    for k, s in enumerate(OUTLETS):
        y = 420 + k * 48
        _arrow(d, (box["print"][2], y), (1745, y), _fade(MUTED, out_on, 0.7), 2)
        d.text((1758, y - 11), s, font=small_f, fill=_fade(INK, out_on))

    for rid, name, line, kind, b in ROOMS:
        border, fill = KIND[kind]
        lit_here = on(rid)
        d.rectangle(b, fill=_fade(fill, lit_here), outline=_fade(border, lit_here), width=4 if lit_here and lit else 3)
        size = 28
        while size > 18 and d.textlength(name, font=font("serif-bold", size)) > b[2] - b[0] - 24:
            size -= 1
        lines = [(name, font("serif-bold", size), _fade(INK, lit_here))]
        lines += [(t, line_f, _fade(MUTED, lit_here)) for t in line.split("\n")]
        _centred(d, b, lines)

    d.text((250, 990), "orange: a language model   blue: ordinary code   purple: a person   grey: something kept",
           font=small_f, fill=_fade(MUTED, True, 0.3))
    return img


if __name__ == "__main__":
    out = Path(sys.argv[1] if len(sys.argv) > 1 else "out")
    out.mkdir(parents=True, exist_ok=True)
    draw_plan().save(out / "plan.png")
    for n, lit in EPISODES.items():
        if lit:
            draw_plan(lit).save(out / f"plan-ep{n:02d}.png")
