"""«3 мифа, из-за которых твоя идея — не приложение» (24.11, 18:10), ~25 с. Диалог с ноутбуком.
Повод переслать: «отправь другу, у которого идея лежит в заметках». Usage: reel_myths3.py voice_dir out.mp4 [--frames sheet.jpg]"""
import math, os, sys
from PIL import Image, ImageDraw
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from reel_speko_kit import *
import reel_kit_ep1 as rk

VD, OUT = sys.argv[1], sys.argv[2]
SUBS = [("3 мифа, из-за которых твоя идея до сих пор не приложение.", "O"),
        ("Миф №1: надо уметь программировать. Нет! Нужно только ТЗ, код пишем мы.", "L"),
        ("Миф №2: приложения — только для больших компаний. Мойке в Сергели оно тоже нужно.", "L"),
        ("Миф №3: нужно сразу всё. Начните с одной главной функции.", "L"),
        ("Отправь другу, у которого идея лежит в заметках. И присылайте ТЗ!", "O")]
LINES = [(f"{VD}/m{i + 1}.wav", s, w) for i, (s, w) in enumerate(SUBS)]
DARK = rk.DARK
RED = (220, 50, 50); GRN = (52, 199, 89)
O_SH = character("shock"); WAVE = character("happy", "wave"); HP = character("happy", "phone")

def notes(k):
    im = Image.new("RGBA", (620, 520), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, 619, 519], 40, fill=(255, 250, 225))
    d.text((40, 30), "Заметки", font=F("Black", 44), fill=(200, 150, 20))
    for i, s in enumerate(["идея: приложение для…", "когда-нибудь сделаю", "надо найти программиста", "2023 · 2024 · 2025…"]):
        if k > i * .2: d.text((40, 120 + i * 90), s, font=F("SemiBold", 36), fill=(60, 60, 70))
    return im

def s1(t, T):
    c = radial((10, 10, 14), (90, 30, 40)).convert("RGBA")
    paste_c(c, pill(["3 МИФА"], F("Black", 120), (255, 255, 255), RED + (255,)), W / 2, 330, pop(t / .3))
    paste_c(c, pill(["почему твоя идея", "всё ещё в заметках"], F("Black", 60), (255, 236, 160), (0, 0, 0, 0)), W / 2, 560, pop((t - .3) / .3) if t > .3 else 0)
    paste_c(c, notes(t / (T * .7)), 680, 1050, 0.85, min(1, t / .4))
    paste_c(c, O_SH, 230, 1200 + math.sin(t * 9) * 5, 0.55)
    return c

def myth(n, myth_lines, truth_lines, icon=None):
    def s(t, T):
        c = DARK.copy()
        paste_c(c, pill([f"Миф №{n}"], F("Black", 56), (255, 255, 255), RED + (255,), pad=(36, 16)), W / 2, 240, pop(t / .3))
        k = ease((t - .2) / .4)
        paste_c(c, pill(myth_lines, F("Black", 64), (255, 255, 255), (0, 0, 0, 0)), W / 2, 450, 1, min(1, max(0, t / .3)))
        if t > T * .42:
            d = ImageDraw.Draw(c); kk = ease((t - T * .42) / .25)
            for yy in (428, 492): d.line([(150, yy), (150 + 780 * kk, yy - 8 * kk)], fill=RED, width=12)
            paste_c(c, pill(truth_lines, F("Black", 58), (20, 20, 24), (255, 236, 160, 255)), W / 2, 720, pop((t - T * .5) / .3) if t > T * .5 else 0)
        paste_c(c, LAP[("smug", talking(t) and t < T - .4)], W / 2, 1180, 0.62)
        return c
    return s

def s5(t, T):
    c = DARK.copy()
    paste_c(c, pill(["Отправь другу,", "у которого идея", "в заметках"], F("Black", 84), (255, 255, 255), (0, 0, 0, 0), colors=[(255, 255, 255), (255, 255, 255), (255, 236, 160)]), W / 2, 420, pop(t / .3))
    paste_c(c, WAVE, W / 2, 1000, 0.6)
    if t > .8: paste_c(c, pill(["Идея есть? Пришлите ТЗ"], F("Bold", 46), (255, 255, 255), PUR + (255,)), W / 2, 1330, pop((t - .8) / .3))
    if t > 1.3: paste_c(c, pill(["+998 90 970 06 03 · подпишись — ты будешь 39-м"], F("SemiBold", 34), (210, 210, 225), (0, 0, 0, 0)), W / 2, 1440, 1, min(1, (t - 1.3) / .3))
    return c

SC = [s1, myth(1, ["Надо уметь", "программировать"], ["Нужно только ТЗ —", "код пишем мы"]),
      myth(2, ["Только для", "больших компаний"], ["Мойке в Сергели", "тоже нужно"]),
      myth(3, ["Нужно", "сразу всё"], ["Начните с одной", "главной функции"]), s5]

if __name__ == "__main__":
    fr = sys.argv[sys.argv.index("--frames") + 1] if "--frames" in sys.argv else False
    make_reel(LINES, SC, OUT, os.path.dirname(os.path.abspath(OUT)) + "/myths_scenes", seed=139, frames=fr, tail=1.8)
