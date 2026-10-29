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

def style(accent, w, h, r=18):
    P = perim(w, h, r)
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

def frame(w, h, accent, body, gid, r=18):
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img">
{style(accent, w, h, r)}
<defs>
  <linearGradient id="bg{gid}" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0" stop-color="#171c26"/><stop offset="1" stop-color="#0d1117"/>
  </linearGradient>
  <radialGradient id="glow{gid}" cx="1" cy="0" r="0.9">
    <stop offset="0" stop-color="{accent}" stop-opacity="0.22"/><stop offset="1" stop-color="{accent}" stop-opacity="0"/>
  </radialGradient>
</defs>
<g class="fade">
  <rect x="1" y="1" width="{w-2}" height="{h-2}" rx="{r}" fill="url(#bg{gid})" stroke="#30363d" stroke-width="1.5"/>
  <rect x="1" y="1" width="{w-2}" height="{h-2}" rx="{r}" fill="url(#glow{gid})"/>
  <rect x="1" y="1" width="{w-2}" height="{h-2}" rx="{r}" fill="none" stroke="{accent}" stroke-width="2.2" stroke-linecap="round" class="run"/>
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


# ───────────────────────── v2 aesthetics ─────────────────────────

# animated section headings (pill with running border)
def heading(fn, text, accent, gid):
    tw = len(text) * 14.5
    w = int(tw + 120); h = 58
    cx = w / 2
    b = f'''<path d="M30 29 l7 -7 l7 7 l-7 7 z" fill="{accent}"/>
<text x="{cx:.0f}" y="37" text-anchor="middle" font-size="23" font-weight="800" letter-spacing="0.5" fill="#e6edf3" class="t">{esc(text)}</text>
<path d="M{w-44} 29 l7 -7 l7 7 l-7 7 z" fill="{accent}"/>'''
    open(f"assets/ui/{fn}.svg", "w").write(frame(w, h, accent, b, gid, r=29))
    print("heading", fn, w)

heading("h-about", "About Me", BLUE, 41)
heading("h-projects", "Projects", GREEN, 42)
heading("h-stack", "Tech Stack", PURPLE, 43)
heading("h-stats", "GitHub Dashboard", AMBER, 44)
heading("h-contact", "Let's Connect", RED, 45)

# nav pills
def navpill(fn, text, accent):
    w, h = 108, 36
    s_ = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img">
<style>.t{{font-family:{SANS}}} .p{{animation:pp 3.2s ease-in-out infinite}} @keyframes pp{{0%,100%{{opacity:1}}50%{{opacity:.4}}}} @media (prefers-reduced-motion: reduce){{.p{{animation:none}}}}</style>
<rect x="1" y="1" width="{w-2}" height="{h-2}" rx="18" fill="#0d1117" stroke="{accent}" stroke-opacity="0.55" stroke-width="1.5"/>
<circle cx="20" cy="18" r="3.2" fill="{accent}" class="p"/>
<text x="64" y="22.5" text-anchor="middle" font-size="11.5" font-weight="700" letter-spacing="1.2" fill="#e6edf3" class="t">{esc(text)}</text>
</svg>"""
    open(f"assets/ui/{fn}.svg", "w").write(s_)

navpill("nav-about", "ABOUT", BLUE)
navpill("nav-projects", "PROJECTS", GREEN)
navpill("nav-stack", "STACK", PURPLE)
navpill("nav-stats", "STATS", AMBER)
navpill("nav-contact", "CONTACT", RED)

# animated divider
open("assets/ui/divider.svg", "w").write(f"""<svg xmlns="http://www.w3.org/2000/svg" width="800" height="12" viewBox="0 0 800 12" role="img">
<style>
  .d{{animation:slide 5s ease-in-out infinite alternate}}
  @keyframes slide{{from{{transform:translateX(0)}}to{{transform:translateX(560px)}}}}
  @media (prefers-reduced-motion: reduce){{.d{{animation:none}}}}
</style>
<defs>
  <linearGradient id="g" x1="0" x2="1">
    <stop offset="0" stop-color="{BLUE}" stop-opacity="0"/><stop offset="0.5" stop-color="{BLUE}" stop-opacity="0.6"/><stop offset="1" stop-color="{PURPLE}" stop-opacity="0"/>
  </linearGradient>
  <linearGradient id="h" x1="0" x2="1">
    <stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset="0.5" stop-color="#fff" stop-opacity="0.95"/><stop offset="1" stop-color="#fff" stop-opacity="0"/>
  </linearGradient>
</defs>
<rect x="0" y="5" width="800" height="2" rx="1" fill="url(#g)"/>
<rect class="d" x="60" y="4.5" width="180" height="3" rx="1.5" fill="url(#h)"/>
</svg>""")

# terminal card with typing animation
def terminal():
    w, h = 600, 296
    lines = [("cmd", "whoami"), ("out", "jivaansh-yadav"),
             ("cmd", "cat stack.txt"), ("out", "TypeScript · React · Cloudflare · Supabase"),
             ("cmd", "./now.sh"), ("out", "building Lambda Prep for CISCE students"),
             ("cmd", "echo $VIBE"), ("out", "full-stack, end-to-end, side-quests")]
    CW = 8.2            # monospace char width estimate at 13.5px
    spd, gap, hold = 0.05, 0.4, 5.0
    t = 0.6
    sched = []
    for kind, txt in lines:
        n = len(txt) + (2 if kind == "cmd" else 0)
        dur = max(0.25, n * spd)
        sched.append((t, dur, n)); t += dur + gap
    T = t + hold
    css, body = "", ""
    y0 = 84
    for i, ((kind, txt), (st, dur, n)) in enumerate(zip(lines, sched)):
        y = y0 + i * 24
        pw = n * CW + 6
        s_pct, e_pct = st / T * 100, (st + dur) / T * 100
        css += (f"@keyframes ty{i}{{0%,{s_pct:.2f}%{{width:0}}{e_pct:.2f}%,100%{{width:{pw:.0f}px}}}}"
                f".c{i}{{animation:ty{i} {T:.1f}s steps({n},end) infinite}}\n")
        body += f'<clipPath id="cp{i}"><rect class="c{i}" x="28" y="{y-16}" width="{pw:.0f}" height="22"/></clipPath>\n'
        if kind == "cmd":
            body += (f'<g clip-path="url(#cp{i})"><text x="28" y="{y}" font-size="13.5" class="m" fill="{GREEN}">$</text>'
                     f'<text x="46" y="{y}" font-size="13.5" class="m" fill="#e6edf3">{esc(txt)}</text></g>\n')
        else:
            body += f'<g clip-path="url(#cp{i})"><text x="46" y="{y}" font-size="13.5" class="m" fill="{BLUE}">{esc(txt)}</text></g>\n'
    cur_y = y0 + len(lines) * 24
    body += f'<text x="28" y="{cur_y}" font-size="13.5" class="m" fill="{GREEN}">$</text><rect class="cur" x="46" y="{cur_y-13}" width="8" height="16" fill="{BLUE}"/>'
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img">
<style>
  .m{{font-family:{MONO}}} .t{{font-family:{SANS}}}
  .cur{{animation:blink 1s steps(1) infinite}}
  @keyframes blink{{0%,50%{{opacity:1}}50.01%,100%{{opacity:0}}}}
  {css}
  @media (prefers-reduced-motion: reduce){{.cur{{animation:none}}{''.join(f'.c{i}{{animation:none}}' for i in range(len(lines)))}}}
</style>
<defs>
  <linearGradient id="tb" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#171c26"/><stop offset="1" stop-color="#0b0e14"/></linearGradient>
</defs>
<rect x="1" y="1" width="{w-2}" height="{h-2}" rx="18" fill="url(#tb)" stroke="#30363d" stroke-width="1.5"/>
<path d="M19 1 H{w-19} A18 18 0 0 1 {w-1} 19 V44 H1 V19 A18 18 0 0 1 19 1 Z" fill="#1c2230"/>
<line x1="1" y1="44" x2="{w-1}" y2="44" stroke="#30363d"/>
<circle cx="28" cy="23" r="6" fill="#ff5f57"/><circle cx="48" cy="23" r="6" fill="#febc2e"/><circle cx="68" cy="23" r="6" fill="#28c840"/>
<text x="{w/2}" y="27" text-anchor="middle" font-size="12" class="m" fill="#8b949e">~/jivaansh — zsh</text>
{body}
</svg>"""
    open("assets/ui/terminal.svg", "w").write(svg)

terminal()

# contact CTA card
b = f'''<text x="300" y="52" text-anchor="middle" font-size="26" font-weight="800" fill="#e6edf3" class="t">Let's build something weird.</text>
<text x="300" y="80" text-anchor="middle" font-size="13.5" fill="#9da7b3" class="t">Got a weird idea, a collab, or a project worth prototyping?</text>
<rect x="238" y="98" width="124" height="32" rx="16" fill="{BLUE}"/>
<text x="300" y="119" text-anchor="middle" font-size="13.5" font-weight="800" fill="#0d1117" class="t">Say hi  →</text>'''
open("assets/ui/cta.svg", "w").write(frame(600, 150, BLUE, b, 51))
