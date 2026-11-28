"""Витрина My School «до/после» «Звонок прозвенел — а класс не уходит?!» (28.11, 20:10, r2), ~23 с.
ДО: алгебра, полкласса спит. ПОСЛЕ: учитель запускает My School, класс сканирует QR, урок-игра, рейтинг, итоги — в админке
завуча и директора. Повод переслать: «Перешли в чат класса — пусть учитель увидит».
Usage: reel_school_bell.py voice_dir out.mp4 [--frames sheet.jpg]"""
import math, os, sys
from PIL import Image, ImageDraw, ImageEnhance
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from reel_speko_kit import *
from school_game_ui import qr, game_phone, admin_phone, class_row, ORG, GRN
import reel_kit_ep1 as rk

VD, OUT = sys.argv[1], sys.argv[2]
SUBS = [("Звонок прозвенел — а класс не уходит?!", "O"),
        ("До: алгебра, половина класса спит.", "O"),
        ("После: учитель запускает My School. Класс сканирует QR-код — и урок превращается в игру.", "O"),
        ("Вопросы на время, рейтинг класса — стараются все. А итоги завуч и директор видят в админке.", "L"),
        ("Перешли в чат класса — пусть учитель увидит! А своё приложение — пришлите ТЗ.", "O")]
LINES = [(f"{VD}/s{i + 1}.wav", s, w) for i, (s, w) in enumerate(SUBS)]
CLASS = vgrad((40, 70, 60), (20, 36, 30)).convert("RGBA")
GLOW = radial((14, 10, 6), (140, 80, 10), cy=0.42, r=1000).convert("RGBA")
DARK = rk.DARK
RED = (220, 50, 50)
UP_SH = character("shock", "up"); SLEEP = character("sleepy"); HAPPY_UP = character("happy", "up"); WAVE = character("happy", "wave")
QR = qr(380, seed=23)

def board(c, title="Алгебра · 8 «Б»", body="x² − 5x + 6 = 0"):
    d = ImageDraw.Draw(c); d.rounded_rectangle([90, 200, W - 90, 560], 24, fill=(30, 60, 45), outline=(150, 110, 70), width=16)
    d.text((140, 236), title, font=F("Bold", 44), fill=(220, 235, 225))
    d.text((140, 320), body, font=F("Black", 96), fill=(255, 255, 255))

def bell(t):
    im = Image.new("RGBA", (220, 220), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.pieslice([30, 20, 190, 220], 180, 360, fill=(255, 200, 40)); d.rectangle([30, 118, 190, 150], fill=(255, 200, 40))
    d.ellipse([92, 140, 128, 176], fill=(200, 140, 20))
    return im.rotate(math.sin(t * 30) * 18, center=(110, 30))

def s1(t, T):  # крючок
    c = CLASS.copy(); board(c, body="ДЗЫНЬ!")
    sh = math.sin(t * 40) * 10 if t < .9 else 0
    paste_c(c, bell(t), 900, 260)
    paste_c(c, pill(["Звонок прозвенел —", "а класс НЕ уходит?!"], F("Black", 80), (255, 255, 255), RED + (255,), colors=[(255, 255, 255), (255, 236, 160)]), W / 2 + sh, 720, pop(t / .3))
    paste_c(c, class_row(1), W / 2, 1360, 0.85)
    paste_c(c, UP_SH, W / 2, 1100 + math.sin(t * 9) * 6, 0.5)
    return c

def s2(t, T):  # ДО
    c = CLASS.copy(); board(c)
    c = ImageEnhance.Color(c.convert("RGB")).enhance(0.25).convert("RGBA")
    paste_c(c, pill(["ДО"], F("Black", 90), (255, 255, 255), (110, 110, 120, 255), pad=(50, 16)), W / 2, 700, pop(t / .3))
    row = ImageEnhance.Color(class_row(0).convert("RGBA")).enhance(0.3)
    paste_c(c, row, W / 2, 1360, 0.85)
    paste_c(c, SLEEP, W / 2, 1060, 0.48)
    for i, x in enumerate([200, 760, 900]):
        if t > .3 + i * .3: paste_c(c, pill(["Zzz"], F("Black", 54), (200, 200, 215), (0, 0, 0, 0)), x, 1200 - ((t * 60 + i * 40) % 80), 1)
    return c

def s3(t, T):  # ПОСЛЕ: QR -> игра
    c = GLOW.copy(); k = t / T
    paste_c(c, pill(["ПОСЛЕ", "My School"], F("Black", 64), (255, 255, 255), GRN + (255,), colors=[(255, 255, 255), (255, 236, 160)]), W / 2, 240, pop(t / .3))
    if k < .42:
        paste_c(c, QR, W / 2, 720, 1.0, min(1, t / .3))
        d = ImageDraw.Draw(c); y = 545 + int(350 * ((t * 1.4) % 1))
        d.rectangle([345, y, 735, y + 8], fill=(255, 70, 70))
        paste_c(c, pill(["Сканируй QR"], F("Black", 60), (20, 20, 24), (255, 255, 255, 255)), W / 2, 1040)
    else:
        paste_c(c, game_phone((k - .42) / .5).crop((0, 0, 620, 1150)), W / 2, 860, 0.82, min(1, (k - .42) / .1))
    paste_c(c, class_row(k * 1.3), W / 2, 1400, 0.7)
    return c

def s4(t, T):  # рейтинг + админка
    c = DARK.copy()
    paste_c(c, pill(["Стараются ВСЕ"], F("Black", 66), (20, 20, 24), (255, 236, 160, 255)), W / 2, 200, pop(t / .3))
    paste_c(c, admin_phone(t / (T * .75)), 420, 860, 0.8)
    paste_c(c, LAP[("smug", talking(t) and t < T - .4)], 870, 1290, 0.4)
    if t > T * .5: paste_c(c, pill(["завуч", "директор"], F("Black", 50), (255, 255, 255), PUR + (255,)), 870, 860, pop((t - T * .5) / .3))
    return c

def chat(k):
    im = Image.new("RGBA", (880, 330), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, 879, 329], 40, fill=(255, 255, 255, 250))
    d.ellipse([36, 36, 136, 136], fill=(60, 150, 255)); d.text((62, 50), "8Б", font=F("Black", 46), fill=(255, 255, 255))
    d.text((160, 40), "Чат класса · 8 «Б»", font=F("Black", 44), fill=(20, 20, 24))
    d.text((160, 100), "32 участника", font=F("SemiBold", 30), fill=(140, 140, 150))
    if k > .3:
        d.rounded_rectangle([160, 170, 840, 290], 30, fill=(225, 245, 230))
        d.text((190, 196), "Рилс: класс не уходит!", font=F("Bold", 40), fill=(20, 120, 50))
    return im

def s5(t, T):  # CTA
    c = DARK.copy()
    paste_c(c, pill(["Перешли", "в чат класса"], F("Black", 92), (255, 255, 255), (0, 0, 0, 0), colors=[(255, 255, 255), (255, 236, 160)]), W / 2, 330, pop(t / .3))
    paste_c(c, chat(t / 1.2), W / 2, 640, 1, min(1, t / .3))
    paste_c(c, WAVE, W / 2, 1060, 0.5)
    if t > .9: paste_c(c, pill(["Своё приложение? Пришлите ТЗ"], F("Bold", 46), (255, 255, 255), PUR + (255,)), W / 2, 1370, pop((t - .9) / .3))
    if t > 1.4: paste_c(c, pill(["+998 90 970 06 03 · TZ yuboring"], F("SemiBold", 36), (210, 210, 225), (0, 0, 0, 0)), W / 2, 1470, 1, min(1, (t - 1.4) / .3))
    return c

if __name__ == "__main__":
    fr = sys.argv[sys.argv.index("--frames") + 1] if "--frames" in sys.argv else False
    make_reel(LINES, [s1, s2, s3, s4, s5], OUT, os.path.dirname(os.path.abspath(OUT)) + "/bell_scenes", seed=257, frames=fr, tail=1.6)
