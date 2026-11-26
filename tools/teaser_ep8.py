"""Видео-история: тизер серии 8 (26.11, 17:10), ~12 с. Решение директора вечером; кто прислал сопернику код — ноутбук знает.
Usage: teaser_ep8.py voice_dir out.mp4 [--frames sheet.jpg]"""
import math, os, sys
from PIL import Image
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from reel_speko_kit import *
import reel_kit_ep1 as rk

VD, OUT = sys.argv[1], sys.argv[2]
LINES = [(f"{VD}/t1.wav", "Директор решит сегодня вечером. А соперник говорит: мой код ему кто-то прислал.", "O"),
         (f"{VD}/t2.wav", "Я уже знаю, кто это. И ты его тоже знаешь.", "L"),
         (f"{VD}/t3.wav", "Серия 8 — завтра в 12:40. Подпишись, чтобы не пропустить!", "O")]
O_SH = character("shock"); O_UP = character("shock", "up")
NIGHT = vgrad((8, 10, 30), (24, 22, 60)).convert("RGBA")
ch = character("neutral"); SIL = Image.new("RGBA", ch.size, (14, 12, 26, 255)); SIL.putalpha(ch.split()[3])
Q = rk.qmark()

def s0(t, T):
    c = NIGHT.copy()
    paste_c(c, pill(["РЕШЕНИЕ ДИРЕКТОРА — ВЕЧЕРОМ"], F("Black", 52), (20, 20, 24), (255, 236, 160, 255)), W / 2, 300, pop(t / .3))
    if t > .8: paste_c(c, pill(["Кто прислал", "ему мой код?"], F("Black", 76), (255, 255, 255), (220, 50, 50, 255)), W / 2, 540, pop((t - .8) / .3))
    paste_c(c, O_SH, 300, 1150, 0.7); paste_c(c, SIL, 800, 1150, 0.62)
    return c

def s1(t, T):
    c = BG2.copy()
    paste_c(c, pill(["Ты его знаешь"], F("Black", 80), (255, 255, 255), PUR + (255,)), W / 2, 380, pop(t / .3))
    paste_c(c, Q, W / 2, 620 + math.sin(t * 3) * 12, 0.8)
    paste_c(c, LAP[("smug", talking(t) and t < T - .3)], W / 2, 1150, 0.85)
    return c

def s2(t, T):
    c = BG.copy()
    paste_c(c, O_UP, W / 2, 1100 + math.sin(t * 9) * 10, 1.0)
    paste_c(c, pill(["Серия 8 — завтра в 12:40"], F("Black", 62), (255, 236, 160), (0, 0, 0, 0)), W / 2, 330, pop(t / .35))
    if t > 1.0: paste_c(c, pill(["Подпишись, чтобы не пропустить"], F("Bold", 46), (255, 255, 255), PUR + (255,)), W / 2, 460, pop((t - 1) / .35))
    return c

if __name__ == "__main__":
    fr = sys.argv[sys.argv.index("--frames") + 1] if "--frames" in sys.argv else False
    make_reel(LINES, [s0, s1, s2], OUT, os.path.dirname(os.path.abspath(OUT)) + "/tz8_scenes", seed=211, frames=fr, tail=0.5)
