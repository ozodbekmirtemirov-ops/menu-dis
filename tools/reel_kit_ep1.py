"""Reel #1: Как Озодбек жил без My Week. 1080x1920, 30fps."""
import math, os, subprocess, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H, FPS = 1080, 1920, 30
OUT = sys.argv[1] if len(sys.argv) > 1 else "reel1.mp4"
TMP = "scenes"; os.makedirs(TMP, exist_ok=True)
FD = "/usr/share/fonts/opentype/inter/"
def F(w, s): return ImageFont.truetype(FD + f"Inter-{w}.otf", s)

# ---------- helpers ----------
def ease(t): t = max(0, min(1, t)); return 1 - (1 - t) ** 3
def pop(t):  # overshoot pop-in 0..1
    t = max(0, min(1, t)); c = 1.70158
    return 1 + (c + 1) * (t - 1) ** 3 + c * (t - 1) ** 2

def vgrad(top, bot):
    a = np.linspace(0, 1, H)[:, None]
    arr = (np.array(top)[None, None] * (1 - a[..., None]) + np.array(bot)[None, None] * a[..., None])
    return Image.fromarray(np.repeat(arr, W, 1).astype(np.uint8), "RGB")

def radial(base, glow, cy=0.45, r=900):
    y, x = np.mgrid[0:H, 0:W]
    d = np.sqrt((x - W / 2) ** 2 + (y - H * cy) ** 2) / r
    k = np.clip(1 - d, 0, 1)[..., None] ** 2
    arr = np.array(base) * (1 - k) + np.array(glow) * k
    return Image.fromarray(arr.astype(np.uint8), "RGB")

def text_size(d, s, f):
    b = d.textbbox((0, 0), s, font=f); return b[2] - b[0], b[3] - b[1], b[1]

def pill(lines, font, fg, bg, pad=(44, 26), radius=34, colors=None):
    """Render a rounded caption box to RGBA."""
    tmp = ImageDraw.Draw(Image.new("RGB", (10, 10)))
    sizes = [text_size(tmp, l, font) for l in lines]
    lh = int(font.size * 1.28)
    w = max(s[0] for s in sizes) + pad[0] * 2
    h = lh * len(lines) + pad[1] * 2 - (lh - font.size) + 6
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, w - 1, h - 1], radius, fill=bg)
    for i, l in enumerate(lines):
        tw, th, oy = sizes[i]
        d.text(((w - tw) / 2, pad[1] + i * lh - oy + 4), l, font=font,
               fill=(colors[i] if colors else fg))
    return im

def paste_c(canvas, im, cx, cy, scale=1.0, alpha=1.0):
    if scale <= 0.01 or alpha <= 0.01: return
    if abs(scale - 1) > 0.005:
        im = im.resize((max(1, int(im.width * scale)), max(1, int(im.height * scale))), Image.LANCZOS)
    if alpha < 1:
        a = im.getchannel("A").point(lambda v: int(v * alpha)); im = im.copy(); im.putalpha(a)
    canvas.alpha_composite(im, (int(cx - im.width / 2), int(cy - im.height / 2)))

# ---------- character: Озодбек, curly 14yo, hoodie ----------
SS = 2
SKIN, SKIN_D = (236, 188, 150), (214, 160, 122)
HAIR, HAIR_L = (52, 34, 26), (78, 52, 38)
HOOD, HOOD_D = (64, 120, 255), (44, 92, 214)

def character(mood="neutral", arms="down"):
    cw, ch = 560 * SS, 900 * SS
    im = Image.new("RGBA", (cw, ch), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    s = SS; cx = cw // 2
    # body / hoodie
    d.rounded_rectangle([cx - 170 * s, 470 * s, cx + 170 * s, 900 * s], 90 * s, fill=HOOD)
    d.polygon([(cx - 60 * s, 470 * s), (cx + 60 * s, 470 * s), (cx, 560 * s)], fill=HOOD_D)
    d.line([(cx - 30 * s, 520 * s), (cx - 34 * s, 640 * s)], fill=(255, 255, 255), width=8 * s)
    d.line([(cx + 30 * s, 520 * s), (cx + 34 * s, 640 * s)], fill=(255, 255, 255), width=8 * s)
    d.rounded_rectangle([cx - 90 * s, 700 * s, cx + 90 * s, 790 * s], 30 * s, fill=HOOD_D)
    # arms
    if arms == "up":
        for sg in (-1, 1):
            d.line([(cx + sg * 150 * s, 520 * s), (cx + sg * 250 * s, 330 * s)], fill=HOOD, width=70 * s)
            d.ellipse([cx + sg * 250 * s - 40 * s, 290 * s, cx + sg * 250 * s + 40 * s, 370 * s], fill=SKIN)
    elif arms == "phone":
        d.line([(cx - 150 * s, 520 * s), (cx - 200 * s, 760 * s)], fill=HOOD, width=70 * s)
        d.line([(cx + 150 * s, 520 * s), (cx + 60 * s, 640 * s)], fill=HOOD, width=70 * s)
        d.rounded_rectangle([cx + 10 * s, 540 * s, cx + 110 * s, 720 * s], 18 * s, fill=(20, 20, 24))
        d.rounded_rectangle([cx + 20 * s, 552 * s, cx + 100 * s, 708 * s], 12 * s, fill=(120, 190, 255))
        d.ellipse([cx + 30 * s, 620 * s, cx + 100 * s, 690 * s], fill=SKIN)
    else:
        for sg in (-1, 1):
            d.line([(cx + sg * 155 * s, 520 * s), (cx + sg * 200 * s, 770 * s)], fill=HOOD, width=70 * s)
            d.ellipse([cx + sg * 200 * s - 38 * s, 750 * s, cx + sg * 200 * s + 38 * s, 826 * s], fill=SKIN)
    # neck + head
    d.rectangle([cx - 45 * s, 400 * s, cx + 45 * s, 480 * s], fill=SKIN_D)
    hx0, hy0, hx1, hy1 = cx - 135 * s, 150 * s, cx + 135 * s, 450 * s
    d.ellipse([hx0 - 18 * s, 270 * s, hx0 + 22 * s, 330 * s], fill=SKIN)
    d.ellipse([hx1 - 22 * s, 270 * s, hx1 + 18 * s, 330 * s], fill=SKIN)
    d.ellipse([hx0, hy0, hx1, hy1], fill=SKIN)
    # curly hair: ring of circles on top
    rng = np.random.default_rng(7)
    for i in range(46):
        a = math.pi * (1.05 + 0.9 * i / 45)
        r = 150 * s + rng.uniform(-10, 14) * s
        x = cx + math.cos(a) * r * 1.02; y = 270 * s + math.sin(a) * r * 0.95
        rr = rng.uniform(34, 48) * s
        d.ellipse([x - rr, y - rr, x + rr, y + rr], fill=HAIR)
    for i in range(26):
        x = cx + rng.uniform(-120, 120) * s; y = rng.uniform(150, 215) * s
        rr = rng.uniform(30, 42) * s
        d.ellipse([x - rr, y - rr, x + rr, y + rr], fill=HAIR)
    for i in range(30):  # curl highlights
        x = cx + rng.uniform(-150, 150) * s; y = rng.uniform(110, 230) * s
        rr = rng.uniform(10, 16) * s
        d.arc([x - rr, y - rr, x + rr, y + rr], 200, 340, fill=HAIR_L, width=5 * s)
    # face
    ey = 305 * s
    if mood == "sleepy":
        for sg in (-1, 1):
            d.arc([cx + sg * 55 * s - 24 * s, ey - 10 * s, cx + sg * 55 * s + 24 * s, ey + 18 * s], 0, 180, fill=(40, 30, 30), width=7 * s)
    else:
        er = 20 * s if mood == "shock" else 16 * s
        for sg in (-1, 1):
            ex = cx + sg * 55 * s
            d.ellipse([ex - er - 6 * s, ey - er - 6 * s, ex + er + 6 * s, ey + er + 6 * s], fill=(255, 255, 255))
            d.ellipse([ex - er + 4 * s, ey - er + 4 * s, ex + er - 4 * s, ey + er - 4 * s], fill=(40, 30, 30))
            d.ellipse([ex + 2 * s, ey - 10 * s, ex + 10 * s, ey - 2 * s], fill=(255, 255, 255))
    # brows
    for sg in (-1, 1):
        bx = cx + sg * 55 * s
        if mood in ("sad", "shock"):
            d.line([(bx - 26 * s, ey - 40 * s + (-sg * 10 if mood == "sad" else 0) * s), (bx + 26 * s, ey - 40 * s - (-sg * 10 if mood == "sad" else 0) * s)], fill=HAIR, width=9 * s)
        else:
            d.line([(bx - 26 * s, ey - 42 * s), (bx + 26 * s, ey - 46 * s)], fill=HAIR, width=9 * s)
    d.ellipse([cx - 10 * s, 335 * s, cx + 10 * s, 355 * s], fill=SKIN_D)
    my = 385 * s
    if mood == "happy":
        d.chord([cx - 55 * s, my - 40 * s, cx + 55 * s, my + 30 * s], 0, 180, fill=(120, 40, 40))
        d.chord([cx - 40 * s, my - 30 * s, cx + 40 * s, my + 0 * s], 0, 180, fill=(255, 255, 255))
        for sg in (-1, 1):
            d.ellipse([cx + sg * 95 * s - 22 * s, 340 * s, cx + sg * 95 * s + 22 * s, 370 * s], fill=(244, 150, 140))
    elif mood == "sad":
        d.arc([cx - 40 * s, my - 6 * s, cx + 40 * s, my + 40 * s], 200, 340, fill=(90, 40, 40), width=8 * s)
    elif mood == "shock":
        d.ellipse([cx - 22 * s, my - 22 * s, cx + 22 * s, my + 26 * s], fill=(90, 30, 30))
    elif mood == "sleepy":
        d.arc([cx - 30 * s, my - 20 * s, cx + 30 * s, my + 10 * s], 20, 160, fill=(90, 40, 40), width=7 * s)
    else:
        d.arc([cx - 40 * s, my - 30 * s, cx + 40 * s, my + 16 * s], 20, 160, fill=(90, 40, 40), width=8 * s)
    return im.resize((cw // SS, ch // SS), Image.LANCZOS)

CHAR = {m: character(m) for m in ("neutral", "sad", "shock", "happy", "sleepy")}
CHAR_UP_HAPPY = character("happy", "up")
CHAR_PHONE = character("shock", "phone")
CHAR_PHONE_HAPPY = character("happy", "phone")

# ---------- props ----------
def sticky(text, color, rot):
    im = Image.new("RGBA", (230, 230), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rectangle([10, 10, 220, 220], fill=color)
    f = F("SemiBold", 30); y = 50
    for line in text.split("\n"):
        tw, th, oy = text_size(d, line, f); d.text(((230 - tw) / 2, y - oy), line, font=f, fill=(40, 40, 40)); y += 44
    return im.rotate(rot, resample=Image.BICUBIC, expand=True)

def alarm_clock(t_str):
    im = Image.new("RGBA", (360, 360), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    for sg in (-1, 1):
        d.ellipse([180 + sg * 110 - 50, 10, 180 + sg * 110 + 50, 90], fill=(230, 60, 60))
    d.ellipse([30, 50, 330, 350], fill=(240, 70, 70)); d.ellipse([60, 80, 300, 320], fill=(255, 255, 255))
    f = F("Bold", 74); tw, th, oy = text_size(d, t_str, f)
    d.text((180 - tw / 2, 200 - th / 2 - oy), t_str, font=f, fill=(230, 50, 50))
    return im

def qmark(col=(255, 70, 70)):
    im = Image.new("RGBA", (150, 150), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.ellipse([5, 5, 145, 145], fill=col); f = F("Black", 100)
    tw, th, oy = text_size(d, "?", f); d.text((75 - tw / 2, 75 - th / 2 - oy), "?", font=f, fill=(255, 255, 255))
    return im

# ---------- phone UI (My Week) ----------
DAYS = ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"]
TASKS = [("Утро", "Подъём в 7:00", (255, 190, 60)), ("Обед", "Школа + домашка", (90, 200, 120)),
         ("Вечер", "Футбол с друзьями", (140, 110, 255)), ("Вечер", "Код: 30 минут", (60, 150, 255))]

def phone(progress, checks):
    pw, ph = 640, 1260
    im = Image.new("RGBA", (pw, ph), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, pw - 1, ph - 1], 90, fill=(18, 18, 22))
    d.rounded_rectangle([18, 18, pw - 19, ph - 19], 74, fill=(248, 248, 250))
    d.rounded_rectangle([pw / 2 - 90, 40, pw / 2 + 90, 82], 21, fill=(18, 18, 22))
    d.text((56, 120), "MY WEEK", font=F("Black", 44), fill=(20, 20, 24))
    d.text((56, 178), "Неделя Озодбека", font=F("Medium", 28), fill=(140, 140, 150))
    # days row
    for i, dy in enumerate(DAYS):
        x = 56 + i * 76; act = i == 0
        d.rounded_rectangle([x, 240, x + 64, 330], 22, fill=(20, 20, 24) if act else (234, 234, 240))
        f = F("SemiBold", 26); tw, th, oy = text_size(d, dy, f)
        d.text((x + 32 - tw / 2, 270 - oy), dy, font=f, fill=(255, 255, 255) if act else (90, 90, 100))
    y = 370
    for i, (sec, task, col) in enumerate(TASKS):
        a = ease(progress * len(TASKS) - i)
        if a <= 0: break
        off = int((1 - a) * 60)
        card = Image.new("RGBA", (pw - 112, 170), (0, 0, 0, 0)); cd = ImageDraw.Draw(card)
        cd.rounded_rectangle([0, 0, card.width - 1, 169], 30, fill=(255, 255, 255), outline=(232, 232, 238), width=2)
        cd.rounded_rectangle([24, 30, 34, 140], 5, fill=col)
        cd.text((58, 34), sec, font=F("SemiBold", 26), fill=(150, 150, 160))
        cd.text((58, 80), task, font=F("Bold", 34), fill=(20, 20, 24))
        done = checks > i
        bx = card.width - 90
        cd.ellipse([bx, 55, bx + 60, 115], fill=(52, 199, 89) if done else None, outline=(52, 199, 89) if done else (200, 200, 210), width=5)
        if done: cd.line([(bx + 15, 86), (bx + 27, 99), (bx + 47, 72)], fill=(255, 255, 255), width=7)
        if a < 1:
            al = card.getchannel("A").point(lambda v: int(v * a)); card.putalpha(al)
        im.alpha_composite(card, (56, y + off)); y += 182
    # stats bar
    if checks >= 4:
        d.rounded_rectangle([56, 1170 - 60, pw - 56, 1170], 26, fill=(20, 20, 24))
        f = F("Bold", 28); s = "Выполнено 4 из 4"
        tw, th, oy = text_size(d, s, f); d.text((pw / 2 - tw / 2, 1140 - th / 2 - oy), s, font=f, fill=(255, 255, 255))
    return im

def app_icon(size=300):
    im = Image.new("RGBA", (size, size), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, size - 1, size - 1], int(size * 0.23), fill=(30, 30, 36))
    g = size * 0.14; cw = (size - 2 * g) / 7
    for i in range(7):
        x = g + i * cw; hh = size * (0.28 + 0.06 * ((i * 3) % 5))
        col = (60, 150, 255) if i != 4 else (52, 199, 89)
        d.rounded_rectangle([x + 4, size - g - hh, x + cw - 4, size - g], 8, fill=col)
    d.text((g, g * 0.6), "7", font=F("Black", int(size * 0.3)), fill=(255, 255, 255))
    return im

# ---------- scenes ----------
CAP = F("Bold", 54); CAP_S = F("SemiBold", 42)
def caption(canvas, lines, t, y=1520, colors=None, delay=0.15, font=None):
    p = pill(lines, font or CAP, (20, 20, 24), (255, 255, 255, 245), colors=colors)
    k = pop((t - delay) / 0.35)
    paste_c(canvas, p, W / 2, y, scale=0.6 + 0.4 * k if k > 0 else 0, alpha=min(1, max(0, (t - delay) / 0.2)))

BG_ROOM = vgrad((206, 222, 245), (238, 242, 250))
def room_bg():
    im = BG_ROOM.copy(); d = ImageDraw.Draw(im)
    d.rectangle([140, 260, 940, 900], fill=(255, 255, 255)); d.rectangle([160, 280, 920, 880], fill=(150, 190, 240))
    for i, (x, h) in enumerate([(190, 380), (300, 520), (420, 300), (520, 460), (640, 360), (760, 540), (850, 320)]):
        d.rectangle([x, 880 - h, x + 90, 880], fill=(120, 160, 220) if i % 2 else (100, 140, 205))
    d.rectangle([530, 280, 550, 880], fill=(255, 255, 255))
    d.rectangle([0, 1330, W, H], fill=(110, 78, 60)); d.rectangle([0, 1330, W, 1350], fill=(90, 62, 48))
    return im.convert("RGBA")
ROOM = room_bg()
DARK = radial((10, 10, 14), (24, 40, 90)).convert("RGBA")
GREEN = radial((8, 12, 10), (20, 90, 50)).convert("RGBA")

def s_hook(t, T):
    c = DARK.copy()
    a = pop(t / 0.4)
    paste_c(c, pill(["Озодбек, 14 лет."], F("Black", 76), (255, 255, 255), (0, 0, 0, 0)), W / 2, 760, 0.7 + 0.3 * a, min(1, t / 0.25))
    paste_c(c, pill(["Неделя без плана"], F("Bold", 60), (20, 20, 24), (255, 255, 255, 255)), W / 2, 900, pop((t - 0.6) / 0.35) if t > 0.6 else 0)
    bob = math.sin(t * 6) * 8
    paste_c(c, CHAR["neutral"], W / 2, 1420 + bob, 0.95, ease((t - 0.3) / 0.4))
    return c

def s_monday(t, T):
    c = ROOM.copy()
    d = ImageDraw.Draw(c); d.rounded_rectangle([90, 1180, 990, 1420], 40, fill=(250, 250, 252)); d.rounded_rectangle([70, 1120, 300, 1300], 40, fill=(255, 255, 255))
    blanket = Image.new("RGBA", (W, H), (0, 0, 0, 0)); bd = ImageDraw.Draw(blanket)
    paste_c(c, CHAR["sleepy"] if t < 1.4 else CHAR["shock"], 300 if t < 1.4 else W / 2, 1120 if t < 1.4 else 1150 - 40 * ease((t - 1.4) / 0.3), 0.75)
    bd.rounded_rectangle([150, 1250, 1000, 1500], 60, fill=(255, 150, 120)); c.alpha_composite(blanket)
    shake = math.sin(t * 60) * 10 if 0.4 < t < 1.6 else 0
    paste_c(c, alarm_clock("08:47"), 820 + shake, 560, 0.9, ease(t / 0.3))
    caption(c, ["Понедельник.", "Опять проспал."], t, y=1660, delay=0.3)
    return c

def s_school(t, T):
    c = ROOM.copy()
    paste_c(c, CHAR["sad"], W / 2, 1160 + math.sin(t * 4) * 6, 0.85)
    for i, (x, y) in enumerate([(240, 520), (840, 470), (540, 360), (200, 820), (880, 800)]):
        k = pop((t - 0.2 - i * 0.15) / 0.3)
        paste_c(c, qmark(), x, y + math.sin(t * 5 + i) * 10, 0.8 * k if t > 0.2 + i * 0.15 else 0)
    caption(c, ["Домашка? Какая домашка?"], t, y=1650, delay=0.5)
    return c

NOTES = [("Сдать\nпроект", (255, 230, 110), 8), ("Купить\nтетради", (255, 180, 200), -10), ("Позвонить\nбабушке", (170, 230, 255), 6),
         ("Повторить\nформулы", (190, 255, 170), -6), ("Тренировка", (255, 210, 150), 12), ("Убрать\nкомнату", (230, 200, 255), -12)]
NOTE_IM = [sticky(*n) for n in NOTES]
NOTE_POS = [(220, 430), (850, 400), (540, 560), (180, 820), (900, 760), (560, 260)]
def s_evening(t, T):
    c = vgrad((40, 36, 70), (90, 70, 110)).convert("RGBA")
    d = ImageDraw.Draw(c); d.rectangle([0, 1330, W, H], fill=(70, 50, 42))
    paste_c(c, CHAR["shock"], W / 2, 1160, 0.85)
    for i, im in enumerate(NOTE_IM):
        st = 0.1 + i * 0.22
        if t < st: continue
        k = ease((t - st) / 0.35); x, y = NOTE_POS[i]
        paste_c(c, im, x, y - 300 * (1 - k), 1.0)
    caption(c, ["Вечер: 10 дел.", "Сделано — ноль."], t, y=1650, delay=0.4, colors=[(20, 20, 24), (230, 50, 50)])
    return c

def s_turn(t, T):
    c = DARK.copy()
    paste_c(c, CHAR_PHONE, W / 2, 1280, 0.95)
    paste_c(c, pill(["А потом друг скинул", "ему одно приложение…"], F("Bold", 56), (255, 255, 255), (0, 0, 0, 0)), W / 2, 540, 1, min(1, t / 0.3))
    return c

def s_app(t, T):
    c = vgrad((236, 240, 248), (250, 250, 252)).convert("RGBA")
    prog = ease(t / 1.6); checks = int(max(0, (t - 1.8) / 0.45)) + (1 if t > 1.8 else 0)
    ph = phone(prog, min(4, checks))
    paste_c(c, ph, W / 2, 900 + 60 * (1 - ease(t / 0.4)), 1.12)
    caption(c, ["Утро, обед, вечер —", "всё по полочкам"], t, y=1720, delay=0.4, font=F("Bold", 50))
    return c

def s_happy(t, T):
    c = GREEN.copy()
    paste_c(c, CHAR_UP_HAPPY, W / 2, 1180 + abs(math.sin(t * 5)) * -30, 0.95)
    paste_c(c, pill(["Тот же Озодбек."], F("Black", 70), (255, 255, 255), (0, 0, 0, 0)), W / 2, 420, pop(t / 0.35), min(1, t / 0.2))
    paste_c(c, pill(["Другая неделя."], F("Black", 70), (90, 230, 130), (0, 0, 0, 0)), W / 2, 530, pop((t - 0.5) / 0.35) if t > 0.5 else 0)
    return c

ICON = app_icon()
def s_end(t, T):
    c = DARK.copy()
    paste_c(c, ICON, W / 2, 640, pop(t / 0.4), min(1, t / 0.2))
    if t > 0.5:
        a = min(1, (t - 0.5) / 0.3)
        paste_c(c, pill(["MY WEEK"], F("Black", 96), (255, 255, 255), (0, 0, 0, 0)), W / 2, 880, 1, a)
        paste_c(c, pill(["Планировщик недели"], F("Medium", 40), (170, 170, 180), (0, 0, 0, 0)), W / 2, 970, 1, a)
        paste_c(c, pill(["by Exclusive Apps"], F("SemiBold", 38), (255, 255, 255), (0, 0, 0, 0)), W / 2, 1050, 1, a)
    if t > 1.1:
        p = pill(["Хотите своё приложение?", "Пришлите ТЗ — сделаем!"], F("Bold", 50), (20, 20, 24), (255, 255, 255, 255), colors=[(20, 20, 24), (110, 70, 255)])
        paste_c(c, p, W / 2, 1300, pop((t - 1.1) / 0.35))
    if t > 1.6:
        paste_c(c, pill(["+998 90 970 06 03"], F("SemiBold", 44), (255, 255, 255), (0, 0, 0, 0)), W / 2, 1480, 1, min(1, (t - 1.6) / 0.3))
    if t > 2.2:
        paste_c(c, pill(["Продолжение завтра →"], F("Medium", 36), (150, 150, 160), (0, 0, 0, 0)), W / 2, 1600, 1, min(1, (t - 2.2) / 0.3))
    return c

SCENES = [(s_hook, 2.6), (s_monday, 3.4), (s_school, 3.0), (s_evening, 3.4), (s_turn, 2.4), (s_app, 4.6), (s_happy, 2.8), (s_end, 4.8)]

def render(fn, dur, path, fade=0.2):
    n = int(round(dur * FPS))
    p = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                          "-c:v", "libx264", "-preset", "veryfast", "-crf", "19", "-pix_fmt", "yuv420p", path + ".tmp.mp4"], stdin=subprocess.PIPE)
    for i in range(n):
        t = i / FPS
        fr = fn(t, dur).convert("RGB")
        k = min(1, t / fade, (dur - t) / fade)
        if k < 1: fr = Image.blend(Image.new("RGB", (W, H), (0, 0, 0)), fr, max(0, k))
        p.stdin.write(fr.tobytes())
    p.stdin.close(); assert p.wait() == 0
    os.replace(path + ".tmp.mp4", path)

if __name__ == "__main__":
    if "--frames" in sys.argv:
        for fn, dur in SCENES:
            fn(dur * 0.8, dur).convert("RGB").resize((360, 640)).save(f"{TMP}/peek_{fn.__name__}.jpg")
        sys.exit()
    files = []
    for i, (fn, dur) in enumerate(SCENES):
        pth = f"{TMP}/{i:02d}.mp4"; render(fn, dur, pth); files.append(pth); print("scene", i, flush=True)
    open(f"{TMP}/list.txt", "w").write("".join(f"file '{os.path.basename(f)}'\n" for f in files))
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", f"{TMP}/list.txt", "-c", "copy", "video_noaudio.mp4"], check=True)
    print("done")
