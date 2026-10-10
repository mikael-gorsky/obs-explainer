"""Episode 1, A news agency with no staff: the draft cut, drawn from its script (episodes/01-*/script.md).

python3 render/ep01.py writes out/ep01-draft.mp4. Each scene's pictures begin with the sentences they illustrate:
cue(k) is the moment sentence k of the scene begins.
"""

from __future__ import annotations

import random
import re
import sys
from functools import lru_cache
from pathlib import Path

from PIL import Image, ImageDraw

import core
from core import (OUT, ROOT, arrow, blank, ease, mix, paste_alpha, progress, scenes_from_script, screenshot,
                  text_centred, voice)
from plan import BG, DROP, H, INK, KIND, MUTED, ROOMS, W, draw_plan, font

SCRIPT = next((ROOT / "episodes").glob("01-*")) / "script.md"
ORANGE = KIND["model"][0]
BLUE = KIND["code"][0]
WHITE = (255, 255, 255)


def faded(img: Image.Image, x: float) -> Image.Image:
    """img blended toward the background by x (0 keeps it, 1 leaves only the background)."""
    return Image.blend(img, Image.new("RGB", img.size, BG), x) if x > 0 else img


# Scene 1. The morning issue.

rng = random.Random(7)
CARDS = [(rng.uniform(-60, W - 100), rng.uniform(0, 2 * H), rng.choice(["EN"] * 6 + ["ZH", "AM"]), rng.uniform(0.8, 1.2))
         for _ in range(200)]


def scene1(t: float, sc: core.Scene) -> Image.Image:
    img = blank()
    d = ImageDraw.Draw(img)
    gather = progress(t, 2.6, 1.4)
    small = font("sans-bold", 16)
    for x0, y0, lang, speed in CARDS:
        y = (y0 - t * 140 * speed) % (2 * H) - H / 2
        x, yy = x0 + (W / 2 - 75 - x0) * gather, y + (H / 2 - 40 - y) * gather
        c = mix(MUTED, BG, 0.25 + 0.75 * gather)
        if gather >= 1:
            break
        d.rectangle((x, yy, x + 150, yy + 80), fill=mix(WHITE, BG, gather), outline=c, width=2)
        d.line((x + 12, yy + 40, x + 130, yy + 40), fill=mix((200, 200, 195), BG, gather), width=4)
        d.line((x + 12, yy + 56, x + 100, yy + 56), fill=mix((200, 200, 195), BG, gather), width=4)
        d.text((x + 12, yy + 10), lang, font=small, fill=c)
    clock = "06:59" if t < 2.2 else "07:00"
    d.rectangle((1640, 40, 1880, 130), fill=WHITE, outline=INK, width=3)
    text_centred(d, (1760, 52), clock, font("sans-bold", 56), INK if t >= 2.2 else MUTED)

    grow = progress(t, 3.4, 1.0)
    if grow > 0:
        w, h = round(760 * (0.3 + 0.7 * grow)), round(900 * (0.3 + 0.7 * grow))
        mail = _email()
        dim = 0.5 * progress(t, sc.starts[2], 0.8)
        paste_alpha(img, faded(mail.resize((w, h)), dim), ((W - w) // 2, 150 + (900 - h) // 2), grow)
        if dim > 0:
            d.rectangle((0, 470, W, 640), fill=mix(BG, BG, 0))
            text_centred(d, (W / 2, 500), "no editor, no staff", font("serif-bold", 96), mix(BG, INK, dim * 2))
    return img


@lru_cache(None)
def _email() -> Image.Image:
    return screenshot("S01", "an AI daily email, as a reader sees it", (760, 900))


# Scene 2. The size of the problem.

KINDS = ["posts", "articles", "newsletters", "papers", "podcasts", "videos", "Telegram"]


def _icon(d: ImageDraw.ImageDraw, x: int, y: int, kind: str, c) -> None:
    if kind == "podcasts":
        d.ellipse((x + 30, y, x + 70, y + 50), outline=c, width=4)
        d.line((x + 50, y + 50, x + 50, y + 75), fill=c, width=4)
    elif kind == "videos":
        d.rectangle((x + 5, y + 5, x + 95, y + 70), outline=c, width=4)
        d.polygon([(x + 40, y + 20), (x + 40, y + 55), (x + 68, y + 37)], fill=c)
    elif kind == "Telegram":
        d.polygon([(x + 10, y + 40), (x + 90, y + 8), (x + 70, y + 72)], outline=c, width=4)
    else:
        d.rectangle((x + 15, y, x + 85, y + 75), outline=c, width=4)
        for k in range(3 if kind != "posts" else 2):
            d.line((x + 25, y + 18 + k * 16, x + 75, y + 18 + k * 16), fill=c, width=3)


def scene2(t: float, sc: core.Scene) -> Image.Image:
    img = blank()
    d = ImageDraw.Draw(img)
    cue = sc.starts
    away = progress(t, cue[4], 0.6)
    a = 1 - away
    if a > 0:
        p = progress(t, 0.2, 0.8)
        text_centred(d, (W / 2, 90), "The Observatory", font("serif-bold", 64), mix(BG, INK, p * a))
        text_centred(d, (W / 2, 170), "a news agency that runs on one laptop", font("sans", 30), mix(BG, MUTED, p * a))
        n = round(575 * progress(t, cue[1], 1.6))
        if t >= cue[1]:
            text_centred(d, (W / 2, 250), f"{n}", font("serif-bold", 150), mix(BG, INK, a))
            text_centred(d, (W / 2, 420), "sources", font("sans", 34), mix(BG, MUTED, a))
        b = progress(t, cue[2], 1.2)
        if b > 0:
            parts = [(497, "English", BLUE), (47, "Chinese", ORANGE), (29, "Amharic", KIND["person"][0]),
                     (2, "French and Russian", MUTED)]
            x, total, y = 360, 1200, 500
            for k, (v, name, c) in enumerate(parts):
                share = progress(t, cue[2] + 0.5 * k, 0.8)
                w = total * v / 575
                d.rectangle((x, y, x + max(2, w * share), y + 60), fill=mix(BG, c, a * share))
                if share > 0.5 and v > 20:
                    label = f"{v} {name}"
                    tx = x + 14 if w > 300 else x + w / 2 - d.textlength(label, font=font("sans", 24)) / 2
                    ty = y + 16 if w > 300 else y + 74 + 34 * (k - 1)
                    d.text((tx, ty), label, font=font("sans", 24), fill=mix(BG, WHITE if w > 300 else INK, a))
                x += w
        for k, kind in enumerate(KINDS):
            p = progress(t, cue[3] + 0.35 * k, 0.5)
            if p > 0:
                x = 260 + k * 205
                _icon(d, x, 720, kind, mix(BG, INK, p * a))
                text_centred(d, (x + 50, 812), kind, font("sans", 24), mix(BG, MUTED, p * a))
    if away > 0:
        _funnel(d, t - cue[4], away, sc, t)
    q = progress(t, cue[5], 0.8)
    if q > 0:
        text_centred(d, (W / 2, 940), "How does a program choose twenty stories out of thousands?",
                     font("serif-bold", 50), mix(BG, INK, q))
    return img


FUNNEL_DOTS = [(rng.uniform(560, 1360), rng.uniform(0, 3.0), rng.uniform(0.0, 1.0)) for _ in range(500)]


def _funnel(d: ImageDraw.ImageDraw, s: float, a: float, sc, t) -> None:
    top, neck, bottom = 140, 620, 700
    c = mix(BG, INK, a)
    d.line([(520, top), (900, neck), (900, bottom)], fill=c, width=4)
    d.line([(1400, top), (1020, neck), (1020, bottom)], fill=c, width=4)
    for x0, delay, lane in FUNNEL_DOTS:
        k = s - delay
        if k < 0:
            continue
        y = top - 60 + k * 260
        if y > neck:
            continue
        half = 440 - (440 - 60) * max(0.0, (y - top) / (neck - top))
        x = 960 + (x0 - 960) * half / 440
        d.ellipse((x - 5, y - 5, x + 5, y + 5), fill=mix(BG, MUTED, a))
    out = int(20 * progress(s, 1.5, 3.0))
    for k in range(out):
        y = bottom + 10 + k * 9
        d.rectangle((900, y, 1020, y + 5), fill=mix(BG, ORANGE, a))
    if out:
        d.text((1050, bottom + 60), f"{out} stories", font=font("sans-bold", 34), fill=mix(BG, INK, a))


# Scene 3. What the agency produces.

AI_PUBS = [("AI daily", "Sunday to Friday, 07:00"), ("Science corner", "Friday, 08:00"),
           ("Agentic Software Engineering", "Friday, 08:00"), ("Spoken AI daily and shorts", "every day")]
ET_PUBS = [("Ethiopia daily brief", "Sunday to Friday, 07:00"), ("Ethiopian banking and fintech", "Friday, 07:00"),
           ("Ethiopia AI weekly", "Wednesday, 07:00")]
THUMBS = [("S02", "a post in the AI Telegram channel"), ("S03", "the public site's home page"),
          ("S04", "a frame of the spoken AI daily"), ("S05", "a frame of an ASE short")]


def scene3(t: float, sc: core.Scene) -> Image.Image:
    img = blank()
    d = ImageDraw.Draw(img)
    cue = sc.starts
    away = progress(t, cue[6], 0.6)
    a = 1 - away
    cols = [(140, "AI desk", "artificial intelligence, and AI that writes software", AI_PUBS, 1, 4),
            (1000, "Ethiopia desk", "news in and about Ethiopia, the economy and banking first", ET_PUBS, 2, 5)]
    for x, head, line, pubs, line_cue, pubs_cue in cols:
        p = progress(t, cue[0], 0.8) * a
        d.text((x, 90), head, font=font("serif-bold", 56), fill=mix(BG, INK, p))
        d.line((x, 170, x + 780, 170), fill=mix(BG, INK, p), width=2)
        q = progress(t, cue[line_cue], 0.8) * a
        d.text((x, 190), line, font=font("sans", 26), fill=mix(BG, MUTED, q))
        span = sc.ends[pubs_cue] - cue[pubs_cue]
        for k, (name, when) in enumerate(pubs):
            r = progress(t, cue[pubs_cue] + span * k / len(pubs), 0.5) * a
            if r <= 0:
                continue
            y = 260 + k * 88 + round(20 * (1 - r))
            border, fill = KIND["model"]
            d.rectangle((x, y, x + 780, y + 70), fill=mix(BG, fill, r), outline=mix(BG, border, r), width=3)
            d.text((x + 20, y + 20), name, font=font("sans-bold", 28), fill=mix(BG, INK, r))
            w = d.textlength(when, font=font("sans", 24))
            d.text((x + 760 - w, y + 23), when, font=font("sans", 24), fill=mix(BG, MUTED, r))
    span = sc.ends[4] - cue[4]
    for k, (name, what) in enumerate(THUMBS):
        r = progress(t, cue[4] + span * k / 4, 0.5) * a
        if r > 0:
            paste_alpha(img, _thumb(name, what), (140 + k * 420, 680), r)
    s = progress(t, cue[6], 0.8)
    if s > 0:
        paste_alpha(img, _thumb("S06", "a reader's subscription page: channel, hour, language", (1100, 760)),
                    (410, 160), s)
    return img


@lru_cache(None)
def _thumb(name: str, what: str, size=(390, 300)) -> Image.Image:
    return screenshot(name, what, size)


# Scene 4. No staff and one machine.

def scene4(t: float, sc: core.Scene) -> Image.Image:
    img = blank()
    d = ImageDraw.Draw(img)
    cue = sc.starts
    p = progress(t, 0.1, 0.8)
    ink = mix(BG, INK, p)
    d.rectangle((780, 420, 1140, 640), fill=mix(BG, WHITE, p), outline=ink, width=5)
    for k in range(5):
        d.line((810, 455 + k * 34, 1110 - (k % 2) * 80, 455 + k * 34), fill=mix(BG, (205, 205, 200), p), width=6)
    d.polygon([(730, 640), (1190, 640), (1230, 675), (690, 675)], fill=mix(BG, WHITE, p), outline=ink)
    d.line((690, 675, 1230, 675), fill=ink, width=5)
    text_centred(d, (960, 690), "one laptop", font("sans", 28), mix(BG, MUTED, p))

    ways = [((690, 530), (370, 530), "sources", (190, 512)), ((960, 410), (960, 210), "language models", (960, 160)),
            ((1230, 530), (1550, 530), "readers", (1660, 512))]
    for k, (a, b, label, at) in enumerate(ways):
        g = progress(t, cue[1] + 0.9 * k, 0.8)
        if g > 0:
            end = (a[0] + (b[0] - a[0]) * g, a[1] + (b[1] - a[1]) * g)
            arrow(d, a, end, INK, 5, 20)
            text_centred(d, (at[0], at[1]), label, font("sans-bold", 34), mix(BG, INK, g))
    g = progress(t, cue[2], 0.9)
    if g > 0:
        y_end = 1040 - (1040 - 830) * g
        for y in range(1040, round(y_end), -24):
            d.line((960, y, 960, max(y_end, y - 12)), fill=DROP, width=5)
        if g >= 1:
            c = progress(t, cue[2] + 0.9, 0.3)
            col = mix(BG, DROP, c)
            d.line((935, 770, 985, 820), fill=col, width=8)
            d.line((985, 770, 935, 820), fill=col, width=8)
    g = progress(t, cue[4] + 1.0, 0.6)
    if g > 0:
        d.rectangle((1180, 300, 1500, 380), fill=mix(BG, WHITE, g), outline=mix(BG, INK, g), width=3)
        text_centred(d, (1340, 318), "about $7 a week", font("sans-bold", 36), mix(BG, INK, g))
    g = progress(t, cue[5], 0.6)
    if g > 0:
        d.text((1300, 640), "Cheap models make mistakes", font=font("serif-bold", 38), fill=mix(BG, ORANGE, g))
    span = sc.ends[6] - cue[6]
    for k, phrase in enumerate(["misreads the source", "adds a detail", "believes the press release"]):
        g = progress(t, cue[6] + span * k / 3, 0.5)
        if g > 0:
            d.text((1300, 710 + k * 56), phrase, font=font("sans", 34), fill=mix(BG, ORANGE, g))
    return img


# Scene 5. Documents before code.

def _page(md: Path, size=(500, 660)) -> Image.Image:
    img = Image.new("RGB", size, WHITE)
    d = ImageDraw.Draw(img)
    d.rectangle((0, 0, size[0] - 1, size[1] - 1), outline=(190, 190, 185), width=2)
    y, width = 30, size[0] - 60
    for raw in md.read_text().splitlines():
        line = re.sub(r"\*\*|\*|`", "", raw).strip()
        if not line or set(line) <= set("|-"):
            continue
        if line.startswith("|"):
            line = " — ".join(c.strip() for c in line.strip("|").split("|") if c.strip())
        f, gap = font("sans", 15), 6
        if raw.startswith("# "):
            line, f, gap = line[2:], font("serif-bold", 28), 16
        elif raw.startswith("#"):
            line, f, gap = line.lstrip("# "), font("serif-bold", 20), 10
        words, cur = line.split(), ""
        for w in words + [None]:
            if w is not None and d.textlength((cur + " " + w).strip(), font=f) <= width:
                cur = (cur + " " + w).strip()
                continue
            d.text((30, y), cur, font=f, fill=INK)
            y += f.size + 5
            cur = w or ""
            if y > size[1] - 40:
                return img
        y += gap
    return img


@lru_cache(None)
def _pages() -> list[Image.Image]:
    flow = Image.open(ROOT / "assets/images/flow.png").convert("RGB")
    flow.thumbnail((500, 660))
    flow_page = Image.new("RGB", (500, 660), WHITE)
    flow_page.paste(flow, (0, 0))
    ImageDraw.Draw(flow_page).rectangle((0, 0, 499, 659), outline=(190, 190, 185), width=2)
    return [_page(ROOT / "assets/docs/glossary-opening.md"), flow_page,
            _page(ROOT / "assets/docs/application-opening.md")]


BUILD = [(5, {"wire"}), (6, {"barrier", "prebook"}), (7, {"ai", "et"}), (8, {"book"}), (9, {"print", "readers"}),
         (10, {"chief", "finance", "lab", "health", "server"})]


@lru_cache(None)
def _plan(show: frozenset | None, lit: frozenset | None = None) -> Image.Image:
    return draw_plan(set(lit) if lit else None, show=set(show) if show is not None else None)


def _building(t: float, sc: core.Scene) -> Image.Image:
    shown: set[str] = set()
    prev, cur, x = None, frozenset(), 1.0
    for k, rooms in BUILD:
        if t >= sc.starts[k]:
            prev, cur = frozenset(shown), frozenset(shown | rooms)
            shown |= rooms
            x = progress(t, sc.starts[k], 0.6)
    full_at = sc.ends[10] + 0.2
    if t >= full_at:
        return Image.blend(_plan(cur), _plan(None), progress(t, full_at, 0.7))
    if prev is None:
        return _plan(frozenset())
    return Image.blend(_plan(prev), _plan(cur), x)


def scene5(t: float, sc: core.Scene) -> Image.Image:
    cue = sc.starts
    away = progress(t, cue[4], 0.7)
    img = _building(t, sc) if t >= cue[4] else blank()
    if away < 1:
        base = blank() if away == 0 else img
        for k, page in enumerate(_pages()):
            p = progress(t, cue[k + 1] - 0.2, 0.6) if k < 3 else 0
            if t < cue[0] + 0.3 and k == 0:
                p = 0
            if p > 0:
                x, y = 200 + k * 520, 220 - round(40 * (1 - p)) - round(260 * away)
                paste_alpha(base, page, (x, y), p * (1 - away))
        if away == 0:
            img = base
    return img


# Scene 6. The map of the series.

DISCS = {"wire": 2, "barrier": 3, "prebook": 3, "ai": 4, "et": 4, "book": 5, "print": 6, "readers": 7, "server": 8,
         "finance": 9, "lab": 9}


def scene6(t: float, sc: core.Scene) -> Image.Image:
    cue = sc.starts
    f = progress(t, cue[2] + 0.8, 1.2)
    img = Image.blend(_plan(None), _plan(None, frozenset({"wire", "sources"})), f) if f > 0 else _plan(None).copy()
    d = ImageDraw.Draw(img)
    boxes = {r[0]: r[4] for r in ROOMS}
    span = sc.ends[0] - cue[0]
    for k, (rid, n) in enumerate(DISCS.items()):
        g = progress(t, cue[0] + span * k / len(DISCS), 0.4) * (1 - f if rid != "wire" else 1)
        if g > 0:
            x, y = boxes[rid][2] - 4, boxes[rid][1] + 4
            d.ellipse((x - 24, y - 24, x + 24, y + 24), fill=mix(BG, INK, g))
            text_centred(d, (x, y - 16), str(n), font("sans-bold", 28), mix(INK, WHITE, g))
    g = progress(t, cue[1] + 1.0, 0.6)
    if g > 0:
        m = progress(t, cue[2] + 1.2, 1.5)
        x, y = 60 + (330 - 60) * m, 270 + (600 - 270) * m
        d.rectangle((x, y, x + 110, y + 62), fill=mix(BG, WHITE, g), outline=mix(BG, DROP, g), width=4)
        d.line((x + 12, y + 24, x + 96, y + 24), fill=mix(BG, (200, 200, 195), g), width=4)
        d.line((x + 12, y + 40, x + 70, y + 40), fill=mix(BG, (200, 200, 195), g), width=4)
    return img


def main() -> None:
    scenes = scenes_from_script(SCRIPT)
    draw = [scene1, scene2, scene3, scene4, scene5, scene6]
    made = []
    for k, (s, fn) in enumerate(zip(scenes, draw)):
        sc = voice(s["sentences"], tail=2.5 if k == len(draw) - 1 else core.SCENE_TAIL)
        print(f"scene {k + 1}: {len(s['sentences'])} sentences, {sc.length:.1f} s", flush=True)
        made.append((sc, fn))
    only = [int(a) for a in sys.argv[1:]]
    if only:
        made = [m for k, m in enumerate(made, 1) if k in only]
    length = core.write(made, OUT / ("ep01-draft.mp4" if not only else f"ep01-scenes-{'-'.join(sys.argv[1:])}.mp4"))
    print(f"{length:.1f} s")


if __name__ == "__main__":
    main()
