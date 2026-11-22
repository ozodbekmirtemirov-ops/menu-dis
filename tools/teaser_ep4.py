"""Видео-история: тизер серии 4 (22.11, 17:10), ~11 с, конвейер reel_speko_local через reel_speko_kit. Usage: teaser_ep3.py voice_dir out.mp4"""
import math, os, sys
from PIL import Image, ImageDraw
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from reel_speko_kit import *

VD, OUT = sys.argv[1], sys.argv[2]
LINES = [(f"{VD}/z1.wav", "Директор вызывает меня в четверг, в 8:00. Зачем?!", "O"),
         (f"{VD}/z2.wav", "Я видел его письмо. Тебе понравится… наверное.", "L"),
         (f"{VD}/z3.wav", "Наверное?! Серия 4 — завтра в 12:40. Подпишись!", "O")]
O_N = character("neutral"); O_UP = character("shock", "up")
SKY = vgrad((120, 170, 230), (210, 225, 245)).convert("RGBA")

def school_bg():
    c = SKY.copy(); d = ImageDraw.Draw(c)
    d.rectangle([90, 520, 990, 1300], fill=(236, 214, 180)); d.polygon([(60, 530), (540, 330), (1020, 530)], fill=(190, 70, 60))
    for r in range(3):
        for k in range(5):
            x = 150 + k * 170; y = 620 + r * 200; d.rounded_rectangle([x, y, x + 110, y + 130], 10, fill=(140, 190, 240))
    d.rounded_rectangle([470, 1100, 610, 1300], 14, fill=(120, 80, 50))
    d.rectangle([340, 470, 740, 530], fill=(255, 255, 255)); f = F("Black", 44); tw = text_size(d, "ШКОЛА", f)[0]
    d.text((540 - tw / 2, 474), "ШКОЛА", font=f, fill=(190, 70, 60))
    d.rectangle([0, 1300, W, H], fill=(120, 120, 130))
    return c
SCH = school_bg()

def s0(t, T):
    c = SCH.copy()
    paste_c(c, pill(["Четверг, 8:00"], F("Black", 64), (255, 255, 255), (220, 50, 50, 255)), W / 2, 300, pop(t / .35))
    paste_c(c, O_N, 380, 1330, 0.85)
    paste_c(c, LAP[("neutral", False)], 790, 1440, 0.45)
    return c

def s1(t, T):
    c = BG2.copy()
    paste_c(c, LAP[("smug", talking(t) and t < T - .3)], W / 2, 900, 1.15)
    paste_c(c, O_N, 860, 1380, 0.45)
    return c

def s2(t, T):
    c = BG.copy()
    paste_c(c, O_UP, W / 2, 1100 + math.sin(t * 9) * 10, 1.0)
    paste_c(c, pill(["Серия 4 — завтра в 12:40"], F("Black", 62), (255, 236, 160), (0, 0, 0, 0)), W / 2, 330, pop(t / .35))
    if t > 1.0: paste_c(c, pill(["Подпишись, чтобы не пропустить"], F("Bold", 46), (255, 255, 255), PUR + (255,)), W / 2, 460, pop((t - 1) / .35))
    return c

if __name__ == "__main__":
    fr = sys.argv[sys.argv.index("--frames") + 1] if "--frames" in sys.argv else False
    make_reel(LINES, [s0, s1, s2], OUT, os.path.dirname(os.path.abspath(OUT)) + "/tz4_scenes", seed=63, frames=fr, tail=0.6)
