"""Обложки 25.11 (JPEG 1080x1920, главное в центре 3:4). Usage: reel_covers_1125.py out_dir"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from reel_kit_ep1 import W, H, F, pill, paste_c, radial
from character_v2 import character
from reel_covers import bg, big, PUR
from school_game_ui import qr

OUT = sys.argv[1]

def ep6():
    c = bg((90, 20, 40))
    paste_c(c, pill(["СЕРИЯ 6 · ЧТ"], F("Black", 60), (255, 255, 255), PUR + (255,), pad=(40, 20)), W / 2, 360)
    big(c, ["Код скопировал.", "А ЭТО — нет"], 570, 96)
    paste_c(c, pill(["Что?!"], F("Black", 62), (255, 255, 255), (220, 50, 50, 255)), W / 2, 800)
    paste_c(c, character("shock", "up"), W / 2, 1230, 0.74)
    paste_c(c, pill(["Озодбек и My Week"], F("Bold", 48), (255, 236, 160), (0, 0, 0, 0)), W / 2, 1620)
    return c

def school():
    c = radial((8, 16, 12), (30, 110, 70), cy=0.45, r=1000).convert("RGBA")
    big(c, ["Двоечник впервые", "поднял руку"], 500, 96)
    paste_c(c, qr(300, seed=11), 820, 1000, 0.8)
    paste_c(c, character("happy", "up"), 400, 1250, 0.8)
    paste_c(c, pill(["Урок = игра по QR"], F("Black", 52), (255, 255, 255), (255, 159, 10, 255)), W / 2, 1620)
    return c

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for name, fn in [("ep6", ep6), ("school_game", school)]:
        fn().convert("RGB").save(f"{OUT}/2026-11-25_{name}_cover.jpg", quality=92)
    print("ok")
