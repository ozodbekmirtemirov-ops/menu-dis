"""Звонок-счётчик №2 «38 / 1000» (23.11, 18:10), ~22 с. Ноутбук звонит Озодбеку; повод переслать: «каждый отправляет рилс одному другу».
Графика звонка — из reel_1000_phonecall.py. Usage: reel_call_38.py voice_dir out.mp4 [--frames sheet.jpg]"""
import math, os, sys
from PIL import Image, ImageDraw
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from reel_speko_kit import *
import reel_1000_phonecall as pc

VD, OUT = sys.argv[1], sys.argv[2]
N, DAYS, PER = 38, 39, 25
SUBS = [(f"Алло, Озодбек? Нас {N}. До тысячи — {DAYS} дней.", "L"),
        (f"Это {PER} человек в день! Как?!", "O"),
        ("Просто. Каждый, кто это смотрит, отправляет рилс одному другу.", "L"),
        ("Одному другу? Тогда завтра нас будет вдвое больше!", "O"),
        (f"Подпишись и отправь другу. Ты будешь {N + 1}-м!", "O")]
LINES = [(f"{VD}/k{i + 1}.wav", s, w) for i, (s, w) in enumerate(SUBS)]
BGC = pc.BG; PLAP = pc.LAP

def desk(c, t, idx, talk_l, expr="neutral", ring=False):
    paste_c(c, PLAP[(expr, talk_l and int(t * 7) % 2 == 0)], W / 2 - 40, 1090 + math.sin(t * 2) * 5, 1.1)
    rr = math.sin(t * 50) * 10 if ring else 0
    paste_c(c, pc.RECV.rotate(-15, expand=True, resample=Image.BICUBIC), W / 2 - 390, 1000, 0.95)
    paste_c(c, pc.PHONE, 860 + rr, 1370, 0.9)

def bubble(c, mood, talk, t):
    paste_c(c, pc.oz_bubble(mood, talk and int(t * 7) % 2 == 0, 1), 880, 560, 0.62)

def calendar(n):
    cal = Image.new("RGBA", (200, 210), (0, 0, 0, 0)); d = ImageDraw.Draw(cal)
    d.rounded_rectangle([0, 0, 199, 209], 26, fill=(255, 255, 255)); d.rounded_rectangle([0, 0, 199, 56], 26, fill=(255, 69, 58)); d.rectangle([0, 30, 199, 56], fill=(255, 69, 58))
    d.text((44, 8), "дней", font=F("Bold", 32), fill=(255, 255, 255))
    f = F("Black", 100); tw = text_size(d, str(n), f)[0]; d.text(((200 - tw) / 2, 66), str(n), font=f, fill=(20, 20, 24))
    return cal

def s1(t, T):
    c = BGC.copy()
    paste_c(c, pill([f"{N} / 1000"], F("Black", 120), (255, 255, 255), PUR + (255,), pad=(50, 24)), W / 2, 330, pop(t / .3))
    desk(c, t, 0, t > .6, ring=t < .6)
    if t > T * .55: paste_c(c, calendar(DAYS), 220, 640, pop((t - T * .55) / .3))
    bubble(c, "neutral", False, t)
    return c

def s2(t, T):
    c = BGC.copy()
    paste_c(c, pill([f"962 ÷ {DAYS} ≈ {PER} в день"], F("Black", 62), (255, 255, 255), (20, 16, 40, 235)), W / 2, 330, pop(t / .3))
    desk(c, t, 1, False, "wide")
    bubble(c, "shock", True, t)
    return c

def chain(k):
    im = Image.new("RGBA", (960, 260), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    items = [("1 рилс", PUR), ("→", None), ("1 друг", (52, 160, 89)), ("→", None), ("×2", (230, 60, 90))]
    x = 0
    for i, (s, col) in enumerate(items):
        if k < i / len(items): break
        f = F("Black", 64); tw = text_size(d, s, f)[0]
        if col: d.rounded_rectangle([x, 60, x + tw + 60, 200], 40, fill=col); d.text((x + 30, 88), s, font=f, fill=(255, 255, 255)); x += tw + 80
        else: d.text((x, 88), s, font=f, fill=(255, 255, 255)); x += tw + 20
    return im

def s3(t, T):
    c = BGC.copy()
    paste_c(c, chain(t / (T * .7)), W / 2 + 20, 290)
    desk(c, t, 2, True, "smug")
    bubble(c, "neutral", False, t)
    return c

def s4(t, T):
    c = BGC.copy()
    k = ease(t / (T * .7)); n = int(N + N * k)
    paste_c(c, pill([f"{n} / 1000"], F("Black", 120), (120, 230, 140), (0, 0, 0, 0)), W / 2, 330, 1)
    paste_c(c, pill(["завтра?"], F("Bold", 50), (20, 20, 24), (255, 236, 160, 255)), W / 2, 470, pop((t - .3) / .3) if t > .3 else 0)
    desk(c, t, 3, False)
    bubble(c, "happy", True, t)
    return c

def s5(t, T):
    c = BGC.copy()
    a = min(1, t / .4); ov = Image.new("RGBA", (W, H), (8, 6, 20, int(200 * a))); c.alpha_composite(ov)
    paste_c(c, pill(["Подпишись", "и отправь другу"], F("Black", 90), (255, 255, 255), (0, 0, 0, 0)), W / 2, 450, pop(t / .3))
    paste_c(c, pill([f"ты будешь {N + 1}-м"], F("Black", 70), (120, 230, 140), (0, 0, 0, 0)), W / 2, 680, pop((t - .3) / .3) if t > .3 else 0)
    paste_c(c, character("happy", "wave"), W / 2, 1060, 0.55)
    if t > .9: paste_c(c, pill(["@exclusive_apps.uz · ТЗ: +998 90 970 06 03"], F("Bold", 38), (20, 20, 24), (255, 255, 255, 245)), W / 2, 1400, pop((t - .9) / .3))
    return c

if __name__ == "__main__":
    fr = sys.argv[sys.argv.index("--frames") + 1] if "--frames" in sys.argv else False
    make_reel(LINES, [s1, s2, s3, s4, s5], OUT, os.path.dirname(os.path.abspath(OUT)) + "/call_scenes", seed=97, frames=fr, tail=1.8)
