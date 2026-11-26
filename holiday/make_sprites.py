#!/usr/bin/env python3
"""Draws the holiday pixel-art sprites as animated GIFs in holiday/sprites/.

Every frame within a sprite must differ from the one before it: PIL merges
identical consecutive GIF frames, and Pixlet ignores per-frame durations, so a
merged frame would silently shorten the animation.
"""
import os
from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "sprites")


def save_gif(frames, name):
    # one shared palette across all frames so colors never drift frame-to-frame
    sheet = Image.new("RGB", (frames[0].width * len(frames), frames[0].height))
    for i, f in enumerate(frames):
        sheet.paste(f, (i * f.width, 0))
    palette = sheet.quantize(colors=32, method=Image.MEDIANCUT)
    pal_frames = [f.quantize(palette=palette, dither=Image.NONE) for f in frames]
    path = os.path.join(OUT, name)
    pal_frames[0].save(path, save_all=True, append_images=pal_frames[1:], duration=100, loop=0, disposal=2)
    assert Image.open(path).n_frames == len(frames), f"{name}: frames were merged"
    print(f"{name}: {len(frames)} frames")


# --- Thanksgiving: dancing turkey (18x22) -----------------------------------

FEATHERS = [(210, 45, 40), (245, 135, 35), (250, 205, 60), (150, 80, 35), (245, 135, 35), (210, 45, 40)]
BODY, BELLY, HEAD = (140, 78, 38), (178, 112, 60), (155, 90, 45)
BEAK, WATTLE, EYE, LEG = (250, 190, 40), (225, 40, 40), (255, 255, 255), (245, 150, 40)


def turkey_frame(tail_deg, body_dy, head_dx, left_up):
    img = Image.new("RGB", (18, 22), (0, 0, 0))
    d = ImageDraw.Draw(img)
    cx, cy = 9, 13 + body_dy

    r, span = 9, 200
    start = 270 - span / 2 + tail_deg
    step = span / len(FEATHERS)
    for i, col in enumerate(FEATHERS):
        a0 = start + i * step
        d.pieslice([cx - r, cy - r, cx + r, cy + r], a0, a0 + step, fill=col)

    for lx, up in ((7, left_up), (11, not left_up)):
        foot_y = 20 + body_dy - (2 if up else 0)
        foot_y = min(foot_y, 21)
        d.line([(lx, 17 + body_dy), (lx, foot_y)], fill=LEG)
        d.line([(lx - 1, foot_y), (lx + 1, foot_y)], fill=LEG)

    d.ellipse([cx - 4, cy - 3, cx + 4, cy + 5], fill=BODY)
    d.ellipse([cx - 2, cy - 1, cx + 2, cy + 4], fill=BELLY)

    hx, hy = cx + head_dx, cy - 6
    d.ellipse([hx - 2, hy - 2, hx + 2, hy + 2], fill=HEAD)
    d.point((hx - 1, hy - 1), fill=EYE)
    d.point((hx + 1, hy - 1), fill=EYE)
    d.point((hx, hy + 1), fill=BEAK)
    d.point((hx + 1, hy + 2), fill=WATTLE)
    d.point((hx + 1, hy + 3), fill=WATTLE)
    return img


def turkey():
    tail = [-18, -9, 0, 9, 18, 9, 0, -9]
    bob = [0, -1, -2, -1, 0, -1, -2, -1]
    head_dx = [-1, -1, 0, 1, 1, 1, 0, -1]
    left_up = [True] * 4 + [False] * 4
    return [turkey_frame(tail[i], bob[i], head_dx[i], left_up[i]) for i in range(8)]


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    save_gif(turkey(), "turkey.gif")
