#!/usr/bin/env python3
"""Writes stores/copy/en/*.txt: every field each store form asks for, with character counts."""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "stores" / "copy" / "en"

VERSION = "1.0"
APPLE_ID = "uk.co.all-the-johnsons.concentration"
ANDROID_ID = "uk.co.allthejohnsons.concentration"
WINDOWS_ID = "49556nodoid.TheConcntrationGame"
WINDOWS_PUBLISHER = "CN=A6EAEB04-6634-41C1-BDFE-695819ECE444"
EMAIL = "paul@all-the-johnsons.co.uk"
SUPPORT = "https://<your web site>/Concentration-Support.html"

NAME = "Concentration"
SUBTITLE = "A gothic memory card game"
PROMO = ("Sixteen cards, eight pairs and not many guesses. Turn two at a time, remember what you saw "
         "and clear the board before your luck runs out.")
KEYWORDS = "memory,pairs,match,cards,tarot,gothic,brain,puzzle,concentrate,pelmanism,horror,matching"
SHORT = "Match eight pairs of gothic tarot cards before your guesses run out."

DESCRIPTION = """\
The classic memory game, played in a fog-bound forest with a deck of dark tarot cards.

Sixteen cards lie face down: eight pairs. Turn two over. If they match, they stay face up; if they don't, they turn back and that's one wrong guess. Find all eight pairs before you run out of guesses.

HOW HARD DO YOU WANT IT?

• Easy: 20 wrong guesses allowed
• Medium: 10 wrong guesses allowed
• Hard: just 5 - you will need a good memory and a little luck

Every pair you find scores points, and harder games score more. Your ten best scores are kept in the high score table, with the difficulty each was set on.

FEATURES

• Eight gothic tarot cards: the Devil, the Lovers, the Magician, the Knight and more
• Three difficulty levels
• Ten-place high score table, saved on your device
• Atmospheric sound: screams, slicing cards and howling wolves
• Quick games - a round takes a minute or two

Based on the original Concentration by Shea Ehrenberger; .NET MAUI version by Paul F. Johnson. No ads, no tracking, no accounts and no internet connection needed."""

WHATS_NEW = "First release: match eight pairs of gothic tarot cards on Easy, Medium or Hard, with a ten-place high score table."

REVIEW_NOTES = """\
Concentration is an offline, single-player memory game. No account, sign-in, network connection or purchase is needed. The app collects no data; high scores are stored only on the device.

HOW TO PLAY
On the start screen tap Easy, Medium or Hard. Sixteen cards are shown face down. Tap a card to turn it, then tap a second card. A matching pair stays face up; a non-matching pair turns back after a second and counts as a wrong guess (the count is shown under the board). The game ends when all eight pairs are found or when the wrong guesses reach the limit for the level (Easy 20, Medium 10, Hard 5). Reset Game starts again and High Scores shows the ten best scores.

QUICK TEST
Choose Easy, turn cards until a pair matches, then keep going until the game ends; the Reset Game and High Scores buttons appear."""

AGE_RATING = """\
Parental controls / age assurance           No / No
Unrestricted web access                     No
User-generated content                      No
Messaging and chat                          No
Advertising                                 No
Profanity or crude humour                   None
Horror or fear themes                       Infrequent/Mild (gothic tarot art: a devil, skulls; scream sounds)
Alcohol, tobacco or drug use or references  None
Medical or treatment information            None
Health or wellness topics                   No
Sexual content or nudity                    None
Cartoon or fantasy violence                 None
Realistic violence                          None
Prolonged graphic or sadistic violence      None
Guns or other weapons                       None
Simulated gambling / contests / loot boxes  None / No / No
Result                                      9+"""


def lines(title, items, limit):
    longest = max(len(i) for i in items)
    assert longest <= limit, f"{title}: a line is {longest} characters, limit {limit}"
    head = f"{title}  (longest line {longest}/{limit})"
    return f"{head}\n{'-' * len(head)}\n" + "\n".join(items) + "\n"


WIN_SHORT = ("The classic memory game in a fog-bound forest: sixteen gothic tarot cards, eight pairs and "
             "only so many wrong guesses. Turn two at a time, remember what you saw and clear the board "
             "on Easy, Medium or Hard.")

WIN_FEATURES = [
    "Match eight pairs of gothic tarot cards",
    "Three levels: 20, 10 or just 5 wrong guesses allowed",
    "Harder games score more points per pair",
    "Ten-place high score table, kept on your PC",
    "Atmospheric sound: screams, slicing cards and an eerie voice",
    "Quick games: a round takes a minute or two",
    "Mouse, touch or pen; runs natively on x64 and Arm PCs",
    "No ads, no accounts, no internet connection needed",
]

WIN_SEARCH = ["memory game", "pairs", "matching", "card game", "tarot", "gothic", "puzzle"]

WIN_CAPTIONS = [
    "Choose Easy, Medium or Hard",
    "Turn two cards at a time and remember what you saw",
    "A match stays face up; a miss costs you a guess",
    "Find all eight pairs to clear the board",
    "Beat the ten best scores",
]

WIN_CERT_NOTES = """Offline, single-player memory game; no account, sign-in, network connection or purchase is needed. On the start screen click Easy, Medium or Hard. Sixteen cards are shown face down: click one to turn it, then click a second. A matching pair stays face up; a pair that doesn't match turns back after a second and counts as a wrong guess (shown under the board). The game ends when all eight pairs are found or the wrong guesses reach the level's limit (Easy 20, Medium 10, Hard 5); Reset Game and High Scores then appear. High scores are saved in the app's own data folder. The package is a .NET MAUI (WinUI 3) desktop app; runFullTrust is its only capability (see restricted capabilities)."""

WIN_RESCAP = """runFullTrust: Concentration is a packaged desktop app built with .NET 10 MAUI on WinUI 3 and the Windows App SDK. Every packaged desktop (Win32) app needs runFullTrust to start its executable (Windows.FullTrustApplication entry point); it is used only to run the game's own process. The game does not use the internet, other apps, the user's documents or system settings, and needs no elevation. It reads the mouse, touch and pen, plays sound, and saves its high score table in its own app data folder."""


def field(title, text, limit=None):
    head = f"{title}  ({len(text)}/{limit} characters)" if limit else title
    if limit:
        assert len(text) <= limit, f"{title} is {len(text)} characters, limit {limit}"
    return f"{head}\n{'-' * len(head)}\n{text}\n"


def block(title, text):
    return f"{title}\n{'-' * len(title)}\n{text}\n"


def header(title, where):
    return f"{title}\n{'=' * len(title)}\n{where}\n"


def apple(platform, console, files, devices, category):
    return "\n".join([
        header(f"CONCENTRATION - {platform} - ENGLISH", f"App Store Connect > Concentration > {console} > {VERSION} > English (U.K.)"),
        field("NAME", NAME, 30),
        field("SUBTITLE", SUBTITLE, 30),
        field("PROMOTIONAL TEXT", PROMO, 170),
        field("KEYWORDS", KEYWORDS, 100),
        field("DESCRIPTION", DESCRIPTION, 4000),
        field("WHAT'S NEW", WHATS_NEW, 4000),
        block("FILES TO UPLOAD", files),
        block("ANSWERS IN THE CONSOLE", f"""\
Bundle ID           {APPLE_ID}
SKU                 concentration
Primary language    English (U.K.)
Category            {category}
Price               Free (or your choice); no in-app purchases
Support URL         {SUPPORT}
Privacy Policy URL  {SUPPORT}#privacy
Copyright           © 2026 Paul F. Johnson
App Privacy         Data Not Collected; no tracking
Encryption          None (ITSAppUsesNonExemptEncryption is false in Info.plist)
Sign-in required    No (App Review Information: untick "Sign-in required")
Devices             {devices}
Contact             Paul F. Johnson, {EMAIL}"""),
        block("AGE RATING", AGE_RATING),
        field("APP REVIEW NOTES", REVIEW_NOTES, 4000),
    ])


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "ios.txt").write_text(apple(
        "APP STORE (IPHONE AND IPAD)", "iOS App",
        f"""\
- iPhone 6.9" (REQUIRED): stores/ios/iphone-6.9in/ (5 x 1320x2868)
- iPhone 6.3": stores/ios/iphone-6.3in/ (5 x 1206x2622)
- iPad 13" (REQUIRED): stores/ios/ipad-13in/ (5 x 2064x2752)
- iPad app preview (optional, 13" iPad slot): ~/Movies/Concentration - iPad app preview 1200x1600 - English.mp4 (29 s; poster frame: 00:00:12)
- Support and privacy page: ~/Downloads/Concentration-Support.html, upload so it is served at the Support URL below
- Build: releases/Concentration-{VERSION}-ios.ipa (Transporter)""",
        "iPhone and iPad, portrait, iOS 18+",
        "Games > Puzzle (secondary: Games > Card)"))
    (OUT / "macos.txt").write_text(apple(
        "MAC APP STORE", "macOS App",
        f"""\
- Screenshots: stores/macos/ (5 x 1440x900)
- Support and privacy page: ~/Downloads/Concentration-Support.html, upload so it is served at the Support URL below
- Build: releases/Concentration-{VERSION}-macos.pkg (Transporter; Intel and Apple silicon)""",
        "Mac (Mac Catalyst), macOS 15+",
        "Games > Puzzle (secondary: Games > Card)"))
    (OUT / "android.txt").write_text("\n".join([
        header("CONCENTRATION - GOOGLE PLAY - ENGLISH", "Play Console > Concentration > Grow > Store presence > Main store listing > English (United Kingdom)"),
        field("APP NAME", NAME, 30),
        field("SHORT DESCRIPTION", SHORT, 80),
        field("FULL DESCRIPTION", DESCRIPTION, 4000),
        field("RELEASE NOTES (en-GB)", WHATS_NEW, 500),
        block("FILES TO UPLOAD", f"""\
- App icon: stores/android/icon-512.png
- Feature graphic: stores/android/feature-graphic-1024x500.png
- Phone screenshots: stores/android/phone/ (5 x 1080x2160)
- 7-inch tablet: stores/android/tablet-7in/ (5 x 1200x1920); 10-inch tablet: stores/android/tablet-10in/ (5 x 1600x2560)
- Support and privacy page: ~/Downloads/Concentration-Support.html, upload so it is served at the Website URL below
- App bundle: releases/Concentration-{VERSION}-android.aab (Production or a testing track)"""),
        block("ANSWERS IN THE CONSOLE", f"""\
Package name                         {ANDROID_ID}
App or game                          Game
Category                             Puzzle (or Card)
Tags                                 Memory, Matching, Puzzle, Card, Single player, Offline
Free or paid                         Free; no in-app purchases
Contains ads                         No
Email                                {EMAIL}
Website                              {SUPPORT}
Privacy policy                       {SUPPORT}#privacy
App access                           All functionality available without special access
Target audience                      13 and over (gothic horror art and scream sounds; not designed for children)
Content rating (IARC)                Horror/fear: mild (scary images, scream sounds); no violence, gambling, user content or sharing
Data safety                          No data collected; no data shared
Government app / financial / health  No / No / No
Play App Signing                     Enrol; upload key signing/concentration-upload.keystore (alias concentration)"""),
    ]))
    (OUT / "windows.txt").write_text("\n".join([
        header("CONCENTRATION - MICROSOFT STORE - ENGLISH", "Partner Center > The Concntration Game > Submission > Store listings > en-gb"),
        field("PRODUCT NAME", NAME, 256),
        field("SHORT DESCRIPTION", WIN_SHORT, 1000),
        field("DESCRIPTION", DESCRIPTION.replace("on your device", "on your PC"), 10000),
        lines("PRODUCT FEATURES (ONE PER BOX)", WIN_FEATURES, 200),
        lines("SEARCH TERMS (ONE PER BOX)", WIN_SEARCH, 30),
        field("WHAT'S NEW IN THIS VERSION", WHATS_NEW, 1500),
        field("SHORT TITLE", NAME, 50),
        field("NOTES FOR CERTIFICATION", WIN_CERT_NOTES, 2000),
        block("FILES TO UPLOAD", f"""\
- Screenshots (5, no text on them): stores/windows/ (1920x1080); captions below
- 1:1 App tile icon: stores/windows/art/app-tile-icon-300x300.png
- 2:3 Poster art (title in top two-thirds): stores/windows/art/poster-art-1440x2160.png (also 720x1080)
- 1:1 Box art (title in top two-thirds): stores/windows/art/box-art-2160x2160.png (also 1080x1080)
- 16:9 Super hero art (no text): stores/windows/art/super-hero-art-3840x2160.png (also 1920x1080)
- Packages (upload both): releases/Concentration-{VERSION}-windows-x64.msix and -windows-arm64.msix
Xbox images (Store listing > Xbox images; the 1920x1080 screenshots above also serve as Xbox screenshots)
- Branded key art 584x800 (title on a branding bar, top two-thirds): stores/windows/xbox/xbox-branded-key-art-584x800.png
- Titled hero art 1920x1080 (title in top two-thirds): stores/windows/xbox/xbox-titled-hero-art-1920x1080.png
- Featured promotional square art 1080x1080 (no title): stores/windows/xbox/xbox-featured-promotional-square-art-1080x1080.png"""),
        lines("SCREENSHOT CAPTIONS (IN ORDER)", [f"{i:02}  {c}" for i, c in enumerate(WIN_CAPTIONS, 1)], 200),
        field("RESTRICTED CAPABILITIES", WIN_RESCAP, 1000),
        block("SYSTEM REQUIREMENTS", """\
OS                              Windows 10 version 1809 (build 17763) or later; Windows 11
Architecture                    x64 and Arm64 (native package for each)
Memory (minimum / recommended)  2 GB / 4 GB
Storage                         About 250 MB
Input                           Mouse, touch or pen
Network                         Not required"""),
        block("PRODUCT DECLARATIONS", """\
Accesses, collects or transmits personal information           No
Tested to meet accessibility guidelines                        No (leave unticked)
Customers can install to alternate drives / removable storage  Yes
Allow Windows to back up app data                              Yes
Depends on non-Microsoft drivers or NT services                No
Requires a Windows Mixed Reality headset                       No
Uses the Microsoft Store in-app purchase system                No"""),
        block("ANSWERS IN THE CONSOLE", f"""\
Reserved app name       The Concntration Game (spelt as reserved; the package's DisplayName must match it)
Package identity        {WINDOWS_ID}
Publisher               {WINDOWS_PUBLISHER} (check Partner Center > Product identity)
Publisher display name  all-the-johnsons
Category                Games > Puzzle & trivia (subcategory: Card & board)
Pricing                 Free; no in-app purchases
Age ratings             IARC questionnaire: answers below
Privacy policy URL      {SUPPORT}#privacy
Website                 {SUPPORT}
Support contact         {EMAIL}
Copyright               © 2026 Paul F. Johnson
Game options            Single player; no online play
Display                 Resizable window; landscape and portrait
Languages               en-gb, en-us"""),
        block("CONTENT RATING (IARC)", """\
Category                             Game
Violence                             No
Fear                                 Mild: gothic tarot art (a devil, skulls) and scream sounds; nothing jumps out
Sexuality / nudity / crude language  No / No / No
Controlled substances                No
Gambling                             No (tarot cards are pictures only; no betting or fortune telling)
Users interact or share content      No
Shares location / digital purchases  No / No
Unrestricted internet                No"""),
    ]))
    for f in sorted(OUT.glob("*.txt")):
        print(f.relative_to(ROOT))


if __name__ == "__main__":
    main()
