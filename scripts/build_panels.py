"""
Builds the coloured section panels and link buttons in /assets.

GitHub strips colour from Markdown, so every coloured section of the profile is
an SVG. Facts live in the data near the top of each builder: edit them and run

    python scripts/build_panels.py

Palette and grammar follow DevDevise: cyan = systems and data in motion,
violet = research and the unresolved, blue = links and interaction,
amber = signal (sparingly). Solid = built, dashed = proposed.
"""
from pathlib import Path
import xml.dom.minidom

OUT = Path(__file__).resolve().parent.parent / "assets"

SANS = "'Inter Tight','Inter',system-ui,-apple-system,'Segoe UI',Helvetica,Arial,sans-serif"
MONO = "'JetBrains Mono',ui-monospace,SFMono-Regular,Menlo,Consolas,'Liberation Mono',monospace"
VOID, PANEL, LINE = "#04060B", "#0B1120", "#161D2E"
INK, GR, FA = "#EEF1F8", "#9AA3B8", "#6B7489"
BLUE, CYAN, VIOLET, AMBER = "#4C8DFF", "#35E3FF", "#9D7BFF", "#FFB547"


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def tw(text, size, mono=False):
    """Approximate rendered text width."""
    return len(text) * size * (0.6 if mono else 0.52)


def wrap(text, max_px, size, mono=False):
    lines, cur = [], ""
    for word in text.split():
        trial = f"{cur} {word}".strip()
        if tw(trial, size, mono) > max_px and cur:
            lines.append(cur)
            cur = word
        else:
            cur = trial
    return lines + ([cur] if cur else [])


def panel(name, w, h, title, desc, num, label, right, head, grad, body, glows=()):
    glow_defs, glow_rects = "", ""
    for i, (cx, cy, rx, ry, col, op) in enumerate(glows):
        glow_defs += (f'<radialGradient id="g{i}" cx="0" cy="0" r="1" gradientUnits="userSpaceOnUse" '
                      f'gradientTransform="translate({cx} {cy}) scale({rx} {ry})">'
                      f'<stop offset="0" stop-color="{col}" stop-opacity="{op}"/>'
                      f'<stop offset="1" stop-color="{col}" stop-opacity="0"/></radialGradient>')
        glow_rects += f'<rect x="2" y="2" width="{w-4}" height="{h-4}" rx="13" fill="url(#g{i})"/>'
    stops = "".join(f'<stop offset="{i/(len(grad)-1):.2f}" stop-color="{c}"/>' for i, c in enumerate(grad))
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" aria-labelledby="title desc">
  <title id="title">{esc(title)}</title>
  <desc id="desc">{esc(desc)}</desc>
  <style>
    .sans{{font-family:{SANS}}}
    .m{{font-family:{MONO}}}
    .in{{animation:in .8s cubic-bezier(.2,.7,.2,1) both}}
    .blink{{animation:blink 1.1s steps(1,end) infinite}}
    @keyframes in{{from{{opacity:0;transform:translateY(8px)}}to{{opacity:1;transform:translateY(0)}}}}
    @keyframes blink{{50%{{opacity:0}}}}
    @media (prefers-reduced-motion:reduce){{.in,.blink{{animation:none}}}}
  </style>
  <defs>
    <linearGradient id="top" x1="0" y1="0" x2="{w}" y2="0" gradientUnits="userSpaceOnUse">{stops}</linearGradient>
    {glow_defs}
  </defs>
  <rect x="1" y="1" width="{w-2}" height="{h-2}" rx="14" fill="{VOID}" stroke="{LINE}" stroke-width="2"/>
  {glow_rects}
  <rect x="1" y="1" width="{w-2}" height="3" rx="1.5" fill="url(#top)"/>
'''
    if num:
        svg += (f'  <text class="m" x="28" y="34" font-size="12" letter-spacing="2" font-weight="700" fill="{head}">{esc(num)} · {esc(label)}</text>\n'
                f'  <text class="m" x="{w-28}" y="34" font-size="12" letter-spacing="1" fill="{FA}" text-anchor="end">{esc(right)}</text>\n')
    svg += body + "\n</svg>\n"
    (OUT / name).write_text(svg, encoding="utf-8")
    xml.dom.minidom.parseString(svg.encode("utf-8"))  # fail loudly on malformed output
    print("wrote", name)


def mark(x, y, kind, col, s=11):
    """Provenance marks: real (solid), experimental (half), illustrative (dashed)."""
    if kind == "real":
        return f'<rect x="{x}" y="{y}" width="{s}" height="{s}" fill="{col}"/>'
    if kind == "exp":
        return (f'<rect x="{x+.5}" y="{y+.5}" width="{s-1}" height="{s-1}" fill="none" stroke="{col}"/>'
                f'<rect x="{x+.5}" y="{y+.5}" width="{(s-1)/2}" height="{s-1}" fill="{col}"/>')
    return f'<rect x="{x+.5}" y="{y+.5}" width="{s-1}" height="{s-1}" fill="none" stroke="{col}" stroke-dasharray="2.5 2"/>'


def pill(x, y, text, col, size=10):
    w = tw(text, size, True) + 18
    return (f'<rect x="{x}" y="{y}" width="{w:.0f}" height="20" rx="10" fill="{col}" fill-opacity=".1" stroke="{col}" stroke-opacity=".6"/>'
            f'<text class="m" x="{x+9}" y="{y+14}" font-size="{size}" letter-spacing="1" fill="{col}">{esc(text)}</text>'), w


# ---------------------------------------------------------------- 01 SIGNAL
def signal():
    import math
    import random
    random.seed(7)
    y0, pts, x = 262, [], 28
    while x <= 380:
        amp = 22 * (1 - (x - 28) / 352 * 0.35)
        pts.append((x, y0 + random.uniform(-amp, amp)))
        x += 9
    while x <= 500:
        t = (x - 380) / 120
        pts.append((x, y0 + 18 * math.sin((x - 380) / 9) * (1 - t * 0.4)))
        x += 4
    d = "M" + " L".join(f"{a:.0f} {b:.1f}" for a, b in pts)
    hi, lo = y0 - 18, y0 + 18
    level = hi
    d += f" L{x} {pts[-1][1]:.1f} L{x} {hi}"
    while x + 22 <= 852:
        nx = x + 22
        d += f" L{nx} {level}"
        level = lo if level == hi else hi
        d += f" L{nx} {level}"
        x = nx
    d += f" L852 {level}"

    fields = [
        (28, 352, CYAN, "ROLE", "Founder & CEO · DevDevise, SysMalla"),
        (452, 352, BLUE, "PRACTICE", "Software engineer · systems architect"),
        (28, 412, VIOLET, "FOCUS", "Intelligent systems · AI / LLM · automation"),
        (452, 412, AMBER, "RECORD", "◆ Gold medal, BS Software Engineering"),
    ]
    f = ""
    for fx, fy, col, lab, val in fields:
        f += (f'<rect x="{fx}" y="{fy}" width="3" height="40" fill="{col}"/>'
              f'<text class="m" x="{fx+14}" y="{fy+12}" font-size="11" letter-spacing="2" font-weight="700" fill="{col}">{lab}</text>'
              f'<text class="sans" x="{fx+14}" y="{fy+36}" font-size="16" fill="{INK}">{esc(val)}</text>\n')
    body = f'''
  <defs>
    <linearGradient id="spec" x1="28" y1="0" x2="852" y2="0" gradientUnits="userSpaceOnUse"><stop offset="0" stop-color="{VIOLET}"/><stop offset=".5" stop-color="{BLUE}"/><stop offset="1" stop-color="{CYAN}"/></linearGradient>
    <linearGradient id="qg" x1="28" y1="0" x2="640" y2="0" gradientUnits="userSpaceOnUse"><stop offset="0" stop-color="#C4B2FF"/><stop offset=".45" stop-color="#7FB0FF"/><stop offset="1" stop-color="{CYAN}"/></linearGradient>
    <filter id="blur" x="-10%" y="-50%" width="120%" height="200%"><feGaussianBlur stdDeviation="4"/></filter>
  </defs>
  <style>.run{{stroke-dasharray:70 1400;animation:run 3.2s linear infinite}}@keyframes run{{from{{stroke-dashoffset:1470}}to{{stroke-dashoffset:0}}}}@media (prefers-reduced-motion:reduce){{.run{{display:none}}}}</style>
  <text class="sans in" x="28" y="88" font-size="18" fill="{GR}" style="animation-delay:.1s">I’m a software engineer and founder. I founded <tspan fill="{INK}" font-weight="600">DevDevise</tspan> on one idea:</text>
  <g class="sans in" font-size="33" font-weight="600" letter-spacing="-.5" fill="url(#qg)" style="animation-delay:.35s">
    <text x="26" y="140">Strong systems should be <tspan fill="#C4B2FF" font-style="italic">devised</tspan></text>
    <text x="26" y="180">through investigation and evidence</text>
    <text x="26" y="220">before they are <tspan fill="{CYAN}">engineered.</tspan></text>
  </g>
  <path d="{d}" fill="none" stroke="url(#spec)" stroke-width="5" opacity=".35" filter="url(#blur)"/>
  <path d="{d}" fill="none" stroke="url(#spec)" stroke-width="1.8" stroke-linejoin="round"/>
  <path class="run" d="{d}" fill="none" stroke="#FFFFFF" stroke-width="2.4" stroke-linecap="round" pathLength="1470" opacity=".9"/>
  <g class="m" font-size="10" letter-spacing="2">
    <text x="28" y="312" fill="{VIOLET}">SIGNAL · NOISE</text>
    <text x="440" y="312" fill="{BLUE}" text-anchor="middle">DEVISE</text>
    <text x="852" y="312" fill="{CYAN}" text-anchor="end">SYSTEM · STRUCTURE</text>
  </g>
  <line x1="28" y1="332" x2="852" y2="332" stroke="{LINE}" stroke-width="1.5"/>
  <g class="in" style="animation-delay:.7s">
  {f}
    <rect x="28" y="472" width="3" height="32" fill="{FA}"/>
    <text class="m" x="42" y="484" font-size="11" letter-spacing="2" font-weight="700" fill="{GR}">SHIPPED</text>
    <text class="sans" x="42" y="502" font-size="14" fill="{GR}">CRMs · ERP modules · order management · calendar sync · AI matchmaking, across Pakistan and the GCC</text>
  </g>'''
    panel("signal.svg", 880, 520, "01 · Signal — who Adnan Yar is",
          "I'm a software engineer and founder. I founded DevDevise on one idea: strong systems should be devised through "
          "investigation and evidence before they are engineered. Role: founder and CEO, DevDevise and SysMalla. Practice: software "
          "engineer, systems architect. Focus: intelligent systems, AI and LLM, automation. Record: gold medal, BS Software Engineering.",
          "01", "SIGNAL", "transmission from adnan.yar", CYAN, (VIOLET, BLUE, CYAN), body,
          glows=[(120, 150, 360, 220, VIOLET, .16), (800, 270, 340, 200, CYAN, .13)])


# ---------------------------------------------------------------- 03 SYSTEMS (header)
def systems_head():
    items = [("real", CYAN, "W-001", "Task4Task", "paid tasks + barter"),
             ("real", CYAN, "W-002", "CivicPulse", "community intelligence"),
             ("exp", VIOLET, "W-003", "Agrimonitor", "remote-sensing R&D")]
    body = (f'<text class="sans in" x="28" y="80" font-size="26" font-weight="600" fill="{INK}">Systems in development, '
            f'<tspan fill="{CYAN}">built through DevDevise.</tspan></text>'
            f'<text class="sans" x="28" y="110" font-size="15" fill="{GR}">Real and active. No user, revenue or accuracy figures are published yet, so none are claimed here.</text>')
    x = 28
    for kind, col, wid, name, what in items:
        body += mark(x, 135, kind, col)
        body += f'<text class="m" x="{x+18}" y="145" font-size="12" font-weight="700" letter-spacing="1" fill="{col}">{wid}</text>'
        body += f'<text class="sans" x="{x+70}" y="145" font-size="14" font-weight="600" fill="{INK}">{esc(name)}</text>'
        body += f'<text class="m" x="{x+18}" y="164" font-size="10.5" fill="{FA}">{esc(what)}</text>'
        x += 280
    panel("h03-systems.svg", 880, 186, "03 · Systems in development",
          "Systems in development, built through DevDevise: W-001 Task4Task, a marketplace for paid tasks and barter; W-002 CivicPulse, "
          "AI community intelligence; W-003 Agrimonitor, remote-sensing R&D. No user, revenue or accuracy figures are published yet.",
          "03", "SYSTEMS", "active · in development", CYAN, (CYAN, BLUE, VIOLET), body,
          glows=[(760, 60, 320, 160, CYAN, .12)])


# ---------------------------------------------------------------- 04 SHIPPED
SHIPPED = [
    dict(id="SHIP-01", name="ChattersHub CRM",
         problem="Lead handling depended on manual effort.",
         system="A CRM built around automating the lead pipeline.",
         stack=["Next.js · React · Tailwind · Node.js", "TypeScript · Express · MongoDB · AWS S3 · Docker"],
         kind="outcome", big="60%", result="less manual lead-handling time"),
    dict(id="SHIP-02", name="Syndication + OMS · Comtanix",
         problem="Posting to every channel by hand; slow order handling.",
         system="A social-media syndication tool, and an order management system.",
         stack=["syndication · order management · e-commerce"],
         kind="outcome", big="90%", result="of posting workflows automated", extra="+30% engagement · +60% team productivity (OMS)"),
    dict(id="SHIP-03", name="Pindot Calendar Sync",
         problem="Google and CalDAV calendars drift apart.",
         system="Sync between Google Calendar and a CalDAV server (Baïkal).",
         stack=["Laravel · MySQL · Google Calendar API · CalDAV"],
         kind="aim", result="One calendar, whichever client edits it."),
    dict(id="SHIP-04", name="Lease Match NYC",
         problem="Matching renters to apartments by hand.",
         system="An AI-powered apartment matchmaking platform.",
         stack=["Express · React · Tailwind · MongoDB", "OpenAI · geolocation"],
         kind="aim", result="Match renters to apartments by fit and place."),
]


def shipped():
    cw, ch = 404, 300
    body = (f'<text class="sans" x="28" y="76" font-size="15" fill="{GR}">Delivered as an engineer, before and alongside DevDevise. '
            f'Read each card <tspan fill="{INK}">problem → system → stack → </tspan><tspan fill="{CYAN}">outcome</tspan>.</text>')
    for i, s in enumerate(SHIPPED):
        x = 28 if i % 2 == 0 else 448
        y = 100 + (i // 2) * (ch + 16)
        col = CYAN if s["kind"] == "outcome" else VIOLET
        delay = .15 * i
        b = f'<g class="in" style="animation-delay:{delay:.2f}s">'
        b += f'<rect x="{x}" y="{y}" width="{cw}" height="{ch}" rx="10" fill="{PANEL}" stroke="{col}" stroke-opacity=".35"/>'
        b += f'<rect x="{x}" y="{y+14}" width="3" height="34" fill="{col}"/>'
        b += mark(x + 18, y + 20, "real", col, 9)
        b += f'<text class="m" x="{x+34}" y="{y+29}" font-size="11" font-weight="700" letter-spacing="1.5" fill="{col}">{s["id"]}</text>'
        b += f'<text class="sans" x="{x+18}" y="{y+50}" font-size="18" font-weight="600" fill="{INK}">{esc(s["name"])}</text>'
        yy = y + 80
        for lab, val in (("PROBLEM", s["problem"]), ("SYSTEM", s["system"])):
            b += f'<text class="m" x="{x+18}" y="{yy}" font-size="10" letter-spacing="2" fill="{FA}">{lab}</text>'
            lines = wrap(val, cw - 110, 13.5)
            for j, line in enumerate(lines):
                b += f'<text class="sans" x="{x+96}" y="{yy + j*18}" font-size="13.5" fill="{GR}">{esc(line)}</text>'
            yy += 18 * len(lines) + 16
        b += f'<text class="m" x="{x+18}" y="{yy}" font-size="10" letter-spacing="2" fill="{FA}">STACK</text>'
        for j, line in enumerate(s["stack"]):
            b += f'<text class="m" x="{x+96}" y="{yy + j*17}" font-size="11" fill="{BLUE}">{esc(line)}</text>'
        yy = y + ch - 52
        b += f'<line x1="{x+18}" y1="{yy-18}" x2="{x+cw-18}" y2="{yy-18}" stroke="{LINE}"/>'
        if s["kind"] == "outcome":
            b += f'<text class="m" x="{x+18}" y="{yy}" font-size="10" letter-spacing="2" fill="{CYAN}">OUTCOME</text>'
            b += f'<text class="sans" x="{x+16}" y="{yy+34}" font-size="34" font-weight="700" fill="{CYAN}">{s["big"]}</text>'
            bx = x + 18 + tw(s["big"], 34) + 18
            b += f'<text class="sans" x="{bx:.0f}" y="{yy+20 if s.get("extra") else yy+30}" font-size="13.5" fill="{INK}">{esc(s["result"])}</text>'
            if s.get("extra"):
                b += f'<text class="sans" x="{bx:.0f}" y="{yy+38}" font-size="12" fill="{GR}">{esc(s["extra"])}</text>'
        else:
            b += f'<text class="m" x="{x+18}" y="{yy}" font-size="10" letter-spacing="2" fill="{VIOLET}">AIM · NOT MEASURED</text>'
            b += f'<text class="sans" x="{x+18}" y="{yy+30}" font-size="16" font-style="italic" fill="#C4B2FF">{esc(s["result"])}</text>'
        body += b + "</g>\n"
    h = 100 + 2 * ch + 16 + 46
    body += (f'<text class="m" x="28" y="{h-18}" font-size="11" letter-spacing=".5" fill="{FA}">'
             f'Where a result was measured it is <tspan fill="{CYAN}">cyan</tspan>; where it wasn’t, the card says aim, in <tspan fill="{VIOLET}">violet</tspan>: unproven.</text>')
    desc = " ".join(f'{s["id"]} {s["name"]}: problem, {s["problem"]} System, {s["system"]} Stack: {" · ".join(s["stack"])}. '
                    + (f'Outcome: {s["big"]} {s["result"]}. {s.get("extra","")}' if s["kind"] == "outcome" else f'Aim, not measured: {s["result"]}')
                    for s in SHIPPED)
    panel("shipped.svg", 880, h, "04 · Shipped — four case files", desc, "04", "SHIPPED",
          "problem → system → stack → outcome", CYAN, (BLUE, CYAN), body,
          glows=[(90, 120, 300, 200, BLUE, .1), (820, 560, 320, 220, CYAN, .1)])


# ---------------------------------------------------------------- 05 ARCHITECTURE
def chips(x0, y0, x1, items, col):
    """Lay out chips left to right, wrapping; returns svg and the bottom y."""
    out, x, y = "", x0, y0
    for it in items:
        w = tw(it, 12, True) + 22
        if x + w > x1:
            x, y = x0, y + 34
        out += (f'<rect x="{x}" y="{y}" width="{w:.0f}" height="26" rx="13" fill="{col}" fill-opacity=".1" stroke="{col}" stroke-opacity=".55"/>'
                f'<text class="m" x="{x + 11}" y="{y + 17}" font-size="12" fill="{INK}">{esc(it)}</text>')
        x += w + 8
    return out, y + 26


def architecture():
    body = ""
    y = 62

    def band(x0, x1, y, label, col, items, sub=None):
        inner, bottom = chips(x0 + 20, y + 44, x1 - 16, items, col)
        hgt = bottom - y + 18
        s = (f'<rect x="{x0}" y="{y}" width="{x1-x0}" height="{hgt}" rx="10" fill="{col}" fill-opacity=".05" stroke="{col}" stroke-opacity=".35"/>'
             f'<rect x="{x0}" y="{y+14}" width="3" height="20" fill="{col}"/>'
             f'<text class="m" x="{x0+20}" y="{y+29}" font-size="11" font-weight="700" letter-spacing="2" fill="{col}">{label}</text>')
        if sub:
            s += f'<text class="m" x="{x1-16}" y="{y+29}" font-size="10" fill="{FA}" text-anchor="end">{esc(sub)}</text>'
        return s + inner, y + hgt

    def link(x, ya, yb, label, pid):
        return (f'<path id="{pid}" d="M{x} {ya}V{yb}" stroke="#3A4766" stroke-width="1.3"/>'
                f'<circle r="3" fill="{CYAN}"><animateMotion dur="1.2s" repeatCount="indefinite"><mpath href="#{pid}"/></animateMotion></circle>'
                + (f'<text class="m" x="{x+12}" y="{(ya+yb)/2+4:.0f}" font-size="10.5" fill="{FA}">{esc(label)}</text>' if label else ""))

    s, y2 = band(28, 852, y, "INTERFACE", BLUE, ["React", "Next.js", "Vue", "Tailwind CSS", "Expo / React Native"], "what people touch")
    body += s
    body += link(440, y2, y2 + 34, "REST · WebSockets · WebRTC", "l1")
    s, y3 = band(28, 852, y2 + 34, "APPLICATION", CYAN,
                 ["Node.js", "TypeScript", "Express", "Laravel", "PHP", "Python", "FastAPI", "RabbitMQ", "outbox / events", "microservices"],
                 "logic, lifecycles, events")
    body += s
    body += link(230, y3, y3 + 34, "", "l2") + link(650, y3, y3 + 34, "", "l3")
    s, ya = band(28, 420, y3 + 34, "DATA", CYAN, ["PostgreSQL", "MySQL", "MongoDB", "Redis", "Firebase RTDB"])
    s2, yb = band(460, 852, y3 + 34, "INTELLIGENCE", VIOLET, ["OpenAI", "LLM flows", "RAG", "pgvector", "Whisper"])
    body += s + s2
    mid = y3 + 34 + 60
    body += (f'<path id="rag" d="M420 {mid}H460" stroke="{VIOLET}" stroke-opacity=".7" stroke-width="1.3" stroke-dasharray="3 3"/>'
             f'<circle r="3" fill="{VIOLET}"><animateMotion dur="1s" repeatCount="indefinite" keyPoints="0;1;0" keyTimes="0;.5;1" calcMode="linear"><mpath href="#rag"/></animateMotion></circle>'
             f'<text class="m" x="440" y="{mid-10}" font-size="9" letter-spacing="1" fill="{VIOLET}" text-anchor="middle">RETRIEVAL</text>')
    y4 = max(ya, yb)
    body += link(440, y4, y4 + 34, "runs on", "l4")
    s, y5 = band(28, 852, y4 + 34, "INFRASTRUCTURE", GR, ["AWS", "Docker", "CI/CD", "Caddy", "Git"], "where it runs")
    body += s
    h = y5 + 28
    panel("architecture.svg", 880, h, "05 · Architecture — the stack as layers",
          "Interface: React, Next.js, Vue, Tailwind CSS, Expo / React Native. Connected over REST, WebSockets and WebRTC to the "
          "application layer: Node.js, TypeScript, Express, Laravel, PHP, Python, FastAPI, RabbitMQ, outbox events, microservices. "
          "Below it, data (PostgreSQL, MySQL, MongoDB, Redis, Firebase Realtime Database) and intelligence (OpenAI, LLM flows, RAG, "
          "pgvector, Whisper), linked by retrieval. Everything runs on AWS, Docker, CI/CD, Caddy and Git.",
          "05", "ARCHITECTURE", "the stack, as layers", BLUE, (BLUE, CYAN, VIOLET), body,
          glows=[(140, 80, 300, 160, BLUE, .1), (760, h - 120, 300, 180, VIOLET, .1)])


# ---------------------------------------------------------------- 06 LAB
QUESTIONS = [
    ("exp", "R-001", "Can a website demonstrate engineering reasoning instead of describing it?",
     "The DevDevise site is the experiment: accessibility audits, responsive checks and sequence timing, run on its own build.",
     ("TESTED · FINDINGS RECORDED", BLUE)),
    ("ill", "EX-01", "Can a retrieval system reliably tell when it doesn’t have the answer?", None, ("NOT RUN", VIOLET)),
    ("ill", "EX-02", "How long can a tool-using agent work before its errors compound?", None, ("NOT RUN", VIOLET)),
    ("ill", "EX-03", "Can we tell a model’s input has drifted before its accuracy drops?", None, ("NOT RUN", VIOLET)),
]
BENCH = [
    ("MedQuery", "Multi-tenant medical RAG API: ingestion, chunking, embeddings, retrieval and chat per workspace.",
     "FastAPI · Postgres + pgvector"),
    ("Medical RAG assistant", "Documents, images and speech feeding one retrieval pipeline.", "Python · vector store · LLM"),
    ("Audio Intelligence Parser", "Local speech-to-text, then strict structured extraction.", "FastAPI · Whisper · OpenAI"),
]


def lab():
    body = (f'<text class="sans" x="28" y="76" font-size="15" fill="{GR}">Questions get the same treatment as systems: '
            f'<tspan fill="#C4B2FF">stated before they’re tested</tspan>, and labelled honestly.</text>')
    y = 104
    for i, (kind, qid, q, note, (state, scol)) in enumerate(QUESTIONS):
        col = VIOLET if kind == "ill" else BLUE
        b = f'<g class="in" style="animation-delay:{.12*i:.2f}s">'
        b += mark(28, y + 4, kind, col, 12)
        if kind == "exp":
            b += (f'<circle cx="34" cy="{y+10}" r="6" fill="none" stroke="{BLUE}">'
                  f'<animate attributeName="r" values="6;16" dur="2s" repeatCount="indefinite"/>'
                  f'<animate attributeName="opacity" values=".8;0" dur="2s" repeatCount="indefinite"/></circle>')
        b += f'<text class="m" x="50" y="{y+15}" font-size="12" font-weight="700" letter-spacing="1" fill="{col}">{qid}</text>'
        b += f'<text class="sans" x="112" y="{y+15}" font-size="16.5" font-weight="{600 if kind=="exp" else 500}" fill="{INK}">{esc(q)}</text>'
        p, _ = pill(112, y + 26, state, scol)
        b += p
        extra = 0
        if note:
            for j, line in enumerate(wrap(note, 730, 13)):
                b += f'<text class="sans" x="112" y="{y+66+j*18}" font-size="13" fill="{GR}">{esc(line)}</text>'
                extra = 18 * (j + 1) + 6
        body += b + "</g>"
        y += 64 + extra
        if i == 0:
            body += f'<line x1="28" y1="{y-8}" x2="852" y2="{y-8}" stroke="{LINE}"/>'
            y += 6
    y += 8
    body += mark(28, y - 10, "exp", VIOLET, 12)
    body += f'<text class="m" x="48" y="{y}" font-size="11" font-weight="700" letter-spacing="2" fill="{VIOLET}">ON THE BENCH</text>'
    body += f'<text class="m" x="852" y="{y}" font-size="10.5" fill="{FA}" text-anchor="end">prototypes, built to learn</text>'
    y += 16
    cw = (824 - 2 * 14) / 3
    for i, (name, what, stack) in enumerate(BENCH):
        x = 28 + i * (cw + 14)
        b = f'<rect x="{x:.0f}" y="{y}" width="{cw:.0f}" height="132" rx="10" fill="{PANEL}" stroke="{VIOLET}" stroke-opacity=".35" stroke-dasharray="5 4"/>'
        b += f'<text class="sans" x="{x+16:.0f}" y="{y+30}" font-size="15" font-weight="600" fill="{INK}">{esc(name)}</text>'
        for j, line in enumerate(wrap(what, cw - 32, 12.5)):
            b += f'<text class="sans" x="{x+16:.0f}" y="{y+54+j*17}" font-size="12.5" fill="{GR}">{esc(line)}</text>'
        b += f'<text class="m" x="{x+16:.0f}" y="{y+118}" font-size="10.5" fill="#C4B2FF">{esc(stack)}</text>'
        body += b
    h = y + 132 + 28
    desc = ("Open questions. " + " ".join(f"{qid}: {q} ({state.lower()})." for _, qid, q, _, (state, _) in QUESTIONS)
            + " On the bench: " + " ".join(f"{n}: {w} {s}." for n, w, s in BENCH))
    panel("lab.svg", 880, h, "06 · Lab — questions and prototypes", desc, "06", "LAB",
          "research notebook", VIOLET, (VIOLET, BLUE), body,
          glows=[(120, 120, 340, 220, VIOLET, .16), (780, h - 60, 300, 160, BLUE, .08)])


# ---------------------------------------------------------------- 07 VECTOR
NOW = [
    ("BUILDING", CYAN, "Task4Task, CivicPulse · through DevDevise"),
    ("RESEARCHING", VIOLET, "Agrimonitor: field conditions from orbit"),
    ("LEARNING", BLUE, "Remote sensing: moisture, stress, change"),
    ("ASKING", VIOLET, "When should a retrieval system say “I don’t know”?"),
    ("DIRECTION", CYAN, "From client systems to systems of our own"),
]


def vector():
    stages = ["engineer", "architect", "researcher", "builder", "founder"]
    xs = [70, 250, 430, 610, 790]
    ys = [216, 194, 166, 134, 102]
    d = f"M{xs[0]} {ys[0]}" + "".join(
        f" C{xs[i-1]+70} {ys[i-1]} {xs[i]-70} {ys[i]} {xs[i]} {ys[i]}" for i in range(1, 5))
    body = f'''<defs><linearGradient id="vg" x1="70" y1="0" x2="790" y2="0" gradientUnits="userSpaceOnUse">
    <stop offset="0" stop-color="{BLUE}"/><stop offset=".55" stop-color="{VIOLET}"/><stop offset="1" stop-color="{CYAN}"/></linearGradient>
    <filter id="vb" x="-5%" y="-50%" width="110%" height="200%"><feGaussianBlur stdDeviation="5"/></filter></defs>
  <path d="{d}" fill="none" stroke="url(#vg)" stroke-width="8" opacity=".3" filter="url(#vb)"/>
  <path id="traj" d="{d}" fill="none" stroke="url(#vg)" stroke-width="2.2"/>
  <path d="M790 102 C840 86 850 80 860 76" fill="none" stroke="{CYAN}" stroke-width="2" stroke-dasharray="3 5" opacity=".6"/>
  <circle r="4" fill="#FFFFFF"><animateMotion dur="4s" repeatCount="indefinite"><mpath href="#traj"/></animateMotion></circle>'''
    for i, (s, x, y) in enumerate(zip(stages, xs, ys)):
        last = i == 4
        col = AMBER if last else ["#7FA6FF", "#8C95FF", VIOLET, "#6FB8FF", CYAN][i]
        body += f'<circle cx="{x}" cy="{y}" r="{8 if last else 6}" fill="{VOID}" stroke="{col}" stroke-width="2"/>'
        body += f'<circle cx="{x}" cy="{y}" r="3" fill="{col}"/>'
        body += (f'<text class="sans" x="{x}" y="{y+30}" font-size="{17 if last else 15}" font-weight="{700 if last else 500}" '
                 f'fill="{INK if last else GR}" text-anchor="middle">{s}</text>')
        body += f'<text class="m" x="{x}" y="{y+48}" font-size="10" letter-spacing="1.5" fill="{FA}" text-anchor="middle">0{i+1}</text>'
    body += (f'<circle cx="790" cy="102" r="8" fill="none" stroke="{AMBER}" stroke-width="1.5">'
             f'<animate attributeName="r" values="8;22" dur="2s" repeatCount="indefinite"/>'
             f'<animate attributeName="opacity" values=".9;0" dur="2s" repeatCount="indefinite"/></circle>'
             f'<rect x="740" y="60" width="100" height="22" rx="11" fill="{AMBER}" fill-opacity=".12" stroke="{AMBER}" stroke-opacity=".7"/>'
             f'<text class="m" x="790" y="75" font-size="10.5" font-weight="700" letter-spacing="2" fill="{AMBER}" text-anchor="middle">YOU ARE HERE</text>')
    body += f'<line x1="28" y1="284" x2="852" y2="276" stroke="{LINE}" stroke-width="1.5"/>'
    body += f'<text class="m" x="28" y="314" font-size="11" font-weight="700" letter-spacing="2" fill="{INK}">NOW</text>'
    y = 344
    for i, (lab, col, val) in enumerate(NOW):
        body += (f'<g class="in" style="animation-delay:{.1*i:.1f}s"><rect x="28" y="{y-14}" width="3" height="18" fill="{col}"/>'
                 f'<text class="m" x="44" y="{y}" font-size="11" font-weight="700" letter-spacing="2" fill="{col}">{lab}</text>'
                 f'<text class="sans" x="190" y="{y}" font-size="16" fill="{INK}">{esc(val)}</text></g>')
        y += 34
    h = y + 6
    panel("vector.svg", 880, h, "07 · Vector — where this is heading",
          "A trajectory: engineer, architect, researcher, builder, founder. You are here: founder. Now: "
          + "; ".join(f"{l.lower()}: {v}" for l, _, v in NOW) + ".",
          "07", "VECTOR", "where this is heading", AMBER, (BLUE, VIOLET, CYAN, AMBER), body,
          glows=[(790, 90, 300, 160, AMBER, .08), (200, 380, 340, 200, VIOLET, .1)])


# ---------------------------------------------------------------- 08 RECORD
# (role, org, impact, start month, end month or None for now, colour); month 0 = Jan 2019
RECORD = [
    ("Founder & CEO", "DevDevise · SysMalla", "R&D-driven software engineering", None, None, CYAN),
    ("Software Developer", "5D Solutions LLC", "3+ ERP modules · +20% process automation", 49, None, CYAN),
    ("Web Developer", "Comtanix", "90% posting automated · +60% productivity", 52, 73, BLUE),
    ("PHP Developer Intern", "Pixako Technologies", "Scrum sprints · deployment scripts", 41, 44, GR),
    ("Software Engineer Intern", "KFUEIT Data Center", "LMS finance modules · +20% accuracy", 37, 40, GR),
    ("BS Software Engineering", "KFUEIT", "◆ gold medal · highest in batch", 0, 48, AMBER),
]
NOW_M = 93  # October 2026


def record():
    x0, x1 = 360, 846
    px = (x1 - x0) / NOW_M
    body = ""
    for yr in range(2019, 2027):
        x = x0 + (yr - 2019) * 12 * px
        body += f'<line x1="{x:.0f}" y1="62" x2="{x:.0f}" y2="400" stroke="#94AAFF" stroke-opacity=".06"/>'
        if x + 34 < x1 - 30:
            body += f'<text class="m" x="{x+3:.0f}" y="72" font-size="10" fill="{FA}">{yr}</text>'
    body += f'<line x1="{x1}" y1="62" x2="{x1}" y2="400" stroke="{CYAN}" stroke-opacity=".35" stroke-dasharray="3 3"/>'
    body += f'<text class="m" x="{x1-4}" y="72" font-size="10" fill="{CYAN}" text-anchor="end">NOW</text>'
    y = 96
    for i, (role, org, impact, a, b, col) in enumerate(RECORD):
        g = f'<g class="in" style="animation-delay:{.1*i:.1f}s">'
        g += f'<text class="sans" x="28" y="{y+12}" font-size="15" font-weight="600" fill="{INK}">{esc(role)}</text>'
        g += f'<text class="m" x="28" y="{y+30}" font-size="11" fill="{col if col != GR else GR}">{esc(org)}</text>'
        g += f'<text class="sans" x="28" y="{y+46}" font-size="12" fill="{FA}">{esc(impact)}</text>'
        if a is None:
            g += (f'<circle cx="{x1}" cy="{y+22}" r="7" fill="{CYAN}"/>'
                  f'<circle cx="{x1}" cy="{y+22}" r="7" fill="none" stroke="{CYAN}"><animate attributeName="r" values="7;18" dur="2s" repeatCount="indefinite"/>'
                  f'<animate attributeName="opacity" values=".8;0" dur="2s" repeatCount="indefinite"/></circle>'
                  f'<text class="m" x="{x1-16}" y="{y+26}" font-size="10.5" fill="{CYAN}" text-anchor="end">current</text>')
        else:
            bx, bw = x0 + a * px, ((b if b is not None else NOW_M) - a) * px
            g += f'<rect x="{bx:.1f}" y="{y+14}" width="{max(bw, 8):.1f}" height="16" rx="8" fill="{col}" fill-opacity=".22" stroke="{col}" stroke-opacity=".8"/>'
            if b is None:
                g += f'<circle cx="{x1-8}" cy="{y+22}" r="3" fill="{col}"><animate attributeName="opacity" values="1;.2;1" dur="1.6s" repeatCount="indefinite"/></circle>'
        body += g + "</g>"
        y += 56
    body += f'<line x1="28" y1="{y+4}" x2="852" y2="{y+4}" stroke="{LINE}" stroke-width="1.5"/>'
    body += (f'<text class="m" x="28" y="{y+30}" font-size="10.5" letter-spacing="1.5" fill="{FA}">CERTIFICATES</text>'
             f'<text class="sans" x="140" y="{y+30}" font-size="13" fill="{GR}">AWS Practitioner (Coursera) · Certified in Cyber Security (NAVTTC)</text>')
    h = y + 52
    desc = "Career record. " + " ".join(f"{r}, {o}: {imp}." for r, o, imp, *_ in RECORD) + \
        " Certificates: AWS Practitioner (Coursera); Certified in Cyber Security (NAVTTC)."
    panel("record.svg", 880, h, "08 · Record — compact, on purpose", desc, "08", "RECORD",
          "compact, on purpose", BLUE, (BLUE, CYAN, AMBER), body,
          glows=[(700, 120, 320, 180, CYAN, .08), (120, h - 60, 300, 160, AMBER, .06)])


# ---------------------------------------------------------------- 09 CHANNEL
def channel():
    body = f'''<text class="m" x="28" y="82" font-size="15" fill="{BLUE}">$ <tspan fill="{INK}">open channel --to adnan.yar</tspan></text>
  <text class="m in" x="28" y="110" font-size="15" fill="{CYAN}" style="animation-delay:.6s">  connected<tspan fill="{FA}"> · reply latency: </tspan><tspan fill="{INK}">human</tspan><tspan class="blink" fill="{CYAN}"> ▍</tspan></text>
  <text class="sans" x="28" y="150" font-size="16" fill="{GR}">Open to conversations about <tspan fill="{VIOLET}">intelligent systems</tspan>, <tspan fill="#C4B2FF">AI and LLM engineering</tspan>,</text>
  <text class="sans" x="28" y="174" font-size="16" fill="{GR}"><tspan fill="{CYAN}">automation</tspan>, <tspan fill="{BLUE}">SaaS architecture</tspan> and <tspan fill="{INK}">product R&amp;D</tspan>. Pick a line below.</text>'''
    panel("channel.svg", 880, 200, "09 · Channel — open",
          "Open channel to Adnan Yar: connected, reply latency human. Open to conversations about intelligent systems, AI and LLM "
          "engineering, automation, SaaS architecture and product R&D.",
          "09", "CHANNEL", "the last terminal", BLUE, (BLUE, CYAN), body,
          glows=[(160, 100, 320, 140, BLUE, .14)])


# ---------------------------------------------------------------- buttons (wrapped in links in the README)
D_MARK = "M0 0 H13 L20 7 V19 L13 26 H0 Z M5.5 5.5 H10.72 L14.5 9.28 V16.72 L10.72 20.5 H5.5 Z"


def button(name, kicker, value, col, icon, w=420, h=64):
    icons = {
        "mail": f'<rect x="22" y="22" width="26" height="20" rx="3" fill="none" stroke="{col}" stroke-width="1.6"/><path d="M23 24l12 9 12-9" fill="none" stroke="{col}" stroke-width="1.6"/>',
        "in": f'<rect x="21" y="18" width="28" height="28" rx="5" fill="{col}" fill-opacity=".15" stroke="{col}" stroke-width="1.6"/><text class="sans" x="35" y="38" font-size="15" font-weight="700" fill="{col}" text-anchor="middle">in</text>',
        "web": f'<circle cx="35" cy="32" r="13" fill="none" stroke="{col}" stroke-width="1.6"/><ellipse cx="35" cy="32" rx="5.5" ry="13" fill="none" stroke="{col}" stroke-width="1.3"/><path d="M22 32H48" stroke="{col}" stroke-width="1.3"/>',
        "dd": f'<path d="M0 0 H13 L20 7 V19 L13 26 H0 Z" fill="none" stroke="{VIOLET}" stroke-width="1.3" stroke-dasharray="2.4 1.8" transform="translate(21 17) rotate(-8 10 13)"/><path fill-rule="evenodd" fill="{CYAN}" transform="translate(26 19)" d="{D_MARK}"/>',
        "route": f'<circle cx="35" cy="32" r="13" fill="{col}" fill-opacity=".12" stroke="{col}" stroke-width="1.6"/><path d="M30 26l7 6-7 6" fill="none" stroke="{col}" stroke-width="2"/>',
    }
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" aria-label="{esc(kicker)}: {esc(value)}">
  <style>.sans{{font-family:{SANS}}}.m{{font-family:{MONO}}}</style>
  <defs><linearGradient id="b" x1="0" y1="0" x2="{w}" y2="0" gradientUnits="userSpaceOnUse"><stop offset="0" stop-color="{col}" stop-opacity=".18"/><stop offset="1" stop-color="{col}" stop-opacity=".02"/></linearGradient></defs>
  <rect x="1" y="1" width="{w-2}" height="{h-2}" rx="12" fill="{VOID}" stroke="{col}" stroke-opacity=".55" stroke-width="1.5"/>
  <rect x="1" y="1" width="{w-2}" height="{h-2}" rx="12" fill="url(#b)"/>
  {icons[icon]}
  <text class="m" x="64" y="27" font-size="10.5" letter-spacing="2" font-weight="700" fill="{col}">{esc(kicker)}</text>
  <text class="sans" x="64" y="48" font-size="16" font-weight="600" fill="{INK}">{esc(value)}</text>
  <path d="M{w-34} 26l7 6-7 6" fill="none" stroke="{col}" stroke-width="2"/>
</svg>
'''
    (OUT / name).write_text(svg, encoding="utf-8")
    xml.dom.minidom.parseString(svg.encode("utf-8"))
    print("wrote", name)


if __name__ == "__main__":
    signal()
    systems_head()
    shipped()
    architecture()
    lab()
    vector()
    record()
    channel()
    button("btn-mail.svg", "MAIL", "adnanyar143@gmail.com", BLUE, "mail")
    button("btn-linkedin.svg", "LINKEDIN", "in/adnanyar", BLUE, "in")
    button("btn-web.svg", "WEB", "adnanyar.com", CYAN, "web")
    button("btn-devdevise.svg", "COMPANY", "devdevise.com", VIOLET, "dd")
    button("route-engineer.svg", "ENTER AS AN ENGINEER", "architecture → lab", BLUE, "route", w=280)
    button("route-founder.svg", "ENTER AS A FOUNDER", "systems → vector", VIOLET, "route", w=280)
    button("route-hiring.svg", "ENTER AS HIRING", "shipped → record", CYAN, "route", w=280)
