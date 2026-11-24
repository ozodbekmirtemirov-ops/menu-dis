"""Видео-история: тизер серии 6 (24.11, 17:10), ~11 с. Что соперник НЕ скопировал? Ноутбук: «этого нет ни в одной строчке кода».
Usage: teaser_ep6.py voice_dir out.mp4 [--frames sheet.jpg]"""
import math, os, sys
from PIL import Image, ImageDraw
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from reel_speko_kit import *
import reel_kit_ep1 as rk

VD, OUT = sys.argv[1], sys.argv[2]
LINES = [(f"{VD}/z1.wav", "Он скопировал мой код. Так что же он НЕ скопировал?", "O"),
         (f"{VD}/z2.wav", "Подсказка: этого нет ни в одной строчке кода.", "L"),
         (f"{VD}/z3.wav", "Серия 6 — завтра в 12:40. Подпишись, чтобы не пропустить!", "O")]
O_SH = character("shock"); O_UP = character("shock", "up")
NIGHT = vgrad((8, 10, 30), (24, 22, 60)).convert("RGBA")
Q = rk.qmark()

def code_lines(t):
    im = Image.new("RGBA", (860, 520), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, 859, 519], 30, fill=(20, 22, 34))
    rows = ["function grades() {", "  notify(parents);", "  save(homework);", "}", "// ???"]
    for i, s in enumerate(rows):
        col = (255, 90, 80) if s.startswith("//") else (150, 200, 255)
        d.text((40, 36 + i * 92), s, font=F("Bold", 48), fill=col)
    return im
CODE = code_lines(0)

def s0(t, T):
    c = NIGHT.copy()
    paste_c(c, pill(["Что он", "НЕ скопировал?"], F("Black", 92), (255, 255, 255), (220, 50, 50, 255)), W / 2, 380, pop(t / .3))
    paste_c(c, Q, 820, 760 + math.sin(t * 3) * 12, 0.7)
    paste_c(c, O_SH, W / 2, 1180, 0.8)
    return c

def s1(t, T):
    c = BG2.copy()
    paste_c(c, CODE, W / 2, 470, 1, min(1, t / .3))
    paste_c(c, LAP[("smug", talking(t) and t < T - .3)], W / 2, 1100, 0.9)
    return c

def s2(t, T):
    c = BG.copy()
    paste_c(c, O_UP, W / 2, 1100 + math.sin(t * 9) * 10, 1.0)
    paste_c(c, pill(["Серия 6 — завтра в 12:40"], F("Black", 62), (255, 236, 160), (0, 0, 0, 0)), W / 2, 330, pop(t / .35))
    if t > 1.0: paste_c(c, pill(["Подпишись, чтобы не пропустить"], F("Bold", 46), (255, 255, 255), PUR + (255,)), W / 2, 460, pop((t - 1) / .35))
    return c

if __name__ == "__main__":
    fr = sys.argv[sys.argv.index("--frames") + 1] if "--frames" in sys.argv else False
    make_reel(LINES, [s0, s1, s2], OUT, os.path.dirname(os.path.abspath(OUT)) + "/tz6_scenes", seed=151, frames=fr, tail=0.6)
