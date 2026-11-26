"""Обложки 26.11 (JPEG 1080x1920, главное в центре 3:4). Usage: reel_covers_1126.py out_dir"""
import os, sys
from PIL import Image
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from reel_kit_ep1 import W, H, F, pill, paste_c, radial, vgrad
from character_v2 import character
from reel_covers import bg, big, PUR

OUT = sys.argv[1]

def ep7():
    c = bg((90, 20, 40))
    paste_c(c, pill(["СЕРИЯ 7 · ПТ · ПЕДСОВЕТ"], F("Black", 54), (255, 255, 255), PUR + (255,), pad=(40, 20)), W / 2, 360)
    big(c, ["Один вопрос —", "и он молчит"], 570, 96)
    paste_c(c, pill(["Что спросил директор?"], F("Black", 54), (255, 255, 255), (220, 50, 50, 255)), W / 2, 800)
    ch = character("neutral"); sil = Image.new("RGBA", ch.size, (14, 12, 26, 255)); sil.putalpha(ch.split()[3])
    paste_c(c, sil, 820, 1250, 0.6)
    paste_c(c, character("shock", "up"), 380, 1250, 0.7)
    paste_c(c, pill(["Озодбек и My Week"], F("Bold", 48), (255, 236, 160), (0, 0, 0, 0)), W / 2, 1620)
    return c

def hw():
    c = vgrad((10, 12, 34), (30, 26, 70)).convert("RGBA")
    paste_c(c, pill(["22:00"], F("Black", 120), (255, 236, 160), (0, 0, 0, 0)), W / 2, 380)
    paste_c(c, pill(["Мама:", "«Домашку сделал?»"], F("Black", 78), (20, 20, 24), (255, 255, 255, 255), colors=[(120, 120, 130), (20, 20, 24)]), W / 2, 640)
    paste_c(c, character("shock"), W / 2, 1230, 0.72)
    paste_c(c, pill(["ЗАБЫЛ!"], F("Black", 90), (255, 255, 255), (220, 50, 50, 255)), 830, 1000)
    paste_c(c, pill(["Знакомо?"], F("Bold", 52), (255, 255, 255), PUR + (255,)), W / 2, 1620)
    return c

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for name, fn in [("ep7", ep7), ("forgot_hw", hw)]:
        fn().convert("RGB").save(f"{OUT}/2026-11-26_{name}_cover.jpg", quality=92)
    print("ok")
