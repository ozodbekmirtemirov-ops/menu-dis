"""Обложки рилсов (JPEG 1080x1920; главное — в центральной зоне 3:4, y≈240..1680, чтобы не обрезалось в сетке профиля).
Usage: reel_covers.py out_dir  -> 2026-11-22_ep3_cover.jpg, _quiz_price_cover.jpg, _napkin_story_cover.jpg"""
import os, sys
from PIL import Image, ImageDraw
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from reel_kit_ep1 import W, H, F, pill, paste_c, radial, text_size
from character_v2 import character
import reel_kit_ep1 as rk

OUT = sys.argv[1]; PUR = (110, 70, 255)
def bg(glow): return radial((10, 10, 16), glow, cy=0.45, r=1000).convert("RGBA")
def big(c, lines, y, size=104, col=(255, 255, 255), colors=None):
    paste_c(c, pill(lines, F("Black", size), col, (0, 0, 0, 0), colors=colors), W / 2, y)

def ep3():
    c = bg((40, 30, 110))
    paste_c(c, pill(["СЕРИЯ 3"], F("Black", 60), (255, 255, 255), PUR + (255,), pad=(40, 20)), W / 2, 360)
    big(c, ["Кто ставил", "задачу?"], 560)
    paste_c(c, pill(["Среда, 15:00 — ???"], F("Black", 58), (255, 255, 255), (220, 50, 50, 255)), W / 2, 790)
    paste_c(c, character("shock", "up"), W / 2, 1270, 0.85)
    paste_c(c, pill(["Озодбек и My Week"], F("Bold", 48), (255, 236, 160), (0, 0, 0, 0)), W / 2, 1620)
    return c

def quiz():
    c = bg((20, 70, 140))
    big(c, ["Сколько стоит", "приложение?"], 470)
    for i, (l, v, col) in enumerate([("А", "$100", (60, 150, 255)), ("Б", "$1 000", (255, 159, 10)), ("В", "$100 000", (230, 60, 90))]):
        im = Image.new("RGBA", (300, 300), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
        d.rounded_rectangle([0, 0, 299, 299], 50, fill=col)
        f = F("Black", 120); tw, th, oy = text_size(d, l, f); d.text((150 - tw / 2, 40 - oy), l, font=f, fill=(255, 255, 255))
        f2 = F("Bold", 50); tw, th, oy = text_size(d, v, f2); d.text((150 - tw / 2, 205 - oy), v, font=f2, fill=(255, 255, 255))
        paste_c(c, im, 210 + i * 330, 820, 0.95)
    paste_c(c, character("neutral", "phone"), W / 2, 1330, 0.7)
    paste_c(c, pill(["Ответ — в видео"], F("Bold", 50), (20, 20, 24), (255, 236, 160, 255)), W / 2, 1610)
    return c

def napkin():
    c = radial((40, 18, 10), (150, 80, 30), cy=0.35, r=1100).convert("RGBA")
    big(c, ["Придумал компанию", "на салфетке"], 470, 92)
    nap = Image.new("RGBA", (700, 420), (0, 0, 0, 0)); d = ImageDraw.Draw(nap)
    d.rounded_rectangle([0, 0, 699, 419], 18, fill=(252, 250, 244))
    for k, s in enumerate(["Вы присылаете ТЗ →", "я делаю приложение!"]): d.text((50, 110 + k * 120), s, font=F("Bold", 54), fill=(40, 60, 160))
    paste_c(c, nap.rotate(-5, resample=Image.BICUBIC, expand=True), W / 2, 870, 1.0)
    paste_c(c, character("happy", "wave"), W / 2, 1390, 0.6)
    paste_c(c, pill(["История Exclusive Apps"], F("Bold", 48), (255, 236, 160), (0, 0, 0, 0)), W / 2, 1640)
    return c

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for name, fn in [("ep3", ep3), ("quiz_price", quiz), ("napkin_story", napkin)]:
        fn().convert("RGB").save(f"{OUT}/2026-11-22_{name}_cover.jpg", quality=92)
    print("ok")
