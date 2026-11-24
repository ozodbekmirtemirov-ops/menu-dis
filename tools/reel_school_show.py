"""Витрина My School «Мама уже знает твою оценку» (24.11, 16:10), ~20 с. Повод переслать: «отправь другу, который прячет дневник».
Голос Speko: Озодбек Dmitry, ноутбук cartesia. Usage: reel_school_show.py voice_dir out.mp4 [--frames sheet.jpg]"""
import math, os, sys
from PIL import Image, ImageDraw
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from reel_speko_kit import *
import reel_kit_ep1 as rk

VD, OUT = sys.argv[1], sys.argv[2]
SUBS = [("Ты ещё идёшь из школы, а мама уже знает твою оценку.", "O"),
        ("Это My School: оценки, домашка и расписание — в одном телефоне.", "O"),
        ("Родителям — уведомление. Учителю — фото домашки. И никаких «я забыл дневник».", "L"),
        ("Отправь другу, который прячет дневник! А своё приложение — пришлите ТЗ.", "O")]
LINES = [(f"{VD}/s{i + 1}.wav", s, w) for i, (s, w) in enumerate(SUBS)]
ORG = (255, 159, 10)
GLOW = radial((14, 10, 6), (140, 80, 10), cy=0.42, r=1000).convert("RGBA")
DARK = rk.DARK
SKY = vgrad((120, 170, 230), (210, 225, 245)).convert("RGBA")
SH = character("shock", "phone"); WAVE = character("happy", "wave"); HP = character("happy", "phone")

def notif(k):
    b = Image.new("RGBA", (900, 230), (0, 0, 0, 0)); d = ImageDraw.Draw(b)
    d.rounded_rectangle([0, 0, 899, 229], 40, fill=(255, 255, 255, 250))
    d.rounded_rectangle([30, 34, 110, 114], 20, fill=ORG); d.text((56, 44), "5", font=F("Black", 54), fill=(255, 255, 255))
    d.text((130, 36), "My School · сейчас", font=F("SemiBold", 30), fill=(140, 140, 150))
    d.text((130, 80), "Алгебра: 3", font=F("Black", 52), fill=(230, 60, 70))
    d.text((130, 150), "Азиз, 8 «Б» · Юнусабад", font=F("Medium", 32), fill=(80, 80, 90))
    return b

def s1(t, T):
    c = SKY.copy(); d = ImageDraw.Draw(c)
    d.rectangle([0, 1350, W, H], fill=(120, 120, 130))
    paste_c(c, pill(["Мама уже знает", "твою оценку"], F("Black", 100), (255, 255, 255), (220, 50, 50, 255)), W / 2, 330, pop(t / .3))
    paste_c(c, notif(1), W / 2, 640 - 60 * (1 - ease((t - .5) / .4)), 1, min(1, max(0, (t - .5) / .3)))
    paste_c(c, SH, W / 2, 1180 + math.sin(t * 9) * 6, 0.85)
    return c

def school_phone(k):
    im, d = phone_frame("My School", "8 «Б» · вторник", accent=ORG)
    rows = [("Алгебра", "5", (52, 199, 89)), ("Физика", "4", (60, 150, 255)), ("Домашка: литература", "фото ✓", ORG),
            ("Расписание", "7:55 · 6 уроков", PUR), ("Родители", "уведомлены ✓", (52, 199, 89))]
    for i, (a, v, col) in enumerate(rows):
        if k > i * .17: card(d, 40, 220 + i * 160, 540, 136, a, v, col)
    return im

def s2(t, T):
    c = GLOW.copy()
    paste_c(c, pill(["My School"], F("Black", 64), (255, 255, 255), ORG + (255,)), W / 2, 230, pop(t / .3))
    paste_c(c, school_phone(t / (T * .8)), W / 2, 920, 0.98)
    return c

def s3(t, T):
    c = DARK.copy()
    items = [("Родителям", "уведомление", (52, 199, 89)), ("Учителю", "фото домашки", (60, 150, 255)), ("Дневник", "не нужен", (220, 50, 50))]
    for i, (a, b, col) in enumerate(items):
        st = i * T * .22
        if t > st:
            paste_c(c, pill([a, b], F("Black", 56), (255, 255, 255), col + (255,), pad=(40, 20)), W / 2 - 150, 330 + i * 270, pop((t - st) / .3))
    paste_c(c, LAP[("smug", talking(t) and t < T - .4)], 830, 1180, 0.5)
    return c

def s4(t, T):
    c = DARK.copy()
    paste_c(c, pill(["Отправь другу,", "который", "прячет дневник"], F("Black", 84), (255, 255, 255), (0, 0, 0, 0), colors=[(255, 255, 255), (255, 255, 255), (255, 236, 160)]), W / 2, 420, pop(t / .3))
    paste_c(c, WAVE, W / 2, 1000, 0.6)
    if t > .8: paste_c(c, pill(["Своё приложение? Пришлите ТЗ"], F("Bold", 46), (255, 255, 255), PUR + (255,)), W / 2, 1330, pop((t - .8) / .3))
    if t > 1.3: paste_c(c, pill(["+998 90 970 06 03 · подпишись — нас 38, цель 1000"], F("SemiBold", 34), (210, 210, 225), (0, 0, 0, 0)), W / 2, 1440, 1, min(1, (t - 1.3) / .3))
    return c

if __name__ == "__main__":
    fr = sys.argv[sys.argv.index("--frames") + 1] if "--frames" in sys.argv else False
    make_reel(LINES, [s1, s2, s3, s4], OUT, os.path.dirname(os.path.abspath(OUT)) + "/school_scenes", seed=127, frames=fr, tail=1.8)
