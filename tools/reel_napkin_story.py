"""История компании «Как я придумал Exclusive Apps на салфетке» (22.11, 18:10). Монолог Озодбека (Dmitry) + реплика ноутбука.
Только Озодбек и ноутбук, других людей нет. Usage: reel_napkin_story.py voice_dir out.mp4 [--frames sheet.jpg]"""
import math, os, sys
from PIL import Image, ImageDraw, ImageFilter
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from reel_speko_kit import *
import reel_kit_ep1 as rk

VD, OUT = sys.argv[1], sys.argv[2]
SUBS = [("Exclusive Apps я придумал… на салфетке. В ресторане. Один.", "O"),
        ("Сижу, жду ужин и думаю: у всех есть идеи приложений. А кто их делает?", "O"),
        ("Беру салфетку и пишу: «Вы присылаете ТЗ — я делаю приложение».", "O"),
        ("Первое приложение — это боль. Бессонные ночи, ошибки, всё ломалось.", "O"),
        ("В 3 часа ночи думал: может, бросить? Но не бросил.", "O"),
        ("Сейчас у нас 3 готовых приложения: My Week, My Capital и My School.", "O"),
        ("А салфетку он до сих пор хранит. Я видел.", "L"),
        ("Есть идея? Пришлите ТЗ — сделаем. И подпишись, чтобы увидеть, что дальше!", "O")]
LINES = [(f"{VD}/n{i + 1}.wav", s, w) for i, (s, w) in enumerate(SUBS)]
DARK = rk.DARK
NIGHT = vgrad((8, 10, 30), (24, 22, 60)).convert("RGBA")
C = {m: character(m) for m in ("neutral", "happy", "shock", "sad", "sleepy")}
UP = character("happy", "up"); WAVE = character("happy", "wave")

def resto():
    c = radial((40, 18, 10), (150, 80, 30), cy=0.3, r=1100).convert("RGBA"); d = ImageDraw.Draw(c)
    for x in (240, 840):   # лампы
        d.line([(x, 0), (x, 180)], fill=(30, 20, 15), width=6)
        d.pieslice([x - 110, 140, x + 110, 300], 180, 360, fill=(60, 40, 30))
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0)); g = ImageDraw.Draw(glow)
    for x in (240, 840): g.ellipse([x - 200, 160, x + 200, 560], fill=(255, 200, 120, 90))
    c.alpha_composite(glow.filter(ImageFilter.GaussianBlur(60)))
    return c
RESTO = resto()
def table(c):
    d = ImageDraw.Draw(c)
    d.rectangle([0, 1250, W, 1460], fill=(120, 70, 40)); d.rectangle([0, 1250, W, 1275], fill=(150, 95, 55))
    d.ellipse([90, 1290, 330, 1380], fill=(245, 245, 245)); d.ellipse([130, 1305, 290, 1365], fill=(225, 225, 225))   # тарелка
    d.rectangle([0, 1460, W, H], fill=(30, 18, 12))

def napkin(prog=1.0, w=700, h=520):
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, w - 1, h - 1], 18, fill=(252, 250, 244))
    for k in range(1, 4): d.line([(0, k * h / 4), (w, k * h / 4)], fill=(236, 232, 222), width=2)
    txt = ["Вы присылаете ТЗ", "↓", "я делаю", "приложение!"]
    n = sum(len(s) for s in txt); show = int(n * prog); f = F("Bold", int(w / 14))
    for i, s in enumerate(txt):
        part = s[:max(0, show)]; show -= len(s)
        d.text((50, 50 + i * 110), part, font=f, fill=(40, 60, 160))
    return im.rotate(-4, resample=Image.BICUBIC, expand=True)
NAP_FULL = napkin(1.0)

def s1(t, T):
    c = RESTO.copy()
    paste_c(c, pill(["Как я придумал", "Exclusive Apps"], F("Black", 70), (255, 255, 255), (0, 0, 0, 0)), W / 2, 420, pop(t / .35))
    paste_c(c, C["neutral"], W / 2, 1060, 0.8); table(c)
    paste_c(c, NAP_FULL, 800, 1300, 0.3)
    return c

IDEAS = [("Учёт в офисе", (60, 150, 255)), ("Магазин онлайн", (255, 159, 10)), ("Школа", (52, 199, 89)), ("Личный бюджет", (230, 60, 90))]
def s2(t, T):
    c = RESTO.copy()
    pos = [(250, 340), (800, 310), (230, 500), (830, 480)]
    for i, ((s, col), (x, y)) in enumerate(zip(IDEAS, pos)):
        st = .3 + i * .35
        if t > st: paste_c(c, pill([s], F("Bold", 44), (255, 255, 255), col + (255,)), x, y + math.sin(t * 2 + i) * 8, pop((t - st) / .3))
    if t > T * .6: paste_c(c, pill(["А кто их делает?"], F("Black", 64), (20, 20, 24), (255, 236, 160, 255)), W / 2, 680, pop((t - T * .6) / .3))
    paste_c(c, C["shock"] if t > T * .6 else C["neutral"], W / 2, 1060, 0.8); table(c)
    return c

def s3(t, T):
    c = RESTO.copy(); table(c)
    paste_c(c, napkin(min(1, t / (T * .8))), W / 2, 720, 1.25)
    paste_c(c, C["happy"], 900, 1350, 0.4)
    return c

def screen_err(t):
    im = Image.new("RGBA", (700, 460), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, 699, 459], 30, fill=(44, 44, 52)); d.rounded_rectangle([20, 20, 679, 439], 18, fill=(18, 18, 26))
    for i in range(6):
        red = (i + int(t * 3)) % 3 == 0
        d.text((50, 50 + i * 62), ("ERROR: crash" if red else "build… ok"), font=F("Bold", 38), fill=(255, 80, 80) if red else (120, 220, 140))
    return im

def s4(t, T):
    c = NIGHT.copy()
    paste_c(c, pill(["Первое приложение"], F("Black", 62), (255, 255, 255), (0, 0, 0, 0)), W / 2, 300, pop(t / .35))
    paste_c(c, screen_err(t), W / 2, 680, 1.0)
    if t > T * .5: paste_c(c, pill(["Ошибка №47"], F("Bold", 46), (255, 255, 255), (220, 50, 50, 255)), W / 2, 960, pop((t - T * .5) / .3))
    paste_c(c, C["sleepy"], W / 2, 1340, 0.66)
    return c

CLK = rk.alarm_clock("3:00")
def s5(t, T):
    c = NIGHT.copy()
    paste_c(c, CLK, W / 2, 520, 0.85)
    turn = t > T * .55
    if turn: paste_c(c, pill(["Но не бросил"], F("Black", 70), (255, 236, 160), (0, 0, 0, 0)), W / 2, 850, pop((t - T * .55) / .3))
    paste_c(c, UP if turn else C["sad"], W / 2, 1270, 0.8)
    return c

def tile(col, glyph, size=220):
    im = Image.new("RGBA", (size, size), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, size - 1, size - 1], int(size * .24), fill=col)
    f = F("Black", int(size * .4)); tw, th, oy = text_size(d, glyph, f)
    d.text(((size - tw) / 2, (size - th) / 2 - oy), glyph, font=f, fill=(255, 255, 255)); return im
APPS = [(rk.app_icon(220), "My Week"), (tile((52, 199, 89), "$"), "My Capital"), (tile((255, 159, 10), "5"), "My School")]
def s6(t, T):
    c = DARK.copy()
    paste_c(c, pill(["Сейчас: 3 готовых приложения"], F("Black", 54), (255, 255, 255), (0, 0, 0, 0)), W / 2, 300, pop(t / .35))
    for i, (ic, name) in enumerate(APPS):
        st = .4 + i * T * .2
        if t > st:
            x = 200 + i * 340; k = pop((t - st) / .3)
            paste_c(c, ic, x, 560, 0.9 * k); paste_c(c, pill([name], F("Bold", 40), (255, 255, 255), (0, 0, 0, 0)), x, 720, k)
    paste_c(c, UP, W / 2, 1200, 0.75)
    return c

def framed():
    nap = napkin(1.0, 600, 460); w, h = nap.width + 80, nap.height + 80
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, w - 1, h - 1], 12, fill=(170, 120, 60)); d.rectangle([28, 28, w - 29, h - 29], fill=(60, 40, 25))
    im.alpha_composite(nap, (40, 40)); return im
FRAMED = framed()
def s7(t, T):
    c = BG2.copy()
    paste_c(c, FRAMED, W / 2, 560, 0.95 * pop(t / .4))
    paste_c(c, LAP[("smug", talking(t) and t < T - .4)], W / 2, 1180, 0.7)
    return c

def s8(t, T):
    c = DARK.copy()
    paste_c(c, pill(["Есть идея?"], F("Black", 86), (255, 255, 255), (0, 0, 0, 0)), W / 2, 310, pop(t / .35))
    paste_c(c, pill(["Пришлите ТЗ — сделаем"], F("Bold", 54), (20, 20, 24), (255, 255, 255, 255)), W / 2, 450, pop((t - .3) / .35) if t > .3 else 0)
    paste_c(c, WAVE, W / 2, 900 + math.sin(t * 7) * 6, 0.6)
    if t > .8: paste_c(c, pill(["+998 90 970 06 03"], F("Black", 58), (255, 255, 255), PUR + (255,), pad=(44, 22)), W / 2, 1300, pop((t - .8) / .35))
    if t > 1.4: paste_c(c, pill(["38 / 1000 · подпишись — ты 39-й"], F("Bold", 40), (255, 255, 255), (0, 0, 0, 0)), W / 2, 1430, 1, min(1, (t - 1.4) / .3))
    return c

if __name__ == "__main__":
    fr = sys.argv[sys.argv.index("--frames") + 1] if "--frames" in sys.argv else False
    make_reel(LINES, [s1, s2, s3, s4, s5, s6, s7, s8], OUT, os.path.dirname(os.path.abspath(OUT)) + "/nap_scenes", seed=58, frames=fr, tail=2.0)
