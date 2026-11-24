"""Эп.5 «Кто парень в приёмной?» (24.11, 12:40), ~25 с. Разгадка: он скопировал My School (в коде «автор — Озодбек»).
Директор: пятница, педсовет — кто лучше покажет, тот делает для района. Клиффхэнгер: «самое главное он не скопировал» — что?
Голос Speko: Озодбек Dmitry, ноутбук cartesia. Usage: reel_ep5.py voice_dir out.mp4 [--frames sheet.jpg]"""
import math, os, sys
from PIL import Image, ImageDraw, ImageFilter
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from reel_speko_kit import *
import reel_kit_ep1 as rk

VD, OUT = sys.argv[1], sys.argv[2]
SUBS = [("Парень в приёмной открыл ноутбук. А там — мой My School!", "O"),
        ("В его коде написано: автор — Озодбек. Он скопировал твоё приложение.", "L"),
        ("Директор: в пятницу педсовет. Кто лучше покажет — тот и делает для всего района!", "O"),
        ("Спокойно. Код у него наш. Но самое главное он не скопировал.", "L"),
        ("Что главное?! Серия 6 — завтра в 12:40. Подпишись!", "O")]
LINES = [(f"{VD}/e{i + 1}.wav", s, w) for i, (s, w) in enumerate(SUBS)]
DARK = rk.DARK
NIGHT = vgrad((8, 10, 30), (24, 22, 60)).convert("RGBA")
C = {m: character(m) for m in ("neutral", "happy", "shock")}
UP_SH = character("shock", "up")
Q = rk.qmark()
ch = character("neutral"); SIL = Image.new("RGBA", ch.size, (14, 12, 26, 255)); SIL.putalpha(ch.split()[3])

def rival_laptop(k):
    im = Image.new("RGBA", (560, 380), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle([30, 0, 530, 330], 18, fill=(30, 30, 40)); d.rounded_rectangle([46, 16, 514, 314], 10, fill=(248, 248, 250))
    d.rectangle([0, 330, 560, 372], fill=(60, 60, 75))
    d.text((70, 36), "My School", font=F("Black", 44), fill=(20, 20, 24))
    for i, (a, col) in enumerate([("Математика  5", (52, 199, 89)), ("Физика  4", (60, 150, 255)), ("Домашка  ✓", (255, 159, 10))]):
        if k > i * .25:
            d.rounded_rectangle([70, 110 + i * 64, 490, 160 + i * 64], 14, fill=(236, 236, 242))
            d.rounded_rectangle([82, 122 + i * 64, 90, 148 + i * 64], 4, fill=col)
            d.text((104, 116 + i * 64), a, font=F("Bold", 30), fill=(20, 20, 24))
    return im

def s1(t, T):  # крючок
    c = NIGHT.copy(); d = ImageDraw.Draw(c)
    paste_c(c, pill(["Серия 5"], F("Bold", 40), (255, 255, 255), PUR + (255,), pad=(28, 12)), W / 2, 230, pop(t / .3))
    sh = math.sin(t * 40) * 8 if t < .8 else 0
    paste_c(c, pill(["Это же", "МОЁ приложение!"], F("Black", 92), (255, 255, 255), (220, 50, 50, 255)), W / 2 + sh, 450, pop(t / .3))
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0)); gd = ImageDraw.Draw(glow)
    gd.ellipse([440, 760, 1060, 1340], fill=(110, 70, 255, 90)); c.alpha_composite(glow.filter(ImageFilter.GaussianBlur(60)))
    paste_c(c, SIL, 800, 1060, 0.7)
    paste_c(c, rival_laptop(t / (T * .6)), 760, 1300, 0.9)
    paste_c(c, C["shock"], 270, 1230, 0.62)
    return c

def code_card(k):
    im = Image.new("RGBA", (900, 420), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, 899, 419], 30, fill=(20, 22, 34))
    d.text((40, 36), "// my_school.js", font=F("Bold", 44), fill=(110, 120, 150))
    d.text((40, 130), "const author =", font=F("Bold", 50), fill=(150, 200, 255))
    s = "\"Ozodbek\";"; n = int(len(s) * min(1, k))
    d.text((40, 220), s[:n], font=F("Black", 74), fill=(255, 236, 120))
    if k > 1.1: d.rounded_rectangle([30, 210, 470, 320], 18, outline=(255, 70, 70), width=6)
    return im

def s2(t, T):
    c = BG2.copy()
    paste_c(c, code_card(t / (T * .45)), W / 2, 470, 1, min(1, t / .3))
    paste_c(c, LAP[("wide", talking(t) and t < T - .4)], 330, 1120, 0.62)
    if t > T * .55: paste_c(c, pill(["СКОПИРОВАЛ"], F("Black", 76), (255, 255, 255), (220, 50, 50, 255)), 700, 880, pop((t - T * .55) / .3))
    return c

def s3(t, T):  # педсовет
    c = DARK.copy()
    paste_c(c, pill(["ПЯТНИЦА · ПЕДСОВЕТ"], F("Black", 60), (20, 20, 24), (255, 236, 160, 255)), W / 2, 280, pop(t / .3))
    if t > .5: paste_c(c, pill(["Кто лучше покажет —", "делает для района"], F("Black", 62), (255, 255, 255), (0, 0, 0, 0)), W / 2, 470, pop((t - .5) / .3))
    paste_c(c, C["neutral"], 280, 1130, 0.6)
    paste_c(c, pill(["VS"], F("Black", 110), (255, 70, 70), (0, 0, 0, 0)), W / 2, 1050, pop((t - .9) / .3) if t > .9 else 0)
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0)); gd = ImageDraw.Draw(glow)
    gd.ellipse([560, 820, 1040, 1440], fill=(220, 60, 80, 110)); c.alpha_composite(glow.filter(ImageFilter.GaussianBlur(70)))
    paste_c(c, SIL, 800, 1130, 0.6)
    return c

def s4(t, T):  # клиффхэнгер
    c = BG.copy()
    paste_c(c, LAP[("smug", talking(t) and t < T - .4)], W / 2, 760, 0.95)
    if t > T * .45:
        paste_c(c, pill(["Самое главное", "он НЕ скопировал"], F("Black", 72), (255, 255, 255), PUR + (255,)), W / 2, 1270, pop((t - T * .45) / .3))
    return c

def s5(t, T):
    c = NIGHT.copy()
    paste_c(c, pill(["Что он не скопировал?"], F("Black", 70), (255, 255, 255), (220, 50, 50, 255)), W / 2, 300, pop(t / .3))
    paste_c(c, Q, 820, 700 + math.sin(t * 3) * 12, 0.7)
    paste_c(c, UP_SH, W / 2 - 80, 900, 0.5)
    paste_c(c, pill(["Серия 6 — завтра в 12:40"], F("Black", 58), (255, 236, 160), (0, 0, 0, 0)), W / 2, 1200, pop((t - .3) / .3) if t > .3 else 0)
    if t > .9: paste_c(c, pill(["Подпишись, чтобы не пропустить"], F("Bold", 44), (255, 255, 255), PUR + (255,)), W / 2, 1320, pop((t - .9) / .3))
    if t > 1.5: paste_c(c, pill(["Своё приложение? Пришлите ТЗ · +998 90 970 06 03"], F("SemiBold", 32), (200, 200, 215), (0, 0, 0, 0)), W / 2, 1430, 1, min(1, (t - 1.5) / .3))
    return c

if __name__ == "__main__":
    fr = sys.argv[sys.argv.index("--frames") + 1] if "--frames" in sys.argv else False
    make_reel(LINES, [s1, s2, s3, s4, s5], OUT, os.path.dirname(os.path.abspath(OUT)) + "/ep5_scenes", seed=113, frames=fr, tail=2.2)
