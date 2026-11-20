"""Эп.1 «Неделя без плана» — версия С ГОЛОСОМ (20.11). Сцены из reel_kit_ep1 (персонаж v2), тайминги по озвучке 37.7 c.
Usage: python3 reel_ep1_voice.py out_dir   (--frames для превью)"""
import os, subprocess, sys
from PIL import Image, ImageDraw
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import reel_kit_ep1 as rk
from reel_kit_ep1 import W, H, F, pop, pill, paste_c, text_size, render, DARK, ICON

rk.caption = lambda *a, **k: None   # подписи-пилюли заменяем субтитрами озвучки

def subtitle(c, text, t, y=1680, col=(255, 236, 160)):
    f = F("Bold", 54); d = ImageDraw.Draw(c)
    words = text.split(); lines = []; cur = ""
    for w_ in words:
        tst = (cur + " " + w_).strip()
        if text_size(d, tst, f)[0] > 940 and cur: lines.append(cur); cur = w_
        else: cur = tst
    lines.append(cur)
    a = min(1, max(0, t / 0.15))
    for i, l in enumerate(lines):
        tw = text_size(d, l, f)[0]; x = (W - tw) / 2; yy = y + i * 68 - (len(lines) - 1) * 34
        d.text((x, yy), l, font=f, fill=col + (int(255 * a),), stroke_width=7, stroke_fill=(10, 8, 20, int(235 * a)))

def with_sub(fn, text, y=1680):
    def g(t, T):
        c = fn(t, T); subtitle(c, text, t - 0.1, y=y); return c
    g.__name__ = fn.__name__; return g

def s_end(t, T):
    c = DARK.copy()
    paste_c(c, ICON, W / 2, 560, pop(t / 0.4), min(1, t / 0.2))
    a = min(1, max(0, (t - 0.4) / 0.3))
    paste_c(c, pill(["MY WEEK"], F("Black", 90), (255, 255, 255), (0, 0, 0, 0)), W / 2, 790, 1, a)
    paste_c(c, pill(["by Exclusive Apps"], F("SemiBold", 38), (200, 200, 210), (0, 0, 0, 0)), W / 2, 880, 1, a)
    if t > 0.6:
        p = pill(["Хотите своё приложение?", "Пришлите ТЗ — сделаем!"], F("Bold", 50), (20, 20, 24), (255, 255, 255, 255), colors=[(20, 20, 24), (110, 70, 255)])
        paste_c(c, p, W / 2, 1090, pop((t - 0.6) / 0.35))
    if t > 1.2:
        paste_c(c, pill(["+998 90 970 06 03"], F("SemiBold", 44), (255, 255, 255), (0, 0, 0, 0)), W / 2, 1260, 1, min(1, (t - 1.2) / 0.3))
    if t > 3.4:
        paste_c(c, pill(["Вторник — завтра →"], F("Bold", 48), (255, 236, 160), (0, 0, 0, 0)), W / 2, 1400, pop((t - 3.4) / .35))
    if t > 5.2:
        paste_c(c, pill(["Подпишись, чтобы не пропустить"], F("Bold", 42), (255, 255, 255), (110, 70, 255, 255)), W / 2, 1530, pop((t - 5.2) / .35))
    return c

def s_turn(t, T):
    c = DARK.copy()
    paste_c(c, rk.CHAR_PHONE, W / 2, 1280, 0.95)
    paste_c(c, pill(["И тут друг скинул", "мне одно приложение…"], F("Bold", 56), (255, 255, 255), (0, 0, 0, 0)), W / 2, 540, 1, min(1, t / 0.3))
    return c

import math
from reel_kit_ep1 import ease, vgrad
from character_v2 import character
O_SLEEP, O_SHOCK = character("sleepy"), character("shock", "phone")
NIGHT = vgrad((8, 10, 30), (24, 22, 60)).convert("RGBA")

def mystery_phone(t):
    pw, ph = 600, 820
    im = Image.new("RGBA", (pw, ph), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, pw - 1, ph - 1], 80, fill=(18, 18, 22))
    d.rounded_rectangle([16, 16, pw - 17, ph - 17], 66, fill=(248, 248, 250))
    d.text((50, 70), "MY WEEK", font=F("Black", 40), fill=(20, 20, 24))
    d.text((50, 122), "Новая задача", font=F("Medium", 28), fill=(140, 140, 150))
    for i, (sec, task) in enumerate([("Вторник", "Подъём в 7:00"), ("Вторник", "Школа + домашка")]):
        y = 190 + i * 150
        d.rounded_rectangle([50, y, pw - 50, y + 130], 26, fill=(255, 255, 255), outline=(232, 232, 238), width=2)
        d.text((80, y + 22), sec, font=F("SemiBold", 24), fill=(150, 150, 160)); d.text((80, y + 60), task, font=F("Bold", 32), fill=(20, 20, 24))
    k = ease((t - 1.6) / 0.4)
    if k > 0:
        y = 500; pulse = 0.5 + 0.5 * math.sin(t * 8)
        d.rounded_rectangle([40, y - 6, pw - 40, y + 196], 30, fill=(255, int(60 + 60 * pulse), int(60 + 60 * pulse)))
        d.rounded_rectangle([50, y, pw - 50, y + 186], 26, fill=(255, 240, 240))
        d.text((80, y + 24), "Среда, 15:00", font=F("Bold", 30), fill=(220, 40, 40))
        d.text((80, y + 72), "???", font=F("Black", 64), fill=(20, 20, 24))
        d.text((240, y + 92), "добавлено: не тобой", font=F("SemiBold", 26), fill=(200, 60, 60))
    return im

def s_night(t, T):
    c = NIGHT.copy(); d = ImageDraw.Draw(c)
    d.ellipse([860, 110, 960, 210], fill=(250, 240, 200))   # луна
    for x, y in [(150, 300), (300, 160), (640, 120), (480, 200), (980, 480)]: d.ellipse([x, y, x + 6, y + 6], fill=(255, 255, 255))
    d.rectangle([0, 1450, W, H], fill=(30, 26, 50))
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0)); gd = ImageDraw.Draw(glow)
    a = int(110 * min(1, t / 0.4)); gd.ellipse([140, 380, 940, 1300], fill=(120, 170, 255, a))
    from PIL import ImageFilter
    c.alpha_composite(glow.filter(ImageFilter.GaussianBlur(80)))
    paste_c(c, mystery_phone(t), W / 2, 930 + 40 * (1 - ease(t / 0.5)), 0.95)
    paste_c(c, O_SLEEP if t < 1.4 else O_SHOCK, W / 2, 1640, 0.42)
    return c

def s_cliff(t, T):
    c = DARK.copy()
    paste_c(c, pill(["Кто поставил", "эту задачу?"], F("Black", 82), (255, 255, 255), (0, 0, 0, 0)), W / 2, 420, pop(t / .35))
    paste_c(c, pill(["Среда, 15:00 — ???"], F("Bold", 54), (255, 255, 255), (220, 50, 50, 255)), W / 2, 610, pop((t - .4) / .35) if t > .4 else 0)
    paste_c(c, O_SHOCK, W / 2, 1000 + math.sin(t * 7) * 6, 0.55)
    if t > 2.6:
        paste_c(c, pill(["Серия 2 — завтра в 12:40"], F("Black", 56), (255, 236, 160), (0, 0, 0, 0)), W / 2, 1320, pop((t - 2.6) / .35))
    if t > 4.6:
        paste_c(c, pill(["Подпишись, чтобы не пропустить"], F("Bold", 44), (255, 255, 255), (110, 70, 255, 255)), W / 2, 1450, pop((t - 4.6) / .35))
    if t > 5.8:
        paste_c(c, pill(["Своё приложение? Пришлите ТЗ · +998 90 970 06 03"], F("SemiBold", 34), (200, 200, 215), (0, 0, 0, 0)), W / 2, 1560, 1, min(1, (t - 5.8) / .3))
    return c

CUTS = [0, 5.5, 10.25, 14.47, 18.21, 21.31, 27.53, 30.44, 37.43, 46.2]
FNS = [with_sub(rk.s_hook, "Привет, я Озодбек, мне 13. И это моя неделя без плана."),
       with_sub(rk.s_monday, "Понедельник. Будильник? Не слышал. Опять проспал!"),
       with_sub(rk.s_school, "В школе спрашивают домашку. А я такой: какая домашка?"),
       with_sub(rk.s_evening, "А вечером — 10 дел. Сделано — ноль."),
       s_turn,
       with_sub(rk.s_app, "My Week. Утро, обед, вечер — всё по полочкам.", y=1700),
       rk.s_happy,
       with_sub(s_night, "Но ночью телефон загорелся… В My Week появилась задача, которую я НЕ добавлял.", y=330),
       s_cliff]
SCENES = list(zip(FNS, [CUTS[i + 1] - CUTS[i] for i in range(len(FNS))]))

if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "."
    if "--frames" in sys.argv:
        tiles = [fn(min(dur * .75, dur - .1), dur).convert("RGB").resize((270, 480)) for fn, dur in SCENES]
        s = Image.new("RGB", (270 * 5, 480 * 2))
        for i, im in enumerate(tiles): s.paste(im, ((i % 5) * 270, (i // 5) * 480))
        s.save(f"{out}/peek_ep1v.jpg"); sys.exit()
    files = []
    for i, (fn, dur) in enumerate(SCENES):
        p = f"{out}/e{i:02d}.mp4"; render(fn, dur, p, fade=0.08); files.append(p); print("scene", i, flush=True)
    open(f"{out}/elist.txt", "w").write("".join(f"file '{os.path.basename(f)}'\n" for f in files))
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", f"{out}/elist.txt", "-c", "copy", f"{out}/ep1v_noaudio.mp4"], check=True)
    print("done")
