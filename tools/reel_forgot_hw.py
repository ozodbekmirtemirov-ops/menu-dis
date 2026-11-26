"""r2 26.11 (20:10, главный): узнаваемая ситуация + витрина My Week «22:00. Мама: „Домашку сделал?“» ~22 с.
Аудитория: школьники и родители Ташкента. Повод переслать: «Отправь другу, который вечно всё забывает».
Usage: reel_forgot_hw.py voice_dir out.mp4 [--frames sheet.jpg]"""
import math, os, sys
from PIL import Image, ImageDraw
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from reel_speko_kit import *
import reel_kit_ep1 as rk

VD, OUT = sys.argv[1], sys.argv[2]
SUBS = [("22:00. Мама: «Домашку сделал?» А я про неё забыл!", "O"),
        ("Классика. Домашка, кружок, подарок другу — всё в голове. И всё забыто.", "L"),
        ("Теперь всё в My Week: дела по дням и напоминание в 17:00.", "O"),
        ("И в 22:00 мама спрашивает — а у тебя уже всё с галочкой.", "L"),
        ("Отправь другу, который вечно всё забывает!", "O")]
LINES = [(f"{VD}/w{i + 1}.wav", s, w) for i, (s, w) in enumerate(SUBS)]
NIGHT = vgrad((10, 12, 34), (30, 26, 70)).convert("RGBA")
DARK = rk.DARK
SH = character("shock"); HP_PH = character("happy", "phone"); WAVE = character("happy", "wave"); UP = character("happy", "up")
RED = (220, 50, 50); GRN = (52, 199, 89)
NOTES = [rk.sticky("Домашка\nалгебра", (255, 230, 110), 8), rk.sticky("Кружок\n16:00", (170, 230, 255), -9),
         rk.sticky("Подарок\nАзизу", (255, 180, 200), 6), rk.sticky("Вернуть\nкнигу", (200, 240, 170), -5)]
NPOS = [(250, 470), (820, 450), (300, 860), (800, 860)]
TASKS = [("15:00", "Алгебра: №145–148", (255, 190, 60)), ("16:00", "Кружок робототехники", (60, 150, 255)),
         ("17:00", "Подарок Азизу", (255, 120, 160)), ("18:00", "Вернуть книгу", (90, 200, 120))]

def week_phone(k, checks):
    im, d = phone_frame("MY WEEK", "Четверг · 4 дела")
    for i, dy in enumerate(rk.DAYS):
        x = 54 + i * 74; act = i == 3
        d.rounded_rectangle([x, 220, x + 62, 300], 20, fill=(20, 20, 24) if act else (234, 234, 240))
        f = F("SemiBold", 26); tw, th, oy = text_size(d, dy, f)
        d.text((x + 31 - tw / 2, 246 - oy), dy, font=f, fill=(255, 255, 255) if act else (90, 90, 100))
    for i, (tm, s, col) in enumerate(TASKS):
        if k <= i * .2: break
        y = 340 + i * 170
        d.rounded_rectangle([40, y, 580, y + 150], 28, fill=(255, 255, 255), outline=(230, 230, 236), width=2)
        d.rounded_rectangle([62, y + 26, 72, y + 124], 5, fill=col)
        d.text((94, y + 22), tm, font=F("SemiBold", 28), fill=(150, 150, 160))
        d.text((94, y + 66), s, font=F("Bold", 34), fill=(20, 20, 24))
        bx = 500; done = checks > i
        d.ellipse([bx, y + 45, bx + 60, y + 105], fill=GRN if done else None, outline=GRN if done else (200, 200, 210), width=5)
        if done: d.line([(bx + 15, y + 76), (bx + 27, y + 89), (bx + 47, y + 62)], fill=(255, 255, 255), width=7)
    if checks >= 4:
        d.rounded_rectangle([40, 1030, 580, 1110], 26, fill=(20, 20, 24))
        f = F("Bold", 32); s = "Выполнено 4 из 4"; tw, th, oy = text_size(d, s, f)
        d.text((310 - tw / 2, 1070 - th / 2 - oy), s, font=f, fill=(255, 255, 255))
    return im

def notif(txt1, txt2):
    b = Image.new("RGBA", (900, 200), (0, 0, 0, 0)); d = ImageDraw.Draw(b)
    d.rounded_rectangle([0, 0, 899, 199], 40, fill=(255, 255, 255, 250))
    paste_c(b, rk.app_icon(96), 78, 100)
    d.text((150, 34), txt1, font=F("SemiBold", 30), fill=(140, 140, 150))
    d.text((150, 86), txt2, font=F("Black", 46), fill=(20, 20, 24))
    return b

def clock(c, s, x=W / 2, y=290, col=(255, 255, 255)):
    paste_c(c, pill([s], F("Black", 120), col, (0, 0, 0, 0)), x, y)

def s1(t, T):  # крючок
    c = NIGHT.copy(); clock(c, "22:00", y=250)
    sh = math.sin(t * 40) * 9 if t < .8 else 0
    paste_c(c, pill(["Мама:", "«Домашку сделал?»"], F("Black", 78), (20, 20, 24), (255, 255, 255, 255), colors=[(120, 120, 130), (20, 20, 24)]), W / 2 + sh, 520, pop(t / .3))
    paste_c(c, SH, W / 2, 1130 + math.sin(t * 10) * 6, 0.72)
    if t > .9: paste_c(c, pill(["ЗАБЫЛ!"], F("Black", 90), (255, 255, 255), RED + (255,)), 820, 900, pop((t - .9) / .3))
    return c

def s2(t, T):  # хаос в голове
    c = DARK.copy()
    paste_c(c, pill(["Всё в голове"], F("Black", 76), (255, 255, 255), PUR + (255,)), W / 2, 230, pop(t / .3))
    d = ImageDraw.Draw(c)
    for i, (n, (x, y)) in enumerate(zip(NOTES, NPOS)):
        if t > i * T * .14:
            paste_c(c, n, x + math.sin(t * 3 + i) * 10, y + math.cos(t * 2.5 + i) * 10, 1.1, min(1, (t - i * T * .14) / .25))
            if t > T * .65:
                xx, yy = x, y; d.line([xx - 110, yy - 110, xx + 110, yy + 110], fill=RED, width=16); d.line([xx + 110, yy - 110, xx - 110, yy + 110], fill=RED, width=16)
    paste_c(c, LAP[("smug", talking(t) and t < T - .4)], W / 2, 1240, 0.5)
    return c

def s3(t, T):  # My Week
    c = radial((10, 10, 16), (20, 70, 140), cy=0.42, r=1000).convert("RGBA")
    paste_c(c, week_phone(t / (T * .7), 0), 360, 760, 0.95, min(1, t / .3))
    if t > T * .55: paste_c(c, notif("My Week · 17:00", "Сделай домашку!"), W / 2, 260 - 40 * (1 - ease((t - T * .55) / .3)), 1, min(1, (t - T * .55) / .3))
    paste_c(c, HP_PH, 900, 1150, 0.42)
    return c

def s4(t, T):  # 22:00 — всё с галочкой
    c = NIGHT.copy(); clock(c, "22:00", 300, 200, (255, 236, 160))
    paste_c(c, week_phone(1, int(t / (T * .5) * 4) if t < T * .5 else 4), 360, 860, 0.85)
    paste_c(c, pill(["«Сделал", "ещё в 18:00»"], F("Black", 56), (20, 20, 24), (255, 255, 255, 255)), 830, 520, pop((t - .3) / .3) if t > .3 else 0)
    paste_c(c, UP, 870, 1150 + math.sin(t * 8) * 6, 0.45)
    return c

def s5(t, T):
    c = DARK.copy()
    paste_c(c, pill(["Отправь другу,", "который вечно", "всё забывает"], F("Black", 86), (255, 255, 255), (0, 0, 0, 0), colors=[(255, 255, 255), (255, 255, 255), (255, 236, 160)]), W / 2, 400, pop(t / .3))
    paste_c(c, WAVE, W / 2, 1010, 0.58)
    if t > .6: paste_c(c, pill(["Своё приложение? Пришлите ТЗ"], F("Bold", 46), (255, 255, 255), PUR + (255,)), W / 2, 1380, pop((t - .6) / .3))
    if t > 1.0: paste_c(c, pill(["+998 90 970 06 03"], F("SemiBold", 38), (200, 200, 215), (0, 0, 0, 0)), W / 2, 1480, 1, min(1, (t - 1) / .3))
    return c

if __name__ == "__main__":
    fr = sys.argv[sys.argv.index("--frames") + 1] if "--frames" in sys.argv else False
    make_reel(LINES, [s1, s2, s3, s4, s5], OUT, os.path.dirname(os.path.abspath(OUT)) + "/hw_scenes", seed=203, frames=fr, tail=1.4)
