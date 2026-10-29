"""
generate_cards.py - rebuilds every SVG in assets/ (cards, stat tiles, about cards, stack labels).

Usage (from the repo root, where README.md and assets/ live):
    python generate_cards.py

Edit things below, re-run, then commit the changed .svg files.

  * Add / edit a project  -> the project_card(...) calls (filename, title, description lines,
                             status text + colour, category text + colour, accent colour, id)
                             then reference assets/cards/<filename>.svg in README.md.
  * Stat tiles            -> the stat(...) calls
  * Bio / quick facts     -> the `lines` list and the `facts` list in the "about cards" section
  * Colours               -> BLUE / GREEN / AMBER / PURPLE / RED
  * Fonts                 -> SANS / MONO at the top (system fonts only; web fonts can't load in README images)
  * Animation speed       -> "7s" in .run, "1.8s" in .pulse
Note: each project_card needs a unique last argument gid=<number>.
"""
import os
os.makedirs("assets/cards", exist_ok=True)
os.makedirs("assets/ui", exist_ok=True)
import html, os

SANS = "'Segoe UI', Ubuntu, 'Helvetica Neue', Arial, sans-serif"
MONO = "'Fira Code', 'SF Mono', Consolas, 'Liberation Mono', monospace"

def esc(s): return html.escape(s, quote=False)

import math
def perim(w, h, r=18):
    return 2*((w-2-2*r)+(h-2-2*r)) + 2*math.pi*r

def style(accent, w, h):
    P = perim(w, h)
    return f"""<style>
  .t{{font-family:{SANS};}}
  .m{{font-family:{MONO};}}
  .fade{{animation:fade .9s ease both}}
  .run{{stroke-dasharray:{P*0.16:.1f} {P*0.84:.1f};animation:run 7s linear infinite}}
  .pulse{{animation:pulse 1.8s ease-in-out infinite;transform-box:fill-box;transform-origin:center}}
  @keyframes fade{{from{{opacity:0}}to{{opacity:1}}}}
  @keyframes run{{from{{stroke-dashoffset:0}}to{{stroke-dashoffset:-{P:.1f}}}}}
  @keyframes pulse{{0%,100%{{opacity:1;transform:scale(1)}}50%{{opacity:.35;transform:scale(1.6)}}}}
  @media (prefers-reduced-motion: reduce){{.fade,.run,.pulse{{animation:none}}}}
</style>"""

def frame(w, h, accent, body, gid):
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img">
{style(accent, w, h)}
<defs>
  <linearGradient id="bg{gid}" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0" stop-color="#171c26"/><stop offset="1" stop-color="#0d1117"/>
  </linearGradient>
  <radialGradient id="glow{gid}" cx="1" cy="0" r="0.9">
    <stop offset="0" stop-color="{accent}" stop-opacity="0.22"/><stop offset="1" stop-color="{accent}" stop-opacity="0"/>
  </radialGradient>
</defs>
<g class="fade">
  <rect x="1" y="1" width="{w-2}" height="{h-2}" rx="18" fill="url(#bg{gid})" stroke="#30363d" stroke-width="1.5"/>
  <rect x="1" y="1" width="{w-2}" height="{h-2}" rx="18" fill="url(#glow{gid})"/>
  <rect x="1" y="1" width="{w-2}" height="{h-2}" rx="18" fill="none" stroke="{accent}" stroke-width="2.2" stroke-linecap="round" class="run"/>
{body}
</g>
</svg>"""

def pill(x, y, text, color, dot=False):
    tw = len(text) * 7.4
    w = tw + 28 + (14 if dot else 0)
    out = f'<rect x="{x}" y="{y}" width="{w:.0f}" height="24" rx="12" fill="{color}" fill-opacity="0.14" stroke="{color}" stroke-opacity="0.55"/>'
    tx = x + 14
    if dot:
        out += f'<circle cx="{x+14}" cy="{y+12}" r="3.5" fill="{color}" class="pulse"/>'
        tx += 14
    out += f'<text x="{tx}" y="{y+16}" font-size="11.5" font-weight="600" fill="{color}" class="t">{esc(text)}</text>'
    return out, w

def project_card(fn, name, lines, status, scolor, cat, ccolor, accent, cta="View repository →", gid=0):
    w, h = 400, 206
    b = f'<text x="28" y="50" font-size="22" font-weight="700" fill="#e6edf3" class="t">{esc(name)}</text>\n'
    y = 82
    for ln in lines:
        b += f'<text x="28" y="{y}" font-size="13.5" fill="#9da7b3" class="t">{esc(ln)}</text>\n'
        y += 22
    p1, w1 = pill(28, 130, status, scolor, dot=True)
    p2, _ = pill(28 + w1 + 8, 130, cat, ccolor)
    b += p1 + "\n" + p2 + "\n"
    b += f'<text x="28" y="186" font-size="13" font-weight="700" fill="{accent}" class="t">{esc(cta)}</text>\n'
    open(f"assets/cards/{fn}.svg", "w").write(frame(w, h, accent, b, gid))

BLUE, GREEN, AMBER, PURPLE, RED = "#36BCF7", "#9ece6a", "#e0af68", "#bb9af7", "#f7768e"

project_card("lambda-prep", "Lambda Prep", ["Resource Hub for CISCE students."],
             "In Progress", AMBER, "Education", BLUE, BLUE, gid=1)
project_card("krishilink", "KrishiLink", ["Bridging agriculture & technology", "for a stronger India."],
             "Shipped", GREEN, "AgriTech", GREEN, GREEN, gid=2)
project_card("flowintel", "FlowIntel", ["Intelligence engine for automation workflows,", "auditing them for security & quality."],
             "Shipped", GREEN, "Automation", PURPLE, PURPLE, gid=3)
project_card("pookoo-run", "Pookoo Run", ["2D endless runner. Dodge firewolves and", "shapeshift through an enchanted forest."],
             "Shipped", GREEN, "Game", RED, RED, gid=4)
project_card("icse-resources", "ICSE Resources", ["Resource hub for ICSE students."],
             "Shipped", GREEN, "Education", BLUE, BLUE, gid=5)
project_card("meteonerd", "MeteoNerd", ["Hyperlocal weather intelligence web app."],
             "Shipped", GREEN, "Weather", AMBER, AMBER, gid=6)

# "more" card
w, h = 400, 206
b = f'''<path d="M200 56 C203 74 208 79 226 82 C208 85 203 90 200 108 C197 90 192 85 174 82 C192 79 197 74 200 56 Z" fill="{BLUE}"/>
<text x="200" y="124" text-anchor="middle" font-size="18" font-weight="700" fill="#e6edf3" class="t">...and much more in the works</text>
<text x="200" y="148" text-anchor="middle" font-size="12.5" fill="#9da7b3" class="t">Follow along for the next weird side-quest.</text>
<text x="200" y="184" text-anchor="middle" font-size="13" font-weight="700" fill="{BLUE}" class="t">Browse all repositories →</text>'''
open("assets/cards/more.svg", "w").write(frame(w, h, BLUE, b, 7))

# stat tiles
def stat(fn, big, label, accent, gid):
    w, h = 190, 104
    b = f'''<text x="95" y="52" text-anchor="middle" font-size="34" font-weight="800" fill="{accent}" class="t">{esc(big)}</text>
<text x="95" y="80" text-anchor="middle" font-size="9.5" font-weight="600" letter-spacing="1.6" fill="#9da7b3" class="t">{esc(label)}</text>'''
    open(f"assets/ui/{fn}.svg", "w").write(frame(w, h, accent, b, gid))

stat("stat-shipped", "5", "PROJECTS SHIPPED", GREEN, 11)
stat("stat-building", "1", "CURRENTLY BUILDING", AMBER, 12)
stat("stat-e2e", "E2E", "FRONTEND → DEPLOY", BLUE, 13)
stat("stat-core", "TS", "REACT & CLOUDFLARE", PURPLE, 14)

# about cards
w, h = 400, 270
lines = ["I move fast, prototype by feel, and iterate",
         "in the open. I build end-to-end (frontend,",
         "backend, deployment), mostly in the",
         "TypeScript / React / Cloudflare world.",
         "",
         "Constantly hunting for the next weird",
         "problem worth prototyping."]
b = f'<text x="28" y="50" font-size="19" font-weight="700" fill="#e6edf3" class="t">Vibe coder, full-stack by feel</text>\n'
y = 84
for ln in lines:
    if ln:
        b += f'<text x="28" y="{y}" font-size="13.5" fill="#9da7b3" class="t">{esc(ln)}</text>\n'
    y += 20
open("assets/ui/about-bio.svg", "w").write(frame(w, h, BLUE, b, 21))

facts = [("BUILDING", "Lambda Prep"), ("CORE STACK", "TypeScript, React, Cloudflare"),
         ("FOCUS", "Resource hubs, web apps, tools"), ("HOBBY", "Weird side-quests")]
b = f'<text x="28" y="50" font-size="19" font-weight="700" fill="#e6edf3" class="t">Quick facts</text>\n'
y = 94
for k, v in facts:
    b += f'<text x="28" y="{y}" font-size="10.5" font-weight="600" letter-spacing="1.4" fill="{PURPLE}" class="t">{k}</text>\n'
    b += f'<text x="28" y="{y+22}" font-size="14" fill="#e6edf3" class="t">{esc(v)}</text>\n'
    y += 46
open("assets/ui/about-facts.svg", "w").write(frame(w, h, PURPLE, b, 22))

# stack group pills
def label(fn, text, accent, gid):
    w, h = 170, 38
    b = f'<text x="85" y="24.5" text-anchor="middle" font-size="12.5" font-weight="700" letter-spacing="0.6" fill="{accent}" class="t">{esc(text)}</text>'
    s = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img">
<style>.t{{font-family:{SANS}}}</style>
<rect x="1" y="1" width="{w-2}" height="{h-2}" rx="19" fill="#0d1117" stroke="{accent}" stroke-opacity="0.6" stroke-width="1.5"/>
{b}
</svg>"""
    open(f"assets/ui/{fn}.svg", "w").write(s)

label("lbl-frontend", "FRONTEND", BLUE, 31)
label("lbl-backend", "BACKEND & INFRA", GREEN, 32)
label("lbl-mobile", "MOBILE", AMBER, 33)
label("lbl-languages", "LANGUAGES", PURPLE, 34)
label("lbl-tools", "TOOLS", RED, 35)
