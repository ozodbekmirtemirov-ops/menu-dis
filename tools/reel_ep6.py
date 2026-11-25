"""Эп.6 «Что он НЕ скопировал» (25.11, 12:40, ЧТ вечер), ~23 с. Разгадка: соперник скопировал код, но не ТЗ — он не знает,
зачем игра и QR (учитель включает игру, класс сканирует QR, даже двоечник старается; результаты видят завуч и директор).
Клиффхэнгер: в My Week задача «Пятница: педсовет. Не бойся» — её поставил НЕ ноутбук. Тогда кто? (разгадка в эп.9)
Голос Speko: Озодбек Dmitry, ноутбук cartesia (atempo 1.08). Usage: reel_ep6.py voice_dir out.mp4 [--frames sheet.jpg]"""
import math, os, sys
from PIL import Image, ImageDraw, ImageFilter
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from reel_speko_kit import *
from school_game_ui import qr, game_phone, admin_phone, class_row, ORG, GRN
import reel_kit_ep1 as rk

VD, OUT = sys.argv[1], sys.argv[2]
SUBS = [("Он скопировал весь мой код. Так что же он НЕ скопировал?", "O"),
        ("ТЗ. Ты месяц слушал учителей: зачем игра, зачем QR-код. А он этого не знает.", "L"),
        ("Точно! Учитель включает игру, класс сканирует QR — и даже двоечник старается.", "O"),
        ("Стоп. Задачу «Пятница: педсовет. Не бойся» поставил не я.", "L"),
        ("Тогда кто?! Серия 7 — завтра в 12:40.", "O")]
FILES = ["fe1", "fe2", "fe3", "fe5", "fe6"]
LINES = [(f"{VD}/{f}.wav", s, w) for f, (s, w) in zip(FILES, SUBS)]
DARK = rk.DARK
NIGHT = vgrad((8, 10, 30), (24, 22, 60)).convert("RGBA")
CLASS = vgrad((40, 70, 60), (20, 36, 30)).convert("RGBA")
C = {m: character(m) for m in ("neutral", "happy", "shock")}
UP_SH = character("shock", "up"); UP_HP = character("happy", "up")
Q = rk.qmark()
ch = character("neutral"); SIL = Image.new("RGBA", ch.size, (14, 12, 26, 255)); SIL.putalpha(ch.split()[3])
QR = qr(380)

def day(c, s="ЧТ · вечер"):
    paste_c(c, pill([s], F("Bold", 34), (20, 20, 24), (255, 236, 160, 255), pad=(24, 10)), 150, 120)
    paste_c(c, pill(["Серия 6"], F("Bold", 34), (255, 255, 255), PUR + (255,), pad=(24, 10)), W - 150, 120)

def s1(t, T):  # крючок
    c = NIGHT.copy(); day(c)
    sh = math.sin(t * 40) * 8 if t < .8 else 0
    paste_c(c, pill(["Что он", "НЕ скопировал?"], F("Black", 100), (255, 255, 255), (220, 50, 50, 255)), W / 2 + sh, 430, pop(t / .3))
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0)); gd = ImageDraw.Draw(glow)
    gd.ellipse([520, 760, 1080, 1340], fill=(220, 60, 80, 90)); c.alpha_composite(glow.filter(ImageFilter.GaussianBlur(60)))
    paste_c(c, SIL, 820, 1080, 0.62)
    paste_c(c, C["shock"], 300, 1150 + math.sin(t * 9) * 5, 0.8)
    return c

def tz_card(k):
    im = Image.new("RGBA", (900, 640), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, 899, 639], 34, fill=(255, 252, 240))
    d.text((44, 30), "ТЗ от учителей", font=F("Black", 54), fill=(20, 20, 24))
    rows = [("Зачем игра?", "чтобы урок был интересным"), ("Зачем QR?", "вход за 2 секунды"), ("Кто видит итоги?", "завуч и директор")]
    for i, (a, b) in enumerate(rows):
        if k > i * .28:
            y = 130 + i * 165
            d.rounded_rectangle([30, y, 870, y + 145], 24, fill=(255, 255, 255), outline=(235, 225, 200), width=2)
            d.text((60, y + 16), a, font=F("Black", 42), fill=(200, 110, 0)); d.text((60, y + 76), b, font=F("Bold", 40), fill=(40, 40, 50))
    return im

def s2(t, T):
    c = BG2.copy(); day(c)
    paste_c(c, tz_card(t / (T * .7)), W / 2, 580, 1, min(1, t / .3))
    paste_c(c, LAP[("smug", talking(t) and t < T - .4)], 290, 1230, 0.55)
    if t > T * .6: paste_c(c, pill(["Этого нет", "в коде"], F("Black", 64), (255, 255, 255), (220, 50, 50, 255)), 760, 1180, pop((t - T * .6) / .3))
    return c

def s3(t, T):  # как работает My School
    c = CLASS.copy(); day(c)
    paste_c(c, pill(["Урок = игра по QR"], F("Black", 70), (255, 255, 255), ORG + (255,)), W / 2, 260, pop(t / .3))
    paste_c(c, QR, 290, 640, 0.9, min(1, t / .3))
    paste_c(c, game_phone(t / (T * .8)), 790, 700, 0.56)
    paste_c(c, class_row(t / (T * .7)), W / 2, 1230, 0.9)
    if t > T * .5: paste_c(c, pill(["Даже двоечник старается!"], F("Black", 56), (20, 20, 24), (255, 236, 160, 255)), W / 2, 1420, pop((t - T * .5) / .3))
    return c

def notif(k):
    b = Image.new("RGBA", (940, 270), (0, 0, 0, 0)); d = ImageDraw.Draw(b)
    d.rounded_rectangle([0, 0, 939, 269], 40, fill=(255, 255, 255, 250))
    paste_c(b, rk.app_icon(96), 82, 82)
    d.text((150, 30), "My Week · 23:00", font=F("SemiBold", 30), fill=(140, 140, 150))
    d.text((150, 72), "Пятница: педсовет.", font=F("Black", 46), fill=(20, 20, 24))
    d.text((150, 128), "Не бойся.", font=F("Black", 46), fill=PUR)
    d.text((150, 200), "добавлено: не тобой", font=F("SemiBold", 32), fill=(230, 60, 70))
    return b

def s4(t, T):  # клиффхэнгер
    c = NIGHT.copy(); day(c, "ЧТ · 23:00")
    paste_c(c, notif(1), W / 2, 420 - 60 * (1 - ease(t / .4)), 1, min(1, t / .3))
    paste_c(c, LAP[("wide", talking(t) and t < T - .4)], W / 2, 1060, 0.8)
    if t > T * .55: paste_c(c, pill(["Это НЕ ноутбук"], F("Black", 70), (255, 255, 255), (220, 50, 50, 255)), W / 2, 1430, pop((t - T * .55) / .3))
    return c

def s5(t, T):
    c = NIGHT.copy(); day(c, "ЧТ · 23:00")
    paste_c(c, pill(["Тогда кто?!"], F("Black", 110), (255, 255, 255), (220, 50, 50, 255)), W / 2, 330, pop(t / .3))
    paste_c(c, Q, 840, 640 + math.sin(t * 3) * 12, 0.7)
    paste_c(c, UP_SH, W / 2 - 80, 900, 0.5)
    paste_c(c, pill(["Серия 7 — завтра в 12:40"], F("Black", 58), (255, 236, 160), (0, 0, 0, 0)), W / 2, 1200, pop((t - .3) / .3) if t > .3 else 0)
    if t > .9: paste_c(c, pill(["Подпишись, чтобы не пропустить"], F("Bold", 44), (255, 255, 255), PUR + (255,)), W / 2, 1320, pop((t - .9) / .3))
    if t > 1.5: paste_c(c, pill(["Своё приложение? Пришлите ТЗ · +998 90 970 06 03"], F("SemiBold", 32), (200, 200, 215), (0, 0, 0, 0)), W / 2, 1430, 1, min(1, (t - 1.5) / .3))
    return c

if __name__ == "__main__":
    fr = sys.argv[sys.argv.index("--frames") + 1] if "--frames" in sys.argv else False
    make_reel(LINES, [s1, s2, s3, s4, s5], OUT, os.path.dirname(os.path.abspath(OUT)) + "/ep6_scenes", seed=163, frames=fr, tail=2.2)
