"""Обложки 28.11 (JPEG 1080x1920, главное в центре 3:4). Usage: reel_covers_1128.py out_dir"""
import os, sys
from PIL import Image
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from reel_kit_ep1 import W, H, F, pill, paste_c, radial, vgrad
from character_v2 import character
from reel_covers import bg, big, PUR
from school_game_ui import class_row

OUT = sys.argv[1]

def ep9():
    c = bg((30, 60, 120))
    paste_c(c, pill(["СЕРИЯ 9 · СУББОТА"], F("Black", 54), (255, 255, 255), PUR + (255,), pad=(40, 20)), W / 2, 360)
    big(c, ["Это был", "ТЫ?!"], 580, 120)
    paste_c(c, pill(["Кто ставил задачи всю неделю"], F("Black", 46), (255, 255, 255), (220, 50, 50, 255)), W / 2, 830)
    paste_c(c, character("shock", "up"), W / 2, 1250, 0.72)
    paste_c(c, pill(["Озодбек и My Week"], F("Bold", 48), (255, 236, 160), (0, 0, 0, 0)), W / 2, 1620)
    return c

def bell():
    c = vgrad((40, 70, 60), (14, 26, 22)).convert("RGBA")
    paste_c(c, pill(["Звонок прозвенел —", "а класс НЕ уходит?!"], F("Black", 84), (255, 255, 255), (220, 50, 50, 255), colors=[(255, 255, 255), (255, 236, 160)]), W / 2, 540)
    paste_c(c, class_row(1), W / 2, 1300, 0.85)
    paste_c(c, character("shock", "up"), W / 2, 1050, 0.55)
    paste_c(c, pill(["My School"], F("Black", 56), (255, 255, 255), (255, 159, 10, 255)), W / 2, 1620)
    return c

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for name, fn in [("ep9", ep9), ("school_bell", bell)]:
        fn().convert("RGB").save(f"{OUT}/2026-11-28_{name}_cover.jpg", quality=92)
    print("ok")
