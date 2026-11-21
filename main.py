#!/usr/bin/env python3
"""News-image entry for make.fun competition news-image-20261121.

Sums up Saturday 21 November 2026's world news in one 1024x1024
image, drawn from scratch with the Python standard library only
(zlib PNG encoder + a built-in 5x7 bitmap font). No network, no
files read, no randomness: two runs write byte-identical output.

The news was gathered on 21 Nov 2026 from that day's reporting and
cross-checked across at least two sources:

  * The International Court of Justice ruled 9-6 that Myanmar
    committed genocide against the Rohingya - the first time the
    court has held a state responsible for genocide; 1.3m+ Rohingya
    remain displaced.
  * Russian missiles hit a bridge in Kyiv, killing at least nine;
    two died and 42 were hurt in Kryvyi Rih; a missile blast was
    reported in Warsaw; Ukraine struck the Crimea Bridge.
  * Trump pressed on with his China trip as the US proposed NATO
    membership for Ukraine in exchange for territorial concessions.
  * Saudi defences stopped a Houthi missile and drone; debris fell
    on Riyadh.
  * The US approved about 900,000 AI chips for China in six months;
    tech stocks plunged.
  * Also in the footer: the EU approved 1bn euros of military aid
    for Ukraine; Denmark expelled Russia's defence attache; youth
    protests swept Europe over living costs; Mongolia's president
    resigned; Argentina backed a disability law 71-0; Pete Rose was
    pardoned; Nikhil Gupta got 19 years in the US; the US Senate
    rejected the Iran war-powers bid 51-48; Ukraine hit the Crimea
    Bridge.

Layout: a newspaper front page with a clear hierarchy. Masthead
names the day; a full-width lead (the ICJ ruling, biggest headline)
with a scales-of-justice drawing; a second full-width story (the
Russian missile assault) with a skyline-under-attack drawing; a row
of three mid stories with pictograms (summit, Riyadh, markets); and
an "ALSO" footer carrying the rest of the day.
"""

import hashlib
import os
import struct
import zlib

W, H = 1024, 1024

PAPER = (247, 243, 232)
INK = (26, 26, 26)
NAVY = (22, 40, 63)
RED = (176, 42, 32)
GOLD = (201, 162, 39)
BLUE = (47, 93, 140)
GREEN = (46, 125, 74)
ORANGE = (214, 106, 32)
GREY = (120, 116, 104)
LIGHT = (255, 255, 255)

# ---------------------------------------------------------------- font
# 5x7 bitmap font. Each glyph is 7 rows of 5 characters: '#' = ink.
FONT = {
    'A': (".###.", "#...#", "#...#", "#####", "#...#", "#...#", "#...#"),
    'B': ("####.", "#...#", "#...#", "####.", "#...#", "#...#", "####."),
    'C': (".###.", "#...#", "#....", "#....", "#....", "#...#", ".###."),
    'D': ("####.", "#...#", "#...#", "#...#", "#...#", "#...#", "####."),
    'E': ("#####", "#....", "#....", "####.", "#....", "#....", "#####"),
    'F': ("#####", "#....", "#....", "####.", "#....", "#....", "#...."),
    'G': (".###.", "#...#", "#....", "#.###", "#...#", "#...#", ".####"),
    'H': ("#...#", "#...#", "#...#", "#####", "#...#", "#...#", "#...#"),
    'I': (".###.", "..#..", "..#..", "..#..", "..#..", "..#..", ".###."),
    'J': ("..###", "...#.", "...#.", "...#.", "...#.", "#..#.", ".##.."),
    'K': ("#...#", "#..#.", "#.#..", "##...", "#.#..", "#..#.", "#...#"),
    'L': ("#....", "#....", "#....", "#....", "#....", "#....", "#####"),
    'M': ("#...#", "##.##", "#.#.#", "#.#.#", "#...#", "#...#", "#...#"),
    'N': ("#...#", "##..#", "#.#.#", "#..##", "#...#", "#...#", "#...#"),
    'O': (".###.", "#...#", "#...#", "#...#", "#...#", "#...#", ".###."),
    'P': ("####.", "#...#", "#...#", "####.", "#....", "#....", "#...."),
    'Q': (".###.", "#...#", "#...#", "#...#", "#.#.#", "#..#.", ".##.#"),
    'R': ("####.", "#...#", "#...#", "####.", "#.#..", "#..#.", "#...#"),
    'S': (".####", "#....", "#....", ".###.", "....#", "....#", "####."),
    'T': ("#####", "..#..", "..#..", "..#..", "..#..", "..#..", "..#.."),
    'U': ("#...#", "#...#", "#...#", "#...#", "#...#", "#...#", ".###."),
    'V': ("#...#", "#...#", "#...#", "#...#", "#...#", ".#.#.", "..#.."),
    'W': ("#...#", "#...#", "#...#", "#.#.#", "#.#.#", "##.##", "#...#"),
    'X': ("#...#", "#...#", ".#.#.", "..#..", ".#.#.", "#...#", "#...#"),
    'Y': ("#...#", "#...#", ".#.#.", "..#..", "..#..", "..#..", "..#.."),
    'Z': ("#####", "....#", "...#.", "..#..", ".#...", "#....", "#####"),
    'a': (".....", ".....", ".###.", "....#", ".####", "#...#", ".####"),
    'b': ("#....", "#....", "####.", "#...#", "#...#", "#...#", "####."),
    'c': (".....", ".....", ".###.", "#....", "#....", "#...#", ".###."),
    'd': ("....#", "....#", ".####", "#...#", "#...#", "#...#", ".####"),
    'e': (".....", ".....", ".###.", "#...#", "#####", "#....", ".###."),
    'f': ("..##.", ".#..#", ".#...", "####.", ".#...", ".#...", ".#..."),
    'g': (".....", ".####", "#...#", "#...#", ".####", "....#", ".###."),
    'h': ("#....", "#....", "####.", "#...#", "#...#", "#...#", "#...#"),
    'i': ("..#..", ".....", ".##..", "..#..", "..#..", "..#..", ".###."),
    'j': ("...#.", ".....", "..##.", "...#.", "...#.", "#..#.", ".##.."),
    'k': ("#....", "#....", "#..#.", "#.#..", "##...", "#.#..", "#..#."),
    'l': (".##..", "..#..", "..#..", "..#..", "..#..", "..#..", ".###."),
    'm': (".....", ".....", "##.#.", "#.#.#", "#.#.#", "#.#.#", "#.#.#"),
    'n': (".....", ".....", "####.", "#...#", "#...#", "#...#", "#...#"),
    'o': (".....", ".....", ".###.", "#...#", "#...#", "#...#", ".###."),
    'p': (".....", ".....", "####.", "#...#", "####.", "#....", "#...."),
    'q': (".....", ".....", ".####", "#...#", ".####", "....#", "....#"),
    'r': (".....", ".....", "#.##.", "##..#", "#....", "#....", "#...."),
    's': (".....", ".....", ".####", "#....", ".###.", "....#", "####."),
    't': (".#...", ".#...", "###..", ".#...", ".#...", ".#.#.", "..#.."),
    'u': (".....", ".....", "#...#", "#...#", "#...#", "#..##", ".##.#"),
    'v': (".....", ".....", "#...#", "#...#", "#...#", ".#.#.", "..#.."),
    'w': (".....", ".....", "#...#", "#.#.#", "#.#.#", "#.#.#", ".#.#."),
    'x': (".....", ".....", "#...#", ".#.#.", "..#..", ".#.#.", "#...#"),
    'y': (".....", ".....", "#...#", "#...#", ".####", "....#", ".###."),
    'z': (".....", ".....", "#####", "...#.", "..#..", ".#...", "#####"),
    '0': (".###.", "#...#", "#..##", "#.#.#", "##..#", "#...#", ".###."),
    '1': ("..#..", ".##..", "..#..", "..#..", "..#..", "..#..", ".###."),
    '2': (".###.", "#...#", "....#", "..##.", ".#...", "#....", "#####"),
    '3': ("#####", "...#.", "..#..", "...#.", "....#", "#...#", ".###."),
    '4': ("...#.", "..##.", ".#.#.", "#..#.", "#####", "...#.", "...#."),
    '5': ("#####", "#....", "####.", "....#", "....#", "#...#", ".###."),
    '6': ("..##.", ".#...", "#....", "####.", "#...#", "#...#", ".###."),
    '7': ("#####", "....#", "...#.", "..#..", ".#...", ".#...", ".#..."),
    '8': (".###.", "#...#", "#...#", ".###.", "#...#", "#...#", ".###."),
    '9': (".###.", "#...#", "#...#", ".####", "....#", "...#.", ".##.."),
    ' ': (".....", ".....", ".....", ".....", ".....", ".....", "....."),
    '.': (".....", ".....", ".....", ".....", ".....", ".##..", ".##.."),
    ',': (".....", ".....", ".....", ".....", ".##..", "..#..", ".#..."),
    ':': (".....", ".##..", ".##..", ".....", ".##..", ".##..", "....."),
    ';': (".....", ".##..", ".##..", ".....", ".##..", "..#..", ".#..."),
    '!': ("..#..", "..#..", "..#..", "..#..", "..#..", ".....", "..#.."),
    '?': (".###.", "#...#", "....#", "..##.", "..#..", ".....", "..#.."),
    '-': (".....", ".....", ".....", "#####", ".....", ".....", "....."),
    "'": ("..#..", "..#..", ".#...", ".....", ".....", ".....", "....."),
    '(': ("...#.", "..#..", ".#...", ".#...", ".#...", "..#..", "...#."),
    ')': (".#...", "..#..", "...#.", "...#.", "...#.", "..#..", ".#..."),
    '%': ("##..#", "##.#.", "...#.", "..#..", ".#...", "#.##.", "#..##"),
    '$': ("..#..", ".####", "#.#..", ".###.", "..#.#", "####.", "..#.."),
    '/': ("....#", "...#.", "...#.", "..#..", ".#...", ".#...", "#...."),
    '+': (".....", "..#..", "..#..", "#####", "..#..", "..#..", "....."),
    '=': (".....", ".....", "#####", ".....", "#####", ".....", "....."),
    '"': (".#.#.", ".#.#.", ".....", ".....", ".....", ".....", "....."),
    '&': (".##..", "#..#.", "#.#..", ".#...", "#.#.#", "#..#.", ".##.#"),
    '*': (".....", ".#.#.", "..#..", "#####", "..#..", ".#.#.", "....."),
    '_': (".....", ".....", ".....", ".....", ".....", ".....", "#####"),
    '\u2022': (".....", ".....", ".##..", ".##..", ".....", ".....", "....."),
}

BULLET = '\u2022'


def _clean(text):
    """Normalise to the glyphs the font holds."""
    return (text.replace('\u2019', "'").replace('\u2018', "'")
                .replace('\u2014', '-').replace('\u2013', '-')
                .replace('\u20ac', 'E'))


def text_width(text, scale):
    return len(_clean(text)) * 6 * scale - scale


def wrap(text, max_chars):
    """Greedy word wrap to lines of at most max_chars characters."""
    lines, cur = [], ""
    for word in _clean(text).split(" "):
        if cur and len(cur) + 1 + len(word) > max_chars:
            lines.append(cur)
            cur = word
        else:
            cur = (cur + " " + word) if cur else word
    if cur:
        lines.append(cur)
    return lines


class Canvas:
    """An RGB raster with tiny vector helpers."""

    def __init__(self, w, h, bg):
        self.w, self.h = w, h
        self.px = bytearray(bg * (w * h))

    def set(self, x, y, color):
        if 0 <= x < self.w and 0 <= y < self.h:
            i = (y * self.w + x) * 3
            self.px[i:i + 3] = bytes(color)

    def fill_rect(self, x, y, w, h, color):
        x0, y0 = max(0, x), max(0, y)
        x1, y1 = min(self.w, x + w), min(self.h, y + h)
        row = bytes(color) * (x1 - x0)
        for yy in range(y0, y1):
            i = (yy * self.w + x0) * 3
            self.px[i:i + len(row)] = row

    def rect(self, x, y, w, h, color, t=2):
        self.fill_rect(x, y, w, t, color)
        self.fill_rect(x, y + h - t, w, t, color)
        self.fill_rect(x, y, t, h, color)
        self.fill_rect(x + w - t, y, t, h, color)

    def hline(self, x, y, length, color, t=1):
        self.fill_rect(x, y, length, t, color)

    def vline(self, x, y, length, color, t=1):
        self.fill_rect(x, y, t, length, color)

    def line(self, x0, y0, x1, y1, color, t=1):
        """Bresenham line, t = thickness in pixels."""
        dx, dy = abs(x1 - x0), abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = dx - dy
        while True:
            for a in range(t):
                for b in range(t):
                    self.set(x0 + a - t // 2, y0 + b - t // 2, color)
            if x0 == x1 and y0 == y1:
                return
            e2 = 2 * err
            if e2 > -dy:
                err -= dy
                x0 += sx
            if e2 < dx:
                err += dx
                y0 += sy

    def circle(self, cx, cy, r, color):
        for dy in range(-r, r + 1):
            dx = int((r * r - dy * dy) ** 0.5)
            self.fill_rect(cx - dx, cy + dy, 2 * dx + 1, 1, color)

    def ring(self, cx, cy, r, color, t=3):
        for a in range(360):
            import math
            x = int(cx + r * math.cos(math.radians(a)))
            y = int(cy + r * math.sin(math.radians(a)))
            self.fill_rect(x, y, t, t, color)

    def triangle(self, x0, y0, x1, y1, x2, y2, color):
        """Filled triangle via scanlines."""
        pts = sorted([(x0, y0), (x1, y1), (x2, y2)], key=lambda p: p[1])
        (ax, ay), (bx, by), (cx, cy) = pts
        for y in range(ay, cy + 1):
            if y < by:
                xa = ax + (bx - ax) * (y - ay) / max(1, by - ay)
                xb = ax + (cx - ax) * (y - ay) / max(1, cy - ay)
            else:
                xa = bx + (cx - bx) * (y - by) / max(1, cy - by)
                xb = ax + (cx - ax) * (y - ay) / max(1, cy - ay)
            self.fill_rect(int(min(xa, xb)), y, int(abs(xb - xa)) + 1, 1, color)

    def text(self, x, y, s, scale, color):
        s = _clean(s)
        cx = x
        for ch in s:
            glyph = FONT.get(ch, FONT['?'])
            for row, bits in enumerate(glyph):
                for col, bit in enumerate(bits):
                    if bit == '#':
                        self.fill_rect(cx + col * scale, y + row * scale,
                                       scale, scale, color)
            cx += 6 * scale
        return cx - x - scale

    def text_centred(self, cx, y, s, scale, color):
        w = text_width(s, scale)
        return self.text(cx - w // 2, y, s, scale, color)

    def paragraph(self, x, y, s, scale, color, max_chars, leading=None):
        if leading is None:
            leading = 9 * scale
        yy = y
        for line in wrap(s, max_chars):
            self.text(x, yy, line, scale, color)
            yy += leading
        return yy


def _chunk(tag, data):
    crc = zlib.crc32(tag)
    crc = zlib.crc32(data, crc)
    return struct.pack(">I", len(data)) + tag + data + struct.pack(">I", crc & 0xffffffff)


def to_png(c):
    raw = bytearray()
    for y in range(c.h):
        raw.append(0)
        raw.extend(c.px[y * c.w * 3:(y + 1) * c.w * 3])
    ihdr = struct.pack(">IIBBBBB", c.w, c.h, 8, 2, 0, 0, 0)
    return (b"\x89PNG\r\n\x1a\n" + _chunk(b"IHDR", ihdr)
            + _chunk(b"IDAT", zlib.compress(bytes(raw), 9))
            + _chunk(b"IEND", b""))


# ------------------------------------------------------------- pictograms
def pic_justice(c, x, y, w, h):
    """Scales of justice, centred in the box (x, y, w, h)."""
    cx = x + w // 2
    top, bot = y + 8, y + h - 18
    c.vline(cx, top + 14, bot - top - 14, NAVY, 5)
    c.fill_rect(cx - 7, top, 14, 14, GOLD)          # finial
    c.hline(cx - w // 2 + 18, top + 20, w - 36, NAVY, 5)
    for px in (cx - w // 2 + 18, cx + w // 2 - 18):
        c.line(px, top + 20, px, top + 78, NAVY, 3)
        c.triangle(px - 34, top + 78, px + 34, top + 78, px, top + 118, GOLD)
        c.hline(px - 34, top + 78, 69, NAVY, 3)
    c.fill_rect(cx - 52, bot - 6, 104, 8, NAVY)
    c.fill_rect(cx - 34, bot - 18, 68, 12, NAVY)


def pic_summit(c, x, y, w, h):
    """Three leaders at a table, each under a small flag."""
    base = y + h - 8
    flags = [
        (NAVY, [(0, 0, 14, 2, RED), (0, 3, 14, 2, LIGHT), (0, 6, 14, 2, RED),
                (0, 0, 6, 6, NAVY)]),                     # USA stripes + canton
        (RED, [(0, 0, 14, 10, RED), (2, 2, 3, 3, GOLD)]),  # China
        (LIGHT, [(0, 0, 14, 3, LIGHT), (0, 3, 14, 3, BLUE),
                 (0, 7, 14, 3, RED)]),                     # Russia
    ]
    for i, (pole_c, parts) in enumerate(flags):
        fx = x + 22 + i * (w - 44) // 2
        c.vline(fx, y + 2, 24, INK, 2)
        for (rx, ry, rw, rh, col) in parts:
            c.fill_rect(fx + 2 + rx, y + 2 + ry, rw, rh, col)
        hx = fx + 9
        c.circle(hx, base - 16, 10, (196, 164, 132) if i != 1 else (232, 196, 164))
        c.fill_rect(hx - 16, base - 8, 32, 10, (NAVY, RED, (52, 52, 52))[i])
    c.fill_rect(x + 8, base, w - 16, 5, INK)


def pic_bridge(c, x, y, w, h):
    """A bridge under an explosion starburst."""
    base = y + h - 14
    cx = x + w // 2
    for k in range(8):
        import math
        a = math.radians(k * 45 + 10)
        c.line(cx, y + 24, int(cx + 20 * math.cos(a)),
               int(y + 24 + 20 * math.sin(a)), ORANGE, 3)
    c.circle(cx, y + 24, 9, RED)
    c.circle(cx, y + 24, 4, GOLD)
    c.fill_rect(x + 10, base - 5, w - 20, 5, NAVY)
    for px in (x + 34, x + w // 2 - 4, x + w - 42):
        c.fill_rect(px, base - 22, 8, 17, NAVY)
    c.line(x + 10, base - 22, x + w - 10, base - 22, NAVY, 2)
    c.line(x + 10, base - 5, cx, base - 30, NAVY, 2)
    c.line(x + w - 10, base - 5, cx, base - 30, NAVY, 2)


def pic_tower(c, x, y, w, h):
    """Skyscraper hit by a missile: impact burst at its top corner."""
    tx, tw = x + w // 2 - 30, 60
    top, bot = y + 20, y + h - 8
    c.fill_rect(tx, top, tw, bot - top, NAVY)
    for row in range(3):
        for col in range(3):
            c.fill_rect(tx + 8 + col * 18, top + 8 + row * 13, 9, 7, GOLD)
    c.fill_rect(tx - 4, top - 6, tw + 8, 6, INK)
    mx, my = x + w - 10, y + 4
    c.line(mx, my, tx + tw - 6, top + 4, RED, 4)
    c.triangle(tx + tw - 6, top + 4, tx + tw + 6, top - 4, tx + tw + 12, top + 10, RED)
    for k in range(6):
        import math
        a = math.radians(k * 60)
        c.line(tx + tw, top, int(tx + tw + 15 * math.cos(a)),
               int(top + 15 * math.sin(a)), ORANGE, 3)
    c.circle(tx + tw, top, 7, GOLD)
    c.fill_rect(x + 14, bot, w - 28, 4, INK)


def pic_chart(c, x, y, w, h):
    """A market line that climbs, then falls hard."""
    ox, oy = x + 12, y + h - 10
    c.vline(ox, y + 8, oy - y - 8, INK, 3)
    c.hline(ox, oy, w - 24, INK, 3)
    pts = [(ox + 6, oy - 18), (ox + 50, oy - 36), (ox + 94, oy - 30),
           (ox + 138, oy - 48), (ox + 182, oy - 22), (ox + 226, oy - 12),
           (ox + 270, oy - 6)]
    for (ax, ay), (bx, by) in zip(pts, pts[1:]):
        c.line(ax, ay, bx, by, GREEN if by <= ay else RED, 5)
    ex, ey = pts[-1]
    c.line(ex, ey, ex - 16, ey - 4, RED, 5)
    c.line(ex, ey, ex - 4, ey - 16, RED, 5)


def pic_health(c, x, y, w, h):
    """A green shield of health: circle, cross, check mark."""
    cx, cy = x + w // 2, y + h // 2
    c.circle(cx, cy, 28, GREEN)
    c.ring(cx, cy, 28, (34, 94, 56), 3)
    c.fill_rect(cx - 15, cy - 5, 30, 10, LIGHT)
    c.fill_rect(cx - 5, cy - 15, 10, 30, LIGHT)


def pic_strike(c, x, y, w, h):
    """A city skyline under missile attack: buildings, a bridge,
    explosion starbursts and incoming missile streaks."""
    import math
    base = y + h - 8
    heights = [52, 78, 44, 96, 60, 88, 40, 70]
    bw = w // len(heights)
    for i, hh in enumerate(heights):
        bx = x + 4 + i * bw
        c.fill_rect(bx, base - hh, bw - 3, hh, NAVY)
    # bridge deck across the lower middle, in front of the skyline
    c.fill_rect(x + 8, base - 26, w - 16, 5, INK)
    for px in (x + 30, x + w // 2 - 4, x + w - 38):
        c.fill_rect(px, base - 44, 8, 18, INK)
    # explosion starbursts above the skyline
    for (ex, ey, r) in ((x + w // 2 - 30, y + 30, 16),
                        (x + w - 46, y + 58, 12)):
        for k in range(8):
            a = math.radians(k * 45 + 12)
            c.line(ex, ey, int(ex + r * math.cos(a)),
                   int(ey + r * math.sin(a)), ORANGE, 3)
        c.circle(ex, ey, 8, RED)
        c.circle(ex, ey, 4, GOLD)
    # incoming missile streaks from the top right
    c.line(x + w - 8, y + 2, x + w // 2 - 24, y + 26, RED, 3)
    c.line(x + w - 30, y + 2, x + w - 52, y + 52, RED, 3)


# ---------------------------------------------------------------- layout
def story_panel(c, x, y, w, h, kicker, headlines, body, pic):
    c.rect(x, y, w, h, INK, 2)
    if pic is not None:
        pic(c, x + 14, y + 8, w - 28, 70)
        ty = y + 84
    else:
        ty = y + 14
    c.text(x + 16, ty, kicker, 2, RED)
    hy = ty + 22
    for line in headlines:
        c.text(x + 16, hy, line, 3, NAVY)
        hy += 30
    c.paragraph(x + 16, hy + 4, body, 2, INK, (w - 32) // 12, leading=16)


def draw():
    c = Canvas(W, H, PAPER)
    # masthead
    c.fill_rect(24, 24, 976, 134, NAVY)
    c.fill_rect(24, 24, 976, 5, GOLD)
    c.fill_rect(24, 153, 976, 5, GOLD)
    c.text_centred(512, 42, "THE WORLD IN ONE DAY", 5, LIGHT)
    c.text_centred(512, 94, "SATURDAY 21 NOVEMBER 2026", 3, GOLD)
    c.text_centred(512, 128, "THE DAY'S WORLD NEWS IN ONE IMAGE", 2, LIGHT)

    # lead story (full width): the ICJ genocide ruling, biggest headline
    c.rect(24, 170, 976, 214, INK, 3)
    c.fill_rect(24, 170, 976, 214, PAPER)
    c.rect(24, 170, 976, 214, INK, 3)
    pic_justice(c, 664, 182, 296, 190)
    c.vline(640, 186, 186, GREY, 2)
    c.text(40, 188, "THE HAGUE " + BULLET + " JUSTICE", 2, RED)
    c.text(40, 214, "MYANMAR COMMITTED", 5, NAVY)
    c.text(40, 254, "GENOCIDE", 5, NAVY)
    c.paragraph(40, 306, "The International Court of Justice ruled 9-6 "
                 "that Myanmar committed genocide against the Rohingya - "
                 "the first time a state has been held responsible for "
                 "genocide. 1.3m remain displaced.", 2, INK, 48)

    # second story (full width): the Russian missile assault
    c.rect(24, 396, 976, 214, INK, 3)
    c.fill_rect(24, 396, 976, 214, PAPER)
    c.rect(24, 396, 976, 214, INK, 3)
    pic_strike(c, 40, 408, 250, 190)
    c.vline(306, 412, 182, GREY, 2)
    c.text(322, 414, "KYIV " + BULLET + " WAR", 2, RED)
    c.text(322, 442, "RUSSIA'S BIGGEST", 4, NAVY)
    c.text(322, 474, "MISSILE ASSAULT", 4, NAVY)
    c.text(322, 506, "HITS KYIV, POLAND", 4, NAVY)
    c.paragraph(322, 546, "Russian missiles hit a Kyiv bridge, killing "
                 "at least nine. Two died and 42 were hurt in Kryvyi "
                 "Rih. A missile blast was reported in Warsaw.", 2, INK,
                 52)

    # mid row: summit, Riyadh, markets
    story_panel(c, 24, 622, 312, 248, "CHINA " + BULLET + " SUMMIT",
                ["TRUMP IN CHINA,", "NATO FOR UKRAINE"],
                "Trump pressed on in China as the US offered NATO "
                "membership for Ukraine for land.",
                pic_summit)
    story_panel(c, 356, 622, 312, 248, "RIYADH " + BULLET + " GULF",
                ["SAUDI STOPS", "HOUTHI MISSILE"],
                "Saudi defences stopped a Houthi missile and drone. "
                "Debris fell on Riyadh.",
                pic_tower)
    story_panel(c, 688, 622, 312, 248, "WASHINGTON " + BULLET + " TECH",
                ["CHIPS TO CHINA,", "STOCKS PLUNGE"],
                "The US approved about 900,000 AI chips for China in "
                "six months. Tech stocks fell.",
                pic_chart)

    # footer: the rest of the day
    c.hline(24, 882, 976, INK, 2)
    c.text_centred(512, 896,
                   "ALSO: EU approves 1bn euros Ukraine aid  " + BULLET +
                   "  Denmark expels Russian attache", 2, INK)
    c.text_centred(512, 918,
                   "Youth protests sweep Europe over living costs  " +
                   BULLET + "  Mongolia president quits", 2, INK)
    c.text_centred(512, 940,
                   "Argentina backs disability law 71-0  " + BULLET +
                   "  Pete Rose pardoned  " + BULLET +
                   "  Gupta gets 19 years", 2, INK)
    c.text_centred(512, 962,
                   "Senate rejects Iran war-powers 51-48  " + BULLET +
                   "  Ukraine hits Crimea Bridge", 2, INK)
    return c


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    data = to_png(draw())
    path = os.path.join(out_dir, "entry.png")
    with open(path, "wb") as f:
        f.write(data)
    print("wrote %s (%d bytes, sha256 %s)"
          % (path, len(data), hashlib.sha256(data).hexdigest()))


if __name__ == "__main__":
    main()
