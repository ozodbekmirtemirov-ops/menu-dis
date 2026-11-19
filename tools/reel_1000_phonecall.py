"""Рилс «1000 подписчиков к 31 декабря»: ноутбук EA говорит по телефону с Озодбеком. 39.35 c."""
import math, os, subprocess, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
sys.path.insert(0, "/home/claude/menu-dis/tools")
sys.path.insert(0, "/home/claude/reel")
from reel_kit_ep1 import W, H, FPS, F, ease, pop, pill, paste_c, text_size, render, TMP
from character_v2 import character
from make_plov import laptop, subtitle

DUR = 39.35
L = [(1.50, 4.27, "O", "К 31 декабря нужна тысяча подписчиков!"),
     (4.59, 6.73, "A", "Сейчас тридцать два, Озодбек."),
     (7.05, 8.08, "O", "Тридцать два?!"),
     (8.40, 11.75, "A", "Тридцать два. Зато настоящие. Каждый."),
     (12.07, 13.48, "O", "Сколько дней осталось?"),
     (13.80, 14.61, "A", "Сорок один."),
     (14.93, 17.91, "O", "Значит, 24 подписчика в день!"),
     (18.23, 21.54, "A", "Я посчитал. Двадцать четыре. Каждый день."),
     (21.86, 23.20, "O", "А где ты их возьмёшь?"),
     (23.52, 27.40, "A", "Два рилса в день. Пять историй. И плов уже в работе."),
     (27.72, 28.20, "O", "Плов?!"),
     (28.90, 33.00, "A", "Если ты это видишь… подпишись. Ты будешь 33-м."),
     (33.60, 35.46, "O", "Алло! С кем ты там говоришь?"),
     (35.78, 37.43, "A", "Ни с кем. Считаю.")]

def line_at(t):
    for i, (a, b, who, txt) in enumerate(L):
        if a - 0.05 <= t <= b + 0.25: return i, who, txt, t - a
    return None, None, None, 0

# ---------- background: night + faint code ----------
def make_bg():
    rng = np.random.default_rng(5)
    y = np.linspace(0, 1, H)[:, None, None]
    arr = (np.array([10, 12, 34]) * (1 - y) + np.array([26, 18, 56]) * y) * np.ones((1, W, 1))
    im = Image.fromarray(arr.astype(np.uint8), "RGB").convert("RGBA")
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    words = ["git push", "rilsy: 2/день", "istorii: 5", "1000", "deploy", "ТЗ", "Click", "Payme", "build ok", "plov.app", "31.12", "+24", "render", "EA"]
    f = F("Medium", 26)
    for _ in range(90):
        d.text((rng.uniform(-50, W), rng.uniform(0, H * .8)), rng.choice(words), font=f, fill=(110, 120, 255, int(rng.uniform(25, 70))))
    im.alpha_composite(lay)
    bok = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(bok)
    for _ in range(18):
        x, yy, r = rng.uniform(0, W), rng.uniform(0, H * .7), rng.uniform(16, 50)
        d.ellipse([x - r, yy - r, x + r, yy + r], fill=(255, 190, 90, int(rng.uniform(40, 90))))
    im.alpha_composite(bok.filter(ImageFilter.GaussianBlur(12)))
    d = ImageDraw.Draw(im)
    d.rectangle([0, 1440, W, H], fill=(30, 22, 44)); d.rectangle([0, 1440, W, 1452], fill=(70, 50, 110))
    return im
BG = make_bg()

LAP = {(e, t): laptop(e, t) for e in ("neutral", "smug", "wide") for t in (False, True)}

def rotary_phone():
    im = Image.new("RGBA", (300, 230), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle([20, 70, 280, 220], 50, fill=(240, 228, 200))
    d.rounded_rectangle([10, 190, 290, 226], 16, fill=(220, 206, 176))
    d.ellipse([90, 90, 210, 210], fill=(250, 244, 228)); d.ellipse([110, 110, 190, 190], fill=(110, 70, 255))
    for k in range(10):
        a = math.radians(-60 + k * 30); x = 150 + math.cos(a) * 46; y = 150 + math.sin(a) * 46
        d.ellipse([x - 9, y - 9, x + 9, y + 9], fill=(250, 244, 228))
    d.rectangle([60, 50, 240, 80], fill=(220, 206, 176))
    return im
PHONE = rotary_phone()

def receiver():
    im = Image.new("RGBA", (120, 300), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle([40, 40, 80, 260], 20, fill=(240, 228, 200))
    d.rounded_rectangle([10, 0, 110, 70], 30, fill=(240, 228, 200)); d.rounded_rectangle([10, 230, 110, 300], 30, fill=(240, 228, 200))
    return im
RECV = receiver()

OZ_HEAD = {}
for m in ("neutral", "happy", "shock", "sad"):
    c = character(m).crop((120, 90, 440, 480)); OZ_HEAD[m] = c
def oz_bubble(mood, talk, t_in):
    b = Image.new("RGBA", (360, 430), (0, 0, 0, 0)); d = ImageDraw.Draw(b)
    d.rounded_rectangle([0, 0, 359, 429], 40, fill=(255, 255, 255, 235))
    head = OZ_HEAD["happy" if talk and mood == "neutral" else mood].resize((240, 293), Image.LANCZOS)
    mask = Image.new("L", (240, 240), 0); ImageDraw.Draw(mask).ellipse([0, 0, 239, 239], fill=255)
    circ = Image.new("RGBA", (240, 240), (210, 220, 255, 255)); circ.alpha_composite(head.crop((0, 20, 240, 260)))
    b.paste(circ, (60, 30), mask)
    f = F("Bold", 34); tw = text_size(d, "Озодбек", f)[0]; d.text(((360 - tw) / 2, 300), "Озодбек", font=f, fill=(20, 20, 24))
    f2 = F("Medium", 26); s = "на линии" if t_in > 0 else "звонит…"
    tw = text_size(d, s, f2)[0]; d.text(((360 - tw) / 2, 352), s, font=f2, fill=(52, 199, 89))
    return b

def badge(lines, cols, bg=(255, 255, 255, 240), size=46):
    return pill(lines, F("Black", size), (20, 20, 24), bg, colors=cols)

def frame(t, T):
    c = BG.copy()
    idx, who, txt, lt = line_at(t)
    # zoom for whisper line
    z = 1.0
    if 28.7 <= t <= 33.3: z = 1 + 0.35 * ease((t - 28.7) / 0.5) - (0.35 * ease((t - 33.0) / 0.3) if t > 33.0 else 0)
    # laptop
    expr = "neutral"
    if idx in (2, 10): expr = "wide"
    if idx == 13 or (idx == 11): expr = "smug"
    talk = who == "A" and int(t * 7) % 2 == 0 and lt < (L[idx][1] - L[idx][0])
    paste_c(c, LAP[(expr, talk)], W / 2 - 40, 1090 - (z - 1) * 120 + math.sin(t * 2) * 5, 1.15 * z)
    # receiver at laptop's left side + phone on desk
    ring = math.sin(t * 50) * 10 if t < 1.4 else 0
    if t >= 1.4:
        paste_c(c, RECV.rotate(-15, expand=True, resample=Image.BICUBIC), W / 2 - 400 * z, 1000 - (z - 1) * 80, 0.95 * z)
        cd = ImageDraw.Draw(c); pts = [(W / 2 - 400 * z + 10 + 8 * math.sin(k * 1.3) , 1130 + k * 9) for k in range(24)]
        cd.line([(x, y) for x, y in pts] + [(860 - 60, 1350)], fill=(225, 210, 180), width=7)
    paste_c(c, PHONE, 860 + ring, 1360 if z < 1.05 else 1400, 0.9)
    if t < 1.4: paste_c(c, RECV.rotate(90, expand=True), 860 + ring, 1300, 0.7)
    # props on desk
    subs = 33 if t > 37.0 else 32
    if t > 4.6 and z < 1.1:
        k = pop((t - 4.6) / .35)
        paste_c(c, badge([f"{subs} / 1000"], [(110, 70, 255)], size=50), 230, 1560, k)
    if t > 13.85 and z < 1.1:
        cal = Image.new("RGBA", (200, 210), (0, 0, 0, 0)); d = ImageDraw.Draw(cal)
        d.rounded_rectangle([0, 0, 199, 209], 26, fill=(255, 255, 255)); d.rounded_rectangle([0, 0, 199, 56], 26, fill=(255, 69, 58)); d.rectangle([0, 30, 199, 56], fill=(255, 69, 58))
        d.text((44, 8), "дней", font=F("Bold", 32), fill=(255, 255, 255))
        tw = text_size(d, "41", F("Black", 100))[0]; d.text(((200 - tw) / 2, 66), "41", font=F("Black", 100), fill=(20, 20, 24))
        paste_c(c, cal, 540, 1580, pop((t - 13.85) / .35))
    if t > 15.6 and z < 1.1:
        paste_c(c, badge(["+24 в день"], [(52, 160, 89)], size=46), 850, 1590, pop((t - 15.6) / .35))
    if 18.4 <= t <= 21.7:
        calc = badge(["968 ÷ 41 = 23,6", "≈ 24 в день"], [(255, 255, 255), (120, 230, 140)], bg=(20, 16, 40, 230), size=48)
        paste_c(c, calc, W / 2, 560, pop((t - 18.4) / .35))
    if 23.6 <= t <= 27.6:
        items = [("2 рилса", 23.6), ("5 историй", 24.7), ("плов", 26.0)]
        for i, (s, st) in enumerate(items):
            if t >= st: paste_c(c, badge([s], [(110, 70, 255)], size=44), [180, 440, 670][i], 580, pop((t - st) / .3))
    # Ozodbek call bubble
    if t < 28.6 or 33.3 < t < 37.5:
        omood = "shock" if idx in (2, 10) else ("neutral" if who != "O" else ("sad" if idx == 12 else "neutral"))
        otalk = who == "O" and int(t * 7) % 2 == 0
        b = oz_bubble(omood, otalk, t - 1.4)
        paste_c(c, b, 880, 560 + (math.sin(t * 40) * 6 if t < 1.4 else 0), 0.62 * pop(t / .35))
    # whisper CTA
    if 29.3 <= t <= 33.2:
        a = min(1, (t - 29.3) / .3)
        paste_c(c, pill(["@exclusive_apps.uz"], F("Black", 64), (255, 255, 255), (110, 70, 255, 240)), W / 2, 1560, 1, a)
        paste_c(c, pill(["Подпишись — ты будешь 33-м"], F("Bold", 46), (20, 20, 24), (255, 255, 255, 240)), W / 2, 1680, 1, a)
    # subtitles (top)
    if txt:
        col = (255, 236, 160) if who == "O" else (255, 255, 255)
        if idx in (2, 10): col = (255, 120, 110)
        subtitle(c, txt, lt + .2, y=260, col=col)
    # end card
    if t > 37.6:
        a = min(1, (t - 37.6) / .4)
        ov = Image.new("RGBA", (W, H), (8, 6, 20, int(200 * a))); c.alpha_composite(ov)
        paste_c(c, pill(["Цель: 1000 до 31 декабря"], F("Black", 62), (255, 255, 255), (0, 0, 0, 0)), W / 2, 760, 1, a)
        paste_c(c, pill(["33 / 1000"], F("Black", 120), (120, 230, 140), (0, 0, 0, 0)), W / 2, 920, 1, a)
        paste_c(c, pill(["Подпишись · @exclusive_apps.uz"], F("Bold", 46), (20, 20, 24), (255, 255, 255, 255), colors=[(110, 70, 255)]), W / 2, 1090, pop((t - 37.8) / .35) if t > 37.8 else 0)
    return c

if __name__ == "__main__":
    if "--frames" in sys.argv:
        ts = [0.7, 3.0, 7.5, 10.0, 14.2, 16.5, 20.0, 26.5, 31.0, 34.5, 36.5, 38.8]
        s = Image.new("RGB", (240 * 6, 427 * 2))
        for i, tt in enumerate(ts): s.paste(frame(tt, DUR).convert("RGB").resize((240, 427)), ((i % 6) * 240, (i // 6) * 427))
        s.save("peek_1000.jpg"); sys.exit()
    render(frame, DUR, f"{TMP}/k1000.mp4", fade=0.1)
    os.replace(f"{TMP}/k1000.mp4", "r1000_noaudio.mp4"); print("done")
