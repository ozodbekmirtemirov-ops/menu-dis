"""Эп.4 «Зачем директор?» (23.11, 12:40), ~24 с. Разгадка: директор увидел My School и хочет его для всех школ района.
Клиффхэнгер: в приёмной сидит другой парень с ноутбуком — тоже с приложением для школ. Голос Speko: Озодбек Dmitry, ноутбук cartesia.
Usage: reel_ep4.py voice_dir out.mp4 [--frames sheet.jpg]"""
import math, os, sys
from PIL import Image, ImageDraw, ImageFilter
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from reel_speko_kit import *
import reel_kit_ep1 as rk

VD, OUT = sys.argv[1], sys.argv[2]
SUBS = [("Директор вызвал меня в 8 утра. Мне 13. Что я натворил?!", "O"),
        ("Ничего. Он увидел твой My School и хочет его для всех школ района.", "L"),
        ("Для всех школ Юнусабада?! Мне 13, а у меня заказ на целый район!", "O"),
        ("Но в приёмной уже сидел парень с ноутбуком. Тоже с приложением для школ. Кто он?!", "O"),
        ("Серия 5 — завтра в 12:40. Подпишись!", "O")]
LINES = [(f"{VD}/e{i + 1}.wav", s, w) for i, (s, w) in enumerate(SUBS)]
DARK = rk.DARK
NIGHT = vgrad((8, 10, 30), (24, 22, 60)).convert("RGBA")
SKY = vgrad((120, 170, 230), (210, 225, 245)).convert("RGBA")
C = {m: character(m) for m in ("neutral", "happy", "shock")}
UP = character("happy", "up"); UP_SH = character("shock", "up")
Q = rk.qmark()

def school_bg():
    c = SKY.copy(); d = ImageDraw.Draw(c)
    d.rectangle([90, 620, 990, 1300], fill=(236, 214, 180)); d.polygon([(60, 630), (540, 450), (1020, 630)], fill=(190, 70, 60))
    for r in range(3):
        for k in range(5):
            x = 150 + k * 170; y = 700 + r * 190; d.rounded_rectangle([x, y, x + 110, y + 120], 10, fill=(140, 190, 240))
    d.rounded_rectangle([470, 1110, 610, 1300], 14, fill=(120, 80, 50))
    d.rectangle([0, 1300, W, H], fill=(120, 120, 130))
    return c
SCH = school_bg()

def s1(t, T):  # крючок: вызвали к директору
    c = SCH.copy()
    paste_c(c, pill(["Серия 4"], F("Bold", 40), (255, 255, 255), PUR + (255,), pad=(28, 12)), W / 2, 230, pop(t / .3))
    sh = math.sin(t * 40) * 8 if t < .9 else 0
    paste_c(c, pill(["Вызвали", "к директору"], F("Black", 96), (255, 255, 255), (220, 50, 50, 255)), W / 2 + sh, 420, pop(t / .3))
    paste_c(c, pill(["Четверг · 8:00"], F("Black", 52), (20, 20, 24), (255, 255, 255, 245)), W / 2, 640, pop((t - .4) / .3) if t > .4 else 0)
    paste_c(c, UP_SH, W / 2, 1230 + math.sin(t * 9) * 6, 0.95)
    return c

def myschool_phone(k):
    im, d = phone_frame("My School", "8 «Б» · сегодня")
    rows = [("Математика", "5", (52, 199, 89)), ("Физика", "4", (60, 150, 255)), ("Английский", "5", (52, 199, 89)), ("Домашка", "фото ✓", (255, 159, 10))]
    for i, (a, b, col) in enumerate(rows):
        if k > i * .2: card(d, 40, 230 + i * 170, 540, 140, a, b, col)
    return im

def s2(t, T):  # разгадка
    c = BG2.copy()
    paste_c(c, pill(["Разгадка"], F("Black", 64), (255, 236, 160), (0, 0, 0, 0)), W / 2, 250, pop(t / .3))
    paste_c(c, myschool_phone(t / (T * .6)), 340, 900, 0.95)
    paste_c(c, LAP[("smug", talking(t) and t < T - .4)], 800, 760, 0.62)
    if t > T * .5:
        paste_c(c, pill(["для ВСЕХ", "школ района"], F("Black", 54), (255, 255, 255), (52, 199, 89, 255)), 800, 1180, pop((t - T * .5) / .3))
    return c

def school_icon(n):
    im = Image.new("RGBA", (170, 170), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle([10, 60, 160, 160], 14, fill=(236, 214, 180)); d.polygon([(0, 66), (85, 8), (170, 66)], fill=(190, 70, 60))
    for k in range(3): d.rectangle([28 + k * 44, 84, 56 + k * 44, 112], fill=(140, 190, 240))
    d.text((70, 120), str(n), font=F("Black", 32), fill=(120, 80, 50))
    return im
ICONS = [school_icon(i + 1) for i in range(12)]

def s3(t, T):  # целый район
    c = DARK.copy()
    paste_c(c, pill(["Юнусабад"], F("Black", 78), (255, 255, 255), (0, 0, 0, 0)), W / 2, 260, pop(t / .3))
    for i in range(12):
        st = .15 + i * (T * .55 / 12)
        if t > st: paste_c(c, ICONS[i], 165 + (i % 4) * 250, 470 + (i // 4) * 200, 0.95 * pop((t - st) / .25))
    if t > T * .65: paste_c(c, pill(["Мне 13 — заказ на район!"], F("Black", 50), (20, 20, 24), (255, 236, 160, 255)), W / 2, 1110, pop((t - T * .65) / .3))
    paste_c(c, UP, W / 2, 1420, 0.55)
    return c

def silhouette():
    ch = character("neutral")
    a = ch.split()[3]; sil = Image.new("RGBA", ch.size, (14, 12, 26, 255)); sil.putalpha(a)
    return sil
SIL = silhouette()

def s4(t, T):  # клиффхэнгер
    c = NIGHT.copy(); d = ImageDraw.Draw(c)
    d.rounded_rectangle([90, 300, 520, 380], 20, fill=(40, 36, 70))
    d.text((120, 312), "ПРИЁМНАЯ", font=F("Black", 46), fill=(200, 200, 230))
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0)); gd = ImageDraw.Draw(glow)
    gd.ellipse([520, 760, 1020, 1260], fill=(110, 70, 255, 90)); c.alpha_composite(glow.filter(ImageFilter.GaussianBlur(60)))
    k = ease(t / .8)
    paste_c(c, SIL, 770, 1100, 0.85)
    lap = Image.new("RGBA", (300, 190), (0, 0, 0, 0)); ld = ImageDraw.Draw(lap)
    ld.rounded_rectangle([20, 0, 280, 160], 14, fill=(30, 30, 40)); ld.rounded_rectangle([34, 14, 266, 146], 8, fill=(150, 120, 255))
    ld.rectangle([0, 160, 300, 186], fill=(60, 60, 75))
    paste_c(c, lap, 770, 1330, 1.0)
    for i, (x, y) in enumerate([(580, 880), (1010, 820)]):
        if t > .6 + i * .2: paste_c(c, Q, x, y + math.sin(t * 3 + i) * 12, 0.6 * pop((t - .6 - i * .2) / .3))
    if t > T * .55: paste_c(c, pill(["Кто он?!"], F("Black", 96), (255, 255, 255), (220, 50, 50, 255)), W / 2, 500, pop((t - T * .55) / .3))
    paste_c(c, C["shock"], 260 - 60 * (1 - k), 1240, 0.62)
    return c

def s5(t, T):
    c = DARK.copy()
    paste_c(c, pill(["Кто этот парень?"], F("Black", 80), (255, 255, 255), (0, 0, 0, 0)), W / 2, 320, pop(t / .3))
    paste_c(c, SIL, 300, 820, 0.5); paste_c(c, C["shock"], 780, 820, 0.5)
    paste_c(c, pill(["Серия 5 — завтра в 12:40"], F("Black", 58), (255, 236, 160), (0, 0, 0, 0)), W / 2, 1200, pop((t - .3) / .3) if t > .3 else 0)
    if t > .9: paste_c(c, pill(["Подпишись, чтобы не пропустить"], F("Bold", 44), (255, 255, 255), PUR + (255,)), W / 2, 1320, pop((t - .9) / .3))
    if t > 1.5: paste_c(c, pill(["Своё приложение? Пришлите ТЗ · +998 90 970 06 03"], F("SemiBold", 32), (200, 200, 215), (0, 0, 0, 0)), W / 2, 1430, 1, min(1, (t - 1.5) / .3))
    return c

if __name__ == "__main__":
    fr = sys.argv[sys.argv.index("--frames") + 1] if "--frames" in sys.argv else False
    make_reel(LINES, [s1, s2, s3, s4, s5], OUT, os.path.dirname(os.path.abspath(OUT)) + "/ep4_scenes", seed=71, frames=fr, tail=2.2)
