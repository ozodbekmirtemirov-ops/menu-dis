"""POV «Клиент прислал ТЗ из одной строки» (21.11, 16:10): Озодбек (Dmitry) + ноутбук (cartesia). Usage: reel_pov_tz.py voice_dir out.mp4 [--frames x.jpg]"""
import math, os, sys
from PIL import Image, ImageDraw
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from reel_speko_kit import *

VD, OUT = sys.argv[1], sys.argv[2]
SUBS = [("Когда клиент присылает ТЗ из одной строки…", "O"),
        ("Новое сообщение: «Сделайте как Instagram, но лучше. До завтра».", "L"),
        ("Паника! Это невозможно! Я перегреваюсь!", "L"),
        ("Спокойно. Задаём три вопроса.", "O"),
        ("Первый: для кого приложение?", "O"),
        ("Отвечает: для салона красоты на Чиланзаре.", "L"),
        ("Второй: что самое главное?", "O"),
        ("Запись к мастеру и оплата через Click.", "L"),
        ("Третий: что можно сделать потом?", "O"),
        ("Бонусы и отзывы.", "L"),
        ("Вот и нормальное ТЗ. Не Instagram, а то, что реально нужно.", "O"),
        ("Не знаете, как написать ТЗ? Напишите нам — поможем.", "L")]
LINES = [(f"{VD}/p{i + 1}.wav", s, w) for i, (s, w) in enumerate(SUBS)]
C = {m: character(m) for m in ("neutral", "happy", "shock")}
WAVE = character("happy", "wave"); UP = character("happy", "up"); PH = character("neutral", "phone")
RED = radial((30, 6, 10), (150, 20, 30), cy=0.45, r=1000).convert("RGBA")

def s1(t, T):
    c = BG.copy()
    paste_c(c, pill(["POV:"], F("Black", 96), (255, 236, 160), (0, 0, 0, 0)), W / 2, 300, pop(t / .3))
    paste_c(c, pill(["клиент прислал ТЗ", "из одной строки"], F("Black", 66), (255, 255, 255), (0, 0, 0, 0)), W / 2, 470, pop((t - .2) / .35) if t > .2 else 0)
    paste_c(c, PH, W / 2, 1200, 1.05)
    return c

def chat(t):
    im = Image.new("RGBA", (900, 360), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.text((10, 0), "Клиент · 23:47", font=F("SemiBold", 30), fill=(200, 200, 215))
    d.rounded_rectangle([0, 50, 880, 330], 44, fill=(255, 255, 255))
    d.text((44, 90), "Сделайте как Instagram,", font=F("Bold", 50), fill=(20, 20, 24))
    d.text((44, 160), "но лучше.", font=F("Bold", 50), fill=(20, 20, 24))
    d.text((44, 230), "До завтра!!!", font=F("Black", 54), fill=(230, 50, 50))
    return im
CHAT = chat(0)

def s2(t, T):
    c = BG2.copy()
    paste_c(c, CHAT, W / 2, 470 + 40 * (1 - ease(t / .35)), 1, ease(t / .25))
    paste_c(c, LAP[("neutral", talking(t, 6) and t < T - .4)], W / 2, 1150, 1.0)
    return c

def s3(t, T):
    c = RED.copy()
    sh = math.sin(t * 60) * 14
    paste_c(c, pill(["ПАНИКА"], F("Black", 120), (255, 255, 255), (230, 40, 40, 255), pad=(50, 24)), W / 2 + sh, 380, pop(t / .25))
    paste_c(c, pill(["100% CPU · 99°C"], F("Bold", 48), (255, 220, 220), (0, 0, 0, 0)), W / 2, 540)
    paste_c(c, LAP[("wide", talking(t, 9))], W / 2 + sh, 1100, 1.1)
    return c

def s4(t, T):
    c = BG.copy()
    paste_c(c, pill(["3 вопроса"], F("Black", 96), (255, 255, 255), PUR + (255,), pad=(50, 24)), W / 2, 400, pop(t / .35))
    paste_c(c, C["happy"] if t > .5 else C["neutral"], W / 2, 1180, 1.1)
    return c

QA = [("1. Для кого?", "Салон красоты, Чиланзар", (60, 150, 255)),
      ("2. Что главное?", "Запись к мастеру + Click", (52, 199, 89)),
      ("3. Что потом?", "Бонусы и отзывы", (255, 159, 10))]
def panel(nq, na, t0):
    h = 160 + nq * 245
    im = Image.new("RGBA", (920, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, 919, h - 1], 44, fill=(246, 246, 250))
    d.text((44, 34), "ТЗ: что мы узнали", font=F("Black", 50), fill=(20, 20, 24))
    for i in range(nq):
        q, a, col = QA[i]; y = 130 + i * 245
        d.rounded_rectangle([30, y, 889, y + 220], 30, fill=(255, 255, 255), outline=(228, 228, 236), width=2)
        d.rounded_rectangle([54, y + 30, 66, y + 190], 6, fill=col)
        d.text((96, y + 30), q, font=F("Bold", 44), fill=(20, 20, 24))
        if i < na: d.text((96, y + 110), a, font=F("SemiBold", 44), fill=col)
        else: d.text((96, y + 110), "…", font=F("SemiBold", 44), fill=(180, 180, 190))
    return im

def qa(nq, na, who):
    def fn(t, T):
        c = BG2.copy()
        p = panel(nq, na, t); paste_c(c, p, W / 2, 300 + p.height / 2, 1, 1)
        if who == "O": paste_c(c, WAVE if talking(t, 5) and t < T - .4 else C["neutral"], 200, 1450, 0.5)
        else: paste_c(c, LAP[("neutral", talking(t, 6) and t < T - .4)], 870, 1440, 0.42)
        return c
    return fn

def s11(t, T):
    c = BG.copy()
    paste_c(c, panel(3, 3, t), W / 2, 760, 0.85)
    paste_c(c, pill(["ТЗ готово ✓"], F("Black", 64), (255, 255, 255), (52, 199, 89, 255)), W / 2, 260, pop(t / .35))
    paste_c(c, UP if talking(t, 4) else C["happy"], 230, 1400, 0.55)
    paste_c(c, LAP[("smug", False)], 820, 1420, 0.45)
    return c

def s12(t, T):
    c = BG2.copy()
    paste_c(c, pill(["Не знаете, как", "написать ТЗ?"], F("Black", 72), (255, 255, 255), (0, 0, 0, 0)), W / 2, 380, pop(t / .35))
    paste_c(c, pill(["Напишите в директ — поможем"], F("Bold", 50), (20, 20, 24), (255, 255, 255, 255), colors=[PUR]), W / 2, 590, pop((t - .4) / .35) if t > .4 else 0)
    if t > 1.0: paste_c(c, pill(["+998 90 970 06 03"], F("Black", 56), (255, 255, 255), PUR + (255,)), W / 2, 720, pop((t - 1) / .35))
    paste_c(c, C["happy"], 330, 1210, 0.8)
    paste_c(c, LAP[("smug", talking(t, 6) and t < T - 1.2)], 790, 1260, 0.55)
    if t > 1.8: paste_c(c, pill(["Подпишись — нас 37, цель 1000"], F("Bold", 42), (255, 236, 160), (0, 0, 0, 0)), W / 2, 840, 1, min(1, (t - 1.8) / .3))
    return c

SC = [s1, s2, s3, s4, qa(1, 0, "O"), qa(1, 1, "L"), qa(2, 1, "O"), qa(2, 2, "L"), qa(3, 2, "O"), qa(3, 3, "L"), s11, s12]
if __name__ == "__main__":
    fr = sys.argv[sys.argv.index("--frames") + 1] if "--frames" in sys.argv else False
    make_reel(LINES, SC, OUT, os.path.dirname(os.path.abspath(OUT)) + "/pov_scenes", seed=13, frames=fr, tail=2.0)
