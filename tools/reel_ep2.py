"""Эп.2 «Первый вторник с планом» (21.11, 12:40). Голос Speko Dmitry. Usage: reel_ep2.py voice_dir out.mp4 [--frames]"""
import math, os, sys
from PIL import Image, ImageDraw, ImageFilter
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from reel_speko_kit import *
import reel_kit_ep1 as rk

VD, OUT = sys.argv[1], sys.argv[2]
SUBS = ["Серия 2. Вторник. Будильник в 7:00 — и я встал. Сам!",
        "Позавтракал. Сдал домашку. Учитель чуть не упал со стула!",
        "А вечером — футбол с друзьями. И ни одного долга.",
        "Но в My Week всё ещё висит та задача: «Среда, 15:00». Я её удаляю…",
        "…а она возвращается! Опять!",
        "Друг клянётся, что это не он. Тогда кто?",
        "И тут уведомление: «Среда, 15:00. Будь у школы. Возьми ноутбук».",
        "Кто это пишет?! Серия 3 — завтра в 12:40. Подпишись!"]
LINES = [(f"{VD}/o{i + 1}.wav", s, "O") for i, s in enumerate(SUBS)]

ROOM = rk.ROOM.convert("RGBA") if rk.ROOM.mode != "RGBA" else rk.ROOM
DARK = rk.DARK; GREEN = rk.GREEN
NIGHT = vgrad((8, 10, 30), (24, 22, 60)).convert("RGBA")
C = {m: character(m) for m in ("neutral", "happy", "shock", "sad", "sleepy")}
UP = character("happy", "up"); PH = character("neutral", "phone"); PH_SH = character("shock", "phone"); UP_SH = character("shock", "up")
CLOCK = rk.alarm_clock("7:00")

def s1(t, T):
    c = ROOM.copy()
    sh = math.sin(t * 50) * 8 if t < 1.6 else 0
    paste_c(c, CLOCK, 270 + sh, 470, 0.8 * pop(t / .3))
    paste_c(c, pill(["Серия 2"], F("Black", 56), (255, 255, 255), PUR + (255,), pad=(36, 18)), 760, 360, pop(t / .35))
    paste_c(c, pill(["Вторник"], F("Black", 72), (20, 20, 24), (0, 0, 0, 0)), 760, 480, pop((t - .2) / .35) if t > .2 else 0)
    paste_c(c, C["sleepy"] if t < 1.4 else UP, W / 2, 1180, 1.05)
    return c

def s2(t, T):
    c = ROOM.copy()
    checks = 1 if t < T * 0.45 else 2
    paste_c(c, rk.phone(1, checks), 330, 900, 0.9)
    paste_c(c, C["happy"], 830, 1250, 0.6)
    if t > T * 0.55:
        paste_c(c, pill(["Домашка сдана ✓"], F("Bold", 44), (255, 255, 255), (52, 199, 89, 255)), 790, 420, pop((t - T * .55) / .3))
        paste_c(c, pill(["Учитель в шоке"], F("Bold", 40), (20, 20, 24), (255, 255, 255, 255)), 790, 530, pop((t - T * .65) / .3) if t > T * .65 else 0)
    return c

def ball(r=70):
    im = Image.new("RGBA", (2 * r, 2 * r), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.ellipse([0, 0, 2 * r - 1, 2 * r - 1], fill=(255, 255, 255), outline=(30, 30, 30), width=4)
    pts = [(r + r * .35 * math.cos(a), r + r * .35 * math.sin(a)) for a in [math.pi * 2 * k / 5 - math.pi / 2 for k in range(5)]]
    d.polygon(pts, fill=(30, 30, 30))
    return im
BALL = ball()

def s3(t, T):
    c = GREEN.copy(); d = ImageDraw.Draw(c)
    d.rectangle([0, 1450, W, H], fill=(30, 110, 60)); d.line([(0, 1452), (W, 1452)], fill=(220, 255, 220), width=6)
    bx = 160 + (t / T) * 760; by = 1000 - abs(math.sin(t * 3.2)) * 380
    paste_c(c, BALL.rotate(-t * 300), bx, by)
    paste_c(c, UP if talking(t, 3) else C["happy"], W / 2, 1150, 1.0)
    paste_c(c, pill(["Выполнено 4 из 4"], F("Black", 52), (255, 255, 255), (20, 20, 24, 255)), W / 2, 330, pop(t / .35))
    return c

def task_card(alpha=1, red=0.0):
    im = Image.new("RGBA", (760, 230), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, 759, 229], 34, fill=(255, int(240 - 120 * red), int(240 - 120 * red)))
    d.text((40, 30), "Среда, 15:00", font=F("Bold", 36), fill=(220, 40, 40))
    d.text((40, 84), "???", font=F("Black", 84), fill=(20, 20, 24))
    d.text((250, 118), "добавлено: не тобой", font=F("SemiBold", 32), fill=(200, 60, 60))
    return im
TASK = task_card()

def s4(t, T):
    c = NIGHT.copy()
    paste_c(c, pill(["MY WEEK"], F("Black", 60), (255, 255, 255), (0, 0, 0, 0)), W / 2, 330)
    k = ease((t - T * 0.5) / (T * 0.4))           # свайп влево
    bin_ = pill(["Удалить"], F("Bold", 44), (255, 255, 255), (230, 50, 50, 255), pad=(40, 30))
    if k > 0: paste_c(c, bin_, 860, 640)
    paste_c(c, TASK, W / 2 - 700 * k, 640, 1, 1 - 0.7 * k)
    paste_c(c, PH, W / 2, 1220, 0.95)
    return c

def s5(t, T):
    c = NIGHT.copy()
    paste_c(c, pill(["MY WEEK"], F("Black", 60), (255, 255, 255), (0, 0, 0, 0)), W / 2, 330)
    sh = math.sin(t * 45) * 10 if t < 1.0 else 0
    paste_c(c, TASK, W / 2 + sh, 640, pop(t / .3))
    paste_c(c, pill(["Задача вернулась"], F("Bold", 44), (255, 255, 255), (230, 50, 50, 255)), W / 2, 850, pop((t - .3) / .3) if t > .3 else 0)
    paste_c(c, UP_SH, W / 2, 1250, 0.95)
    return c

Q = rk.qmark()
def s6(t, T):
    c = DARK.copy()
    for i, (x, y) in enumerate([(200, 520), (880, 470), (160, 900), (920, 880)]):
        paste_c(c, Q, x, y + math.sin(t * 3 + i) * 14, 0.8 * pop((t - i * .15) / .3) if t > i * .15 else 0)
    paste_c(c, pill(["Друг: «Это не я!»"], F("Bold", 54), (20, 20, 24), (255, 255, 255, 255)), W / 2, 340, pop(t / .35))
    paste_c(c, C["shock"], W / 2, 1180, 1.0)
    return c

def notif(t):
    im = Image.new("RGBA", (960, 250), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, 959, 249], 44, fill=(245, 245, 250, 245))
    paste_c(im, rk.app_icon(110), 90, 125)
    d.text((170, 34), "MY WEEK · сейчас", font=F("SemiBold", 30), fill=(120, 120, 130))
    d.text((170, 80), "Среда 15:00: будь у школы.", font=F("Bold", 40), fill=(20, 20, 24))
    d.text((170, 140), "Возьми ноутбук.", font=F("Bold", 40), fill=(220, 40, 40))
    return im
NOTIF = notif(0)

def s7(t, T):
    c = NIGHT.copy(); d = ImageDraw.Draw(c)
    d.ellipse([860, 110, 960, 210], fill=(250, 240, 200))
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0)); ImageDraw.Draw(glow).ellipse([200, 800, 880, 1500], fill=(120, 170, 255, int(90 * min(1, t / .4))))
    c.alpha_composite(glow.filter(ImageFilter.GaussianBlur(70)))
    y = -150 + 650 * ease(t / .45)
    paste_c(c, NOTIF, W / 2, y)
    paste_c(c, PH_SH, W / 2, 1200, 1.0)
    return c

def s8(t, T):
    c = DARK.copy()
    paste_c(c, pill(["Кто это пишет?"], F("Black", 86), (255, 255, 255), (0, 0, 0, 0)), W / 2, 330, pop(t / .35))
    paste_c(c, pill(["Среда, 15:00 · у школы · ноутбук"], F("Bold", 42), (255, 255, 255), (220, 50, 50, 255)), W / 2, 470, pop((t - .3) / .35) if t > .3 else 0)
    paste_c(c, C["shock"], W / 2, 900 + math.sin(t * 7) * 6, 0.62)
    if t > 1.2: paste_c(c, pill(["Серия 3 — завтра в 12:40"], F("Black", 58), (255, 236, 160), (0, 0, 0, 0)), W / 2, 1270, pop((t - 1.2) / .35))
    if t > 2.0: paste_c(c, pill(["Подпишись, чтобы не пропустить"], F("Bold", 44), (255, 255, 255), PUR + (255,)), W / 2, 1390, pop((t - 2.0) / .35))
    if t > 2.6: paste_c(c, pill(["Своё приложение? Пришлите ТЗ · +998 90 970 06 03"], F("SemiBold", 32), (200, 200, 215), (0, 0, 0, 0)), W / 2, 1490, 1, min(1, (t - 2.6) / .3))
    return c

if __name__ == "__main__":
    fr = sys.argv[sys.argv.index("--frames") + 1] if "--frames" in sys.argv else False
    make_reel(LINES, [s1, s2, s3, s4, s5, s6, s7, s8], OUT, os.path.dirname(os.path.abspath(OUT)) + "/ep2_scenes", seed=7, frames=fr, tail=2.2)
