#!/usr/bin/env python3
"""Writes the store Support / Privacy page (one self-contained HTML file) to ~/Downloads.

Upload it as Concentration-Support.html; the store copy links to it and to its #privacy section.
Run tools/store_assets.py first: the icon comes from stores/android/icon-512.png.
"""
import base64
import io
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
OUT = Path.home() / "Downloads" / "Concentration-Support.html"
EMAIL = "paul@all-the-johnsons.co.uk"


def data_uri(path, size, quality=None):
    im = Image.open(path).convert("RGB")
    im.thumbnail((size, size), Image.LANCZOS)
    buf = io.BytesIO()
    if quality:
        im.save(buf, "JPEG", quality=quality, optimize=True)
        kind = "jpeg"
    else:
        im.save(buf, "PNG", optimize=True)
        kind = "png"
    return f"data:image/{kind};base64,{base64.b64encode(buf.getvalue()).decode()}"


ICON = data_uri(ROOT / "stores" / "android" / "icon-512.png", 192)
SHOT = data_uri(ROOT / "stores" / "ios" / "iphone-6.9in" / "02-play.png", 640, quality=80)
MAIL = f"mailto:{EMAIL}?subject=Concentration%20support"

PAGE = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Concentration Support</title>
<meta name="description" content="Help, questions, contact and privacy for Concentration on iPhone, iPad, Mac, Android and Windows.">
<link rel="icon" href="{ICON}">
<style>
:root {{
  --bg: #f7f5f3; --surface: #ffffff; --text: #221c1c; --muted: #625858;
  --line: #e2dcd9; --accent: #9b1313; --hero1: #120c0c; --hero2: #3a1414;
}}
@media (prefers-color-scheme: dark) {{
  :root:not([data-theme="light"]) {{
    --bg: #110d0d; --surface: #1b1515; --text: #ece6e4; --muted: #ab9f9d;
    --line: #2f2626; --accent: #ef6a5a;
  }}
}}
:root[data-theme="dark"] {{
  --bg: #110d0d; --surface: #1b1515; --text: #ece6e4; --muted: #ab9f9d;
  --line: #2f2626; --accent: #ef6a5a;
}}
* {{ box-sizing: border-box; }}
body {{ margin: 0; background: var(--bg); color: var(--text);
  font: 16px/1.6 -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; }}
a {{ color: var(--accent); }}
header {{ background: linear-gradient(180deg, var(--hero1), var(--hero2)); color: #f2e8e4; }}
.wrap {{ max-width: 860px; margin: 0 auto; padding: 0 16px; }}
.hero {{ display: flex; align-items: center; gap: 24px; padding: 48px 0 40px; }}
.hero img {{ width: 96px; height: 96px; border-radius: 22px; flex: none; box-shadow: 0 6px 20px rgba(0,0,0,.5); }}
.hero h1 {{ margin: 0; font-size: clamp(28px, 6vw, 44px); line-height: 1.1; font-weight: 600; }}
.hero h1 span {{ color: #e8473a; }}
.hero p {{ margin: 8px 0 0; color: #cdb9b5; }}
nav {{ display: flex; flex-wrap: wrap; gap: 8px 18px; padding: 14px 0; border-bottom: 1px solid var(--line); font-size: 15px; }}
nav a {{ text-decoration: none; }}
main {{ padding: 8px 0 48px; }}
section {{ padding-top: 28px; }}
h2 {{ font-size: 22px; margin: 0 0 12px; }}
h3 {{ font-size: 17px; margin: 18px 0 6px; }}
.card {{ background: var(--surface); border: 1px solid var(--line); border-radius: 12px; padding: 18px 20px; }}
.contact {{ display: grid; gap: 12px; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); }}
.contact .card p {{ margin: 6px 0 0; color: var(--muted); }}
.btn {{ display: inline-block; margin-top: 10px; padding: 9px 16px; border-radius: 8px; background: var(--accent);
  color: var(--bg); text-decoration: none; font-weight: 600; }}
.play {{ display: grid; gap: 20px; grid-template-columns: 1fr 200px; align-items: start; }}
.play img {{ width: 100%; border-radius: 14px; border: 1px solid var(--line); }}
@media (max-width: 600px) {{ .play {{ grid-template-columns: 1fr; }} .play img {{ max-width: 220px; }} }}
details {{ background: var(--surface); border: 1px solid var(--line); border-radius: 10px; padding: 12px 16px; margin: 8px 0; }}
summary {{ cursor: pointer; font-weight: 600; }}
details p, details ul {{ margin: 8px 0 2px; color: var(--muted); }}
ul {{ padding-left: 20px; }}
table {{ width: 100%; border-collapse: collapse; font-size: 15px; }}
td, th {{ text-align: left; padding: 8px 6px; border-bottom: 1px solid var(--line); vertical-align: top; }}
th {{ color: var(--muted); font-weight: 600; }}
.scroll {{ overflow-x: auto; }}
footer {{ border-top: 1px solid var(--line); padding: 20px 0 32px; color: var(--muted); font-size: 14px; }}
@media (max-width: 520px) {{ .hero {{ flex-direction: column; align-items: flex-start; padding: 32px 0 28px; }} .hero img {{ width: 72px; height: 72px; }} }}
</style>
</head>
<body>
<header>
  <div class="wrap hero">
    <img src="{ICON}" alt="Concentration icon">
    <div>
      <h1><span>Concentration</span> Support</h1>
      <p>A gothic memory card game for iPhone, iPad, Mac, Android and Windows.</p>
    </div>
  </div>
</header>

<div class="wrap">
<nav>
  <a href="#contact">Contact</a><a href="#play">How to play</a><a href="#scores">Scoring</a>
  <a href="#faq">FAQ</a><a href="#privacy">Privacy</a><a href="#requirements">Requirements</a>
</nav>

<main>
<section id="contact">
  <h2>Get help</h2>
  <div class="contact">
    <div class="card">
      <strong>Report a problem or ask a question</strong>
      <p>Email <a href="{MAIL}">{EMAIL}</a>. Say which device and system version you use and what happened. A screenshot helps.</p>
      <a class="btn" href="{MAIL}">Email support</a>
    </div>
    <div class="card">
      <strong>Through the store</strong>
      <p>You can also contact the developer from the Concentration page on the App Store, Google Play or the Microsoft Store.</p>
    </div>
  </div>
</section>

<section id="play">
  <h2>How to play</h2>
  <div class="card play">
    <div>
      <ul>
        <li><strong>Start:</strong> on the title screen choose <strong>Easy</strong>, <strong>Medium</strong> or <strong>Hard</strong>.</li>
        <li><strong>The board:</strong> sixteen tarot cards lie face down: eight pairs.</li>
        <li><strong>Your turn:</strong> tap (or click) a card to turn it over, then a second card.</li>
        <li><strong>A match</strong> stays face up. Cards that don't match turn back after a second, and that counts as one wrong guess.</li>
        <li><strong>The end:</strong> you win by finding all eight pairs. You lose when your wrong guesses reach the limit:
          20 on Easy, 10 on Medium and just 5 on Hard.</li>
        <li><strong>Again:</strong> <strong>Reset Game</strong> deals a fresh board and <strong>High Scores</strong> shows the table.</li>
      </ul>
    </div>
    <img src="{SHOT}" alt="A game of Concentration in progress">
  </div>
</section>

<section id="scores">
  <h2>Scoring and high scores</h2>
  <div class="card">
    <p>Every pair you find scores points, and harder games score more:</p>
    <div class="scroll">
      <table>
        <tr><th>Level</th><th>Wrong guesses allowed</th><th>Points per pair</th><th>Best possible</th></tr>
        <tr><td>Easy</td><td>20</td><td>5</td><td>40</td></tr>
        <tr><td>Medium</td><td>10</td><td>10</td><td>80</td></tr>
        <tr><td>Hard</td><td>5</td><td>20</td><td>160</td></tr>
      </table>
    </div>
    <p>The ten best scores are kept on your device, with the level each was played on.</p>
  </div>
</section>

<section id="faq">
  <h2>Frequently asked questions</h2>
  <details><summary>I can't hear any sound.</summary>
    <p>Check the volume and, on iPhone, that the ring/silent switch is not set to silent. The game plays a slicing sound for every card, an eerie voice when a game ends and a scream when you reset the board.</p></details>
  <details><summary>The sounds or pictures are too scary for my child.</summary>
    <p>Concentration has gothic art (a devil, skulls) and scream sounds. It is rated 9+ on the App Store and is not designed for young children.</p></details>
  <details><summary>How do I clear the high score table?</summary>
    <p>The table is stored only on your device. Deleting and reinstalling the app clears it.</p></details>
  <details><summary>Do my high scores move to my new phone?</summary>
    <p>No. Scores are kept only on the device you played on and are not uploaded anywhere.</p></details>
  <details><summary>Does it need an internet connection?</summary>
    <p>No. The game works completely offline.</p></details>
  <details><summary>Is there a cost, adverts or in-app purchases?</summary>
    <p>No. There are no adverts, no in-app purchases and no account to create.</p></details>
</section>

<section id="privacy">
  <h2>Privacy policy</h2>
  <div class="card">
    <p><strong>Concentration collects no personal data.</strong> It has no accounts, adverts, analytics or tracking, and it never connects to the internet.</p>
    <ul>
      <li><strong>On your device:</strong> the high score table (score, level, date and the name "The champ" or "The contender") is saved in the app's own storage. It never leaves your device, and deleting the app deletes it.</li>
      <li><strong>Shared with others:</strong> nothing. No data is sent to the developer or any third party.</li>
      <li><strong>Children:</strong> the app collects no information from anyone, including children.</li>
      <li><strong>Store data:</strong> Apple, Google and Microsoft may collect download and crash information under their own privacy policies. If you have shared crash reports with developers, the developer may see anonymous crash reports.</li>
      <li><strong>Emails:</strong> if you email support, your email address and message are used only to answer you.</li>
    </ul>
    <p>Questions about privacy: <a href="mailto:{EMAIL}?subject=Concentration%20privacy">{EMAIL}</a>. If this policy changes, this page will be updated. Last updated 23 October 2026.</p>
  </div>
</section>

<section id="requirements">
  <h2>System requirements</h2>
  <div class="card scroll">
    <table>
      <tr><th>Platform</th><th>Requires</th></tr>
      <tr><td>iPhone and iPad</td><td>iOS / iPadOS 18 or later</td></tr>
      <tr><td>Mac</td><td>macOS 15 Sequoia or later, Apple silicon or Intel</td></tr>
      <tr><td>Android</td><td>Android 12L (API 32) or later, phones and tablets</td></tr>
      <tr><td>Windows</td><td>Windows 10 version 1809 or later, or Windows 11; x64 or Arm64</td></tr>
    </table>
  </div>
</section>
</main>

<footer>
  © 2026 Paul F. Johnson · Based on the original Concentration by Shea Ehrenberger ·
  <a href="#privacy">Privacy policy</a>
</footer>
</div>
</body>
</html>
"""

OUT.write_text(PAGE)
print(f"{OUT} ({OUT.stat().st_size // 1024} KB)")
