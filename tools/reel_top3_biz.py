"""Топ-3 приложения для бизнеса в Ташкенте (21.11, 18:10): монолог Озодбека (Dmitry) + реплика ноутбука. Usage: reel_top3_biz.py voice_dir out.mp4 [--frames x.jpg]"""
import math, os, sys
import numpy as np
from PIL import Image, ImageDraw
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from reel_speko_kit import *

VD, OUT = sys.argv[1], sys.argv[2]
N = 37
SUBS = [("3 приложения, которые нужны бизнесу в Ташкенте прямо сейчас", "O"),
        ("№3: автомойка. Онлайн-очередь — и никто не ждёт час в Сергели.", "O"),
        ("№2: учебный центр. Расписание, оплата через Payme, и родители видят, был ли ребёнок на уроке.", "O"),
        ("№1: спортзал. Абонемент в телефоне, вход по QR-коду и напоминание, если пропустил тренировку.", "O"),
        ("А какое приложение нужно вашему бизнесу?", "L"),
        ("Пришлите ТЗ — сделаем. И подпишись: нас уже 37, цель — 1000!", "O")]
LINES = [(f"{VD}/t{i + 1}.wav", s, w) for i, (s, w) in enumerate(SUBS)]
C = {m: character(m) for m in ("neutral", "happy", "shock")}
WAVE = character("happy", "wave"); UP = character("happy", "up")
BGS = [radial((10, 10, 16), g, cy=0.4, r=1000).convert("RGBA") for g in [(40, 30, 110), (10, 80, 120), (20, 90, 60), (110, 40, 40)]]

def num_badge(n, col):
    return pill([f"№{n}"], F("Black", 90), (255, 255, 255), col + (255,), pad=(40, 16), radius=40)

def wash():
    im, d = phone_frame("Мойка «Сергели»", "Онлайн-очередь")
    for i, (car, st, col) in enumerate([("Cobalt · 01 A 123 BC", "моется", (52, 199, 89)), ("Malibu · 10 B 777 AA", "следующий", (255, 159, 10)),
                                        ("Вы · Spark", "3-й · ~20 мин", PUR)]):
        card(d, 40, 230 + i * 190, 540, 170, st, car, col)
    d.rounded_rectangle([40, 860, 580, 960], 30, fill=PUR)
    f = F("Black", 38); tw = text_size(d, "Записаться", f)[0]; d.text((310 - tw / 2, 888), "Записаться", font=f, fill=(255, 255, 255))
    d.text((60, 1000), "Без очереди у ворот ✓", font=F("Bold", 32), fill=(52, 199, 89))
    return im
def school():
    im, d = phone_frame("Учебный центр", "Юнусабад · английский")
    card(d, 40, 230, 540, 170, "Сегодня 16:00", "English B1 · каб. 3", (60, 150, 255))
    card(d, 40, 420, 540, 170, "Посещаемость", "Алишер был ✓", (52, 199, 89), (52, 160, 80))
    card(d, 40, 610, 540, 170, "Оплата за месяц", "450 000 сум", (255, 159, 10))
    d.rounded_rectangle([40, 820, 580, 920], 30, fill=(20, 200, 200))
    f = F("Black", 38); tw = text_size(d, "Оплатить Payme", f)[0]; d.text((310 - tw / 2, 848), "Оплатить Payme", font=f, fill=(255, 255, 255))
    return im
def gym():
    im, d = phone_frame("Спортзал", "Абонемент: 8 из 12")
    rng = np.random.default_rng(4); x0, y0, s = 130, 240, 360; n = 21; cs = s / n
    d.rounded_rectangle([x0 - 20, y0 - 20, x0 + s + 20, y0 + s + 20], 24, fill=(255, 255, 255), outline=(230, 230, 236), width=2)
    for i in range(n):
        for j in range(n):
            fo = [(0, 0), (0, n - 7), (n - 7, 0)]; on = None
            for fi, fj in fo:
                if fi <= i < fi + 7 and fj <= j < fj + 7:
                    a_, b_ = i - fi, j - fj; on = a_ in (0, 6) or b_ in (0, 6) or (2 <= a_ <= 4 and 2 <= b_ <= 4)
            if on is not None: pass
            else: on = rng.random() < .5
            if on: d.rectangle([x0 + j * cs, y0 + i * cs, x0 + (j + 1) * cs, y0 + (i + 1) * cs], fill=(20, 20, 24))
    d.text((150, 650), "Вход по QR-коду", font=F("Bold", 36), fill=(20, 20, 24))
    card(d, 40, 720, 540, 170, "Напоминание", "Ты пропустил 2 дня!", (255, 69, 58), (230, 50, 50))
    return im
PH = [wash(), school(), gym()]

def s1(t, T):
    c = BGS[0].copy()
    paste_c(c, pill(["ТОП-3"], F("Black", 130), (255, 236, 160), (0, 0, 0, 0)), W / 2, 330, pop(t / .3))
    paste_c(c, pill(["приложения для бизнеса", "в Ташкенте"], F("Black", 64), (255, 255, 255), (0, 0, 0, 0)), W / 2, 520, pop((t - .2) / .35) if t > .2 else 0)
    paste_c(c, WAVE if talking(t, 5) else C["happy"], W / 2, 1180, 1.05)
    return c

def item(k, title, col):
    def fn(t, T):
        c = BGS[k + 1].copy()
        paste_c(c, num_badge(3 - k, col), 230, 330, pop(t / .3))
        paste_c(c, pill([title], F("Black", 62), (255, 255, 255), (0, 0, 0, 0)), 650, 330, pop((t - .15) / .3) if t > .15 else 0)
        paste_c(c, PH[k], 420, 960 + 60 * (1 - ease(t / .4)), 0.92, ease(t / .3))
        paste_c(c, C["happy"] if talking(t, 4) else C["neutral"], 900, 1250, 0.42)
        return c
    return fn

CHIPS = [("Салон", (255, 69, 58)), ("Магазин", (255, 159, 10)), ("Офис", (60, 150, 255)), ("Клиника", (52, 199, 89)), ("Такси", (180, 120, 255)), ("Своё?", PUR)]
def s5(t, T):
    c = BG2.copy()
    paste_c(c, pill(["А вашему бизнесу?"], F("Black", 74), (255, 255, 255), (0, 0, 0, 0)), W / 2, 330, pop(t / .3))
    for i, (g, col) in enumerate(CHIPS):
        x = 220 + (i % 3) * 320; y = 490 + (i // 3) * 120
        paste_c(c, pill([g], F("Bold", 44), (255, 255, 255), col + (255,), pad=(30, 16)), x, y, pop((t - .2 - i * .1) / .3) if t > .2 + i * .1 else 0)
    paste_c(c, LAP[("neutral", talking(t, 6) and t < T - .4)], W / 2, 1150, 1.0)
    return c

def s6(t, T):
    c = BGS[0].copy()
    paste_c(c, pill(["Пришлите ТЗ — сделаем!"], F("Black", 64), (255, 255, 255), (0, 0, 0, 0)), W / 2, 300, pop(t / .35))
    paste_c(c, pill(["+998 90 970 06 03"], F("Black", 56), (255, 255, 255), PUR + (255,)), W / 2, 430, pop((t - .3) / .35) if t > .3 else 0)
    if t > 1.0:
        paste_c(c, pill([f"{N} / 1000"], F("Black", 60), (20, 20, 24), (255, 255, 255, 255), colors=[PUR]), W / 2, 570, pop((t - 1) / .35))
        d = ImageDraw.Draw(c); x0, x1, y = 190, 890, 660
        d.rounded_rectangle([x0, y, x1, y + 30], 15, fill=(50, 50, 70)); d.rounded_rectangle([x0, y, x0 + max(30, (x1 - x0) * N / 1000), y + 30], 15, fill=PUR)
    if t > 2.0: paste_c(c, pill([f"Подпишись — ты будешь {N + 1}-м"], F("Bold", 46), (255, 236, 160), (0, 0, 0, 0)), W / 2, 760, 1, min(1, (t - 2) / .3))
    paste_c(c, UP if talking(t, 4) and t < T - 1 else C["happy"], W / 2, 1250, 0.85)
    return c

SC = [s1, item(0, "Автомойка", (60, 150, 255)), item(1, "Учебный центр", (52, 199, 89)), item(2, "Спортзал", (255, 69, 58)), s5, s6]
if __name__ == "__main__":
    fr = sys.argv[sys.argv.index("--frames") + 1] if "--frames" in sys.argv else False
    make_reel(LINES, SC, OUT, os.path.dirname(os.path.abspath(OUT)) + "/top_scenes", seed=21, frames=fr, tail=2.0)
