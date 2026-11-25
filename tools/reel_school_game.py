"""Витрина My School (ПРАВИЛЬНАЯ) «Двоечник впервые поднял руку» (25.11, 20:10, r2), ~22 с.
Учитель запускает игру -> класс сканирует QR -> урок-игра, стараются все -> результаты в админке завуча и директора.
Повод переслать: «Отправь учителю, у которого скучные уроки». Usage: reel_school_game.py voice_dir out.mp4 [--frames sheet.jpg]"""
import math, os, sys
from PIL import Image, ImageDraw
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from reel_speko_kit import *
from school_game_ui import qr, game_phone, admin_phone, class_row, ORG, GRN
import reel_kit_ep1 as rk

VD, OUT = sys.argv[1], sys.argv[2]
SUBS = [("Двоечник впервые поднял руку. Знаете, почему?", "O"),
        ("Учитель запустил игру My School. Класс сканирует QR-код — и урок превращается в игру.", "O"),
        ("Стараются все, даже задние парты. А результаты класса завуч и директор видят в админке.", "L"),
        ("Отправь учителю, у которого скучные уроки! А своё приложение — пришлите ТЗ.", "O")]
LINES = [(f"{VD}/s{i + 1}.wav", s, w) for i, (s, w) in enumerate(SUBS)]
GLOW = radial((14, 10, 6), (140, 80, 10), cy=0.42, r=1000).convert("RGBA")
CLASS = vgrad((40, 70, 60), (20, 36, 30)).convert("RGBA")
DARK = rk.DARK
UP = character("happy", "up"); WAVE = character("happy", "wave")
QR = qr(400, seed=11)

def board(c):
    d = ImageDraw.Draw(c); d.rounded_rectangle([90, 180, W - 90, 640], 24, fill=(30, 60, 45), outline=(150, 110, 70), width=16)
    d.text((140, 220), "Алгебра · 8 «Б»", font=F("Bold", 44), fill=(220, 235, 225))
    d.text((140, 300), "7 × 8 = ?", font=F("Black", 120), fill=(255, 255, 255))

def s1(t, T):  # крючок: двоечник поднял руку
    c = CLASS.copy(); board(c)
    paste_c(c, pill(["Двоечник впервые", "поднял руку"], F("Black", 92), (255, 255, 255), (220, 50, 50, 255)), W / 2, 760, pop(t / .3))
    paste_c(c, UP, W / 2, 1270 + math.sin(t * 9) * 8, 0.78)
    if t > .6: paste_c(c, pill(["оценка: 2"], F("Black", 44), (255, 255, 255), (120, 120, 130, 255), pad=(26, 12)), 830, 1050, pop((t - .6) / .3))
    return c

def s2(t, T):  # QR -> игра
    c = GLOW.copy()
    paste_c(c, pill(["My School"], F("Black", 64), (255, 255, 255), ORG + (255,)), W / 2, 220, pop(t / .3))
    k = t / T
    if k < .4:
        paste_c(c, QR, W / 2, 700, 1.0, min(1, t / .3))
        d = ImageDraw.Draw(c); y = 520 + int(360 * ((t * 1.4) % 1))
        d.rectangle([330, y, 750, y + 8], fill=(255, 70, 70))
        paste_c(c, pill(["Сканируй QR"], F("Black", 60), (20, 20, 24), (255, 255, 255, 255)), W / 2, 1050)
    else:
        paste_c(c, game_phone((k - .4) / .55), W / 2, 830, 0.88, min(1, (k - .4) / .1))
    paste_c(c, class_row(k * 1.2), W / 2, 1360, 0.8)
    return c

def s3(t, T):  # админка
    c = DARK.copy()
    paste_c(c, pill(["Стараются все"], F("Black", 64), (20, 20, 24), (255, 236, 160, 255)), W / 2, 200, pop(t / .3))
    paste_c(c, admin_phone(t / (T * .75)), 440, 880, 0.82)
    paste_c(c, LAP[("smug", talking(t) and t < T - .4)], 880, 1300, 0.42)
    if t > T * .45: paste_c(c, pill(["завуч", "директор"], F("Black", 50), (255, 255, 255), PUR + (255,)), 880, 880, pop((t - T * .45) / .3))
    return c

def s4(t, T):
    c = DARK.copy()
    paste_c(c, pill(["Отправь учителю,", "у которого", "скучные уроки"], F("Black", 84), (255, 255, 255), (0, 0, 0, 0), colors=[(255, 255, 255), (255, 255, 255), (255, 236, 160)]), W / 2, 420, pop(t / .3))
    paste_c(c, WAVE, W / 2, 1000, 0.6)
    if t > .8: paste_c(c, pill(["Своё приложение? Пришлите ТЗ"], F("Bold", 46), (255, 255, 255), PUR + (255,)), W / 2, 1330, pop((t - .8) / .3))
    if t > 1.3: paste_c(c, pill(["+998 90 970 06 03 · TZ yuboring"], F("SemiBold", 36), (210, 210, 225), (0, 0, 0, 0)), W / 2, 1440, 1, min(1, (t - 1.3) / .3))
    return c

if __name__ == "__main__":
    fr = sys.argv[sys.argv.index("--frames") + 1] if "--frames" in sys.argv else False
    make_reel(LINES, [s1, s2, s3, s4], OUT, os.path.dirname(os.path.abspath(OUT)) + "/sg_scenes", seed=171, frames=fr, tail=1.8)
