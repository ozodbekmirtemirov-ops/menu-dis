"""Обложки 23.11 (JPEG 1080x1920, главное в центре 3:4). Usage: reel_covers_1123.py out_dir"""
import os, sys
from PIL import Image, ImageDraw
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from reel_kit_ep1 import W, H, F, pill, paste_c, radial, text_size
from character_v2 import character
from reel_covers import bg, big, PUR

OUT = sys.argv[1]

def ep4():
    c = bg((90, 20, 40))
    paste_c(c, pill(["СЕРИЯ 4"], F("Black", 60), (255, 255, 255), PUR + (255,), pad=(40, 20)), W / 2, 360)
    big(c, ["Вызвали", "к директору"], 570)
    paste_c(c, pill(["Четверг, 8:00"], F("Black", 58), (255, 255, 255), (220, 50, 50, 255)), W / 2, 800)
    paste_c(c, character("shock", "up"), W / 2, 1230, 0.74)
    paste_c(c, pill(["Озодбек и My Week"], F("Bold", 48), (255, 236, 160), (0, 0, 0, 0)), W / 2, 1620)
    return c

def cap():
    c = radial((8, 12, 10), (20, 110, 60), cy=0.45, r=1000).convert("RGBA")
    big(c, ["Сколько у тебя", "денег?"], 500, 110)
    paste_c(c, pill(["не на карте — ВСЕГО"], F("Black", 58), (20, 20, 24), (255, 236, 160, 255)), W / 2, 760)
    paste_c(c, character("shock", "phone"), W / 2, 1290, 0.8)
    paste_c(c, pill(["My Capital"], F("Black", 52), (255, 255, 255), (52, 199, 89, 255)), W / 2, 1620)
    return c

def call():
    c = bg((40, 30, 110))
    big(c, ["Нас 38."], 420, 130)
    big(c, ["Нужно 1000"], 590, 96, (255, 236, 160))
    paste_c(c, pill(["за 39 дней"], F("Black", 58), (255, 255, 255), (220, 50, 50, 255)), W / 2, 760)
    paste_c(c, character("shock", "phone"), W / 2, 1290, 0.8)
    paste_c(c, pill(["Есть простой способ →"], F("Bold", 50), (20, 20, 24), (255, 255, 255, 255)), W / 2, 1620)
    return c

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for name, fn in [("ep4", ep4), ("capital_show", cap), ("call_38", call)]:
        fn().convert("RGB").save(f"{OUT}/2026-11-23_{name}_cover.jpg", quality=92)
    print("ok")
