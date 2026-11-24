"""Обложки 24.11 (JPEG 1080x1920, главное в центре 3:4). Usage: reel_covers_1124.py out_dir"""
import os, sys
from PIL import Image, ImageDraw
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from reel_kit_ep1 import W, H, F, pill, paste_c, radial, text_size
from character_v2 import character
from reel_covers import bg, big, PUR

OUT = sys.argv[1]

def ep5():
    c = bg((90, 20, 40))
    paste_c(c, pill(["СЕРИЯ 5"], F("Black", 60), (255, 255, 255), PUR + (255,), pad=(40, 20)), W / 2, 360)
    big(c, ["Он скопировал", "моё приложение"], 570, 96)
    paste_c(c, pill(["Кто он?!"], F("Black", 62), (255, 255, 255), (220, 50, 50, 255)), W / 2, 800)
    paste_c(c, character("shock", "up"), W / 2, 1230, 0.74)
    paste_c(c, pill(["Озодбек и My Week"], F("Bold", 48), (255, 236, 160), (0, 0, 0, 0)), W / 2, 1620)
    return c

def school():
    c = radial((14, 10, 6), (140, 80, 10), cy=0.45, r=1000).convert("RGBA")
    big(c, ["Мама уже знает", "твою оценку"], 500, 100)
    paste_c(c, pill(["Алгебра: 3"], F("Black", 60), (255, 255, 255), (220, 50, 50, 255)), W / 2, 750)
    paste_c(c, character("shock", "phone"), W / 2, 1290, 0.8)
    paste_c(c, pill(["My School"], F("Black", 52), (255, 255, 255), (255, 159, 10, 255)), W / 2, 1620)
    return c

def myths():
    c = bg((90, 30, 40))
    paste_c(c, pill(["3 МИФА"], F("Black", 120), (255, 255, 255), (220, 50, 50, 255)), W / 2, 430)
    big(c, ["почему твоя идея", "всё ещё в заметках"], 660, 76, (255, 236, 160))
    paste_c(c, character("shock"), W / 2, 1260, 0.74)
    paste_c(c, pill(["Особенно миф №1 →"], F("Bold", 50), (20, 20, 24), (255, 255, 255, 255)), W / 2, 1620)
    return c

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for name, fn in [("ep5", ep5), ("school_show", school), ("myths3", myths)]:
        fn().convert("RGB").save(f"{OUT}/2026-11-24_{name}_cover.jpg", quality=92)
    print("ok")
