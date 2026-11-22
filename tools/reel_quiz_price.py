"""Мини-квиз «Сколько стоит приложение? А/Б/В» (22.11, 16:10). Диалог Озодбек (Dmitry) + ноутбук (cartesia).
Цену НЕ называем: «зависит от ТЗ — пришлите, посчитаем». Usage: reel_quiz_price.py voice_dir out.mp4 [--frames sheet.jpg]"""
import math, os, sys
from PIL import Image, ImageDraw
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from reel_speko_kit import *
import reel_kit_ep1 as rk

VD, OUT = sys.argv[1], sys.argv[2]
SUBS = [("Сколько стоит своё приложение? А — $100, Б — $1000, В — $100 000? Пиши букву в комментариях!", "O"),
        ("Правильный ответ… зависит от трёх вещей.", "L"),
        ("Первое: сколько экранов. Запись в салон — это 5 экранов, а не 50.", "L"),
        ("Второе: функции. Оплата Click и Payme, карта, уведомления — каждая добавляет работу.", "L"),
        ("Третье: только Android — или ещё iPhone и сайт.", "L"),
        ("То есть — ни А, ни Б, ни В?", "O"),
        ("Цена — из вашего ТЗ. Пришлите его — и мы посчитаем.", "L"),
        ("Пиши «ТЗ» в директ. И подпишись — ты будешь 39-м!", "O")]
LINES = [(f"{VD}/q{i + 1}.wav", s, w) for i, (s, w) in enumerate(SUBS)]
DARK = rk.DARK
C = {m: character(m) for m in ("neutral", "happy", "shock")}
UP = character("happy", "up"); UP_SH = character("shock", "up"); WAVE = character("happy", "wave")
OPTS = [("А", "$100", (60, 150, 255)), ("Б", "$1 000", (255, 159, 10)), ("В", "$100 000", (230, 60, 90))]

def opt(letter, val, col, crossed=0.0):
    im = Image.new("RGBA", (300, 300), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, 299, 299], 50, fill=col)
    f = F("Black", 120); tw, th, oy = text_size(d, letter, f); d.text((150 - tw / 2, 40 - oy), letter, font=f, fill=(255, 255, 255))
    f2 = F("Bold", 50); tw, th, oy = text_size(d, val, f2); d.text((150 - tw / 2, 205 - oy), val, font=f2, fill=(255, 255, 255))
    if crossed > 0:
        e = 30 + 240 * crossed; d.line([(30, 30), (e, e)], fill=(20, 20, 24), width=22)
    return im
OPT = [opt(*o) for o in OPTS]

def s1(t, T):
    c = DARK.copy()
    paste_c(c, pill(["Сколько стоит", "приложение?"], F("Black", 82), (255, 255, 255), (0, 0, 0, 0)), W / 2, 360, pop(t / .35))
    for i in range(3):
        st = .5 + i * .35
        if t > st: paste_c(c, OPT[i], 210 + i * 330, 720, 0.95 * pop((t - st) / .3))
    paste_c(c, C["neutral"] if t < T * .6 else WAVE, W / 2, 1230, 0.72)
    if t > T * .6: paste_c(c, pill(["Пиши букву в комменты 👇".replace(" 👇", "")], F("Bold", 44), (20, 20, 24), (255, 236, 160, 255)), W / 2, 960, pop((t - T * .6) / .3))
    return c

def lap_scene(title, talk_until):
    def f(t, T):
        c = BG2.copy()
        paste_c(c, pill([title], F("Black", 62), (255, 255, 255), PUR + (255,)), W / 2, 310, pop(t / .35))
        paste_c(c, LAP[("smug", talking(t) and t < T - talk_until)], W / 2, 860, 1.1)
        paste_c(c, C["neutral"], 870, 1350, 0.42)
        return c
    return f
s2 = lap_scene("Ответ зависит от 3 вещей", .4)

def mini(col):
    im = Image.new("RGBA", (120, 220), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, 119, 219], 22, fill=(20, 20, 24)); d.rounded_rectangle([8, 8, 111, 211], 16, fill=(250, 250, 252))
    d.rounded_rectangle([20, 30, 100, 60], 8, fill=col); d.rounded_rectangle([20, 80, 100, 100], 6, fill=(225, 225, 232))
    d.rounded_rectangle([20, 115, 80, 135], 6, fill=(225, 225, 232)); return im
MINIS = [mini(c) for c in [(110, 70, 255), (52, 199, 89), (255, 159, 10), (60, 150, 255), (230, 60, 90)]]

def s3(t, T):
    c = DARK.copy()
    paste_c(c, pill(["1. Сколько экранов"], F("Black", 64), (255, 255, 255), (0, 0, 0, 0)), W / 2, 300, pop(t / .35))
    for i in range(5):
        st = .3 + i * .25
        if t > st: paste_c(c, MINIS[i], 180 + i * 180, 640, pop((t - st) / .3))
    paste_c(c, pill(["Салон красоты = 5 экранов"], F("Bold", 46), (20, 20, 24), (255, 255, 255, 255)), W / 2, 880, pop((t - 1.8) / .3) if t > 1.8 else 0)
    paste_c(c, LAP[("neutral", talking(t) and t < T - .4)], W / 2, 1260, 0.6)
    return c

def s4(t, T):
    c = DARK.copy(); d = ImageDraw.Draw(c)
    paste_c(c, pill(["2. Функции"], F("Black", 64), (255, 255, 255), (0, 0, 0, 0)), W / 2, 300, pop(t / .35))
    feats = [("Оплата", "Click / Payme", (52, 199, 89)), ("Карта", "Доставка по Ташкенту", (60, 150, 255)), ("Уведомления", "Напоминания клиентам", (255, 159, 10))]
    for i, (lab, val, col) in enumerate(feats):
        st = .4 + i * T * .22
        if t > st:
            im = Image.new("RGBA", (800, 150), (0, 0, 0, 0)); card(ImageDraw.Draw(im), 0, 0, 798, 148, lab, val, col)
            paste_c(c, im, W / 2 + 60 * (1 - ease((t - st) / .35)), 470 + i * 180, 1, min(1, (t - st) / .25))
    paste_c(c, LAP[("neutral", talking(t) and t < T - .4)], W / 2, 1270, 0.55)
    return c

def plat(name, col):
    return pill([name], F("Black", 52), (255, 255, 255), col + (255,), pad=(46, 34))
PLATS = [plat("Android", (52, 199, 89)), plat("iPhone", (60, 60, 70)), plat("Сайт", (60, 150, 255))]
def s5(t, T):
    c = DARK.copy()
    paste_c(c, pill(["3. Где работает"], F("Black", 64), (255, 255, 255), (0, 0, 0, 0)), W / 2, 300, pop(t / .35))
    paste_c(c, PLATS[0], W / 2, 500, pop((t - .3) / .3) if t > .3 else 0)
    for i in (1, 2):
        st = T * .45 + (i - 1) * .3
        if t > st: paste_c(c, PLATS[i], 300 if i == 1 else 780, 680, pop((t - st) / .3))
    paste_c(c, LAP[("neutral", talking(t) and t < T - .4)], W / 2, 1220, 0.6)
    return c

def s6(t, T):
    c = DARK.copy()
    for i in range(3):
        cr = ease((t - .2 - i * .25) / .3)
        paste_c(c, opt(*OPTS[i], crossed=cr) if cr > 0 else OPT[i], 210 + i * 330, 520, 0.9)
    paste_c(c, UP_SH, W / 2, 1200, 0.9)
    return c

def doc():
    im, d = phone_frame("Ваше ТЗ", "→ расчёт стоимости", pw=640, ph=760)
    for i, s in enumerate(["Экраны: 5", "Оплата: Click", "Платформа: Android"]):
        d.rounded_rectangle([50, 260 + i * 130, 590, 360 + i * 130], 26, fill=(255, 255, 255), outline=(230, 230, 236), width=2)
        d.text((80, 288 + i * 130), s, font=F("Bold", 38), fill=(20, 20, 24))
    return im
DOC = doc()
def s7(t, T):
    c = BG2.copy()
    paste_c(c, DOC, 360, 760, 0.95 * pop(t / .4))
    paste_c(c, LAP[("smug", talking(t) and t < T - .4)], 820, 1300, 0.55)
    return c

def s8(t, T):
    c = DARK.copy()
    paste_c(c, pill(["Цена — из вашего ТЗ"], F("Black", 70), (255, 236, 160), (0, 0, 0, 0)), W / 2, 300, pop(t / .35))
    paste_c(c, pill(["Напишите «ТЗ» в директ"], F("Bold", 52), (20, 20, 24), (255, 255, 255, 255)), W / 2, 440, pop((t - .3) / .35) if t > .3 else 0)
    paste_c(c, UP, W / 2, 900 + math.sin(t * 7) * 6, 0.6)
    if t > .8: paste_c(c, pill(["+998 90 970 06 03"], F("Black", 58), (255, 255, 255), PUR + (255,), pad=(44, 22)), W / 2, 1300, pop((t - .8) / .35))
    if t > 1.4: paste_c(c, pill(["38 / 1000 · подпишись — ты 39-й"], F("Bold", 40), (255, 255, 255), (0, 0, 0, 0)), W / 2, 1430, 1, min(1, (t - 1.4) / .3))
    return c

if __name__ == "__main__":
    fr = sys.argv[sys.argv.index("--frames") + 1] if "--frames" in sys.argv else False
    make_reel(LINES, [s1, s2, s3, s4, s5, s6, s7, s8], OUT, os.path.dirname(os.path.abspath(OUT)) + "/quiz_scenes", seed=44, frames=fr, tail=2.0)
