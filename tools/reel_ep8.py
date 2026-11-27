"""Эп.8 «Код прислал директор» (27.11, 12:40, ПТ вечер), ~25 с. Разгадка тизера 26.11 («ты его знаешь»): код сопернику
прислал САМ директор — проверял, кто понимает приложение, а кто копирует. Решение: My School для района делает Озодбек,
соперник — в его команде. Клиффхэнгер: новая задача в My Week «Суббота, 10:00. Узнаешь, кто я», добавлено не тобой и не
ноутбуком → эп.9 (СБ) раскрывает, кто ставил задачи всю неделю. Usage: reel_ep8.py voice_dir out.mp4 [--frames sheet.jpg]"""
import math, os, sys
from PIL import Image, ImageDraw, ImageFilter
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from reel_speko_kit import *
from school_game_ui import qr
import reel_kit_ep1 as rk

VD, OUT = sys.argv[1], sys.argv[2]
SUBS = [("Код сопернику прислал… сам директор?!", "O"),
        ("Да. Он хотел проверить: кто понимает приложение, а кто просто копирует.", "L"),
        ("И решение: My School для всего района делаю я! А соперник — в моей команде.", "O"),
        ("Неплохо для пятницы. Но смотри: в My Week новая задача. Добавлено — не тобой. И не мной.", "L"),
        ("«Суббота, 10:00. Узнаешь, кто я». Кто это?! Серия 9 — завтра в 12:40.", "O")]
LINES = [(f"{VD}/e{i + 1}.wav", s, w) for i, (s, w) in enumerate(SUBS)]
HALL = vgrad((30, 24, 52), (12, 10, 26)).convert("RGBA")
NIGHT = vgrad((8, 10, 30), (24, 22, 60)).convert("RGBA")
GLOW = radial((8, 16, 12), (30, 110, 70), cy=0.4, r=1000).convert("RGBA")
C = {m: character(m) for m in ("neutral", "happy", "shock")}
UP_SH = character("shock", "up"); UP_HP = character("happy", "up"); PH = character("shock", "phone")
ch = character("neutral"); SIL = Image.new("RGBA", ch.size, (14, 12, 26, 255)); SIL.putalpha(ch.split()[3])
RED = (220, 50, 50); GRN = (52, 199, 89)

def day(c, s="ПТ · вечер"):
    paste_c(c, pill([s], F("Bold", 34), (20, 20, 24), (255, 236, 160, 255), pad=(24, 10)), 170, 120)
    paste_c(c, pill(["Серия 8"], F("Bold", 34), (255, 255, 255), PUR + (255,), pad=(24, 10)), W - 150, 120)

def mail(k):  # письмо «от: Директор»
    im = Image.new("RGBA", (860, 300), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, 859, 299], 36, fill=(255, 255, 255, 250))
    d.rounded_rectangle([36, 36, 136, 136], 24, fill=(255, 236, 160)); d.polygon([(52, 60), (120, 60), (86, 96)], outline=(20, 20, 24), width=5); d.rectangle([52, 60, 120, 112], outline=(20, 20, 24), width=5)
    d.text((170, 40), "От: Директор школы", font=F("Black", 44), fill=(20, 20, 24))
    d.text((170, 100), "Кому: сопернику", font=F("SemiBold", 34), fill=(140, 140, 150))
    if k > .4: d.text((40, 190), "Вложение: my_school_code.zip", font=F("Bold", 42), fill=PUR)
    return im

def s1(t, T):  # крючок
    c = HALL.copy(); day(c)
    sh = math.sin(t * 40) * 10 if t < .9 else 0
    paste_c(c, pill(["Код прислал…", "ДИРЕКТОР?!"], F("Black", 104), (255, 255, 255), RED + (255,), colors=[(255, 255, 255), (255, 236, 160)]), W / 2 + sh, 420, pop(t / .3))
    paste_c(c, mail(t / .8), W / 2, 760, 0.85, min(1, t / .4))
    paste_c(c, UP_SH, W / 2, 1220 + math.sin(t * 9) * 6, 0.68)
    return c

def test_card(k):
    im = Image.new("RGBA", (920, 560), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, 919, 559], 40, fill=(255, 252, 240))
    d.text((44, 30), "Проверка директора", font=F("Bold", 42), fill=(200, 110, 0))
    rows = [("Понимает, ЗАЧЕМ кнопка", "Озодбек", GRN, "✓"), ("Просто копирует код", "соперник", RED, "✗")]
    for i, (a, b, col, m) in enumerate(rows):
        if k > .2 + i * .35:
            y = 130 + i * 200
            d.rounded_rectangle([30, y, 889, y + 170], 30, fill=(255, 255, 255), outline=(230, 230, 236), width=3)
            d.ellipse([60, y + 35, 160, y + 135], fill=col); d.text((88, y + 38), m, font=F("Black", 70), fill=(255, 255, 255))
            d.text((190, y + 28), a, font=F("Black", 46), fill=(20, 20, 24))
            d.text((190, y + 96), b, font=F("SemiBold", 38), fill=col)
    return im

def s2(t, T):
    c = HALL.copy(); day(c)
    paste_c(c, test_card(t / (T * .7)), W / 2, 560, 1, min(1, t / .3))
    paste_c(c, LAP[("smug", talking(t) and t < T - .4)], W / 2, 1210, 0.6)
    return c

def s3(t, T):  # решение
    c = GLOW.copy(); day(c)
    paste_c(c, pill(["Решение директора"], F("Bold", 50), (20, 20, 24), (255, 236, 160, 255)), W / 2, 280, pop(t / .3))
    if t > .4: paste_c(c, pill(["My School —", "для всего района"], F("Black", 88), (255, 255, 255), GRN + (255,)), W / 2, 490, pop((t - .4) / .3))
    if t > T * .55: paste_c(c, pill(["Команда: Озодбек + соперник"], F("Bold", 48), (255, 255, 255), PUR + (255,)), W / 2, 730, pop((t - T * .55) / .3))
    paste_c(c, UP_HP, 380, 1200 + math.sin(t * 8) * 6, 0.62)
    paste_c(c, SIL, 760, 1220, 0.58)
    return c

def notif(k):
    b = Image.new("RGBA", (940, 280), (0, 0, 0, 0)); d = ImageDraw.Draw(b)
    d.rounded_rectangle([0, 0, 939, 279], 40, fill=(255, 255, 255, 250))
    paste_c(b, rk.app_icon(96), 82, 82)
    d.text((150, 30), "My Week · ПТ 21:47", font=F("SemiBold", 30), fill=(140, 140, 150))
    d.text((150, 72), "Суббота, 10:00.", font=F("Black", 48), fill=(20, 20, 24))
    d.text((150, 132), "Узнаешь, кто я.", font=F("Black", 48), fill=PUR)
    if k > .5: d.text((150, 206), "добавлено: не тобой", font=F("SemiBold", 34), fill=RED)
    return b

def s4(t, T):
    c = NIGHT.copy(); day(c, "ПТ · 21:47")
    paste_c(c, notif(t / (T * .5)), W / 2, 420 - 60 * (1 - ease(t / .4)), 1, min(1, t / .3))
    paste_c(c, LAP[("wide", talking(t) and t < T - .4)], 330, 1080, 0.55)
    paste_c(c, PH, 790, 1120, 0.6)
    if t > T * .72: paste_c(c, pill(["И НЕ ноутбуком"], F("Black", 64), (255, 255, 255), RED + (255,)), W / 2, 1450, pop((t - T * .72) / .3))
    return c

def s5(t, T):  # клиффхэнгер
    c = NIGHT.copy(); day(c, "ПТ · 21:47")
    paste_c(c, pill(["«Узнаешь, кто я»"], F("Black", 80), (20, 20, 24), (255, 255, 255, 255)), W / 2, 330, pop(t / .3))
    if t > .9: paste_c(c, pill(["Кто это?!"], F("Black", 100), (255, 255, 255), RED + (255,)), W / 2, 560, pop((t - .9) / .3))
    paste_c(c, rk.qmark(), 820, 860 + math.sin(t * 3) * 12, 0.6)
    paste_c(c, UP_SH, 360, 950 + math.sin(t * 9) * 6, 0.5)
    if t > 2.0: paste_c(c, pill(["Серия 9 — завтра в 12:40"], F("Black", 58), (255, 236, 160), (0, 0, 0, 0)), W / 2, 1250, pop((t - 2.0) / .3))
    if t > 2.6: paste_c(c, pill(["Подпишись, чтобы не пропустить"], F("Bold", 44), (255, 255, 255), PUR + (255,)), W / 2, 1370, pop((t - 2.6) / .3))
    if t > 3.1: paste_c(c, pill(["Своё приложение? Пришлите ТЗ · +998 90 970 06 03"], F("SemiBold", 32), (200, 200, 215), (0, 0, 0, 0)), W / 2, 1475, 1, min(1, (t - 3.1) / .3))
    return c

if __name__ == "__main__":
    fr = sys.argv[sys.argv.index("--frames") + 1] if "--frames" in sys.argv else False
    make_reel(LINES, [s1, s2, s3, s4, s5], OUT, os.path.dirname(os.path.abspath(OUT)) + "/ep8_scenes", seed=223, frames=fr, tail=0.9)
