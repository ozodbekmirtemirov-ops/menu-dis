"""Видео-история: тизер серии 5 (23.11, 17:10), ~12 с. Кто парень в приёмной? Ноутбук: «в его коде знакомое имя».
Usage: teaser_ep5.py voice_dir out.mp4 [--frames sheet.jpg]"""
import math, os, sys
from PIL import Image, ImageDraw
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from reel_speko_kit import *
import reel_kit_ep1 as rk

VD, OUT = sys.argv[1], sys.argv[2]
LINES = [(f"{VD}/z1.wav", "Кто этот парень у директора? Он тоже принёс приложение для школ!", "O"),
         (f"{VD}/z2.wav", "Я заглянул в его код. Там… очень знакомое имя.", "L"),
         (f"{VD}/z3.wav", "Знакомое?! Серия 5 — завтра в 12:40. Подпишись!", "O")]
O_SH = character("shock"); O_UP = character("shock", "up")
ch = character("neutral"); SIL = Image.new("RGBA", ch.size, (14, 12, 26, 255)); SIL.putalpha(ch.split()[3])
NIGHT = vgrad((8, 10, 30), (24, 22, 60)).convert("RGBA")
Q = rk.qmark()

def s0(t, T):
    c = NIGHT.copy()
    paste_c(c, pill(["Кто он?"], F("Black", 100), (255, 255, 255), (220, 50, 50, 255)), W / 2, 330, pop(t / .3))
    paste_c(c, SIL, 760, 1150, 0.8); paste_c(c, Q, 760, 640 + math.sin(t * 3) * 12, 0.7)
    paste_c(c, O_SH, 290, 1240, 0.6)
    return c

def code_card():
    im = Image.new("RGBA", (860, 380), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, 859, 379], 30, fill=(20, 22, 34))
    rows = [("// school_app.js", (110, 120, 150)), ("const author = \"", (150, 200, 255)), ("", None)]
    for i, (s, col) in enumerate(rows):
        if s: d.text((40, 40 + i * 100), s, font=F("Bold", 48), fill=col)
    d.rounded_rectangle([70, 255, 330, 305], 10, fill=(255, 90, 80)); d.rounded_rectangle([350, 255, 520, 305], 10, fill=(255, 90, 80))
    d.text((540, 240), "\";", font=F("Bold", 48), fill=(150, 200, 255))
    return im
CODE = code_card()

def s1(t, T):
    c = BG2.copy()
    paste_c(c, CODE, W / 2, 420, 1, min(1, t / .3))
    paste_c(c, LAP[("smug", talking(t) and t < T - .3)], W / 2, 1050, 1.0)
    return c

def s2(t, T):
    c = BG.copy()
    paste_c(c, O_UP, W / 2, 1100 + math.sin(t * 9) * 10, 1.0)
    paste_c(c, pill(["Серия 5 — завтра в 12:40"], F("Black", 62), (255, 236, 160), (0, 0, 0, 0)), W / 2, 330, pop(t / .35))
    if t > 1.0: paste_c(c, pill(["Подпишись, чтобы не пропустить"], F("Bold", 46), (255, 255, 255), PUR + (255,)), W / 2, 460, pop((t - 1) / .35))
    return c

if __name__ == "__main__":
    fr = sys.argv[sys.argv.index("--frames") + 1] if "--frames" in sys.argv else False
    make_reel(LINES, [s0, s1, s2], OUT, os.path.dirname(os.path.abspath(OUT)) + "/tz5_scenes", seed=101, frames=fr, tail=0.6)
