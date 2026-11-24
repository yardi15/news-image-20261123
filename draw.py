"""Drawing engine for the 23 Nov 2026 world-news front page.

Pure Python standard library only. Renders into an in-memory RGB
canvas, encodes a PNG by hand (zlib + struct), and ships a small
5x7 bitmap font drawn from scratch for this page.
"""

import binascii
import struct
import zlib

# ---------------------------------------------------------------- font

FONT = {
    "0": (" ### ", "#   #", "#  ##", "# # #", "##  #", "#   #", " ### "),
    "1": ("  #  ", " ##  ", "# #  ", "  #  ", "  #  ", "  #  ", "#####"),
    "2": (" ### ", "#   #", "    #", "   # ", "  #  ", " #   ", "#####"),
    "3": ("#### ", "    #", "    #", " ### ", "    #", "    #", "#### "),
    "4": ("   # ", "  ## ", " # # ", "#  # ", "#####", "   # ", "   # "),
    "5": ("#####", "#    ", "#### ", "    #", "    #", "#   #", " ### "),
    "6": (" ### ", "#   #", "#    ", "#### ", "#   #", "#   #", " ### "),
    "7": ("#####", "    #", "   # ", "   # ", "  #  ", "  #  ", "  #  "),
    "8": (" ### ", "#   #", "#   #", " ### ", "#   #", "#   #", " ### "),
    "9": (" ### ", "#   #", "#   #", " ####", "    #", "#   #", " ### "),
    "A": (" ### ", "#   #", "#   #", "#####", "#   #", "#   #", "#   #"),
    "B": ("#### ", "#   #", "#   #", "#### ", "#   #", "#   #", "#### "),
    "C": (" ### ", "#   #", "#    ", "#    ", "#    ", "#   #", " ### "),
    "D": ("###  ", "#  # ", "#   #", "#   #", "#   #", "#  # ", "###  "),
    "E": ("#####", "#    ", "#    ", "#### ", "#    ", "#    ", "#####"),
    "F": ("#####", "#    ", "#    ", "#### ", "#    ", "#    ", "#    "),
    "G": (" ### ", "#   #", "#    ", "#  ##", "#   #", "#   #", " ### "),
    "H": ("#   #", "#   #", "#   #", "#####", "#   #", "#   #", "#   #"),
    "I": (" ### ", "  #  ", "  #  ", "  #  ", "  #  ", "  #  ", " ### "),
    "J": ("  ###", "   # ", "   # ", "   # ", "   # ", "#  # ", " #   "),
    "K": ("#   #", "#  # ", "# #  ", "##   ", "# #  ", "#  # ", "#   #"),
    "L": ("#    ", "#    ", "#    ", "#    ", "#    ", "#    ", "#####"),
    "M": ("#   #", "## ##", "# # #", "# # #", "#   #", "#   #", "#   #"),
    "N": ("#   #", "##  #", "# # #", "#  ##", "#   #", "#   #", "#   #"),
    "O": (" ### ", "#   #", "#   #", "#   #", "#   #", "#   #", " ### "),
    "P": ("#### ", "#   #", "#   #", "#### ", "#    ", "#    ", "#    "),
    "Q": (" ### ", "#   #", "#   #", "#   #", "# # #", "#  # ", " ## #"),
    "R": ("#### ", "#   #", "#   #", "#### ", "# #  ", "#  # ", "#   #"),
    "S": (" ####", "#    ", "#    ", " ### ", "    #", "    #", "#### "),
    "T": ("#####", "  #  ", "  #  ", "  #  ", "  #  ", "  #  ", "  #  "),
    "U": ("#   #", "#   #", "#   #", "#   #", "#   #", "#   #", " ### "),
    "V": ("#   #", "#   #", "#   #", "#   #", "#   #", " # # ", "  #  "),
    "W": ("#   #", "#   #", "#   #", "# # #", "# # #", "## ##", "#   #"),
    "X": ("#   #", "#   #", " # # ", "  #  ", " # # ", "#   #", "#   #"),
    "Y": ("#   #", "#   #", " # # ", "  #  ", "  #  ", "  #  ", "  #  "),
    "Z": ("#####", "    #", "   # ", "  #  ", " #   ", "#    ", "#####"),
    "a": ("     ", "     ", " ### ", "    #", " ####", "#   #", " ####"),
    "b": ("#    ", "#    ", "#### ", "#   #", "#   #", "#   #", "#### "),
    "c": ("     ", "     ", " ### ", "#    ", "#    ", "#   #", " ### "),
    "d": ("    #", "    #", " ####", "#   #", "#   #", "#   #", " ####"),
    "e": ("     ", "     ", " ### ", "#   #", "#####", "#    ", " ### "),
    "f": ("  ## ", " #  #", " #   ", "#### ", " #   ", " #   ", " #   "),
    "g": ("     ", " ####", "#   #", "#   #", " ####", "    #", " ### "),
    "h": ("#    ", "#    ", "#### ", "#   #", "#   #", "#   #", "#   #"),
    "i": ("     ", "  #  ", "     ", " ##  ", "  #  ", "  #  ", " ### "),
    "j": ("     ", "   # ", "     ", "  ## ", "   # ", "   # ", "##   "),
    "k": ("#    ", "#    ", "#  # ", "# #  ", "##   ", "# #  ", "#  # "),
    "l": (" ##  ", "  #  ", "  #  ", "  #  ", "  #  ", "  #  ", " ### "),
    "m": ("     ", "     ", "## # ", "# # #", "# # #", "# # #", "# # #"),
    "n": ("     ", "     ", "#### ", "#   #", "#   #", "#   #", "#   #"),
    "o": ("     ", "     ", " ### ", "#   #", "#   #", "#   #", " ### "),
    "p": ("     ", "     ", "#### ", "#   #", "#   #", "#### ", "#    "),
    "q": ("     ", "     ", " ####", "#   #", "#   #", " ####", "    #"),
    "r": ("     ", "     ", "# ## ", "##  #", "#    ", "#    ", "#    "),
    "s": ("     ", "     ", " ####", "#    ", " ### ", "    #", "#### "),
    "t": (" #   ", " #   ", "#### ", " #   ", " #   ", " #  #", "  ## "),
    "u": ("     ", "     ", "#   #", "#   #", "#   #", "#  ##", " ## #"),
    "v": ("     ", "     ", "#   #", "#   #", "#   #", " # # ", "  #  "),
    "w": ("     ", "     ", "#   #", "# # #", "# # #", "# # #", " # # "),
    "x": ("     ", "     ", "#   #", " # # ", "  #  ", " # # ", "#   #"),
    "y": ("     ", "     ", "#   #", "#   #", "#   #", " ####", "    #"),
    "z": ("     ", "     ", "#####", "   # ", "  #  ", " #   ", "#####"),
    " ": ("     ", "     ", "     ", "     ", "     ", "     ", "     "),
    "!": ("  #  ", "  #  ", "  #  ", "  #  ", "  #  ", "     ", "  #  "),
    '"': (" # # ", " # # ", " # # ", "     ", "     ", "     ", "     "),
    "'": ("  #  ", "  #  ", " #   ", "     ", "     ", "     ", "     "),
    "(": ("   # ", "  #  ", "  #  ", "  #  ", "  #  ", "  #  ", "   # "),
    ")": (" #   ", "  #  ", "  #  ", "  #  ", "  #  ", "  #  ", " #   "),
    ",": ("     ", "     ", "     ", "     ", "  #  ", "  #  ", " #   "),
    "-": ("     ", "     ", "     ", "#####", "     ", "     ", "     "),
    ".": ("     ", "     ", "     ", "     ", "     ", "     ", "  #  "),
    "/": ("    #", "    #", "   # ", "  #  ", "  #  ", " #   ", "#    "),
    ":": ("     ", "  #  ", "     ", "     ", "     ", "  #  ", "     "),
    ";": ("     ", "  #  ", "     ", "     ", "  #  ", "  #  ", " #   "),
    "?": (" ### ", "#   #", "    #", "   # ", "  #  ", "     ", "  #  "),
    "%": ("#   #", "#  # ", "   # ", "  #  ", " #   ", "#  # ", "#   #"),
    "&": (" ### ", "#   #", "#   #", " # # ", "# #  ", "# #  ", " ## #"),
    "+": ("     ", "  #  ", "  #  ", "#####", "  #  ", "  #  ", "     "),
    "=": ("     ", "     ", "#####", "     ", "#####", "     ", "     "),
    "$": ("  #  ", " ####", "# # #", " ### ", "  # #", "# # #", "  #  "),
    "\u2022": ("     ", "     ", "  #  ", "  #  ", "     ", "     ", "     "),
    "\u2014": ("     ", "     ", "     ", "#####", "     ", "     ", "     "),
    "\u00d7": ("     ", "     ", "#   #", " # # ", "  #  ", " # # ", "#   #"),
}

CHAR_W = 5
CHAR_H = 7


def text_width(s, scale=1):
    return len(s) * (CHAR_W + 1) * scale - scale


# ---------------------------------------------------------------- canvas

class Canvas:
    def __init__(self, w, h, bg):
        self.w = w
        self.h = h
        self.px = bytearray(w * h * 3)
        self.fill(bg)

    def fill(self, color):
        r, g, b = color
        self.px[:] = bytes((r, g, b)) * (self.w * self.h)

    def set(self, x, y, color):
        if 0 <= x < self.w and 0 <= y < self.h:
            i = (y * self.w + x) * 3
            self.px[i], self.px[i + 1], self.px[i + 2] = color

    def fill_rect(self, x, y, w, h, color):
        x0 = max(0, x)
        y0 = max(0, y)
        x1 = min(self.w, x + w)
        y1 = min(self.h, y + h)
        if x1 <= x0 or y1 <= y0:
            return
        r, g, b = color
        row = bytes((r, g, b)) * (x1 - x0)
        for yy in range(y0, y1):
            i = (yy * self.w + x0) * 3
            self.px[i:i + len(row)] = row

    def rect(self, x, y, w, h, color, t=1):
        self.fill_rect(x, y, w, t, color)
        self.fill_rect(x, y + h - t, w, t, color)
        self.fill_rect(x, y, t, h, color)
        self.fill_rect(x + w - t, y, t, h, color)

    def hline(self, x, y, w, color, t=1):
        self.fill_rect(x, y, w, t, color)

    def vline(self, x, y, h, color, t=1):
        self.fill_rect(x, y, t, h, color)

    def line(self, x0, y0, x1, y1, color, t=1):
        dx = abs(x1 - x0)
        dy = -abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = dx + dy
        while True:
            if t == 1:
                self.set(x0, y0, color)
            else:
                self.fill_rect(x0 - t // 2, y0 - t // 2, t, t, color)
            if x0 == x1 and y0 == y1:
                break
            e2 = 2 * err
            if e2 >= dy:
                err += dy
                x0 += sx
            if e2 <= dx:
                err += dx
                y0 += sy

    def circle(self, cx, cy, r, color, filled=True):
        if filled:
            for dy in range(-r, r + 1):
                dx = int((r * r - dy * dy) ** 0.5)
                self.fill_rect(cx - dx, cy + dy, 2 * dx + 1, 1, color)
        else:
            x, y, d = 0, r, 3 - 2 * r
            while x <= y:
                for px, py in ((cx + x, cy + y), (cx - x, cy + y),
                               (cx + x, cy - y), (cx - x, cy - y),
                               (cx + y, cy + x), (cx - y, cy + x),
                               (cx + y, cy - x), (cx - y, cy - x)):
                    self.set(px, py, color)
                if d < 0:
                    d += 4 * x + 6
                else:
                    d += 4 * (x - y) + 10
                    y -= 1
                x += 1

    def ellipse(self, cx, cy, rx, ry, color):
        for dy in range(-ry, ry + 1):
            dx = int(rx * (1 - (dy * dy) / (ry * ry)) ** 0.5) if ry else 0
            self.fill_rect(cx - dx, cy + dy, 2 * dx + 1, 1, color)

    def triangle(self, pts, color):
        # pts: list of 3 (x, y); scanline fill
        xs = [p[0] for p in pts]
        ys = [p[1] for p in pts]
        for y in range(min(ys), max(ys) + 1):
            nodes = []
            for i in range(3):
                x0, y0 = pts[i]
                x1, y1 = pts[(i + 1) % 3]
                if y0 == y1:
                    continue
                if (y0 <= y < y1) or (y1 <= y < y0):
                    nodes.append(x0 + (y - y0) * (x1 - x0) / (y1 - y0))
            if len(nodes) >= 2:
                nodes.sort()
                self.fill_rect(int(nodes[0]), y, int(nodes[-1]) - int(nodes[0]) + 1, 1, color)

    def polygon(self, pts, color):
        n = len(pts)
        for y in range(min(p[1] for p in pts), max(p[1] for p in pts) + 1):
            nodes = []
            for i in range(n):
                x0, y0 = pts[i]
                x1, y1 = pts[(i + 1) % n]
                if y0 == y1:
                    continue
                if (y0 <= y < y1) or (y1 <= y < y0):
                    nodes.append(x0 + (y - y0) * (x1 - x0) / (y1 - y0))
            nodes.sort()
            for i in range(0, len(nodes) - 1, 2):
                self.fill_rect(int(nodes[i]), y, int(nodes[i + 1]) - int(nodes[i]) + 1, 1, color)

    # ------------------------------------------------------------- text

    def text(self, s, x, y, scale=1, color=(0, 0, 0), bold=False):
        cx = x
        for ch in s:
            glyph = FONT.get(ch)
            if glyph is None:
                cx += (CHAR_W + 1) * scale
                continue
            for row in range(CHAR_H):
                bits = glyph[row]
                for col in range(CHAR_W):
                    if bits[col] == "#":
                        bx = cx + col * scale
                        by = y + row * scale
                        self.fill_rect(bx, by, scale, scale, color)
                        if bold:
                            self.fill_rect(bx + 1, by, scale, scale, color)
            cx += (CHAR_W + 1) * scale
        return cx

    def text_center(self, s, cx, y, scale=1, color=(0, 0, 0), bold=False):
        w = text_width(s, scale)
        return self.text(s, cx - w // 2, y, scale, color, bold)

    def text_right(self, s, x, y, scale=1, color=(0, 0, 0), bold=False):
        w = text_width(s, scale)
        return self.text(s, x - w, y, scale, color, bold)


def wrap_text(s, width_px, scale=1):
    """Greedy word wrap; returns a list of lines fitting width_px."""
    max_chars = max(1, (width_px + scale) // ((CHAR_W + 1) * scale))
    words = s.split(" ")
    lines = []
    cur = ""
    for word in words:
        if not cur:
            cur = word
        elif len(cur) + 1 + len(word) <= max_chars:
            cur += " " + word
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


# ------------------------------------------------------------------- png

def _chunk(kind, data):
    c = struct.pack(">I", len(data)) + kind + data
    c += struct.pack(">I", binascii.crc32(kind + data) & 0xFFFFFFFF)
    return c


def write_png(canvas, path):
    w, h = canvas.w, canvas.h
    raw = bytearray()
    for y in range(h):
        raw.append(0)
        raw += canvas.px[y * w * 3:(y + 1) * w * 3]
    comp = zlib.compress(bytes(raw), 9)
    ihdr = struct.pack(">IIBBBBB", w, h, 8, 2, 0, 0, 0)
    png = b"\x89PNG\r\n\x1a\n"
    png += _chunk(b"IHDR", ihdr)
    png += _chunk(b"IDAT", comp)
    png += _chunk(b"IEND", b"")
    with open(path, "wb") as f:
        f.write(png)
    return len(png)

# ------------------------------------------------------------ palettes

PAPER = (248, 243, 227)
PANEL = (255, 253, 245)
INK = (25, 23, 19)
RED = (166, 27, 27)
RULE = (120, 110, 90)
GREY = (107, 100, 88)
WHITE = (255, 255, 255)

STATUS_COLORS = {
    "CONFIRMED": (21, 128, 61),
    "OFFICIAL": (29, 78, 216),
    "REPORTED": (180, 83, 9),
    "CLAIM": (194, 65, 12),
    "PENDING": (107, 114, 128),
}

REGION_COLORS = {
    "NORTH AMERICA": (37, 99, 235),
    "LATIN AMERICA": (8, 145, 178),
    "EUROPE": (124, 58, 237),
    "MIDDLE EAST": (217, 119, 6),
    "ASIA": (220, 38, 38),
    "AFRICA": (101, 163, 13),
    "OCEANIA": (5, 150, 105),
    "GLOBAL": (71, 85, 105),
}

STATUS_DEFS = [
    ("CONFIRMED", "verified by 2+ outlets"),
    ("OFFICIAL", "govt / institution statement"),
    ("REPORTED", "outlet reporting, one source"),
    ("CLAIM", "one side's claim, unverified"),
    ("PENDING", "developing, unconfirmed"),
]


def _grad(cv, x, y, w, h, c1, c2, bands=8):
    for i in range(bands):
        t0 = i / bands
        t1 = (i + 1) / bands
        r = int(c1[0] + (c2[0] - c1[0]) * (t0 + t1) / 2)
        g = int(c1[1] + (c2[1] - c1[1]) * (t0 + t1) / 2)
        b = int(c1[2] + (c2[2] - c1[2]) * (t0 + t1) / 2)
        cv.fill_rect(x, y + int(h * t0), w, int(h * t1) - int(h * t0) + 1, (r, g, b))


def _star4(cv, cx, cy, r, color):
    cv.polygon([(cx, cy - r), (cx + r // 3, cy - r // 3), (cx + r, cy),
                (cx + r // 3, cy + r // 3), (cx, cy + r),
                (cx - r // 3, cy + r // 3), (cx - r, cy),
                (cx - r // 3, cy - r // 3)], color)


def _rays(cv, cx, cy, r0, r1, n, color):
    import math
    for k in range(n):
        a = 2 * math.pi * k / n
        cv.line(int(cx + r0 * math.cos(a)), int(cy + r0 * math.sin(a)),
                int(cx + r1 * math.cos(a)), int(cy + r1 * math.sin(a)), color, 2)


def _arrow_up(cv, x, y, w, h, color):
    # bold upward arrow inside box x,y,w,h
    hw = w // 2
    cv.polygon([(x + hw, y), (x + w, y + h // 2), (x + hw + w // 6, y + h // 2),
                (x + hw + w // 6, y + h), (x + hw - w // 6, y + h),
                (x + hw - w // 6, y + h // 2), (x, y + h // 2)], color)


def _arrow_down(cv, x, y, w, h, color):
    hw = w // 2
    cv.polygon([(x + hw, y + h), (x + w, y + h // 2), (x + hw + w // 6, y + h // 2),
                (x + hw + w // 6, y), (x + hw - w // 6, y),
                (x + hw - w // 6, y + h // 2), (x, y + h // 2)], color)


# --------------------------------------------------------- illustrations
# Each draws a distinct scene into (x, y, w, h). No text inside except
# where a big number is part of the picture.

def illo_chip(cv, x, y, w, h):
    _grad(cv, x, y, w, h, (11, 61, 46), (4, 38, 28))
    cx, cy = x + w // 3, y + h // 2
    s = min(w, h) - 26
    # chip pins
    for i in range(4):
        py = cy - s // 2 + 6 + i * (s - 12) // 3
        cv.fill_rect(cx - s // 2 - 10, py, 10, 4, (212, 175, 55))
        cv.fill_rect(cx + s // 2, py, 10, 4, (212, 175, 55))
    cv.fill_rect(cx - s // 2, cy - s // 2, s, s, (16, 120, 70))
    cv.rect(cx - s // 2, cy - s // 2, s, s, (212, 175, 55), 2)
    cv.fill_rect(cx - s // 4, cy - s // 4, s // 2, s // 2, (212, 175, 55))
    cv.text("NV", cx - 11, cy - 4, 1, (11, 61, 46), bold=True)
    ax, ay = x + 2 * w // 3 - 18, y + 12
    _arrow_up(cv, ax, ay, 34, h - 24, (255, 255, 255))


def illo_strait(cv, x, y, w, h):
    _grad(cv, x, y, w, h, (186, 214, 235), (70, 130, 180))
    # tanker
    hx, hy = x + w // 6, y + h // 2 + 4
    cv.fill_rect(hx, hy, w // 2, 12, (30, 41, 59))
    cv.polygon([(hx + w // 2, hy), (hx + w // 2 + 16, hy + 6), (hx + w // 2, hy + 12)], (30, 41, 59))
    for i in range(3):
        cv.fill_rect(hx + 6 + i * 16, hy - 12, 13, 12, (194, 65, 12) if i != 1 else (37, 99, 235))
    # drone above
    dx, dy = x + 3 * w // 4, y + h // 4
    cv.fill_rect(dx - 12, dy - 2, 24, 4, (25, 23, 19))
    cv.fill_rect(dx - 3, dy - 6, 6, 12, (25, 23, 19))
    cv.circle(dx - 12, dy, 3, (25, 23, 19))
    cv.circle(dx + 12, dy, 3, (25, 23, 19))
    # blockade line
    for i in range(0, w, 10):
        cv.fill_rect(x + i, y + h - 12, 6, 3, (166, 27, 27))
    cv.fill_rect(x, y + h - 6, w, 2, (166, 27, 27))


def illo_sanctions(cv, x, y, w, h):
    _grad(cv, x, y, w, h, (24, 42, 92), (12, 24, 60))
    import math
    cx, cy, r = x + w // 2, y + h // 2, min(w, h) // 2 - 6
    for k in range(12):
        a = 2 * math.pi * k / 12 - math.pi / 2
        _star4(cv, int(cx + r * math.cos(a)), int(cy + r * math.sin(a)), 4, (255, 209, 0))
    # bank building in the middle
    bx, by = cx - 26, cy - 10
    cv.fill_rect(bx, by + 16, 52, 14, (226, 232, 240))
    cv.polygon([(bx - 4, by + 16), (bx + 26, by - 4), (bx + 56, by + 16)], (226, 232, 240))
    for i in range(4):
        cv.fill_rect(bx + 4 + i * 12, by + 18, 4, 12, (24, 42, 92))
    cv.line(bx - 8, by - 8, bx + 60, by + 38, (220, 38, 38), 4)


def illo_peaks(cv, x, y, w, h):
    _grad(cv, x, y, w, h, (147, 197, 253), (219, 234, 254))
    _rays(cv, x + w - 16, y + 14, 6, 11, 8, (250, 204, 21))
    cv.circle(x + w - 16, y + 14, 6, (250, 204, 21))
    cv.polygon([(x + 4, y + h), (x + w // 3, y + h // 4), (x + 2 * w // 3 - 8, y + h)], (100, 116, 139))
    cv.polygon([(x + w // 3 - 12, y + h // 4 + 12), (x + w // 3, y + h // 4),
                (x + w // 3 + 12, y + h // 4 + 12)], (255, 255, 255))
    cv.polygon([(x + w // 3, y + h), (x + 2 * w // 3, y + h // 3), (x + w - 4, y + h)], (71, 85, 105))
    cv.polygon([(x + 2 * w // 3 - 10, y + h // 3 + 10), (x + 2 * w // 3, y + h // 3),
                (x + 2 * w // 3 + 10, y + h // 3 + 10)], (255, 255, 255))
    cv.fill_rect(x, y + h - 8, w, 8, (34, 197, 94))


def illo_corvette(cv, x, y, w, h):
    _grad(cv, x, y, w, h, (125, 180, 220), (30, 80, 130))
    # explosion burst
    ex, ey = x + w // 2, y + h // 3
    _star4(cv, ex, ey, 22, (249, 115, 22))
    _star4(cv, ex, ey, 12, (250, 204, 21))
    # ship
    sx, sy = x + w // 6, y + 2 * h // 3
    cv.fill_rect(sx, sy, 2 * w // 3, 10, (30, 41, 59))
    cv.fill_rect(sx + 10, sy - 10, 30, 10, (51, 65, 85))
    cv.line(sx + 25, sy - 10, sx + 25, sy - 24, (30, 41, 59), 2)
    # waves
    for i in range(4):
        cv.line(x + 6 + i * 22, y + h - 8, x + 16 + i * 22, y + h - 8, (255, 255, 255), 2)


def illo_rubble(cv, x, y, w, h):
    _grad(cv, x, y, w, h, (203, 213, 225), (148, 163, 184))
    # damaged apartment block
    bx, by = x + w // 5, y + 8
    bw, bh = w // 2, h - 26
    cv.fill_rect(bx, by, bw, bh, (120, 113, 108))
    cv.polygon([(bx, by), (bx + bw // 2, by + 12), (bx + bw, by)], (120, 113, 108))
    for r in range(3):
        for c in range(3):
            cv.fill_rect(bx + 6 + c * (bw - 12) // 3, by + 16 + r * (bh - 20) // 3,
                         8, 8, (253, 230, 138))
    # rubble pile
    cv.polygon([(x + w // 2, y + h), (x + 3 * w // 4, y + h // 2),
                (x + w - 4, y + h)], (87, 83, 78))
    cv.polygon([(x + 2 * w // 3, y + h), (x + 5 * w // 6, y + 2 * h // 3),
                (x + w - 2, y + h)], (68, 64, 60))
    # searchlight beam
    cv.polygon([(x + w - 14, y + 6), (x + w - 30, y + h // 2), (x + w - 6, y + h // 2)],
               (254, 249, 195))


def illo_un(cv, x, y, w, h):
    _grad(cv, x, y, w, h, (254, 243, 199), (226, 196, 130))
    # UN building
    bx, by = x + w // 6, y + h // 3
    cv.fill_rect(bx, by, w // 2, h // 2, (226, 232, 240))
    for r in range(3):
        for c in range(5):
            cv.fill_rect(bx + 4 + c * 10, by + 5 + r * 9, 6, 5, (37, 99, 235))
    # UN flag
    fx = x + w - 30
    cv.line(fx, y + 8, fx, y + h // 2, (25, 23, 19), 2)
    cv.fill_rect(fx, y + 8, 24, 14, (37, 99, 235))
    cv.circle(fx + 12, y + 15, 5, (255, 255, 255))
    # drone + smoke
    dx, dy = x + w // 4, y + 10
    cv.fill_rect(dx - 10, dy, 20, 3, (25, 23, 19))
    cv.circle(dx - 10, dy + 1, 2, (25, 23, 19))
    cv.circle(dx + 10, dy + 1, 2, (25, 23, 19))
    cv.circle(x + 3 * w // 4, y + h - 16, 8, (107, 114, 128))
    cv.circle(x + 3 * w // 4 + 10, y + h - 12, 6, (156, 163, 175))


def illo_well(cv, x, y, w, h):
    _grad(cv, x, y, w, h, (254, 243, 199), (214, 182, 120))
    # well with roof
    wx, wy = x + w // 4, y + h // 2
    cv.line(wx, wy, wx, wy - 22, (120, 53, 15), 3)
    cv.line(wx + 34, wy, wx + 34, wy - 22, (120, 53, 15), 3)
    cv.polygon([(wx - 6, wy - 22), (wx + 17, wy - 34), (wx + 40, wy - 22)], (146, 64, 14))
    cv.ellipse(wx + 17, wy + 6, 20, 8, (100, 116, 139))
    cv.ellipse(wx + 17, wy + 4, 16, 5, (30, 80, 130))
    # blue flag
    fx = x + 3 * w // 4
    cv.line(fx, y + 6, fx, y + h // 2 + 8, (25, 23, 19), 2)
    cv.fill_rect(fx, y + 6, 22, 12, (37, 99, 235))
    cv.circle(fx + 11, y + 12, 4, (255, 255, 255))


def illo_chart(cv, x, y, w, h):
    cv.fill_rect(x, y, w, h, (255, 253, 245))
    # grid
    for i in range(4):
        cv.hline(x + 4, y + 8 + i * (h - 16) // 3, w - 8, (226, 220, 200))
    # candles: falling red, one green rebound
    xs = [x + 10, x + 34, x + 58, x + 82, x + 106, x + 130, x + 154]
    tops = [14, 20, 26, 34, 40, 46, 30]
    bots = [30, 34, 42, 50, 56, 60, 52]
    for i in range(7):
        col = (22, 163, 74) if i == 6 else (220, 38, 38)
        cx = xs[i]
        cv.vline(cx + 5, y + tops[i] - 4, bots[i] - tops[i] + 8, col, 1)
        cv.fill_rect(cx, y + tops[i], 10, bots[i] - tops[i], col)
    _arrow_down(cv, x + w - 34, y + 6, 26, 26, (220, 38, 38))


def illo_cuffs(cv, x, y, w, h):
    _grad(cv, x, y, w, h, (254, 215, 170), (226, 160, 90))
    # desert mountains
    cv.polygon([(x, y + h), (x + w // 3, y + h // 2), (x + 2 * w // 3, y + h)], (180, 120, 60))
    cv.polygon([(x + w // 3, y + h), (x + 2 * w // 3, y + h // 3), (x + w, y + h)], (160, 100, 50))
    # handcuffs
    cy = y + h // 2 + 6
    cv.circle(x + w // 3, cy, 12, (226, 232, 240))
    cv.circle(x + w // 3, cy, 7, (254, 215, 170))
    cv.circle(x + 2 * w // 3, cy, 12, (226, 232, 240))
    cv.circle(x + 2 * w // 3, cy, 7, (254, 215, 170))
    cv.line(x + w // 3 + 10, cy - 4, x + 2 * w // 3 - 10, cy - 4, (226, 232, 240), 3)
    cv.circle(x + w // 3, cy, 12, (100, 116, 139), filled=False)
    cv.circle(x + 2 * w // 3, cy, 12, (100, 116, 139), filled=False)


def illo_cop(cv, x, y, w, h):
    _grad(cv, x, y, w, h, (186, 230, 253), (240, 249, 255))
    cx, cy = x + w // 2, y + h // 2
    r = min(w, h) // 2 - 6
    cv.circle(cx, cy, r, (37, 99, 235))
    cv.ellipse(cx - 6, cy - 8, 10, 7, (34, 197, 94))
    cv.ellipse(cx + 10, cy + 6, 8, 6, (34, 197, 94))
    cv.ellipse(cx - 12, cy + 10, 6, 4, (34, 197, 94))
    # crack across the globe
    cv.line(cx - r, cy - r // 2, cx - r // 3, cy, (25, 23, 19), 2)
    cv.line(cx - r // 3, cy, cx + r // 4, cy + r // 3, (25, 23, 19), 2)
    cv.line(cx + r // 4, cy + r // 3, cx + r, cy + r // 2, (25, 23, 19), 2)
    cv.fill_rect(x, y + h - 6, w, 6, (220, 38, 38))


def illo_court(cv, x, y, w, h):
    _grad(cv, x, y, w, h, (226, 232, 240), (203, 213, 225))
    # courthouse
    cx = x + w // 2
    cv.polygon([(cx - 40, y + 16), (cx, y + 2), (cx + 40, y + 16)], (100, 116, 139))
    for i in range(4):
        cv.fill_rect(cx - 34 + i * 18, y + 18, 6, h - 30, (226, 232, 240))
        cv.rect(cx - 34 + i * 18, y + 18, 6, h - 30, (100, 116, 139), 1)
    cv.fill_rect(cx - 42, y + h - 12, 84, 4, (100, 116, 139))
    # gavel
    gx, gy = x + w - 30, y + h - 22
    cv.fill_rect(gx, gy, 20, 8, (120, 53, 15))
    cv.line(gx + 10, gy + 8, gx + 16, gy + 18, (120, 53, 15), 3)


def illo_cricket(cv, x, y, w, h):
    _grad(cv, x, y, w, h, (134, 239, 172), (34, 197, 94))
    # pitch strip
    cv.fill_rect(x + w // 4, y, w // 2, h, (214, 182, 130))
    # stumps
    sx = x + w // 2 - 12
    for i in range(3):
        cv.fill_rect(sx + i * 9, y + 10, 4, 22, (250, 204, 21))
    cv.fill_rect(sx - 2, y + 8, 30, 3, (250, 204, 21))
    # bat
    cv.polygon([(x + w // 3, y + h - 8), (x + w // 3 + 10, y + h - 8),
                (x + w // 2 + 14, y + h // 2), (x + w // 2 + 4, y + h // 2)], (180, 140, 90))
    # ball
    cv.circle(x + 3 * w // 4, y + h // 3, 7, (220, 38, 38))
    cv.circle(x + 3 * w // 4, y + h // 3, 7, (255, 255, 255), filled=False)


ILLOS = {
    "chip": illo_chip,
    "strait": illo_strait,
    "sanctions": illo_sanctions,
    "peaks": illo_peaks,
    "corvette": illo_corvette,
    "rubble": illo_rubble,
    "un": illo_un,
    "well": illo_well,
    "chart": illo_chart,
    "cuffs": illo_cuffs,
    "cop": illo_cop,
    "court": illo_court,
    "cricket": illo_cricket,
}


# ------------------------------------------------------------------- map

# Coarse equirectangular land mask: 32 rows (85N..-58S), 64 columns
# (180W..180E). Spans are (first_col, last_col) inclusive per row.
LAND_SPANS = {
    0: [(17, 19), (21, 27)],
    1: [(8, 19), (21, 28), (33, 34)],
    2: [(5, 15), (17, 19), (21, 27), (36, 60)],
    3: [(3, 16), (21, 26), (35, 61)],
    4: [(2, 15), (28, 33), (35, 61)],
    5: [(2, 14), (28, 34), (36, 60)],
    6: [(4, 14), (27, 35), (37, 59)],
    7: [(5, 14), (27, 36), (37, 58)],
    8: [(6, 14), (27, 37), (38, 55)],
    9: [(6, 14), (28, 37), (38, 53), (56, 58)],
    10: [(6, 13), (28, 31), (36, 41), (45, 52), (56, 58)],
    11: [(7, 12), (29, 31), (36, 40), (43, 46), (48, 52), (55, 57)],
    12: [(8, 12), (29, 37), (39, 41), (43, 46), (47, 50)],
    13: [(9, 12), (29, 38), (43, 46), (47, 49)],
    14: [(10, 13), (30, 38), (44, 46), (48, 50)],
    15: [(11, 14), (31, 38), (49, 51)],
    16: [(12, 16), (31, 38), (50, 53)],
    17: [(13, 17), (32, 37), (51, 55)],
    18: [(13, 18), (33, 36), (51, 56)],
    19: [(14, 18), (33, 36), (50, 57)],
    20: [(14, 18), (33, 35), (50, 57)],
    21: [(14, 17), (33, 35), (40, 41), (52, 57)],
    22: [(15, 17), (34, 35), (40, 41), (51, 56)],
    23: [(15, 17), (34, 35), (40, 41), (52, 55)],
    24: [(15, 17), (34, 35), (40, 41), (53, 55)],
    25: [(15, 16), (53, 55)],
    26: [(15, 16), (61, 62)],
    27: [(15, 16), (61, 63)],
    28: [(16, 16), (62, 63)],
    29: [(16, 16)],
    30: [(16, 16)],
}

LAND_COLOR = (148, 163, 120)
SEA_COLOR = (208, 224, 235)


def project(lon, lat, mx, my, cw, ch):
    col = (lon + 180.0) / 5.625
    row = (85.0 - lat) / 4.53
    return mx + col * cw, my + row * ch


def draw_map(cv, x, y, w, h, pins):
    """Dot-grid world map with numbered region-colored pins.
    pins: list of (lon, lat, number, region)."""
    cv.fill_rect(x, y, w, h, SEA_COLOR)
    cw = w / 64.0
    ch = h / 32.0
    for row, spans in LAND_SPANS.items():
        for c0, c1 in spans:
            for c in range(c0, c1 + 1):
                dx = int(x + c * cw + cw / 2)
                dy = int(y + row * ch + ch / 2)
                cv.fill_rect(dx - 1, dy - 1, 2, 2, LAND_COLOR)
    for lon, lat, num, region in pins:
        px, py = project(lon, lat, x, y, cw, ch)
        px, py = int(px), int(py)
        col = REGION_COLORS[region]
        cv.circle(px, py, 7, WHITE)
        cv.circle(px, py, 6, col)
        s = str(num)
        tw = text_width(s, 1)
        cv.text(s, px - tw // 2, py - 3, 1, WHITE, bold=True)


# ------------------------------------------------------------ status chip

def draw_status(cv, x, y, status):
    col = STATUS_COLORS[status]
    w = text_width(status, 1) + 10
    cv.fill_rect(x, y, w, 11, col)
    cv.text(status, x + 5, y + 2, 1, WHITE, bold=True)
    return w
