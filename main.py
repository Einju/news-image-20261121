#!/usr/bin/env python3
import os
import sys
import zlib
import struct
import math

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
    '\'': ["01100", "01100", "00100", "00000", "00000", "00000", "00000"],
    ';': ["00000", "01100", "01100", "00000", "01100", "01100", "00100"],
    '•': ["00000", "00000", "01110", "01110", "01110", "00000", "00000"],
    '~': ["00000", "00000", "00110", "11001", "00000", "00000", "00000"],
    '(': ["00010", "00100", "01000", "01000", "01000", "00100", "00010"],
    ')': ["01000", "00100", "00010", "00010", "00010", "00100", "01000"],
    '+': ["00000", "00100", "00100", "11111", "00100", "00100", "00000"],
    '/': ["00001", "00010", "00100", "01000", "10000", "00000", "00000"],
    '&': ["01100", "10010", "10100", "01000", "10101", "10010", "01101"],
    '!': ["00100", "00100", "00100", "00100", "00100", "00000", "00100"],
    '?': ["01110", "10001", "00001", "00110", "00100", "00000", "00100"],
    '#': ["01010", "11111", "01010", "01010", "11111", "01010", "00000"],
    '—': ["00000", "00000", "00000", "11111", "00000", "00000", "00000"],
    '[': ["01110", "01000", "01000", "01000", "01000", "01000", "01110"],
    ']': ["01110", "00010", "00010", "00010", "00010", "00010", "01110"],
    '|': ["00100", "00100", "00100", "00100", "00100", "00100", "00100"],
}

def draw_pixel(buf, width, height, x, y, r, g, b):
    if 0 <= x < width and 0 <= y < height:
        idx = (y * width + x) * 3
        buf[idx] = r
        buf[idx+1] = g
        buf[idx+2] = b

def draw_rect(buf, width, height, x, y, w, h, r, g, b, fill=True):
    if fill:
        for cy in range(max(0, y), min(height, y + h)):
            for cx in range(max(0, x), min(width, x + w)):
                idx = (cy * width + cx) * 3
                buf[idx] = r
                buf[idx+1] = g
                buf[idx+2] = b
    else:
        draw_line(buf, width, height, x, y, x + w - 1, y, r, g, b)
        draw_line(buf, width, height, x, y + h - 1, x + w - 1, y + h - 1, r, g, b)
        draw_line(buf, width, height, x, y, x, y + h - 1, r, g, b)
        draw_line(buf, width, height, x + w - 1, y, x + w - 1, y + h - 1, r, g, b)

def draw_line(buf, width, height, x0, y0, x1, y1, r, g, b):
    dx = abs(x1 - x0)
    dy = abs(y1 - y0)
    sx = 1 if x0 < x1 else -1
    sy = 1 if y0 < y1 else -1
    err = dx - dy
    while True:
        draw_pixel(buf, width, height, x0, y0, r, g, b)
        if x0 == x1 and y0 == y1:
            break
        e2 = 2 * err
        if e2 > -dy:
            err -= dy
            x0 += sx
        if e2 < dx:
            err += dx
            y0 += sy

def draw_circle(buf, width, height, cx, cy, radius, r, g, b, fill=True):
    for sy in range(cy - radius, cy + radius + 1):
        for sx in range(cx - radius, cx + radius + 1):
            if (sx - cx)**2 + (sy - cy)**2 <= radius**2:
                draw_pixel(buf, width, height, sx, sy, r, g, b)

def draw_char(buf, width, height, x, y, ch, scale, r, g, b):
    ch = ch.upper()
    glyph = FONT_5X7.get(ch, FONT_5X7.get('?'))
    for row_idx, row_str in enumerate(glyph):
        for col_idx, bit in enumerate(row_str):
            if bit == '1':
                for sy in range(scale):
                    for sx in range(scale):
                        draw_pixel(buf, width, height, x + col_idx * scale + sx, y + row_idx * scale + sy, r, g, b)
    return 6 * scale

def draw_text(buf, width, height, x, y, text, scale, r, g, b):
    curr_x = x
    for ch in text:
        draw_char(buf, width, height, curr_x, y, ch, scale, r, g, b)
        curr_x += 6 * scale
    return curr_x - x

def draw_wrapped_text(buf, width, height, x, y, max_w, text, scale, line_spacing, r, g, b):
    words = text.split(' ')
    lines = []
    current_line = []
    char_w = 6 * scale
    for word in words:
        test_line = ' '.join(current_line + [word])
        if len(test_line) * char_w <= max_w or not current_line:
            current_line.append(word)
        else:
            lines.append(' '.join(current_line))
            current_line = [word]
    if current_line:
        lines.append(' '.join(current_line))
    
    line_h = 7 * scale + line_spacing
    curr_y = y
    for line in lines:
        draw_text(buf, width, height, x, curr_y, line, scale, r, g, b)
        curr_y += line_h
    return curr_y - y

def write_png(filename, width, height, pixels):
    raw_data = bytearray()
    for y in range(height):
        raw_data.append(0)
        row = pixels[y * width * 3 : (y + 1) * width * 3]
        raw_data.extend(row)
    
    def chunk(tag, data):
        return struct.pack('>I', len(data)) + tag + data + struct.pack('>I', zlib.crc32(tag + data) & 0xFFFFFFFF)

    ihdr_data = struct.pack('>IIBBBBB', width, height, 8, 2, 0, 0, 0)
    idat_data = zlib.compress(bytes(raw_data), level=6)
    
    png = b'\x89PNG\r\n\x1a\n' + chunk(b'IHDR', ihdr_data) + chunk(b'IDAT', idat_data) + chunk(b'IEND', b'')
    out_dir = os.environ.get('MAKEFUN_OUTPUT_DIR', 'out')
    os.makedirs(out_dir, exist_ok=True)
    filepath = os.path.join(out_dir, 'entry.png')
    with open(filepath, 'wb') as f:
        f.write(png)

def downsample_2x2(buf_2048, w_2048, h_2048):
    w_1024 = w_2048 // 2
    h_1024 = h_2048 // 2
    buf_1024 = bytearray(w_1024 * h_1024 * 3)
    for y in range(h_1024):
        for x in range(w_1024):
            r_sum = g_sum = b_sum = 0
            for dy in (0, 1):
                for dx in (0, 1):
                    px = 2 * x + dx
                    py = 2 * y + dy
                    idx = (py * w_2048 + px) * 3
                    r_sum += buf_2048[idx]
                    g_sum += buf_2048[idx+1]
                    b_sum += buf_2048[idx+2]
            out_idx = (y * w_1024 + x) * 3
            buf_1024[out_idx] = r_sum // 4
            buf_1024[out_idx+1] = g_sum // 4
            buf_1024[out_idx+2] = b_sum // 4
    return buf_1024, w_1024, h_1024

def main():
    W = 2048
    H = 2048
    # Cream background #f2ede0 -> (242, 237, 224)
    buf = bytearray([242, 237, 224] * (W * H))

    # Colors
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    GOLD = (232, 200, 50)
    DARK_GRAY = (50, 50, 50)
    LIGHT_BLUE = (214, 228, 240)
    GREEN = (168, 200, 160)
    RED = (204, 34, 34)
    BORDER_GRAY = (120, 120, 120)

    # 1. MASTHEAD BAND (y 0-164)
    draw_rect(buf, W, H, 0, 0, 2048, 164, *BLACK)
    # "THE WORLD TODAY" scale 8 (height 56) -> y around 25
    title_w = len("THE WORLD TODAY") * 6 * 8
    draw_text(buf, W, H, (2048 - title_w) // 2, 20, "THE WORLD TODAY", 8, *WHITE)
    # "SATURDAY, 21 NOVEMBER 2026" scale 3 -> y around 88
    date_w = len("SATURDAY, 21 NOVEMBER 2026") * 6 * 3
    draw_text(buf, W, H, (2048 - date_w) // 2, 88, "SATURDAY, 21 NOVEMBER 2026", 3, *GOLD)
    # "40 STORIES - ANDES, TIMOR, ANTALYA, BASRA & GLOBAL" scale 2 -> y around 130
    sub_w = len("40 STORIES - ANDES, TIMOR, ANTALYA, BASRA & GLOBAL") * 6 * 2
    draw_text(buf, W, H, (2048 - sub_w) // 2, 130, "40 STORIES - ANDES, TIMOR, ANTALYA, BASRA & GLOBAL", 2, *WHITE)
    # Gold rule line under band
    draw_rect(buf, W, H, 0, 160, 2048, 4, *GOLD)

    # 2. TIMELINE STRIP (y 172-292) -> y 172 to 292
    draw_rect(buf, W, H, 34, 172, 1980, 120, *WHITE)
    draw_rect(buf, W, H, 34, 172, 1980, 120, *BORDER_GRAY, fill=False)
    draw_text(buf, W, H, 50, 184, "UTC TIMELINE (21 NOV 2026):", 2, *BLACK)
    
    col1_events = [
        "00:09 - PERU M6.8 QUAKE (JUNIN)",
        "01:30 - KYIV DRONES & MISSILES",
        "01:53 - RIYADH HOUTHI MISSILES",
        "03:00 - BASRA HARTHA FIRE"
    ]
    col2_events = [
        "04:00 - GENEVA KILLER ROBOTS",
        "09:30 - TIMOR M6.8 BANDA SEA",
        "14:00 - PARIS COST OF LIVING",
        "18:24 - BEPICOLOMBO MERCURY DUE"
    ]
    for i, ev in enumerate(col1_events):
        draw_text(buf, W, H, 50, 216 + i * 18, ev, 1, *DARK_GRAY)
    for i, ev in enumerate(col2_events):
        draw_text(buf, W, H, 1050, 216 + i * 18, ev, 1, *DARK_GRAY)

    # 3. HEROES 2x2 GRID (y 300 to 640 top row, y 650 to 990 bottom row)
    # Box dimensions: width 980, height 338 each
    hero_boxes = [
        # (x, y, illustration_func, title, body)
        (34, 300, 'h1', "M6.8 ANDES QUAKE STRIKES JUNIN", "M6.8 quake struck central Andes at 00:09 UTC Saturday. Felt in Lima, depth 129km. No casualties or tsunami threat reported initially."),
        (1034, 300, 'h2', "SECOND M6.8 QUAKE HITS BANDA SEA", "Second M6.8 earthquake of the day struck Banda Sea east of Timor-Leste at 09:30 UTC. Felt in Dili and Darwin. No immediate damage recorded."),
        (34, 650, 'h3', "COP31 ANTALYA TALKS STALEMATE", "Antalya climate summit passed Friday deadline without deal. Third draft awaited Saturday. 23 nations demand fossil transition text be restored."),
        (1034, 650, 'h4', "BASRA POWER PLANT BLAZE KILLS 4", "Fire at Hartha power plant north of Basra at ~03:00 GMT following gas pipe rupture. At least 4 killed, 30+ injured, plant operations halted.")
    ]

    for bx, by, htype, htitle, hbody in hero_boxes:
        # Outer box
        draw_rect(buf, W, H, bx, by, 980, 338, *WHITE)
        draw_rect(buf, W, H, bx, by, 980, 338, *BORDER_GRAY, fill=False)
        
        # Left illustration panel (width 440, height 322)
        ill_x = bx + 8
        ill_y = by + 8
        ill_w = 440
        ill_h = 322
        
        if htype == 'h1':
            # Peru M6.8 quake: sky blue, mountain triangles, red sun
            draw_rect(buf, W, H, ill_x, ill_y, ill_w, ill_h, *LIGHT_BLUE)
            # Mountains (gray triangles)
            # Big mountain
            for my_y in range(120):
                mw = my_y * 2
                draw_line(buf, W, H, ill_x + 220 - mw//2, ill_y + ill_h - 40 - my_y, ill_x + 220 + mw//2, ill_y + ill_h - 40 - my_y, 140, 140, 140)
            # Small mountain
            for my_y in range(80):
                mw = my_y * 2
                draw_line(buf, W, H, ill_x + 320 - mw//2, ill_y + ill_h - 40 - my_y, ill_x + 320 + mw//2, ill_y + ill_h - 40 - my_y, 110, 110, 110)
            # Sun circle
            draw_circle(buf, W, H, ill_x + 120, ill_y + 100, 40, *RED)
        elif htype == 'h2':
            # Banda Sea quake: blue-gray panel, two red zigzag seismograph lines
            draw_rect(buf, W, H, ill_x, ill_y, ill_w, ill_h, 190, 205, 220)
            # Zigzag lines
            for lx in range(40, ill_w - 40, 20):
                y1 = ill_y + 100 + (20 if (lx//20)%2==0 else -20)
                y2 = ill_y + 100 + (-20 if (lx//20)%2==0 else 20)
                draw_line(buf, W, H, ill_x + lx, y1, ill_x + lx + 20, y2, *RED)
            for lx in range(40, ill_w - 40, 20):
                y1 = ill_y + 220 + (-15 if (lx//20)%2==0 else 15)
                y2 = ill_y + 220 + (15 if (lx//20)%2==0 else -15)
                draw_line(buf, W, H, ill_x + lx, y1, ill_x + lx + 20, y2, *RED)
            # Dark bottom bar
            draw_rect(buf, W, H, ill_x, ill_y + ill_h - 20, ill_w, 20, 80, 80, 80)
        elif htype == 'h3':
            # COP31 no deal: beige panel, orange sun circle, red X over circle
            draw_rect(buf, W, H, ill_x, ill_y, ill_w, ill_h, 235, 225, 210)
            draw_circle(buf, W, H, ill_x + ill_w//2, ill_y + ill_h//2 - 10, 60, 230, 130, 40)
            # Red X
            cx, cy = ill_x + ill_w//2, ill_y + ill_h//2 - 10
            for offset in range(-3, 4):
                draw_line(buf, W, H, cx - 50 + offset, cy - 50, cx + 50 + offset, cy + 50, *RED)
                draw_line(buf, W, H, cx - 50 + offset, cy + 50, cx + 50 + offset, cy - 50, *RED)
            draw_rect(buf, W, H, ill_x, ill_y + ill_h - 20, ill_w, 20, 100, 90, 80)
        elif htype == 'h4':
            # Basra fire: light pinkish panel, two tall gray smokestacks with dark round tops, orange base
            draw_rect(buf, W, H, ill_x, ill_y, ill_w, ill_h, 245, 230, 230)
            # Smokestack 1
            draw_rect(buf, W, H, ill_x + 120, ill_y + 80, 50, 180, 130, 130, 130)
            draw_circle(buf, W, H, ill_x + 145, ill_y + 80, 30, 80, 80, 80)
            # Smokestack 2
            draw_rect(buf, W, H, ill_x + 270, ill_y + 110, 50, 150, 130, 130, 130)
            draw_circle(buf, W, H, ill_x + 295, ill_y + 110, 30, 80, 80, 80)
            # Orange base platform
            draw_rect(buf, W, H, ill_x + 60, ill_y + 260, 320, 30, 220, 120, 40)

        # Right text side (x = bx + 460 to bx + 970)
        txt_x = bx + 464
        txt_y = by + 16
        txt_w = 504
        
        draw_text(buf, W, H, txt_x, txt_y, "HERO STORY", 1, *RED)
        # Headline in 2 lines (scale 2)
        words = htitle.split(' ')
        mid_idx = len(words) // 2
        line1 = ' '.join(words[:mid_idx])
        line2 = ' '.join(words[mid_idx:])
        draw_text(buf, W, H, txt_x, txt_y + 20, line1, 2, *BLACK)
        draw_text(buf, W, H, txt_x, txt_y + 44, line2, 2, *BLACK)
        
        # Body text (scale 1)
        draw_wrapped_text(buf, W, H, txt_x, txt_y + 80, txt_w, hbody, 1, 6, *DARK_GRAY)

    # 4. MIDS (y 1004 to 1454)
    draw_rect(buf, W, H, 34, 1004, 1980, 48, *BLACK)
    draw_text(buf, W, H, 50, 1018, "WORLD DISPATCHES - STORIES 1 TO 12", 2, *WHITE)
    
    # 2 columns x 6 rows grid
    mids_data = [
        ("1. [UKRAINE] OVERNIGHT BARRAGE: 3 BALLISTIC + 148 DRONES", "117 shot down across 19 locations; Kyiv, Kryvyi Rih hit. CONFIRMED"),
        ("2. [YEMEN/SAUDI] SAUDI COALITION INTERCEPTS 3 MISSILES", "Ballistic missiles intercepted over Riyadh; 2nd attack in 3 days. CONFIRMED"),
        ("3. [OMAN/IRAN] TWO NEW TANKER INCIDENTS NEAR KHASAB", "UKMTO reports hits to stern and engine room north of Khasab. CONFIRMED"),
        ("4. [IRAN/USA] IRGC CLAIMS DOWNING 58TH US MQ-9 DRONE", "Strait of Hormuz incident claimed using new air defense; US silent. CLAIM"),
        ("5. [UN/SWISS] KILLER ROBOTS TALKS END IN GENEVA", "CCW talks pledge new rules by 2028 after resistance from major powers. CONFIRMED"),
        ("6. [UKRAINE] KRYVYI RIH CASUALTIES RISE TO 58 INJURED", "Two killed, injuries revised following 20 Nov evening double-tap. CONFIRMED"),
        ("7. [FRANCE] COST OF LIVING PROTESTS ACROSS EUROPE", "Paris march République to Nation; 70k police deployed across France. CONFIRMED"),
        ("8. [SPACE] BEPICOLOMBO MERCURY INSERTION BURN", "ESA/JAXA probe scheduled engine ignition tonight 18:24 UTC. CONFIRMED"),
        ("9. [HORMUZ] SWIMMER LEWIS PUGH COMPLETES 15 KM SWIM", "Strait of Hormuz swim highlights wartime environmental damage. CONFIRMED"),
        ("10. [QUAD] US SECSTATE CONFIRMS QUAD BUSINESS FORUM", "Early 2027 forum announced; $17B in SE Asia deals highlighted. CONFIRMED"),
        ("11. [ISRAEL] LIEBERMAN CONFIDENT EISENKOT COALITION", "100 percent certainty expressed over upcoming government formation. CONFIRMED"),
        ("12. [GAZA] WINTER STORM DEEPENS SHELTER CRISIS", "150k tents remain held at border crossings amid severe cold. CONFIRMED")
    ]

    cell_w = 980
    cell_h = 63
    start_mx = 34
    start_my = 1056

    for i, (mtitle, mdesc) in enumerate(mids_data):
        col = i // 6
        row = i % 6
        cx = start_mx + col * 1000
        cy = start_my + row * cell_h
        
        # Cell background & border
        draw_rect(buf, W, H, cx, cy, cell_w, cell_h, *WHITE)
        draw_rect(buf, W, H, cx, cy, cell_w, cell_h, *BORDER_GRAY, fill=False)
        
        draw_text(buf, W, H, cx + 12, cy + 10, mtitle, 1, *BLACK)
        draw_text(buf, W, H, cx + 12, cy + 32, mdesc, 1, *DARK_GRAY)

    # 5. MAP (y 1462 to 1708)
    draw_rect(buf, W, H, 34, 1462, 1980, 40, LIGHT_BLUE[0], LIGHT_BLUE[1], LIGHT_BLUE[2])
    draw_text(buf, W, H, 50, 1474, "GLOBAL DISPATCH MAP - HEROES & MIDS LOCATIONS", 2, *BLACK)
    
    # Map container
    map_x = 34
    map_y = 1502
    map_w = 1980
    map_h = 206
    draw_rect(buf, W, H, map_x, map_y, map_w, map_h, *LIGHT_BLUE)
    draw_rect(buf, W, H, map_x, map_y, map_w, map_h, *BORDER_GRAY, fill=False)
    
    # Simplified green continent blobs (#a8c8a0)
    # Americas blob
    draw_circle(buf, W, H, map_x + 350, map_y + 110, 50, *GREEN)
    draw_circle(buf, W, H, map_x + 420, map_y + 150, 40, *GREEN)
    # Europe / Africa blob
    draw_circle(buf, W, H, map_x + 950, map_y + 80, 45, *GREEN)
    draw_circle(buf, W, H, map_x + 980, map_y + 140, 55, *GREEN)
    # Asia blob
    draw_circle(buf, W, H, map_x + 1300, map_y + 75, 70, *GREEN)
    draw_circle(buf, W, H, map_x + 1450, map_y + 100, 50, *GREEN)
    # Australia blob
    draw_circle(buf, W, H, map_x + 1750, map_y + 160, 40, *GREEN)

    # Red numbered pins for 4 heroes + 12 mids (1 to 16)
    pins = [
        (400, 160, "1"),   # Peru (H1)
        (1750, 170, "2"),  # Timor / Banda Sea (H2)
        (960, 75, "3"),    # Antalya (H3)
        (1100, 110, "4"),  # Basra (H4)
        (980, 60, "5"),    # Kyiv (M1)
        (1150, 120, "6"),  # Riyadh (M2)
        (1120, 135, "7"),  # Oman / Khasab (M3)
        (1200, 125, "8"),  # Hormuz (M4)
        (910, 70, "9"),    # Geneva (M5)
        (990, 65, "10"),   # Kryvyi Rih (M6)
        (930, 75, "11"),   # Paris (M7)
        (1400, 50, "12"),  # Space / Bepi (M8)
        (1130, 130, "13"), # Hormuz Pugh (M9)
        (1500, 110, "14"), # Quad Asia (M10)
        (1080, 105, "15"), # Israel (M11)
        (1090, 115, "16"), # Gaza (M12)
    ]
    for px, py, pnum in pins:
        draw_circle(buf, W, H, map_x + px, map_y + py, 14, *RED)
        # White number offset
        num_x = map_x + px - (4 if len(pnum)==1 else 8)
        num_y = map_y + py - 7
        draw_text(buf, W, H, num_x, num_y, pnum, 1, *WHITE)

    # 6. ALSO ON (y 1716 to 1942)
    draw_rect(buf, W, H, 34, 1716, 1980, 40, *WHITE)
    draw_text(buf, W, H, 50, 1728, "ALSO ON SATURDAY 21 NOV (STORIES 13 TO 36)", 2, *BLACK)
    
    also_on_box_x = 34
    also_on_box_y = 1758
    also_on_box_w = 1980
    also_on_box_h = 184
    draw_rect(buf, W, H, also_on_box_x, also_on_box_y, also_on_box_w, also_on_box_h, *WHITE)
    draw_rect(buf, W, H, also_on_box_x, also_on_box_y, also_on_box_w, also_on_box_h, *BORDER_GRAY, fill=False)

    also_stories = [
        "13. [SOUTH AFRICA] Tributes flow for late ex-VP Phumzile Mlambo-Ngcuka",
        "14. [HAITI] 3rd Salvadoran soldier killed after blast handling explosives",
        "15. [INDIA] Manipur spurious alcohol death toll rises to 15",
        "16. [GAZA] Israeli strikes kill 9; settler attacks on olive farmers continue",
        "17. [SPORT] Saturday football fixtures: Man City, Newcastle-Arsenal, Real Madrid",
        "18. [KOREA] BTS wins 5 awards at MAMA in Osaka",
        "19. [KOREA] Choi Min-jeong wins 3rd straight World Tour 1000m in Seoul",
        "20. [GERMANY] Harry Kane out for months with torn ankle ligament",
        "21. [AUSTRALIA] North Melbourne reaches 4th straight AFLW grand final",
        "22. [SCIENCE] CERN finds first evidence of ultra-rare particle decay",
        "23. [KENYA] Kenya begins onshore oil drilling in Turkana South Lokichar",
        "24. [USA] US sells first deep-sea mining lease off American Samoa",
        "25. [FRANCE] Paris probes Depardieu and Houellebecq over assault claims",
        "26. [ETHIOPIA] 700k displaced in southern Ethiopia from ethnic clashes",
        "27. [SCIENCE] Blue sucker fish lives 100+ years via radiocarbon dating",
        "28. [SCIENCE] DESY XFEL laser flashes shorter than atomic spacing",
        "29. [SCIENCE] Ancient Himalayan-scale mountains found under Antarctic ice",
        "30. [SCIENCE] Taung Child fossil study questions human ancestor grouping",
        "31. [SCIENCE] UC Berkeley experimental compound aids fat burning",
        "32. [SPORT] Mao Shimada leads Finland Trophy after short program",
        "33. [FRANCE] Three Paris police jailed over racist beating of Michel Zecler",
        "34. [USA] YouTube finalizes multi-billion dollar school district settlement",
        "35. [SPACE] Voyager 1 signal now takes full 24 light-hours to reach Earth",
        "36. [CHINA/ASIA] GTA VI: uncensored in Korea, separate build in Japan"
    ]

    col_w = 640
    row_h = 21
    for i, story in enumerate(also_stories):
        col = i // 8
        row = i % 8
        ax = also_on_box_x + 16 + col * col_w
        ay = also_on_box_y + 12 + row * row_h
        draw_text(buf, W, H, ax, ay, story, 1, *DARK_GRAY)

    # 7. DATE CHECK (y 1950 to 2010)
    draw_rect(buf, W, H, 34, 1950, 1980, 50, *WHITE)
    draw_rect(buf, W, H, 34, 1950, 1980, 50, *BORDER_GRAY, fill=False)
    draw_text(buf, W, H, 50, 1958, "DATE CHECK: DELIBERATELY EXCLUDED (NOT 21 NOV):", 1, *RED)
    excluded_text = "Ukraine 400+ drone attack (20 Nov), ICJ Myanmar verdict (19 Nov), AI stock sell-off (20 Nov), GTA VI $3.79B opening (20 Nov), Riemann hypothesis claim (20 Nov), Bayer $7.25B verdict (20 Nov), LA M4.2 quake (20 Nov), EU €7.9B Ukraine aid (20 Nov)."
    draw_wrapped_text(buf, W, H, 50, 1976, 1940, excluded_text, 1, 4, *DARK_GRAY)

    # 8. FOOTER (y 2016 to 2048)
    draw_rect(buf, W, H, 0, 2016, 2048, 32, *BLACK)
    footer_text = "ALL STORIES VERIFIED FOR SATURDAY 21 NOVEMBER 2026. SOURCES: REUTERS, AP, AFP, AL JAZEERA, GFZ, IGP PERU, ANI, UKMTO, ESA, YONHAP, BBC, KYIV INDEPENDENT, NATION PRESS, SCIENCEDAILY, ALLAFRICA."
    draw_text(buf, W, H, 20, 2026, footer_text, 1, *WHITE)

    # Downsample 2x2 to 1024x1024
    print("Downsampling from 2048x2048 to 1024x1024...", file=sys.stderr)
    buf_1024, w_1024, h_1024 = downsample_2x2(buf, W, H)

    # Write PNG
    print("Writing PNG to output...", file=sys.stderr)
    write_png('entry.png', w_1024, h_1024, buf_1024)
    print("Done!", file=sys.stderr)

if __name__ == '__main__':
    main()
