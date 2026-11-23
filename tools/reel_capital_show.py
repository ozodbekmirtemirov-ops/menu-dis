"""Витрина My Capital «Сколько у тебя денег?» (23.11, 16:10, Trial Reel), ~21 с. Повод переслать: «отправь другу, у которого всегда „денег нет“».
Голос Speko: Озодбек Dmitry, ноутбук cartesia. Usage: reel_capital_show.py voice_dir out.mp4 [--frames sheet.jpg]"""
import math, os, sys
from PIL import Image, ImageDraw
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from reel_speko_kit import *
import reel_kit_ep1 as rk

VD, OUT = sys.argv[1], sys.argv[2]
SUBS = [("Сколько у тебя денег? Не на карте — вообще всего?", "O"),
        ("В My Capital всё в одном месте: квартира, машина, бизнес, наличные и золото.", "O"),
        ("Я рисую диаграмму и показываю, что растёт, а что падает.", "L"),
        ("А ИИ-советчик подсказывает, что пора продать.", "O"),
        ("Отправь другу, у которого всегда «денег нет». А своё приложение — пришлите ТЗ!", "O")]
LINES = [(f"{VD}/c{i + 1}.wav", s, w) for i, (s, w) in enumerate(SUBS)]
GLOW = radial((8, 12, 10), (20, 110, 60), cy=0.42, r=1000).convert("RGBA")
DARK = rk.DARK
GRN = (52, 199, 89)
ASSETS = [("Квартира", "950 млн сум", (60, 150, 255)), ("Машина", "210 млн сум", (255, 159, 10)), ("Бизнес", "300 млн сум", (110, 70, 255)),
          ("Наличные", "45 млн сум", GRN), ("Золото", "60 млн сум", (230, 190, 40))]
SH = character("shock", "phone"); HP = character("happy", "phone"); WAVE = character("happy", "wave")

def s1(t, T):
    c = GLOW.copy()
    paste_c(c, pill(["Сколько у тебя", "денег?"], F("Black", 108), (255, 255, 255), (0, 0, 0, 0)), W / 2, 380, pop(t / .3))
    if t > T * .45: paste_c(c, pill(["не на карте — ВСЕГО"], F("Black", 54), (20, 20, 24), (255, 236, 160, 255)), W / 2, 620, pop((t - T * .45) / .3))
    paste_c(c, SH, W / 2, 1180 + math.sin(t * 8) * 6, 0.95)
    return c

def cap_phone(k, total=True):
    im, d = phone_frame("My Capital", "весь капитал")
    for i, (a, v, col) in enumerate(ASSETS):
        if k > i * .16: card(d, 40, 220 + i * 150, 540, 128, a, v, col)
    if total and k > .9:
        d.rounded_rectangle([40, 990, 580, 1120], 28, fill=(20, 20, 24))
        d.text((70, 1008), "Итого", font=F("SemiBold", 28), fill=(170, 170, 180))
        d.text((70, 1050), "1,56 млрд сум", font=F("Black", 46), fill=(120, 230, 140))
    return im

def s2(t, T):
    c = GLOW.copy()
    paste_c(c, pill(["My Capital"], F("Black", 64), (255, 255, 255), GRN + (255,)), W / 2, 230, pop(t / .3))
    paste_c(c, cap_phone(t / (T * .85)), W / 2, 920, 0.98)
    return c

def donut(k):
    s = 560; im = Image.new("RGBA", (s, s), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    vals = [950, 210, 300, 45, 60]; tot = sum(vals); a0 = -90
    for v, (_, _, col) in zip(vals, ASSETS):
        a1 = a0 + 360 * v / tot * k
        d.pieslice([0, 0, s - 1, s - 1], a0, a1, fill=col); a0 = a0 + 360 * v / tot
    d.ellipse([150, 150, s - 150, s - 150], fill=(16, 18, 28))
    return im

def s3(t, T):
    c = DARK.copy()
    paste_c(c, donut(ease(t / (T * .5))), 380, 640, 0.95)
    paste_c(c, LAP[("smug", talking(t) and t < T - .4)], 850, 1000, 0.5)
    if t > T * .4: paste_c(c, pill(["Бизнес  +12% ▲"], F("Black", 52), (255, 255, 255), GRN + (255,)), W / 2, 1150, pop((t - T * .4) / .3))
    if t > T * .6: paste_c(c, pill(["Машина  −8% ▼"], F("Black", 52), (255, 255, 255), (230, 60, 70, 255)), W / 2, 1290, pop((t - T * .6) / .3))
    return c

def s4(t, T):
    c = GLOW.copy()
    b = Image.new("RGBA", (880, 330), (0, 0, 0, 0)); d = ImageDraw.Draw(b)
    d.rounded_rectangle([0, 0, 879, 329], 44, fill=(255, 255, 255))
    d.rounded_rectangle([36, 34, 150, 84], 20, fill=PUR); d.text((58, 38), "ИИ", font=F("Black", 36), fill=(255, 255, 255))
    d.text((170, 40), "советчик", font=F("SemiBold", 34), fill=(140, 140, 150))
    d.text((40, 120), "Машина дешевеет 3-й месяц.", font=F("Bold", 44), fill=(20, 20, 24))
    d.text((40, 190), "Пора продать?", font=F("Black", 58), fill=(230, 60, 70))
    paste_c(c, b, W / 2, 470 + 40 * (1 - ease(t / .4)), 1, min(1, t / .3))
    paste_c(c, HP, W / 2, 1150, 0.9)
    return c

def s5(t, T):
    c = DARK.copy()
    paste_c(c, pill(["Отправь другу,", "у которого", "«денег нет»"], F("Black", 84), (255, 255, 255), (0, 0, 0, 0), colors=[(255, 255, 255), (255, 255, 255), (255, 236, 160)]), W / 2, 420, pop(t / .3))
    paste_c(c, WAVE, W / 2, 1000, 0.6)
    if t > .8: paste_c(c, pill(["Своё приложение? Пришлите ТЗ"], F("Bold", 46), (255, 255, 255), PUR + (255,)), W / 2, 1330, pop((t - .8) / .3))
    if t > 1.3: paste_c(c, pill(["+998 90 970 06 03 · подпишись — ты 39-й"], F("SemiBold", 36), (210, 210, 225), (0, 0, 0, 0)), W / 2, 1440, 1, min(1, (t - 1.3) / .3))
    return c

if __name__ == "__main__":
    fr = sys.argv[sys.argv.index("--frames") + 1] if "--frames" in sys.argv else False
    make_reel(LINES, [s1, s2, s3, s4, s5], OUT, os.path.dirname(os.path.abspath(OUT)) + "/cap_scenes", seed=83, frames=fr, tail=1.6)
