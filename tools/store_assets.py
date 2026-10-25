#!/usr/bin/env python3
"""Builds stores/ from the captures in artifacts/capture/ (see stores/README.md).

Screenshots are copied at each store's exact size; the Google Play icon and feature graphic are
drawn from the game's own artwork (Resources/) and font. Needs Pillow and rsvg-convert.
"""
import base64
import io
import re
import shutil
import subprocess
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = Path(__file__).resolve().parent.parent
CAP = ROOT / "artifacts" / "capture"
OUT = ROOT / "stores"
RES = ROOT / "Concentration" / "Resources"
SHOTS = ["01-title", "02-play", "03-board", "04-win", "05-scores"]

# capture folder -> (stores folder, exact size)
SETS = {
    "iphone-6.9": ("ios/iphone-6.9in", (1320, 2868)),
    "iphone-6.3": ("ios/iphone-6.3in", (1206, 2622)),
    "ipad-13": ("ios/ipad-13in", (2064, 2752)),
    "mac": ("macos", (1440, 900)),
    "android-phone": ("android/phone", (1080, 2160)),
    "android-tablet-7": ("android/tablet-7in", (1200, 1920)),
    "android-tablet-10": ("android/tablet-10in", (1600, 2560)),
    "windows": ("windows", (1920, 1080)),
}


def fit(im, size):
    """Scale to cover size, then centre-crop (the Mac window is 1108x693, a hair off 16:10)."""
    w, h = size
    scale = max(w / im.width, h / im.height)
    im = im.resize((round(im.width * scale), round(im.height * scale)), Image.LANCZOS)
    left, top = (im.width - w) // 2, (im.height - h) // 2
    return im.crop((left, top, left + w, top + h))


def screenshots():
    for src, (dst, size) in SETS.items():
        out = OUT / dst
        shutil.rmtree(out, ignore_errors=True)
        out.mkdir(parents=True)
        for name in SHOTS:
            im = Image.open(CAP / src / f"{name}.png").convert("RGB")  # stores reject alpha
            if im.size != size:
                im = fit(im, size)
            im.save(out / f"{name}.png", optimize=True)
        print(f"{dst}: {len(SHOTS)} x {size[0]}x{size[1]}")


def svg(path, width):
    png = subprocess.run(["rsvg-convert", "-w", str(width), str(path)], check=True, capture_output=True).stdout
    return Image.open(io.BytesIO(png)).convert("RGBA")


def background():
    # background.svg is an Inkscape wrapper round one embedded PNG; too large for rsvg to parse
    text = (RES / "Images" / "background.svg").read_text()
    data = re.search(r'data:image/png;base64,([^"]+)"', text).group(1)
    data = re.sub(r"&#10;|\s", "", data)
    return Image.open(io.BytesIO(base64.b64decode(data))).convert("RGB")


def icon():
    # the app icon is the skull on white (MauiIcon Color="#FFFFFF")
    out = Image.new("RGB", (512, 512), "white")
    skull = svg(RES / "AppIcon" / "appicon.svg", 440)
    out.paste(skull, ((512 - skull.width) // 2, (512 - skull.height) // 2), skull)
    out.save(OUT / "android" / "icon-512.png")
    print("android/icon-512.png")


def card(name, size):
    # a face-up card as the game draws it: art on a rounded black tile
    tile = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    ImageDraw.Draw(tile).rounded_rectangle((0, 0, size - 1, size - 1), radius=size // 9, fill="black")
    pad = size // 9
    art = svg(RES / "Images" / f"{name}.svg", size - 2 * pad).resize((size - 2 * pad, size - 2 * pad), Image.LANCZOS)
    tile.paste(art, (pad, pad), art)
    return tile


def feature_graphic():
    w, h = 1024, 500
    im = fit(background(), (w, h)).convert("RGBA")
    shade = Image.new("RGBA", (w, h), (0, 0, 0, 70))
    im = Image.alpha_composite(im, shade)

    draw = ImageDraw.Draw(im)
    font = ImageFont.truetype(str(RES / "Fonts" / "AmaticSC_Bold.ttf"), 150)
    sub = ImageFont.truetype(str(RES / "Fonts" / "AmaticSC_Bold.ttf"), 52)
    title, tag = "CONCENTRATION", "Find the pairs before your guesses run out"

    def centred(text, f, y, fill):
        tw = draw.textlength(text, font=f)
        if bar:
            ImageDraw.Draw(im).rectangle((0, 0, w, ty + f.size * 1.25), fill=(14, 8, 8, 235))
            ImageDraw.Draw(im).rectangle((0, ty + f.size * 1.25, w, ty + f.size * 1.25 + max(2, h // 200)), fill=(155, 19, 19, 255))
        glow = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        ImageDraw.Draw(glow).text(((w - tw) / 2, y), text, font=f, fill=(0, 0, 0, 200))
        im.alpha_composite(glow.filter(ImageFilter.GaussianBlur(6)))
        ImageDraw.Draw(im).text(((w - tw) / 2, y), text, font=f, fill=fill)

    centred(title, font, 10, (190, 16, 16, 255))
    centred(tag, sub, 178, (245, 240, 235, 255))

    names = ["devil", "lovers", "back", "magician", "queen"]
    size, gap = 150, 24
    x = (w - (len(names) * size + (len(names) - 1) * gap)) // 2
    for i, name in enumerate(names):
        c = card(name, size)
        im.alpha_composite(c, (x + i * (size + gap), 290))
    im.convert("RGB").save(OUT / "android" / "feature-graphic-1024x500.png")
    print("android/feature-graphic-1024x500.png")


def key_art(w, h, title=True, bar=False):
    """Microsoft Store art: the forest, a fan of cards and (for box and poster art) the title in the top two-thirds.
    bar puts the title on a dark branding bar across the top (Xbox branded key art)."""
    im = fit(background(), (w, h)).convert("RGBA")
    im = Image.alpha_composite(im, Image.new("RGBA", (w, h), (0, 0, 0, 60)))
    names = ["devil", "lovers", "back", "magician", "queen"]
    if h > w:   # poster: two rows, three cards over two
        size = round(min(w * 0.24, h * 0.17))
        rows = [names[:3], names[3:]]
    else:
        size = round(min(w, h) * (0.2 if w > h else 0.15))
        rows = [names]
    gap = round(size * 0.16)
    # Xbox overlays the bottom third, so titled art keeps the cards above it
    centre = h * (0.5 if not title else 0.47 if h > w else 0.5 if w > h else 0.66)
    top = round(centre - (len(rows) * size + (len(rows) - 1) * gap) / 2)
    places = []
    for r, row in enumerate(rows):
        x = (w - (len(row) * size + (len(row) - 1) * gap)) // 2
        places += [(name, x + i * (size + gap), top + r * (size + gap)) for i, name in enumerate(row)]
    shadow = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    for _, x, y in places:
        ImageDraw.Draw(shadow).rounded_rectangle((x + size // 20, y + size // 12, x + size + size // 20, y + size + size // 12),
                                                radius=size // 9, fill=(0, 0, 0, 170))
    im.alpha_composite(shadow.filter(ImageFilter.GaussianBlur(size // 14)))
    for name, x, y in places:
        im.alpha_composite(card(name, size), (x, y))
    if title:
        f = ImageFont.truetype(str(RES / "Fonts" / "AmaticSC_Bold.ttf"), round(w * (0.155 if w >= h else 0.17)))
        draw = ImageDraw.Draw(im)
        text = "CONCENTRATION"
        tw = draw.textlength(text, font=f)
        ty = round(h * (0.2 if w == h else 0.17)) - f.size // 2
        if bar:
            ImageDraw.Draw(im).rectangle((0, 0, w, ty + f.size * 1.25), fill=(14, 8, 8, 235))
            ImageDraw.Draw(im).rectangle((0, ty + f.size * 1.25, w, ty + f.size * 1.25 + max(2, h // 200)), fill=(155, 19, 19, 255))
        glow = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        ImageDraw.Draw(glow).text(((w - tw) / 2, ty), text, font=f, fill=(0, 0, 0, 220))
        im.alpha_composite(glow.filter(ImageFilter.GaussianBlur(max(4, w // 160))))
        ImageDraw.Draw(im).text(((w - tw) / 2, ty), text, font=f, fill=(190, 16, 16, 255))
    return im.convert("RGB")


def windows_art():
    out = OUT / "windows" / "art"
    shutil.rmtree(out, ignore_errors=True)
    out.mkdir(parents=True)
    tile = Image.new("RGB", (300, 300), "white")
    skull = svg(RES / "AppIcon" / "appicon.svg", 256)
    tile.paste(skull, ((300 - skull.width) // 2, (300 - skull.height) // 2), skull)
    tile.save(out / "app-tile-icon-300x300.png")
    for name, (w, h), title in [("box-art", (2160, 2160), True), ("poster-art", (1440, 2160), True),
                                ("super-hero-art", (3840, 2160), False)]:
        big = key_art(w, h, title)
        big.save(out / f"{name}-{w}x{h}.png", optimize=True)
        small = big.resize((w // 2, h // 2), Image.LANCZOS)
        small.save(out / f"{name}-{w // 2}x{h // 2}.png", optimize=True)
    for f in sorted(out.iterdir()):
        print(f"windows/art/{f.name}")


def xbox_art():
    """Xbox images: key art and titled hero art carry the title, the promotional square must not."""
    out = OUT / "windows" / "xbox"
    shutil.rmtree(out, ignore_errors=True)
    out.mkdir(parents=True)
    for name, (w, h), title, bar in [("branded-key-art", (584, 800), True, True),
                                     ("titled-hero-art", (1920, 1080), True, False),
                                     ("featured-promotional-square-art", (1080, 1080), False, False)]:
        key_art(w, h, title, bar).save(out / f"xbox-{name}-{w}x{h}.png", optimize=True)
    for f in sorted(out.iterdir()):
        print(f"windows/xbox/{f.name}")


if __name__ == "__main__":
    import sys
    if sys.argv[1:] == ["windows-art"]:
        windows_art()
        xbox_art()
    else:
        screenshots()
        icon()
        feature_graphic()
        windows_art()
        xbox_art()
