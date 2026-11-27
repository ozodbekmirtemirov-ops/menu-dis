"""Обложки 27.11 (JPEG 1080x1920, главное в центре 3:4). Usage: reel_covers_1127.py out_dir"""
import os, sys
from PIL import Image
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from reel_kit_ep1 import W, H, F, pill, paste_c, radial, vgrad
from character_v2 import character
from reel_covers import bg, big, PUR

OUT = sys.argv[1]

def ep8():
    c = bg((90, 20, 40))
    paste_c(c, pill(["СЕРИЯ 8 · ПТ · ВЕЧЕР"], F("Black", 54), (255, 255, 255), PUR + (255,), pad=(40, 20)), W / 2, 360)
    big(c, ["Код прислал…", "ДИРЕКТОР?!"], 570, 100)
    paste_c(c, pill(["Решение по району"], F("Black", 54), (255, 255, 255), (220, 50, 50, 255)), W / 2, 800)
    paste_c(c, character("shock", "up"), W / 2, 1250, 0.72)
    paste_c(c, pill(["Озодбек и My Week"], F("Bold", 48), (255, 236, 160), (0, 0, 0, 0)), W / 2, 1620)
    return c

def dad():
    c = vgrad((10, 12, 34), (14, 50, 34)).convert("RGBA")
    paste_c(c, pill(["Папа, сколько", "у нас денег?"], F("Black", 96), (255, 255, 255), (220, 50, 50, 255)), W / 2, 520)
    paste_c(c, character("shock"), W / 2, 1180, 0.72)
    paste_c(c, pill(["$ в шкафу?"], F("Black", 64), (20, 20, 24), (255, 236, 160, 255)), 760, 930)
    paste_c(c, pill(["My Capital"], F("Black", 56), (255, 255, 255), (52, 199, 89, 255)), W / 2, 1620)
    return c

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for name, fn in [("ep8", ep8), ("dad_money", dad)]:
        fn().convert("RGB").save(f"{OUT}/2026-11-27_{name}_cover.jpg", quality=92)
    print("ok")
