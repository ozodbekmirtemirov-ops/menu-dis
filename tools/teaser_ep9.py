"""Видео-история: тизер серии 9 (27.11, 17:10), ~11 с. «Суббота, 10:00 — узнаю, кто ставил задачи всю неделю»;
подсказка ноутбука: «он был рядом с самого первого дня». Usage: teaser_ep9.py voice_dir out.mp4 [--frames sheet.jpg]"""
import math, os, sys
from PIL import Image
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from reel_speko_kit import *
import reel_kit_ep1 as rk

VD, OUT = sys.argv[1], sys.argv[2]
LINES = [(f"{VD}/t1.wav", "Завтра в 10:00 я узнаю, кто ставил мне задачи всю неделю.", "O"),
         (f"{VD}/t2.wav", "Подсказка: он был рядом с самого первого дня.", "L"),
         (f"{VD}/t3.wav", "Серия 9 — завтра в 12:40. Подпишись, чтобы не пропустить!", "O")]
O_SH = character("shock", "phone"); O_UP = character("shock", "up")
NIGHT = vgrad((8, 10, 30), (24, 22, 60)).convert("RGBA")
Q = rk.qmark()

def s0(t, T):
    c = NIGHT.copy()
    paste_c(c, pill(["СУББОТА · 10:00"], F("Black", 64), (20, 20, 24), (255, 236, 160, 255)), W / 2, 300, pop(t / .3))
    if t > .7: paste_c(c, pill(["Кто ставил задачи", "всю неделю?"], F("Black", 72), (255, 255, 255), (220, 50, 50, 255)), W / 2, 540, pop((t - .7) / .3))
    paste_c(c, O_SH, W / 2, 1180, 0.72)
    return c

def s1(t, T):
    c = BG2.copy()
    paste_c(c, pill(["Он был рядом", "с первого дня"], F("Black", 78), (255, 255, 255), PUR + (255,)), W / 2, 400, pop(t / .3))
    paste_c(c, Q, W / 2, 680 + math.sin(t * 3) * 12, 0.7)
    paste_c(c, LAP[("smug", talking(t) and t < T - .3)], W / 2, 1180, 0.8)
    return c

def s2(t, T):
    c = BG.copy()
    paste_c(c, O_UP, W / 2, 1100 + math.sin(t * 9) * 10, 1.0)
    paste_c(c, pill(["Серия 9 — завтра в 12:40"], F("Black", 62), (255, 236, 160), (0, 0, 0, 0)), W / 2, 330, pop(t / .35))
    if t > 1.0: paste_c(c, pill(["Подпишись, чтобы не пропустить"], F("Bold", 46), (255, 255, 255), PUR + (255,)), W / 2, 460, pop((t - 1) / .35))
    return c

if __name__ == "__main__":
    fr = sys.argv[sys.argv.index("--frames") + 1] if "--frames" in sys.argv else False
    make_reel(LINES, [s0, s1, s2], OUT, os.path.dirname(os.path.abspath(OUT)) + "/tz9_scenes", seed=239, frames=fr, tail=0.6)
