"""What every episode is made with: the narration read sentence by sentence, the timing it gives, drawing helpers, and
the writer that turns frames and audio into a video (production-guide.md, How an episode is made).

Each sentence is read on its own, so the time each one begins is known exactly and a picture can begin with it. A
reading is kept under out/voice/, named by a hash of its text and voice settings, and made again only when they change.
"""

from __future__ import annotations

import hashlib
import math
import os
import re
import subprocess
import wave
from dataclasses import dataclass, field
from pathlib import Path

from PIL import Image, ImageDraw

from plan import BG, H, INK, MUTED, W, font

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "out"
FPS = 30
RATE = 22050
VOICE = {"model": "en_GB-cori-high", "length_scale": 1.05}
SENTENCE_GAP = 0.45   # seconds of quiet between sentences
SCENE_TAIL = 1.0      # seconds of quiet at the end of a scene
PIPER_HOME = Path(os.environ.get("PIPER_HOME", "/tmp/claude-0/-home-user-observatory/"
                                 "f901dd63-4e41-555c-9ab6-41c77fc31e45/scratchpad"))


def sentences(text: str) -> list[str]:
    return [s.strip() for s in re.split(r"(?<=[.?!])\s+", text.strip()) if s.strip()]


def scenes_from_script(path: Path) -> list[dict]:
    """The scenes of a script.md: each one's title and the sentences of its narration."""
    text = path.read_text()
    out = []
    for block in re.split(r"^## ", text, flags=re.M)[1:]:
        title = block.splitlines()[0].strip()
        m = re.search(r"\*\*Narration\.\*\*\s*(.+?)(?:\n\n|\Z)", block, flags=re.S)
        if m:
            out.append({"title": title, "sentences": sentences(m.group(1).replace("\n", " "))})
    return out


def _read(text: str) -> Path:
    key = hashlib.sha1(f"{VOICE['model']}|{VOICE['length_scale']}|{text}".encode()).hexdigest()[:16]
    path = OUT / "voice" / f"{key}.wav"
    if not path.exists():
        path.parent.mkdir(parents=True, exist_ok=True)
        subprocess.run([str(PIPER_HOME / "piper-venv/bin/piper"), "-m", str(PIPER_HOME / f"voices/{VOICE['model']}.onnx"),
                        "--length-scale", str(VOICE["length_scale"]), "-f", str(path)],
                       input=text.encode(), check=True, capture_output=True)
    return path


@dataclass
class Scene:
    """One scene's narration: its audio as samples, and when each sentence begins and ends, in seconds from the
    scene's start."""
    sentences: list[str]
    samples: bytearray = field(default_factory=bytearray)
    starts: list[float] = field(default_factory=list)
    ends: list[float] = field(default_factory=list)

    @property
    def length(self) -> float:
        return len(self.samples) / 2 / RATE


def voice(scene_sentences: list[str], tail: float = SCENE_TAIL) -> Scene:
    sc = Scene(scene_sentences)
    for k, s in enumerate(scene_sentences):
        with wave.open(str(_read(s))) as w:
            data = w.readframes(w.getnframes())
        sc.starts.append(len(sc.samples) / 2 / RATE)
        sc.samples += data
        sc.ends.append(len(sc.samples) / 2 / RATE)
        gap = tail if k == len(scene_sentences) - 1 else SENTENCE_GAP
        sc.samples += b"\x00\x00" * int(gap * RATE)
    return sc


# Timing and easing.

def ease(x: float) -> float:
    x = min(1.0, max(0.0, x))
    return x * x * (3 - 2 * x)


def progress(t: float, start: float, length: float) -> float:
    return ease((t - start) / length) if length > 0 else float(t >= start)


def mix(a, b, x: float):
    return tuple(round(p + (q - p) * x) for p, q in zip(a, b))


# Drawing.

def blank() -> Image.Image:
    return Image.new("RGB", (W, H), BG)


def text_centred(d: ImageDraw.ImageDraw, xy: tuple[float, float], text: str, f, fill=INK) -> None:
    w = d.textlength(text, font=f)
    d.text((xy[0] - w / 2, xy[1]), text, font=f, fill=fill)


def placeholder(size: tuple[int, int], name: str, what: str) -> Image.Image:
    """A grey card standing in for a screenshot the author has not yet supplied."""
    img = Image.new("RGB", size, (228, 227, 222))
    d = ImageDraw.Draw(img)
    w, h = size
    for x in range(0, w, 24):
        d.line([(x, 0), (x + 12, 0)], fill=MUTED, width=3)
        d.line([(x, h - 2), (x + 12, h - 2)], fill=MUTED, width=3)
    for y in range(0, h, 24):
        d.line([(0, y), (0, y + 12)], fill=MUTED, width=3)
        d.line([(w - 2, y), (w - 2, y + 12)], fill=MUTED, width=3)
    big = font("serif-bold", max(22, min(48, w // 14)))
    small = font("sans", max(16, min(26, w // 26)))
    text_centred(d, (w / 2, h / 2 - big.size), name, big)
    text_centred(d, (w / 2, h / 2 + 10), what, small, MUTED)
    return img


def screenshot(name: str, what: str, size: tuple[int, int]) -> Image.Image:
    """The author's screenshot assets/screenshots/<name>.png fitted to size, or a placeholder until it exists."""
    path = ROOT / "assets" / "screenshots" / f"{name}.png"
    if path.exists():
        img = Image.open(path).convert("RGB")
        img.thumbnail(size)
        card = Image.new("RGB", size, BG)
        card.paste(img, ((size[0] - img.width) // 2, (size[1] - img.height) // 2))
        return card
    return placeholder(size, name, what)


def paste_alpha(base: Image.Image, img: Image.Image, xy: tuple[int, int], alpha: float) -> None:
    if alpha <= 0:
        return
    if alpha >= 1:
        base.paste(img, xy)
        return
    region = base.crop((xy[0], xy[1], xy[0] + img.width, xy[1] + img.height))
    base.paste(Image.blend(region, img, alpha), xy)


def arrow(d: ImageDraw.ImageDraw, a, b, colour, width: int = 4, head: int = 16) -> None:
    d.line([a, b], fill=colour, width=width)
    ang = math.atan2(b[1] - a[1], b[0] - a[0])
    left = (b[0] - head * math.cos(ang - 0.45), b[1] - head * math.sin(ang - 0.45))
    right = (b[0] - head * math.cos(ang + 0.45), b[1] - head * math.sin(ang + 0.45))
    d.polygon([b, left, right], fill=colour)


# Writing the video.

def write(scenes: list[tuple[Scene, callable]], out: Path) -> float:
    """Draw every frame of every scene with its function frame(t, scene), and join them with the narration."""
    out.parent.mkdir(parents=True, exist_ok=True)
    audio = out.with_suffix(".wav")
    with wave.open(str(audio), "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(RATE)
        for sc, _ in scenes:
            w.writeframes(bytes(sc.samples))
    proc = subprocess.Popen(
        ["ffmpeg", "-loglevel", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS),
         "-i", "-", "-i", str(audio), "-c:v", "libx264", "-preset", "medium", "-crf", "20", "-pix_fmt", "yuv420p",
         "-c:a", "aac", "-b:a", "160k", "-shortest", str(out)],
        stdin=subprocess.PIPE)
    total = 0.0
    for sc, frame in scenes:
        n = round(sc.length * FPS)
        for k in range(n):
            proc.stdin.write(frame(k / FPS, sc).tobytes())
        total += n / FPS
    proc.stdin.close()
    proc.wait()
    audio.unlink()
    return total
