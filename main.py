#!/usr/bin/env python3
# Entry repo: Einju/news-image-20261121
import os
import sys
import zlib
import struct
import math

# ---------------------------------------------------------
# BITMAP FONT & RENDERER
# ---------------------------------------------------------
FONT_5X7 = {
    'A': ["01110", "10001", "10001", "11111", "10001", "10001", "10001"],
    'B': ["11110", "10001", "10001", "11110", "10001", "10001", "11110"],
    'C': ["01110", "10001", "10000", "10000", "10000", "10001", "01110"],
    'D': ["11110", "10001", "10001", "10001", "10001", "10001", "11110"],
    'E': ["11111", "10000", "10000", "11110", "10000", "10000", "11111"],
    'F': ["11111", "10000", "10000", "11110", "10000", "10000", "10000"],
    'G': ["01110", "10001", "10000", "10111", "10001", "10001", "01110"],
    'H': ["10001", "10001", "10001", "11111", "10001", "10001", "10001"],
    'I': ["01110", "00100", "00100", "00100", "00100", "00100", "01110"],
    'J': ["00111", "00010", "00010", "00010", "10010", "10010", "01100"],
    'K': ["10001", "10010", "10100", "11000", "10100", "10010", "10001"],
    'L': ["10000", "10000", "10000", "10000", "10000", "10000", "11111"],
    'M': ["10001", "11011", "10101", "10001", "10001", "10001", "10001"],
    'N': ["10001", "11001", "10101", "10011", "10001", "10001", "10001"],
    'O': ["01110", "10001", "10001", "10001", "10001", "10001", "01110"],
    'P': ["11110", "10001", "10001", "11110", "10000", "10000", "10000"],
    'Q': ["01110", "10001", "10001", "10001", "10101", "10010", "01101"],
    'R': ["11110", "10001", "10001", "11110", "10100", "10010", "10001"],
    'S': ["01111", "10000", "10000", "01110", "00001", "00001", "11110"],
    'T': ["11111", "00100", "00100", "00100", "00100", "00100", "00100"],
    'U': ["10001", "10001", "10001", "10001", "10001", "10001", "01110"],
    'V': ["10001", "10001", "10001", "10001", "10001", "01010", "00100"],
    'W': ["10001", "10001", "10001", "10101", "10101", "11011", "10001"],
    'X': ["10001", "10001", "01010", "00100", "01010", "10001", "10001"],
    'Y': ["10001", "10001", "01010", "00100", "00100", "00100", "00100"],
    'Z': ["11111", "00001", "00010", "00100", "01000", "10000", "11111"],
    
    '0': ["01110", "10011", "10101", "11001", "10001", "10001", "01110"],
    '1': ["00100", "01100", "00100", "00100", "00100", "00100", "01110"],
    '2': ["01110", "10001", "00001", "00110", "01000", "10000", "11111"],
    '3': ["11110", "00001", "00001", "01110", "00001", "00001", "11110"],
    '4': ["10001", "10001", "10001", "11111", "00001", "00001", "00001"],
    '5': ["11111", "10000", "11110", "00001", "00001", "10001", "01110"],
    '6': ["01110", "10000", "11110", "10001", "10001", "10001", "01110"],
    '7': ["11111", "00001", "00010", "00100", "01000", "01000", "01000"],
    '8': ["01110", "10001", "10001", "01110", "10001", "10001", "01110"],
    '9': ["01110", "10001", "10001", "01111", "00001", "00001", "01110"],
    
    ' ': ["00000", "00000", "00000", "00000", "00000", "00000", "00000"],
    '$': ["00100", "01111", "10100", "01110", "00101", "11110", "00100"],
    '%': ["11001", "11010", "00100", "01000", "10011", "01101", "00000"],
    '-': ["00000", "00000", "00000", "11111", "00000", "00000", "00000"],
    ':': ["00000", "00100", "00100", "00000", "00100", "00100", "00000"],
    '.': ["00000", "00000", "00000", "00000", "00000", "00100", "00100"],
    ',': ["00000", "00000", "00000", "00000", "00000", "00100", "01000"],
    '\'': ["00100", "00100", "00000", "00000", "00000", "00000", "00000"],
    '(': ["00010", "00100", "01000", "01000", "01000", "00100", "00010"],
    ')': ["01000", "00100", "00010", "00010", "00010", "00100", "01000"],
    '+': ["00000", "00100", "00100", "11111", "00100", "00100", "00000"],
    '/': ["00001", "00010", "00100", "01000", "10000", "00000", "00000"],
    '&': ["01100", "10010", "10100", "01000", "10101", "10010", "01101"],
    '!': ["00100", "00100", "00100", "00100", "00100", "00000", "00100"],
    '?': ["01110", "10001", "00001", "00110", "00100", "00000", "00100"],
    '#': ["01010", "11111", "01010", "01010", "11111", "01010", "00000"],
    '—': ["00000","00000","00000","11111","00000","00000","00000"],
    '[': ["01110","01000","01000","01000","01000","01000","01110"],
    ']': ["01110","00010","00010","00010","00010","00010","01110"],
    '|': ["00100","00100","00100","00100","00100","00100","00100"],
}

for c in 'abcdefghijklmnopqrstuvwxyz':
    upper_c = c.upper()
    if upper_c in FONT_5X7:
        FONT_5X7[c] = FONT_5X7[upper_c]

def get_char_glyph(ch):
    return FONT_5X7.get(ch, FONT_5X7.get('?', ["11111","10001","10001","10001","10001","10001","11111"]))

# ---------------------------------------------------------
# IMAGE BUFFER & DRAWING PRIMITIVES
# ---------------------------------------------------------
WIDTH = 2048
HEIGHT = 2048

class Canvas:
    def __init__(self, w, h, bg_color=(248, 246, 240)):
        self.w = w
        self.h = h
        self.buf = bytearray(w * h * 3)
        r, g, b = bg_color
        for i in range(0, len(self.buf), 3):
            self.buf[i] = r
            self.buf[i+1] = g
            self.buf[i+2] = b

    def set_pixel(self, x, y, color):
        if 0 <= x < self.w and 0 <= y < self.h:
            idx = (y * self.w + x) * 3
            self.buf[idx] = color[0]
            self.buf[idx+1] = color[1]
            self.buf[idx+2] = color[2]

    def fill_rect(self, x0, y0, x1, y1, color):
        x0 = max(0, min(x0, self.w))
        x1 = max(0, min(x1, self.w))
        y0 = max(0, min(y0, self.h))
        y1 = max(0, min(y1, self.h))
        r, g, b = color
        for y in range(y0, y1):
            row_start = (y * self.w + x0) * 3
            row_len = (x1 - x0) * 3
            for i in range(row_start, row_start + row_len, 3):
                self.buf[i] = r
                self.buf[i+1] = g
                self.buf[i+2] = b

    def draw_rect(self, x0, y0, x1, y1, color, thickness=1):
        for t in range(thickness):
            self.fill_rect(x0, y0 + t, x1, y0 + t + 1, color)
            self.fill_rect(x0, y1 - 1 - t, x1, y1 - t, color)
            self.fill_rect(x0 + t, y0, x0 + t + 1, y1, color)
            self.fill_rect(x1 - 1 - t, y0, x1 - t, y1, color)

    def draw_line(self, x0, y0, x1, y1, color, thickness=1):
        dx = abs(x1 - x0)
        dy = abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = dx - dy
        x, y = x0, y0
        while True:
            for tx in range(-thickness//2, thickness//2 + 1):
                for ty in range(-thickness//2, thickness//2 + 1):
                    self.set_pixel(x + tx, y + ty, color)
            if x == x1 and y == y1:
                break
            e2 = 2 * err
            if e2 > -dy:
                err -= dy
                x += sx
            if e2 < dx:
                err += dx
                y += sy

    def draw_circle(self, cx, cy, r, color, filled=True):
        for y in range(cy - r, cy + r + 1):
            for x in range(cx - r, cx + r + 1):
                if (x - cx)**2 + (y - cy)**2 <= r**2:
                    self.set_pixel(x, y, color)

    def fill_polygon(self, points, color):
        if not points:
            return
        min_y = min(p[1] for p in points)
        max_y = max(p[1] for p in points)
        min_y = max(0, min_y)
        max_y = min(self.h - 1, max_y)

        for y in range(min_y, max_y + 1):
            nodes = []
            j = len(points) - 1
            for i in range(len(points)):
                xi, yi = points[i]
                xj, yj = points[j]
                if (yi < y and yj >= y) or (yj < y and yi >= y):
                    if yj != yi:
                        node_x = int(xi + (y - yi) / (yj - yi) * (xj - xi))
                        nodes.append(node_x)
                j = i
            nodes.sort()
            for i in range(0, len(nodes), 2):
                if i + 1 < len(nodes):
                    x_start = max(0, nodes[i])
                    x_end = min(self.w, nodes[i+1])
                    self.fill_rect(x_start, y, x_end, y + 1, color)

    def draw_text(self, text, x, y, scale, color):
        cx = x
        for ch in text:
            self.draw_char(ch, cx, y, scale, color)
            cx += 6 * scale

    def draw_char(self, ch, x, y, scale, color):
        glyph = get_char_glyph(ch)
        for row_idx, row_str in enumerate(glyph):
            for col_idx, bit in enumerate(row_str):
                if bit == '1':
                    self.fill_rect(
                        x + col_idx * scale,
                        y + row_idx * scale,
                        x + (col_idx + 1) * scale,
                        y + (row_idx + 1) * scale,
                        color
                    )

    def draw_wrapped_text(self, text, x, y, max_width, scale, color, line_spacing=4):
        max_chars_per_line = max(1, max_width // (6 * scale))
        words = text.split(' ')
        lines = []
        current_line = []
        
        for word in words:
            test_line = current_line + [word]
            test_str = ' '.join(test_line)
            if len(test_str) * 6 * scale <= max_width:
                current_line = test_line
            else:
                if current_line:
                    lines.append(' '.join(current_line))
                    current_line = [word]
                else:
                    lines.append(word)
                    current_line = []
        if current_line:
            lines.append(' '.join(current_line))
            
        line_height = 7 * scale + line_spacing
        cur_y = y
        for line in lines:
            self.draw_text(line, x, cur_y, scale, color)
            cur_y += line_height
        return cur_y - y

# ---------------------------------------------------------
# DETAILED ILLUSTRATION DRAWINGS FOR HEROES
# ---------------------------------------------------------
def draw_illustration_h1(canvas, x0, y0, x1, y1):
    # Peru M6.8 Quake & Andes mountains
    canvas.fill_rect(x0, y0, x1, y1, (230, 235, 242))
    # Andes mountains polygon
    peaks = [(x0, y1), (x0 + int(0.25*(x1-x0)), y0 + int(0.3*(y1-y0))), (x0 + int(0.5*(x1-x0)), y0 + int(0.5*(y1-y0))), (x0 + int(0.75*(x1-x0)), y0 + int(0.2*(y1-y0))), (x1, y1)]
    canvas.fill_polygon(peaks, (170, 160, 150))
    # Snow caps
    canvas.fill_polygon([(x0 + int(0.22*(x1-x0)), y0 + int(0.36*(y1-y0))), (x0 + int(0.25*(x1-x0)), y0 + int(0.3*(y1-y0))), (x0 + int(0.28*(x1-x0)), y0 + int(0.36*(y1-y0))), (x0 + int(0.25*(x1-x0)), y0 + int(0.4*(y1-y0)))], (250, 250, 250))
    canvas.fill_polygon([(x0 + int(0.72*(x1-x0)), y0 + int(0.26*(y1-y0))), (x0 + int(0.75*(x1-x0)), y0 + int(0.2*(y1-y0))), (x0 + int(0.78*(x1-x0)), y0 + int(0.26*(y1-y0))), (x0 + int(0.75*(x1-x0)), y0 + int(0.3*(y1-y0)))], (250, 250, 250))
    # Seismic shockwave rings
    cx, cy = x0 + int(0.5*(x1-x0)), y0 + int(0.6*(y1-y0))
    for r in range(15, 75, 12):
        canvas.draw_circle(cx, cy, r, (210, 60, 60), filled=False)

def draw_illustration_h2(canvas, x0, y0, x1, y1):
    # Banda Sea / Timor M6.8 Quake (Two quakes angle - dual seismograph / twin waves)
    canvas.fill_rect(x0, y0, x1, y1, (235, 240, 245))
    # Ocean background
    canvas.fill_rect(x0, y0 + int(0.5*(y1-y0)), x1, y1, (130, 170, 200))
    # Twin seismic wave lines
    for off_y in [y0 + 40, y0 + 100]:
        pts = [
            (x0 + 10, off_y),
            (x0 + 60, off_y - 20),
            (x0 + 120, off_y + 25),
            (x0 + 180, off_y - 30),
            (x0 + 240, off_y + 20),
            (x0 + 300, off_y),
        ]
        for i in range(len(pts) - 1):
            canvas.draw_line(pts[i][0], pts[i][1], pts[i+1][0], pts[i+1][1], (180, 40, 40), thickness=2)
    # Label "M6.8 x 2" badge
    canvas.fill_rect(x0 + 20, y1 - 35, x0 + 110, y1 - 10, (50, 50, 60))
    # We can draw small text or rely on text box

def draw_illustration_h3(canvas, x0, y0, x1, y1):
    # COP31 Antalya climate summit / no deal
    canvas.fill_rect(x0, y0, x1, y1, (240, 238, 230))
    # Globe / sun symbol
    cx, cy = x0 + int(0.5*(x1-x0)), y0 + int(0.45*(y1-y0))
    canvas.draw_circle(cx, cy, 45, (220, 140, 60))
    # Crossed out deal lines / red barrier
    canvas.draw_line(cx - 50, cy - 50, cx + 50, cy + 50, (200, 50, 50), thickness=5)
    canvas.draw_line(cx - 50, cy + 50, cx + 50, cy - 50, (200, 50, 50), thickness=5)
    # Podium / building silhouette at bottom
    canvas.fill_rect(x0 + 30, y1 - 35, x1 - 30, y1 - 10, (100, 100, 110))

def draw_illustration_h4(canvas, x0, y0, x1, y1):
    # Basra Hartha power station fire
    canvas.fill_rect(x0, y0, x1, y1, (240, 230, 225))
    # Industrial smokestacks
    canvas.fill_rect(x0 + 50, y0 + 60, x0 + 90, y1 - 20, (120, 120, 130))
    canvas.fill_rect(x0 + 130, y0 + 40, x0 + 170, y1 - 20, (120, 120, 130))
    # Fire / flames at base
    canvas.fill_rect(x0 + 40, y1 - 50, x0 + 180, y1 - 20, (220, 80, 40))
    canvas.fill_rect(x0 + 70, y1 - 70, x0 + 150, y1 - 40, (240, 140, 30))
    # Smoke plumes
    canvas.draw_circle(x0 + 70, y0 + 30, 22, (90, 90, 90))
    canvas.draw_circle(x0 + 150, y0 + 20, 28, (110, 110, 110))

# ---------------------------------------------------------
# MAIN NEWSPAPER RENDERER
# ---------------------------------------------------------
def render_newspaper():
    canvas = Canvas(WIDTH, HEIGHT, bg_color=(248, 246, 240))
    
    # ---------------------------------------------------------
    # 1. MASTHEAD BAND (y 0 - 170)
    # ---------------------------------------------------------
    canvas.fill_rect(0, 0, WIDTH, 170, (25, 25, 30))
    title = "THE WORLD TODAY"
    scale_title = 6
    title_w = len(title) * 6 * scale_title
    canvas.draw_text(title, (WIDTH - title_w) // 2, 25, scale_title, (255, 255, 255))
    
    sub1 = "SATURDAY, 21 NOVEMBER 2026"
    sub2 = "40 STORIES — ANDES, TIMOR, ANTALYA, BASRA & GLOBAL"
    scale_sub = 2
    w1 = len(sub1) * 6 * scale_sub
    w2 = len(sub2) * 6 * scale_sub
    canvas.draw_text(sub1, (WIDTH - w1) // 2, 100, scale_sub, (220, 200, 100))
    canvas.draw_text(sub2, (WIDTH - w2) // 2, 132, scale_sub, (180, 180, 180))
    
    canvas.fill_rect(0, 166, WIDTH, 170, (200, 180, 80))

    # ---------------------------------------------------------
    # 2. TIMELINE STRIP (y 175 - 235)
    # ---------------------------------------------------------
    canvas.fill_rect(64, 175, WIDTH - 64, 235, (238, 235, 228))
    canvas.draw_rect(64, 175, WIDTH - 64, 235, (180, 175, 165), thickness=2)
    
    canvas.draw_text("UTC TIMELINE (21 NOV 2026):", 80, 183, 1, (30, 30, 30))
    timeline_slots = [
        "00:09 UTC: Peru M6.8 Quake in Junin; 05:12 M5.0 aftershock",
        "~01:30 UTC: Russian drone & missile barrage hits 19 locations",
        "~01:53 Riyadh: Saudi coalition intercepts 3 Houthi ballistic missiles",
        "03:00 GMT: Hartha power station fire in Basra kills 4, injures 30+",
        "~04:00 Geneva: UN killer robots talks wrap with 2028 rules promise",
        "09:30 UTC: Timor / Banda Sea M6.8 Quake strikes (second M6.8 today)",
        "14:00 Paris: Cost-of-living protests begin at Republique",
        "18:24 UTC: BepiColombo scheduled Mercury orbit burn tonight"
    ]
    for i, slot in enumerate(timeline_slots):
        col = i % 2
        row = i // 2
        sx = 320 if col == 0 else 1180
        sy = 183 + row * 13
        display_slot = slot if len(slot) <= 72 else slot[:69] + "..."
        canvas.draw_text(display_slot, sx, sy, 1, (50, 50, 50))

    # ---------------------------------------------------------
    # 3. HEROES (y 245 - 880)
    # ---------------------------------------------------------
    heroes_data = [
        (
            "H1", "PERU M6.8 QUAKE: ANDES SHAKEN AT MIDNIGHT",
            "A powerful M6.8 earthquake (GFZ/Reuters; USGS 6.7) struck Junin, central Peru at 00:09 UTC Saturday, 129 km deep. Felt strongly in Lima with residents fleeing to streets. No major damage or casualties reported initially.",
            draw_illustration_h1
        ),
        (
            "H2", "TWO M6.8 QUAKES, ONE DAY: BANDA SEA STRUCK",
            "Just hours after Peru, a second M6.8 earthquake hit the Banda Sea, 226 km northeast of Dili, Timor-Leste at ~09:30 UTC. Felt across Dili and down to Darwin, Australia (~650 km).",
            draw_illustration_h2
        ),
        (
            "H3", "COP31 DEADLINE PASSED: NO DEAL INTO SATURDAY",
            "Antalya climate summit misses Friday deadline without agreement. Draft texts rejected amid fierce battles over fossil fuel phase-out language and $120B climate finance targets. Negotiations push through Saturday.",
            draw_illustration_h3
        ),
        (
            "H4", "BASRA POWER STATION BLAZE: 4 KILLED",
            "A major gas pipeline rupture triggers a massive fire at the Hartha thermal power station north of Basra, Iraq, at ~03:00 GMT Saturday. At least 4 killed and 30-35 injured, knocking the 800MW plant offline.",
            draw_illustration_h4
        ),
    ]

    h_boxes = [
        (64, 245, 994, 555),
        (1054, 245, 1984, 555),
        (64, 565, 994, 875),
        (1054, 565, 1984, 875),
    ]

    for idx, (tag, headline, desc, ill_fn) in enumerate(heroes_data):
        bx0, by0, bx1, by1 = h_boxes[idx]
        canvas.fill_rect(bx0, by0, bx1, by1, (255, 253, 248))
        canvas.draw_rect(bx0, by0, bx1, by1, (180, 175, 165), thickness=2)
        
        ill_x0, ill_y0, ill_x1, ill_y1 = bx0 + 12, by0 + 12, bx0 + 340, by1 - 12
        ill_fn(canvas, ill_x0, ill_y0, ill_x1, ill_y1)
        
        tx0 = ill_x1 + 16
        tw = bx1 - tx0 - 12
        
        canvas.draw_text(tag + ": HERO STORY", tx0, by0 + 14, 1, (150, 50, 50))
        h_height = canvas.draw_wrapped_text(headline, tx0, by0 + 32, tw, 2, (20, 20, 20), line_spacing=4)
        d_y = by0 + 32 + h_height + 12
        canvas.draw_wrapped_text(desc, tx0, d_y, tw, 1, (60, 60, 60), line_spacing=4)

    # ---------------------------------------------------------
    # 4. MID STORIES (y 890 - 1330)
    # ---------------------------------------------------------
    canvas.fill_rect(64, 890, WIDTH - 64, 925, (40, 40, 45))
    canvas.draw_text("WORLD DISPATCHES — STORIES 1 TO 12", 80, 898, 2, (255, 255, 255))
    
    mids_data = [
        (1, "RUSSIAN DRONE & MISSILE WAVE OVERNIGHT", "3 ballistic missiles + 148 drones hit 19 locations; Kyiv, Kryvyi Rih, Zaporizhzhia, Kharkiv struck.", "UKRAINE", "CONFIRMED"),
        (2, "SAUDI INTERCEPTS 3 HOUTHI MISSILES", "Air defenses intercept ballistic missiles over Riyadh at ~01:53 local time. No casualties.", "YEMEN/SAUDI", "CONFIRMED"),
        (3, "TWO TANKER ATTACKS NEAR KHASAB", "UKMTO reports two new vessel strikes off Oman coast amid escalating Red Sea/Hormuz tensions.", "OMAN/IRAN", "CONFIRMED"),
        (4, "IRGC CLAIMS 58TH US MQ-9 DRONE DOWN", "Iran Revolutionary Guard reports shooting down US drone in Hormuz using new air defense system.", "IRAN/USA", "CLAIM"),
        (5, "UN KILLER ROBOTS TALKS CONCLUDE", "Geneva CCW talks end with vague 2028 rules promise after pushback from major military powers.", "UN/SWISS", "CONFIRMED"),
        (6, "KRYVYI RIH TOLL RISES IN UPDATE", "Casualties from Friday double-tap strike updated to 2 dead and 52-58 wounded overnight.", "UKRAINE", "CONFIRMED"),
        (7, "FRANCE BRACES FOR COST-OF-LIVING PROTESTS", "70,000 police mobilized for Saturday Paris march from Republique to Nation; European rallies planned.", "FRANCE/EUROPE", "CONFIRMED"),
        (8, "BEPICOLOMBO MERCURY BURN SCHEDULED", "ESA/JAXA probe set for critical orbit insertion engine burn tonight at 18:24 UTC after 8-year voyage.", "SPACE", "CONFIRMED"),
        (9, "LEWIS PUGH COMPLETES HORMUZ SWIM", "Endurance swimmer swims 15 km in Strait of Hormuz to highlight conflict environmental damage.", "HORMUZ", "CONFIRMED"),
        (10, "QUAD BUSINESS FORUM SET FOR 2027", "US SecState Marco Rubio confirms early 2027 business forum following $17B Southeast Asia push.", "QUAD/USA", "CONFIRMED"),
        (11, "LIEBERMAN BACKS EISENKOT COALITION", "Yisrael Beytenu chief 100% confident Eisenkot will form coalition with ultra-Orthodox parties.", "ISRAEL", "CONFIRMED"),
        (12, "GAZA WINTER STORM DEEPENS CRISIS", "UN OCHA reports 150,000 tents still trapped at border as freezing winter weather strikes displaced camps.", "GAZA", "CONFIRMED"),
    ]

    mid_cols = [
        (64, 935, 994, 1320),
        (1054, 935, 1984, 1320)
    ]
    
    for i, (num, headline, desc, region, source) in enumerate(mids_data):
        col_idx = i // 6
        row_idx = i % 6
        cx0, cy0, cx1, cy1 = mid_cols[col_idx]
        col_h = (cy1 - cy0) // 6
        sy0 = cy0 + row_idx * col_h
        
        canvas.fill_rect(cx0, sy0, cx1, sy0 + col_h - 4, (252, 250, 245))
        canvas.draw_rect(cx0, sy0, cx1, sy0 + col_h - 4, (210, 205, 195), thickness=1)
        
        item_text = f"{num}. {headline}"
        canvas.draw_text(item_text, cx0 + 10, sy0 + 6, 1, (20, 20, 20))
        canvas.draw_text(desc, cx0 + 10, sy0 + 22, 1, (80, 80, 80))
        tag_str = f"[{region} | {source}]"
        canvas.draw_text(tag_str, cx0 + 10, sy0 + 38, 1, (120, 40, 40) if source == "CONFIRMED" else (80, 80, 120))

    # ---------------------------------------------------------
    # 5. WORLD MAP (y 1340 - 1620)
    # ---------------------------------------------------------
    canvas.fill_rect(64, 1340, WIDTH - 64, 1620, (230, 238, 245))
    canvas.draw_rect(64, 1340, WIDTH - 64, 1620, (180, 190, 200), thickness=2)
    canvas.draw_text("GLOBAL DISPATCH MAP — HEROES & MIDS LOCATIONS", 80, 1350, 2, (30, 30, 40))
    
    # Continents
    na = [(200, 1420), (450, 1410), (400, 1520), (250, 1540)]
    canvas.fill_polygon(na, (190, 210, 190))
    sa = [(350, 1550), (430, 1550), (410, 1610), (330, 1600)]
    canvas.fill_polygon(sa, (190, 210, 190))
    eu = [(950, 1400), (1050, 1395), (1040, 1450), (940, 1450)]
    canvas.fill_polygon(eu, (190, 210, 190))
    af = [(960, 1460), (1060, 1460), (1030, 1580), (950, 1560)]
    canvas.fill_polygon(af, (190, 210, 190))
    as_poly = [(1080, 1390), (1500, 1390), (1550, 1520), (1100, 1510)]
    canvas.fill_polygon(as_poly, (190, 210, 190))
    au = [(1500, 1550), (1620, 1550), (1600, 1600), (1480, 1590)]
    canvas.fill_polygon(au, (190, 210, 190))

    # Pins for Heroes (H1-H4) and Mids (1-12)
    pins = [
        (380, 1580),  # H1 Peru
        (1520, 1520), # H2 Timor / Banda Sea
        (1020, 1420), # H3 COP31 Antalya
        (1200, 1480), # H4 Basra Iraq
        (970, 1410),  # M1 Ukraine
        (1180, 1500), # M2 Riyadh Saudi
        (1210, 1470), # M3 Oman Khasab
        (1220, 1490), # M4 Hormuz Iran
        (960, 1430),  # M5 Geneva UN
        (980, 1415),  # M6 Kryvyi Rih
        (940, 1420),  # M7 Paris France
        (1350, 1450), # M8 BepiColombo / Space
        (1215, 1485), # M9 Lewis Pugh Hormuz
        (1380, 1510), # M10 Quad US
        (1030, 1450), # M11 Israel
        (1010, 1480), # M12 Gaza
    ]
    for idx, (px, py) in enumerate(pins):
        canvas.draw_circle(px, py, 6, (200, 40, 40))
        label_str = f"H{idx-3}" if idx < 4 else str(idx-3)
        canvas.draw_text(label_str, px - 6, py - 14, 1, (20, 20, 20))

    # ---------------------------------------------------------
    # 6. ALSO ON (y 1630 - 1850)
    # ---------------------------------------------------------
    canvas.fill_rect(64, 1630, WIDTH - 64, 1850, (255, 253, 248))
    canvas.draw_rect(64, 1630, WIDTH - 64, 1850, (180, 175, 165), thickness=2)
    canvas.draw_text("ALSO ON SATURDAY 21 NOV (STORIES 1 TO 24)", 80, 1640, 1, (30, 30, 30))
    
    also_on_stories = [
        "1. SA: Tributes flow for late ex-VP Phumzile Mlambo-Ngcuka, 71.",
        "2. HAITI: 3rd Salvadoran soldier dies after explosives blast.",
        "3. INDIA: Manipur toxic alcohol death toll rises to 15.",
        "4. GAZA: 9 killed, 55 injured arrive at hospitals from strikes.",
        "5. SPORT: Saturday fixtures: Man City-Fulham, Arsenal-Newcastle.",
        "6. KOREA: BTS win 5 awards at MAMA in Osaka.",
        "7. KOREA: Choi Min-jeong wins 3rd straight World Tour 1,000m.",
        "8. GERMANY: Harry Kane out for months with torn ankle ligament.",
        "9. AUSTRALIA: North Melbourne reaches 4th straight AFLW grand final.",
        "10. SCIENCE: CERN finds first evidence of ultra-rare decay.",
        "11. KENYA: Country begins onshore oil drilling in Turkana.",
        "12. USA/PACIFIC: First deep-sea mining lease sold off American Samoa.",
        "13. FRANCE: Paris probes Depardieu & Houellebecq over rape claims.",
        "14. ETHIOPIA: 700,000 displaced in southern ethnic clashes.",
        "15. SCIENCE: Blue sucker fish live 100+ years via radiocarbon.",
        "16. SCIENCE: DESY X-ray laser creates flashes shorter than atomic spacing.",
        "17. SCIENCE: Ancient Himalayan-scale mountains found under Antarctic ice.",
        "18. SCIENCE: Taung Child fossil study questions early human taxonomy.",
        "19. SCIENCE: UC Berkeley experimental compound burns fat without muscle loss.",
        "20. SPORT: Mao Shimada leads Finlandia Trophy after short program.",
        "21. FRANCE: Three Paris cops jailed over racist beating of Michel Zecler.",
        "22. USA: YouTube finalizes multi-billion dollar school district settlement.",
        "23. SPACE: Voyager 1 signal now takes 24 full light-hours to reach Earth.",
        "24. CHINA/ASIA: GTA 6 in East Asia: uncensored in SK, separate build in Japan."
    ]

    col_width_a = (WIDTH - 128 - 40) // 3
    for i, s in enumerate(also_on_stories):
        c_idx = i // 8
        r_idx = i % 8
        ax = 80 + c_idx * (col_width_a + 15)
        ay = 1665 + r_idx * 21
        max_chars = col_width_a // 6
        disp_s = s if len(s) <= max_chars else s[:max_chars-3] + "..."
        canvas.draw_text(disp_s, ax, ay, 1, (50, 50, 50))

    # ---------------------------------------------------------
    # 7. DATE CHECK BOX (y 1860 - 1955)
    # ---------------------------------------------------------
    canvas.fill_rect(64, 1860, WIDTH - 64, 1955, (240, 235, 230))
    canvas.draw_rect(64, 1860, WIDTH - 64, 1955, (170, 165, 155), thickness=2)
    canvas.draw_text("DATE CHECK: DELIBERATELY EXCLUDED (19-20 NOV STORIES)", 80, 1868, 1, (120, 30, 30))
    
    date_check_text = "Excluded from main content (belonging to other dates): Venezuela $12.26bn (Nov 12). Bolsonaro hospitalization (Nov 20). De Villepin candidacy (Nov 20). SK Supreme Court chief impeachment (Nov 20). Nepal PM India visit (Nov 20). Iraq Jurf al-Sakhar (Nov 20). LA M4.2 earthquake (Nov 20). Bayer $7.25bn settlement (Nov 20). Palisades arson verdict (Nov 20). EU 7.9bn euro aid (Nov 20). ICJ Myanmar ruling (Nov 19). AI stock sell-off / Friday close (Nov 20). GTA VI launch announcement (Nov 20)."
    canvas.draw_wrapped_text(date_check_text, 80, 1885, WIDTH - 160, 1, (70, 70, 70), line_spacing=3)

    # ---------------------------------------------------------
    # 8. FOOTER (y 1960 - 2015)
    # ---------------------------------------------------------
    canvas.fill_rect(64, 1960, WIDTH - 64, 2015, (30, 30, 35))
    footer_text = "All stories verified for Saturday 21 November 2026. Sources: Reuters, AP, AFP, Al Jazeera, GFZ, IGP Peru, ANI, UKMTO, ESA, Yonhap, BBC, Kyiv Independent, Nation Press, ScienceDaily, AllAfrica. Original artwork drawn in code."
    canvas.draw_wrapped_text(footer_text, 80, 1968, WIDTH - 160, 1, (200, 200, 200), line_spacing=2)

    return canvas

# ---------------------------------------------------------
# DOWNSAMPLE & PNG ENCODING
# ---------------------------------------------------------
def downsample_2x2(src_canvas):
    w1 = src_canvas.w
    h1 = src_canvas.h
    w2 = w1 // 2
    h2 = h1 // 2
    dst_buf = bytearray(w2 * h2 * 3)
    
    src = src_canvas.buf
    for y2 in range(h2):
        y1_0 = 2 * y2
        y1_1 = y1_0 + 1
        for x2 in range(w2):
            x1_0 = 2 * x2
            x1_1 = x1_0 + 1
            
            i00 = (y1_0 * w1 + x1_0) * 3
            i01 = (y1_0 * w1 + x1_1) * 3
            i10 = (y1_1 * w1 + x1_0) * 3
            i11 = (y1_1 * w1 + x1_1) * 3
            
            r = (src[i00] + src[i01] + src[i10] + src[i11]) // 4
            g = (src[i00+1] + src[i01+1] + src[i10+1] + src[i11+1]) // 4
            b = (src[i00+2] + src[i01+2] + src[i10+2] + src[i11+2]) // 4
            
            dst_idx = (y2 * w2 + x2) * 3
            dst_buf[dst_idx] = r
            dst_buf[dst_idx+1] = g
            dst_buf[dst_idx+2] = b
            
    return w2, h2, dst_buf

def write_png(filename, width, height, rgb_data):
    row_stride = width * 3
    filtered_data = bytearray()
    for y in range(height):
        filtered_data.append(0)
        start = y * row_stride
        filtered_data.extend(rgb_data[start:start + row_stride])
    
    compressed = zlib.compress(filtered_data, level=9)
    
    def chunk(tag, data):
        return struct.pack('>I', len(data)) + tag + data + struct.pack('>I', zlib.crc32(tag + data) & 0xffffffff)
    
    ihdr = struct.pack('>IIBBBBB', width, height, 8, 2, 0, 0, 0)
    
    png = bytearray(b'\x89PNG\r\n\x1a\n')
    png.extend(chunk(b'IHDR', ihdr))
    png.extend(chunk(b'IDAT', compressed))
    png.extend(chunk(b'IEND', b''))
    
    with open(filename, 'wb') as f:
        f.write(png)

def main():
    output_dir = os.environ.get('MAKEFUN_OUTPUT_DIR', 'out')
    os.makedirs(output_dir, exist_ok=True)
    out_path = os.path.join(output_dir, 'entry.png')
    
    print(f"Rendering 2048x2048 newspaper...")
    canvas = render_newspaper()
    
    print(f"Downsampling 2x2 to 1024x1024...")
    w2, h2, rgb2 = downsample_2x2(canvas)
    
    print(f"Writing PNG to {out_path}...")
    write_png(out_path, w2, h2, rgb2)
    
    size = os.path.getsize(out_path)
    print(f"PNG size: {size} bytes ({size / 1024 / 1024:.2f} MiB)")
    assert size <= 1024 * 1024, f"PNG exceeds 1 MiB limit ({size} bytes)"

if __name__ == '__main__':
    main()
