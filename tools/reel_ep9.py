"""Эп.9 «Это был ТЫ?!» (28.11, 12:40, СБ), ~21 с. Разгадка тизера 27.11 («он был рядом с первого дня»): задачи «Не бойся»
и «Суббота, 10:00. Узнаешь, кто я» ставил ДРУГ — тот самый, что в эп.1 скинул My Week (у него был доступ к общей неделе),
он болел за Озодбека. («Среда, 15:00» — ноутбук, разгадано в эп.3.) Клиффхэнгер: друг принёс конверт «ТЗ. Открыть в
воскресенье» → «Финал — завтра в 12:40». Usage: reel_ep9.py voice_dir out.mp4 [--frames sheet.jpg]"""
import math, os, sys
from PIL import Image, ImageDraw
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from reel_speko_kit import *
import character_v2 as cv
import reel_kit_ep1 as rk

VD, OUT = sys.argv[1], sys.argv[2]
SUBS = [("Суббота, 10:00. Звонок в дверь… Это ТЫ?!", "O"),
        ("Это твой друг. Тот самый, что в понедельник скинул тебе My Week.", "L"),
        ("Так «Не бойся» и «Узнаешь, кто я» — это писал ты?! Всю неделю?!", "O"),
        ("Он болел за тебя. И принёс конверт: «ТЗ. Открыть в воскресенье».", "L"),
        ("Что внутри?! Финал — завтра в 12:40.", "O")]
LINES = [(f"{VD}/e{i + 1}.wav", s, w) for i, (s, w) in enumerate(SUBS)]
MORN = vgrad((60, 90, 150), (20, 30, 70)).convert("RGBA")
WARM = radial((20, 12, 8), (150, 90, 30), cy=0.42, r=1000).convert("RGBA")
NIGHT = vgrad((8, 10, 30), (24, 22, 60)).convert("RGBA")
UP_SH = character("shock", "up"); SH = character("shock"); HP = character("happy"); PH = character("shock", "phone")
RED = (220, 50, 50); GRN = (52, 199, 89); ORG = (255, 159, 10)

def friend(mood="happy", arms="wave"):
    """Друг: тот же рисовальщик, но оранжевое худи и кепка (чтобы не путать с героем)."""
    keep = (cv.HOOD, cv.HOOD_D, cv.HOOD_L)
    cv.HOOD, cv.HOOD_D, cv.HOOD_L = (255, 140, 40), (220, 110, 20), (255, 175, 90)
    try: im = cv.character(mood, arms)
    finally: cv.HOOD, cv.HOOD_D, cv.HOOD_L = keep
    d = ImageDraw.Draw(im); w = im.size[0]
    d.chord([w / 2 - 165, 40, w / 2 + 165, 330], 180, 360, fill=(30, 30, 40))
    d.rounded_rectangle([w / 2 - 20, 175, w / 2 + 230, 205], 14, fill=(30, 30, 40))
    return im
FR = friend(); FR_N = friend("neutral", "down")

def day(c, s="СБ · 10:00"):
    paste_c(c, pill([s], F("Bold", 34), (20, 20, 24), (255, 236, 160, 255), pad=(24, 10)), 170, 120)
    paste_c(c, pill(["Серия 9"], F("Bold", 34), (255, 255, 255), PUR + (255,), pad=(24, 10)), W - 150, 120)

def door(c, k):
    d = ImageDraw.Draw(c); x0, x1 = 600, 1000
    d.rectangle([x0 - 20, 640, x1 + 20, 1520], fill=(90, 60, 40))
    d.rectangle([x0, 660, x1, 1520], fill=(255, 230, 180))  # проём (свет)
    op = int((x1 - x0) * ease(min(1, k)))
    d.polygon([(x0 + op, 660), (x1, 660), (x1, 1520), (x0 + op, 1520)], fill=(140, 95, 60))

def s1(t, T):  # крючок
    c = MORN.copy(); day(c)
    door(c, t / .8)
    if t > .5: paste_c(c, FR, 800, 1240, 0.62, min(1, (t - .5) / .3))
    sh = math.sin(t * 40) * 10 if t < .9 else 0
    paste_c(c, pill(["Это был", "ТЫ?!"], F("Black", 120), (255, 255, 255), RED + (255,), colors=[(255, 255, 255), (255, 236, 160)]), W / 2 + sh, 400, pop(t / .3))
    paste_c(c, UP_SH, 320, 1250 + math.sin(t * 9) * 6, 0.66)
    return c

def s2(t, T):  # кто это
    c = WARM.copy(); day(c)
    paste_c(c, pill(["Друг из понедельника"], F("Black", 70), (20, 20, 24), (255, 236, 160, 255)), W / 2, 300, pop(t / .3))
    # чат эп.1: «лови приложение»
    if t > .5:
        b = Image.new("RGBA", (860, 210), (0, 0, 0, 0)); d = ImageDraw.Draw(b)
        d.rounded_rectangle([0, 0, 859, 209], 40, fill=(255, 255, 255, 250))
        paste_c(b, rk.app_icon(110), 90, 105)
        d.text((175, 34), "ПН · друг:", font=F("SemiBold", 32), fill=(140, 140, 150))
        d.text((175, 88), "Лови: My Week!", font=F("Black", 54), fill=(20, 20, 24))
        paste_c(c, b, W / 2, 540, 1, min(1, (t - .5) / .3))
    paste_c(c, FR, 330, 1180, 0.6)
    paste_c(c, LAP[("smug", talking(t) and t < T - .4)], 800, 1230, 0.5)
    return c

def task(txt, k):
    b = Image.new("RGBA", (900, 150), (0, 0, 0, 0)); d = ImageDraw.Draw(b)
    d.rounded_rectangle([0, 0, 899, 149], 34, fill=(255, 255, 255, 250))
    d.text((40, 22), txt, font=F("Black", 46), fill=(20, 20, 24))
    d.text((40, 88), "добавил: друг", font=F("Bold", 32), fill=ORG if k > .5 else (180, 180, 190))
    if k > .5: d.ellipse([800, 40, 870, 110], fill=ORG); d.text((815, 36), "✓", font=F("Black", 54), fill=(255, 255, 255))
    return b

def s3(t, T):  # разгадка задач
    c = NIGHT.copy(); day(c)
    paste_c(c, pill(["Кто ставил задачи"], F("Black", 64), (255, 255, 255), PUR + (255,)), W / 2, 270, pop(t / .3))
    for i, s in enumerate(["ЧТ · «Не бойся»", "ПТ · «Узнаешь, кто я»"]):
        st = .3 + i * .8
        if t > st: paste_c(c, task(s, (t - st) / .9), W / 2, 470 + i * 190, 1, min(1, (t - st) / .25))
    paste_c(c, SH, 330, 1270 + math.sin(t * 9) * 6, 0.6)
    paste_c(c, FR, 780, 1270, 0.58)
    return c

def envelope(k):
    im = Image.new("RGBA", (700, 460), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, 699, 459], 30, fill=(250, 240, 220))
    d.polygon([(0, 0), (699, 0), (350, 260)], fill=(235, 220, 190), outline=(200, 180, 150))
    d.ellipse([310, 220, 390, 300], fill=RED)
    d.text((222, 310), "ТЗ", font=F("Black", 110), fill=(20, 20, 24))
    return im

def s4(t, T):  # конверт
    c = WARM.copy(); day(c)
    paste_c(c, pill(["Он болел за тебя"], F("Black", 72), (255, 255, 255), GRN + (255,)), W / 2, 270, pop(t / .3))
    if t > .6: paste_c(c, envelope(1), W / 2, 620 + math.sin(t * 4) * 8, 0.95, pop((t - .6) / .3))
    if t > T * .55: paste_c(c, pill(["Открыть в воскресенье"], F("Black", 56), (20, 20, 24), (255, 236, 160, 255)), W / 2, 900, pop((t - T * .55) / .3))
    paste_c(c, FR_N, 330, 1300, 0.55)
    paste_c(c, LAP[("wide", talking(t) and t < T - .4)], 790, 1280, 0.48)
    return c

def s5(t, T):  # клиффхэнгер
    c = NIGHT.copy(); day(c, "СБ · вечер")
    paste_c(c, envelope(1), 720, 460 + math.sin(t * 3) * 10, 0.6)
    paste_c(c, rk.qmark(), 300, 440 + math.sin(t * 3 + 1) * 12, 0.5)
    if t > .2: paste_c(c, pill(["Что внутри?!"], F("Black", 100), (255, 255, 255), RED + (255,)), W / 2, 720, pop((t - .2) / .3))
    paste_c(c, PH, W / 2, 1040, 0.42)
    if t > 1.2: paste_c(c, pill(["ФИНАЛ — завтра в 12:40"], F("Black", 66), (255, 236, 160), (0, 0, 0, 0)), W / 2, 1330, pop((t - 1.2) / .3))
    if t > 1.8: paste_c(c, pill(["Подпишись, чтобы не пропустить"], F("Bold", 44), (255, 255, 255), PUR + (255,)), W / 2, 1450, pop((t - 1.8) / .3))
    return c

if __name__ == "__main__":
    fr = sys.argv[sys.argv.index("--frames") + 1] if "--frames" in sys.argv else False
    make_reel(LINES, [s1, s2, s3, s4, s5], OUT, os.path.dirname(os.path.abspath(OUT)) + "/ep9_scenes", seed=251, frames=fr, tail=2.0)
