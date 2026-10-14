#!/usr/bin/env python3
"""
GitHub profile card for Harsha, in the style of Andrew6rant/Andrew6rant.

  python3 today.py --build photo.png   redraw dark_mode.svg / light_mode.svg from a photo on a plain white
                                       backdrop (local only, needs Pillow + numpy; the photo is not kept in the repo)
  python3 today.py           refresh uptime + GitHub stats inside both SVGs (CI, stdlib only, needs ACCESS_TOKEN)
  python3 today.py --test    self-check
"""

import datetime
import html
import http.client
import itertools
import json
import os
import sys
import time
import urllib.request
import xml.etree.ElementTree as ET

USER_NAME = os.environ.get("USER_NAME", "Harsha-code-per")
ACCESS_TOKEN = os.environ.get("ACCESS_TOKEN")
BIRTHDAY = datetime.date(2005, 11, 20)
ROOT = os.path.dirname(os.path.abspath(__file__))
SVGS = {"dark": os.path.join(ROOT, "dark_mode.svg"), "light": os.path.join(ROOT, "light_mode.svg")}

# ---------------------------------------------------------------- shared

def dots(n):
    """Filler of exactly n chars: '', ' ', '  ', ' . ', ' .. ', ..."""
    return "" if n <= 0 else " " * n if n <= 2 else " " + "." * (n - 2) + " "


def calculate_uptime(birthday, today=None):
    today = today or datetime.date.today()
    years, months, days = today.year - birthday.year, today.month - birthday.month, today.day - birthday.day
    if days < 0:
        months -= 1
        first = today.replace(day=1)
        days += (first - (first - datetime.timedelta(days=1)).replace(day=1)).days  # length of previous month
    if months < 0:
        years -= 1
        months += 12
    cake = " 🎂" if months == 0 and days == 0 else ""
    return f"{years} years, {months} months, {days} days{cake}"

# ---------------------------------------------------------------- stats (GraphQL)

def gql(query, **variables):
    req = urllib.request.Request(
        "https://api.github.com/graphql",
        json.dumps({"query": query, "variables": variables}).encode(),
        {"Authorization": f"bearer {ACCESS_TOKEN}", "User-Agent": USER_NAME},
    )
    for attempt in range(4):  # GitHub drops the odd connection / 502s on big history pages
        try:
            with urllib.request.urlopen(req, timeout=60) as resp:
                data = json.load(resp)
            break
        except (OSError, http.client.HTTPException):
            if attempt == 3:
                raise
            time.sleep(2 ** attempt * 5)
    if data.get("errors"):
        raise RuntimeError(data["errors"])
    return data["data"]


REPOS_Q = """query($login: String!, $cursor: String) { user(login: $login) {
  id followers { totalCount }
  repositories(first: 100, after: $cursor, ownerAffiliations: [OWNER, COLLABORATOR, ORGANIZATION_MEMBER]) {
    pageInfo { hasNextPage endCursor }
    nodes { name owner { login } stargazerCount defaultBranchRef { name } }
  } } }"""

HISTORY_Q = """query($owner: String!, $name: String!, $author: ID!, $cursor: String) { repository(owner: $owner, name: $name) {
  defaultBranchRef { target { ... on Commit {
    history(first: 100, after: $cursor, author: { id: $author }) {
      totalCount pageInfo { hasNextPage endCursor } nodes { additions deletions }
  } } } } } }"""


def fetch_stats(login):
    repos, cursor = [], None
    while True:
        user = gql(REPOS_Q, login=login, cursor=cursor)["user"]
        page = user["repositories"]
        repos += page["nodes"]
        if not page["pageInfo"]["hasNextPage"]:
            break
        cursor = page["pageInfo"]["endCursor"]

    owned = [r for r in repos if r["owner"]["login"].lower() == login.lower()]
    commits = added = deleted = 0
    # ponytail: full recount of my commits every run; add Andrew6rant's per-repo cache/ if this gets slow or rate-limited
    for r in repos:
        if not r["defaultBranchRef"]:
            continue  # empty repo
        cursor = None
        while True:
            hist = gql(HISTORY_Q, owner=r["owner"]["login"], name=r["name"], author=user["id"], cursor=cursor)
            hist = hist["repository"]["defaultBranchRef"]["target"]["history"]
            added += sum(c["additions"] for c in hist["nodes"])
            deleted += sum(c["deletions"] for c in hist["nodes"])
            if not hist["pageInfo"]["hasNextPage"]:
                commits += hist["totalCount"]
                break
            cursor = hist["pageInfo"]["endCursor"]

    return {
        "repo_data": len(owned),
        "contrib_data": len(repos),
        "star_data": sum(r["stargazerCount"] for r in owned),
        "commit_data": commits,
        "follower_data": user["followers"]["totalCount"],
        "loc_data": added - deleted,
        "loc_add": added,
        "loc_del": deleted,
    }


def patch_svg(path, values):
    """Set each <tspan id=k> to its value and re-pad <tspan id=k_dots> so the row keeps its width."""
    ET.register_namespace("", "http://www.w3.org/2000/svg")
    tree = ET.parse(path)
    root = tree.getroot()
    for key, value in values.items():
        value = f"{value:,}" if isinstance(value, int) else value
        el, filler = root.find(f".//*[@id='{key}']"), root.find(f".//*[@id='{key}_dots']")
        width = len(el.text or "") + len(filler.text or "")
        n = width - len(value)
        el.text, filler.text = value, dots(n) if filler.get("class") == "cc" else " " * max(n, 0)
    tree.write(path, encoding="utf-8", xml_declaration=True)

# ---------------------------------------------------------------- build (local only)

W = 66            # chars per info row; every row is exactly this wide
CW = 7.8          # px per info char at 13px (textLength pins it, so Consolas/Menlo/DejaVu all align)
STEP = 18.5       # info line height
INFO_X = 400
HEIGHT = 540

# portrait knobs (fitted separately against each theme's background)
GLYPH_FONT = "/usr/share/fonts/TTF/DejaVuSansMono-Bold.ttf"   # any bold monospace TTF; only used to measure glyph shapes
COLS = 88
P_X, P_Y, P_W = 15, 12, 360                             # portrait box; P_W = textLength of every line
P_CELL_W = P_W / COLS
P_STEP = P_CELL_W / 0.55                                # monospace cell is ~0.55 wide : 1 tall
ROWS = int((HEIGHT - 2 * P_Y) / P_STEP)
P_FONT = P_STEP * 0.95                                  # tall glyphs, squeezed into the cell width by textLength
CROP_CX, CROP_TOP, CROP_W = 0.50, 0.04, 0.60            # fractions of the photo; height follows the grid aspect
DETAIL_R, DETAIL_K = 14, 2.5                            # local contrast: makes glasses / eyes / mouth survive
TONE = {"dark": (40, 255), "light": (0, 235)}           # photo range per theme: lift blacks on dark, dim whites on light
BACKDROP = 200                                          # photo pixels brighter than this AND connected to the top/sides = backdrop
BG_MIX = 0.6                                            # cell background = this much of the photo colour over the card bg
GLYPH_BOOST = 1.5                                       # glyph colour overshoot vs its cell background (thin strokes)
FX, FY = 3, 5                                           # sub-cell samples used to match glyph shapes
FLAT_PCT = 60                                           # flattest N% of cells spell FILL instead of a fitted glyph
FILL = "HARSHAVARDHAN"
CHARS = [chr(i) for i in range(32, 127) if chr(i) != "`"]

THEMES = {
    "dark":  dict(bg="#161b22", text="#c9d1d9", key="#ffa657", value="#a5d6ff", add="#3fb950", dele="#f85149", cc="#616e7f", border=""),
    "light": dict(bg="#ffffff", text="#24292f", key="#953800", value="#0a3069", add="#1a7f37", dele="#cf222e", cc="#c2cfde",
                  border=' stroke="#d0d7de" stroke-width="1.5"'),
}


def portrait_cells(photo, theme):
    """-> ROWS x COLS of (glyph, glyph colour | None, cell background | None), colours as "#rrggbb".

    Like a truecolour terminal, every cell has a background (the photo colour, dimmed) and a glyph on top.
    Per cell every glyph is tried: its coverage map at the best intensity, over that background, is compared with
    that patch of the photo and the least-error glyph wins, so glasses / eyes / jaw get edge-shaped glyphs.
    Flat cells spell FILL instead.
    """
    import numpy as np
    from PIL import Image, ImageDraw, ImageFilter, ImageFont

    # coverage of each glyph sampled on an FX x FY grid
    up = 8
    font = ImageFont.truetype(GLYPH_FONT, round(P_FONT * up))
    cov = []
    for c in CHARS:
        im = Image.new("L", (round(0.602 * P_FONT * up), round(P_STEP * up)))  # one advance wide, squeezed below
        ImageDraw.Draw(im).text((0, P_STEP * up * 0.8), c, fill=255, font=font, anchor="ls")
        cov.append(np.asarray(im.resize((FX, FY), Image.Resampling.BOX), float).ravel() / 255)
    G = np.array(cov)                                                   # (K, F)

    img = Image.open(photo).convert("RGB")
    w, h = img.size
    cw = CROP_W * w
    ch = cw * (ROWS * P_STEP) / P_W
    x0, y0 = CROP_CX * w - cw / 2, CROP_TOP * h
    img = img.crop((int(x0), int(y0), int(x0 + cw), int(y0 + ch)))
    rgb = np.asarray(img, float)
    lum = np.asarray(img.convert("L"), float)
    blur = np.asarray(img.convert("L").filter(ImageFilter.GaussianBlur(DETAIL_R)), float)
    # local contrast, scaled by neighbourhood brightness: sharpens glasses on skin, but leaves black hair calm
    rgb = np.clip(rgb + DETAIL_K * ((lum - blur) * (blur / 255) ** 1.5)[..., None], 0, 255)
    lo, hi = TONE[theme]
    rgb = lo + rgb * (hi - lo) / 255
    panel = np.array(list(bytes.fromhex(THEMES[theme]["bg"][1:])), float)

    # backdrop = near-white pixels flood-filled from the top and side edges. A plain "is it white" test also
    # swallows the light-blue shirt (it is ~(238, 249, 251)), which then rendered as dark holes.
    mask = Image.fromarray(np.uint8((np.asarray(img).min(-1) > BACKDROP) * 255)).copy()  # copy: fromarray buffers are read-only
    mw, mh = mask.size
    for xy in [(x, 0) for x in range(0, mw, 4)] + [(0, y) for y in range(0, mh, 4)] + [(mw - 1, y) for y in range(0, mh, 4)]:
        if mask.getpixel(xy) == 255:
            ImageDraw.floodfill(mask, xy, 128)
    is_bg = np.asarray(mask) == 128
    rgb[is_bg] = panel

    def to_grid(a, fx, fy):
        return np.asarray(Image.fromarray(np.uint8(a)).resize((COLS * fx, ROWS * fy), Image.Resampling.BOX), float)

    T = to_grid(rgb, FX, FY).reshape(ROWS, FY, COLS, FX, 3).transpose(0, 2, 1, 3, 4).reshape(ROWS * COLS, FX * FY, 3)
    fg = to_grid(~is_bg * 255, 1, 1).ravel() > 127

    # cell background (like a truecolour terminal): the cell's mean colour, dimmed toward the panel
    cell_bg = panel + BG_MIX * (T.mean(1) - panel)
    cell_bg = np.where(fg[:, None], cell_bg // 16 * 16 + 8, panel)
    W3 = np.array([0.299, 0.587, 0.114])
    r = (T - cell_bg[:, None]) @ W3                                     # what the glyph still has to add (N, F)

    # least-squares intensity per (cell, glyph); the glyph with the smallest error wins
    rg = r @ G.T
    gg = (G ** 2).sum(1)
    base = (cell_bg @ W3)[:, None]
    a = np.clip(rg / np.maximum(gg, 1e-9), -base, 255 - base)
    err = gg * a ** 2 - 2 * a * rg + (r ** 2).sum(1)[:, None]
    best = np.where(fg, err.argmin(1), 0)
    n = np.arange(best.size)
    detail = r.std(1)
    flat = fg & (detail < np.percentile(detail[fg], FLAT_PCT))
    best = np.where(flat, [CHARS.index(FILL[i % len(FILL)]) for i in n], best)

    # glyph colour = photo colour under its strokes, pushed away from the cell background to make up for thin strokes
    g = G[best]
    under = (g[..., None] * T).sum(1) / np.maximum(g.sum(1), 1e-6)[:, None]
    col = np.clip(cell_bg + GLYPH_BOOST * (under - cell_bg), 0, 255) // 16 * 16 + 8

    hexc = lambda c: "#%02x%02x%02x" % tuple(int(v) for v in c)
    cells = [(CHARS[b] if f else " ", hexc(c) if b else None, hexc(cb) if f else None)
             for b, c, cb, f in zip(best, col, cell_bg, fg)]
    return [cells[y * COLS:(y + 1) * COLS] for y in range(ROWS)]


def portrait_svg(cells):
    rects, lines = [], []
    for y, row in enumerate(cells):
        top = P_Y + y * P_STEP
        x = 0
        for fill, run in itertools.groupby(row, key=lambda c: c[2]):  # one <rect> per same-background run
            k = len(list(run))
            if fill:
                rects.append(f'<rect x="{P_X + x * P_CELL_W:.2f}" y="{top:.2f}" width="{k * P_CELL_W:.2f}" height="{P_STEP:.2f}" fill="{fill}"/>')
            x += k
        spans = []
        for fill, run in itertools.groupby(row, key=lambda c: c[1]):  # one <tspan> per same-colour run
            text = html.escape("".join(c[0] for c in run))
            spans.append(f'<tspan fill="{fill}">{text}</tspan>' if fill else text)
        lines.append(f'<text x="{P_X}" y="{top + 0.8 * P_STEP:.2f}" textLength="{P_W}" lengthAdjust="spacingAndGlyphs">{"".join(spans)}</text>')
    return '<g shape-rendering="crispEdges">\n' + "\n".join(rects) + "\n</g>\n" + "\n".join(lines)


def field(vid, value, width, cls="value"):
    """filler + value pair that today.py can re-pad later; a classless filler pads with spaces instead of dots."""
    pad = dots(width - len(value)) if cls == "value" else " " * (width - len(value))
    return [("cc" if cls == "value" else None, pad, vid + "_dots"), (cls, value, vid)]


def kv(keys, value, vid=None):
    head = [("cc", ". ", None)]
    for i, k in enumerate(keys):
        head += ([(None, ".", None)] if i else []) + [("key", k, None)]
    head.append((None, ":", None))
    width = W - sum(len(t) for _, t, _ in head)
    if vid:
        return head + field(vid, value, width)
    return head + [("cc", dots(width - len(value)), None), ("value", value, None)]


def header(title):
    return [(None, f"{title} " + "-" * (W - len(title) - 1), None)]


INFO = [
    header("harsha@workstation"),
    kv(["OS"], "Windows 11, Android 16, Linux (Arch)"),
    kv(["Uptime"], calculate_uptime(BIRTHDAY), "age_data"),
    kv(["Host"], "R.M.K. CET, B.Tech (Class of 2028)"),
    kv(["Kernel"], "AI Intern @ Sennovate"),
    kv(["Previously"], "AI Intern @ Zensphere, ResPro Labs"),
    kv(["Research"], "IEEE Xplore, ICSCN 2025 (UAV security)"),
    kv(["IDE"], "VS Code, Antigravity IDE, Kate"),
    None,
    kv(["Languages", "Programming"], "Python, Java, TypeScript, SQL"),
    kv(["AI", "DataScience"], "LLMs, RAG, PyTorch, Azure AI"),
    kv(["Frameworks", "FullStack"], "FastAPI, Django, Next.js, React"),
    kv(["Motion", "ImmersiveUI"], "Three.js, WebGL, GSAP, Framer Motion"),
    kv(["Cloud", "Systems"], "Docker, Kubernetes, AWS, Azure"),
    kv(["Languages", "Real"], "English, Telugu, Tamil, Hindi"),
    kv(["Hobbies", "Sport"], "Badminton, Strength training"),
    None,
    header("- Contact"),
    kv(["Email", "Work"], "HKrishnaiah@sennovate.com"),
    kv(["Email", "Personal"], "harshavardhan3259@gmail.com"),
    kv(["LinkedIn"], "harshavardhan-20-k"),
    kv(["Portfolio"], "harshavardhan-k.me"),
    None,
    header("- GitHub Stats"),
    [("cc", ". ", None), ("key", "Repos", None), (None, ":", None), *field("repo_data", "0", 6),
     (None, " {", None), ("key", "Contributed", None), (None, ":", None), *field("contrib_data", "0", 4),
     (None, "} | ", None), ("key", "Stars", None), (None, ":", None), *field("star_data", "0", 24)],
    [("cc", ". ", None), ("key", "Commits", None), (None, ":", None), *field("commit_data", "0", 21),
     (None, " | ", None), ("key", "Followers", None), (None, ":", None), *field("follower_data", "0", 22)],
    [("cc", ". ", None), ("key", "Lines of Code", None), (None, ":", None), *field("loc_data", "0", 18),
     (None, " ( ", None), *field("loc_add", "0", 11, "add"), ("add", "++", None),
     (None, ", ", None), *field("loc_del", "0", 10, "dele"), ("dele", "--", None), (None, " )", None)],
]


def info_svg():
    out = []
    for i, row in enumerate(INFO):
        if row is None:
            continue
        assert sum(len(t) for _, t, _ in row) == W, f"row {i} is not {W} chars"
        spans = "".join(
            f'<tspan{f" class=\"{c}\"" if c else ""}{f" id=\"{sid}\"" if sid else ""}>{html.escape(t)}</tspan>'
            if c or sid else html.escape(t)
            for c, t, sid in row
        )
        out.append(f'<text x="{INFO_X}" y="{30 + i * STEP:.1f}" textLength="{W * CW}">{spans}</text>')
    return "\n".join(out)


def build(photo):
    info = info_svg()
    width = INFO_X + W * CW + 15
    for theme, path in SVGS.items():
        t = THEMES[theme]
        portrait = portrait_svg(portrait_cells(photo, theme))
        svg = f"""<?xml version='1.0' encoding='UTF-8'?>
<svg xmlns="http://www.w3.org/2000/svg" xml:space="preserve" font-family="ConsolasFallback,Consolas,Menlo,'DejaVu Sans Mono',monospace" width="{width:.0f}px" height="{HEIGHT}px" font-size="13px">
<style>
@font-face {{ src: local('Consolas'), local('Consolas Bold'); font-family: 'ConsolasFallback'; font-display: swap; size-adjust: 109%; }}
.key {{fill: {t['key']};}} .value {{fill: {t['value']};}} .add {{fill: {t['add']};}} .dele {{fill: {t['dele']};}} .cc {{fill: {t['cc']};}}
text, tspan {{white-space: pre;}}
.portrait {{font-size: {P_FONT:.2f}px; font-weight: bold;}}
</style>
<rect width="{width:.0f}px" height="{HEIGHT}px" fill="{t['bg']}" rx="15"{t['border']}/>
<g class="portrait">
{portrait}
</g>
<g fill="{t['text']}">
{info}
</g>
</svg>
"""
        with open(path, "w", encoding="utf-8") as f:
            f.write(svg)
        print(f"wrote {path} ({len(svg) // 1024} KB)")

# ---------------------------------------------------------------- main

def test():
    assert calculate_uptime(BIRTHDAY, datetime.date(2026, 10, 14)) == "20 years, 10 months, 24 days"
    assert calculate_uptime(BIRTHDAY, datetime.date(2026, 11, 20)) == "21 years, 0 months, 0 days 🎂"
    assert calculate_uptime(BIRTHDAY, datetime.date(2027, 3, 1)) == "21 years, 3 months, 9 days"  # borrows Feb (28)
    assert dots(0) == "" and dots(2) == "  " and dots(5) == " ... "
    print("ok")


def main():
    if "--test" in sys.argv:
        return test()
    if "--build" in sys.argv:
        build(sys.argv[sys.argv.index("--build") + 1])
    values = {"age_data": calculate_uptime(BIRTHDAY)}
    if ACCESS_TOKEN:
        values |= fetch_stats(USER_NAME)
    elif "--build" not in sys.argv:
        sys.exit("ACCESS_TOKEN is not set; refusing to publish stale stats")
    for path in SVGS.values():
        patch_svg(path, values)
    print(values)


if __name__ == "__main__":
    main()
