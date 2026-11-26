"""Эп.7 «Один вопрос директора» (26.11, 12:40, ПТ — педсовет), ~25 с. Разгадка тизера 25.11: директор задаёт ОДИН вопрос —
«учителя химии хотят свою игру, сколько займёт?» — соперник молчит, Озодбек отвечает «один вечер» (знает ТЗ: учитель пишет
вопросы, тот же QR). Решение директора — вечером (эп.8). Клиффхэнгер: соперник «Я не крал твой код. Мне его ПРИСЛАЛИ». Кто?
Загадку «Не бойся»/«Среда, 15:00» НЕ раскрываем (эп.9). Usage: reel_ep7.py voice_dir out.mp4 [--frames sheet.jpg]"""
import math, os, sys
from PIL import Image, ImageDraw, ImageFilter
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from reel_speko_kit import *
from school_game_ui import qr, ORG, GRN
import reel_kit_ep1 as rk

VD, OUT = sys.argv[1], sys.argv[2]
SUBS = [("Педсовет. Директор задал один вопрос — и он молчит!", "O"),
        ("Вопрос был такой: учителя химии хотят свою игру. Сколько это займёт?", "L"),
        ("Один вечер! Учитель пишет свои вопросы, класс сканирует тот же QR-код — и всё.", "O"),
        ("Директор улыбнулся: решение — вечером. Но смотри, соперник идёт к тебе.", "L"),
        ("Он сказал: «Я не крал твой код. Мне его прислали». Кто?! Серия 8 — завтра в 12:40.", "O")]
LINES = [(f"{VD}/e{i + 1}.wav", s, w) for i, (s, w) in enumerate(SUBS)]
HALL = vgrad((30, 24, 52), (12, 10, 26)).convert("RGBA")
NIGHT = vgrad((8, 10, 30), (24, 22, 60)).convert("RGBA")
C = {m: character(m) for m in ("neutral", "happy", "shock")}
UP_SH = character("shock", "up"); UP_HP = character("happy", "up")
Q = rk.qmark()
ch = character("neutral"); SIL = Image.new("RGBA", ch.size, (14, 12, 26, 255)); SIL.putalpha(ch.split()[3])
QR = qr(300, seed=21)
RED = (220, 50, 50)

def day(c, s="ПТ · педсовет"):
    paste_c(c, pill([s], F("Bold", 34), (20, 20, 24), (255, 236, 160, 255), pad=(24, 10)), 170, 120)
    paste_c(c, pill(["Серия 7"], F("Bold", 34), (255, 255, 255), PUR + (255,), pad=(24, 10)), W - 150, 120)

def table(c):
    d = ImageDraw.Draw(c); d.rounded_rectangle([60, 1330, W - 60, 1420], 20, fill=(90, 60, 40)); d.rectangle([60, 1380, W - 60, 1420], fill=(70, 45, 30))

def bubble(lines, size=50, fg=(20, 20, 24), bg=(255, 255, 255, 255)):
    return pill(lines, F("Black", size), fg, bg, pad=(36, 22))

def s1(t, T):  # крючок: он молчит
    c = HALL.copy(); day(c)
    sh = math.sin(t * 40) * 9 if t < .8 else 0
    paste_c(c, pill(["Один вопрос —", "и он МОЛЧИТ"], F("Black", 96), (255, 255, 255), RED + (255,)), W / 2 + sh, 420, pop(t / .3))
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0)); gd = ImageDraw.Draw(glow)
    gd.ellipse([540, 760, 1060, 1300], fill=(220, 60, 80, 80)); c.alpha_composite(glow.filter(ImageFilter.GaussianBlur(60)))
    paste_c(c, SIL, 810, 1060, 0.6)
    if t > .5: paste_c(c, bubble(["…"], 70), 820, 700, pop((t - .5) / .3))
    paste_c(c, C["shock"], 290, 1080 + math.sin(t * 9) * 5, 0.72)
    table(c)
    return c

def qcard(k):
    im = Image.new("RGBA", (900, 520), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, 899, 519], 34, fill=(255, 252, 240))
    d.text((44, 32), "Вопрос директора", font=F("Bold", 40), fill=(200, 110, 0))
    lines = ["Учителя химии хотят", "свою игру.", "Сколько это займёт?"]
    for i, s in enumerate(lines):
        if k > i * .25: d.text((44, 120 + i * 120), s, font=F("Black", 62), fill=(20, 20, 24) if i < 2 else RED)
    return im

def s2(t, T):
    c = HALL.copy(); day(c)
    paste_c(c, qcard(t / (T * .6)), W / 2, 520, 1, min(1, t / .3))
    paste_c(c, LAP[("wide", talking(t) and t < T - .4)], 300, 1150, 0.55)
    paste_c(c, SIL, 820, 1120, 0.5)
    if t > T * .55: paste_c(c, bubble(["…"], 60), 830, 860, pop((t - T * .55) / .3))
    table(c)
    return c

def s3(t, T):  # ответ Озодбека
    c = radial((8, 16, 12), (30, 110, 70), cy=0.4, r=1000).convert("RGBA"); day(c)
    paste_c(c, pill(["Один вечер!"], F("Black", 110), (20, 20, 24), (255, 236, 160, 255)), W / 2, 300, pop(t / .3))
    steps = [("1", "Учитель пишет вопросы"), ("2", "Тот же QR-код"), ("3", "Класс играет")]
    for i, (n, s) in enumerate(steps):
        kk = (t - .4 - i * T * .18) / .3
        if kk > 0: paste_c(c, pill([f"{n}. {s}"], F("Bold", 50), (20, 20, 24), (255, 255, 255, 250), pad=(34, 18)), 650, 520 + i * 120, pop(kk))
    paste_c(c, QR, 150, 640, 0.48, min(1, t / .4))
    paste_c(c, UP_HP, W / 2, 1150 + math.sin(t * 8) * 6, 0.62)
    return c

def s4(t, T):  # решение вечером + соперник идёт
    c = HALL.copy(); day(c)
    paste_c(c, pill(["Решение —", "вечером"], F("Black", 90), (255, 255, 255), PUR + (255,)), W / 2, 380, pop(t / .3))
    x = 900 - 260 * ease(t / T)
    paste_c(c, C["neutral"], 260, 1120, 0.62)
    paste_c(c, SIL, x, 1120, 0.62)
    paste_c(c, LAP[("smug", talking(t) and t < T - .4)], W / 2, 720, 0.4)
    table(c)
    return c

def s5(t, T):  # клиффхэнгер
    c = NIGHT.copy(); day(c, "ПТ · после педсовета")
    paste_c(c, bubble(["«Я не крал твой код.", "Мне его ПРИСЛАЛИ»"], 64), W / 2, 330, pop(t / .3))
    paste_c(c, SIL, 820, 900, 0.5)
    paste_c(c, UP_SH, 300, 920 + math.sin(t * 9) * 6, 0.5)
    if t > .8: paste_c(c, pill(["Кто?!"], F("Black", 100), (255, 255, 255), RED + (255,)), W / 2, 640, pop((t - .8) / .3))
    if t > 1.6: paste_c(c, pill(["Серия 8 — завтра в 12:40"], F("Black", 58), (255, 236, 160), (0, 0, 0, 0)), W / 2, 1250, pop((t - 1.6) / .3))
    if t > 2.2: paste_c(c, pill(["Подпишись, чтобы не пропустить"], F("Bold", 44), (255, 255, 255), PUR + (255,)), W / 2, 1370, pop((t - 2.2) / .3))
    if t > 2.8: paste_c(c, pill(["Своё приложение? Пришлите ТЗ · +998 90 970 06 03"], F("SemiBold", 32), (200, 200, 215), (0, 0, 0, 0)), W / 2, 1475, 1, min(1, (t - 2.8) / .3))
    return c

if __name__ == "__main__":
    fr = sys.argv[sys.argv.index("--frames") + 1] if "--frames" in sys.argv else False
    make_reel(LINES, [s1, s2, s3, s4, s5], OUT, os.path.dirname(os.path.abspath(OUT)) + "/ep7_scenes", seed=191, frames=fr, tail=1.2)
