"""Видео-история: тизер ФИНАЛА (серия 10) (28.11, 17:10), ~11 с. Конверт «ТЗ. Открыть в воскресенье»; подсказка ноутбука:
«внутри — чья-то мечта». Usage: teaser_ep10.py voice_dir out.mp4 [--frames sheet.jpg]"""
import math, os, sys
from PIL import Image, ImageDraw
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from reel_speko_kit import *
import reel_kit_ep1 as rk

VD, OUT = sys.argv[1], sys.argv[2]
LINES = [(f"{VD}/t1.wav", "Конверт с надписью «ТЗ». Открыть в воскресенье. Завтра!", "O"),
         (f"{VD}/t2.wav", "Подсказка: внутри — чья-то мечта.", "L"),
         (f"{VD}/t3.wav", "Финал сериала — завтра в 12:40. Не пропусти!", "O")]
O_PH = character("shock", "phone"); O_UP = character("happy", "up")
NIGHT = vgrad((8, 10, 30), (24, 22, 60)).convert("RGBA")

def envelope():
    im = Image.new("RGBA", (700, 460), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, 699, 459], 30, fill=(250, 240, 220))
    d.polygon([(0, 0), (699, 0), (350, 260)], fill=(235, 220, 190), outline=(200, 180, 150))
    d.ellipse([310, 220, 390, 300], fill=(220, 50, 50))
    d.text((222, 310), "ТЗ", font=F("Black", 110), fill=(20, 20, 24))
    return im
ENV = envelope()

def s0(t, T):
    c = NIGHT.copy()
    paste_c(c, pill(["ФИНАЛ · ЗАВТРА"], F("Black", 70), (20, 20, 24), (255, 236, 160, 255)), W / 2, 280, pop(t / .3))
    paste_c(c, ENV, W / 2, 620 + math.sin(t * 4) * 10, 0.9, min(1, t / .4))
    paste_c(c, O_PH, W / 2, 1200, 0.6)
    return c

def s1(t, T):
    c = BG2.copy()
    paste_c(c, pill(["Внутри —", "чья-то мечта"], F("Black", 84), (255, 255, 255), PUR + (255,)), W / 2, 400, pop(t / .3))
    paste_c(c, rk.qmark(), W / 2, 700 + math.sin(t * 3) * 12, 0.6)
    paste_c(c, LAP[("smug", talking(t) and t < T - .3)], W / 2, 1180, 0.8)
    return c

def s2(t, T):
    c = BG.copy()
    paste_c(c, O_UP, W / 2, 1100 + math.sin(t * 9) * 10, 0.95)
    paste_c(c, pill(["Финал — завтра в 12:40"], F("Black", 64), (255, 236, 160), (0, 0, 0, 0)), W / 2, 330, pop(t / .35))
    if t > 1.0: paste_c(c, pill(["Подпишись, чтобы не пропустить"], F("Bold", 46), (255, 255, 255), PUR + (255,)), W / 2, 460, pop((t - 1) / .35))
    return c

if __name__ == "__main__":
    fr = sys.argv[sys.argv.index("--frames") + 1] if "--frames" in sys.argv else False
    make_reel(LINES, [s0, s1, s2], OUT, os.path.dirname(os.path.abspath(OUT)) + "/tz10_scenes", seed=263, frames=fr, tail=0.6)
