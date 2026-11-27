"""r2 27.11 (20:10, главный): «Спросил папу: сколько у нас денег?» — узнаваемая семейная ситуация + витрина My Capital, ~23 с.
Аудитория: школьники/родители, семейный бюджет. Повод переслать: «Отправь папе, который хранит доллары в шкафу».
Голос Speko: Озодбек Dmitry, ноутбук cartesia. Usage: reel_dad_money.py voice_dir out.mp4 [--frames sheet.jpg]"""
import math, os, sys
from PIL import Image, ImageDraw
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from reel_speko_kit import *
import reel_kit_ep1 as rk

VD, OUT = sys.argv[1], sys.argv[2]
SUBS = [("Спросил папу: сколько у нас денег? Он считает уже целый час!", "O"),
        ("Квартира, Нексия, мамино золото, доллары в шкафу. Всё в разных местах.", "L"),
        ("А в My Capital — всё на одном экране. И итог сразу в сумах.", "O"),
        ("Золото выросло, машина подешевела. И ИИ подскажет, что делать.", "L"),
        ("Отправь папе, который хранит доллары в шкафу!", "O")]
LINES = [(f"{VD}/k{i + 1}.wav", s, w) for i, (s, w) in enumerate(SUBS)]
GLOW = radial((8, 12, 10), (20, 110, 60), cy=0.42, r=1000).convert("RGBA")
DARK = rk.DARK
GRN = (52, 199, 89); RED = (230, 60, 70); GOLD = (230, 190, 40)
ASSETS = [("Квартира · Юнусабад", "950 млн сум", (60, 150, 255)), ("Nexia 3", "120 млн сум", (255, 159, 10)),
          ("Золото", "85 млн сум", GOLD), ("Доллары · $3 000", "38 млн сум", GRN), ("Карта Uzcard", "6 млн сум", (110, 70, 255))]
SH = character("shock"); HP = character("happy", "phone"); WAVE = character("happy", "wave"); UP = character("happy", "up")

def calc(k):  # «папин калькулятор» — бумажка с подсчётами
    im = Image.new("RGBA", (560, 520), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, 559, 519], 20, fill=(255, 250, 225))
    for i in range(7): d.line([30, 90 + i * 60, 530, 90 + i * 60], fill=(200, 215, 240), width=2)
    rows = ["квартира ?", "машина ??", "золото ???", "$ в шкафу…", "= ??????"]
    for i, s in enumerate(rows):
        if k > i * .18: d.text((40, 40 + i * 92), s, font=F("Bold", 54), fill=(60, 60, 200) if i < 4 else RED)
    return im

def s1(t, T):  # крючок
    c = DARK.copy()
    sh = math.sin(t * 40) * 9 if t < .8 else 0
    paste_c(c, pill(["Папа, сколько", "у нас денег?"], F("Black", 100), (255, 255, 255), RED + (255,)), W / 2 + sh, 360, pop(t / .3))
    if t > T * .5: paste_c(c, pill(["считает уже 1 час"], F("Black", 56), (20, 20, 24), (255, 236, 160, 255)), W / 2, 590, pop((t - T * .5) / .3))
    paste_c(c, calc(t / (T * .9)), 770, 1000, 0.85, min(1, t / .3))
    paste_c(c, SH, 290, 1150 + math.sin(t * 9) * 5, 0.7)
    return c

ICONS = [("Квартира", (60, 150, 255), (190, 470)), ("Nexia", (255, 159, 10), (870, 430)), ("Золото", GOLD, (220, 860)),
         ("$ в шкафу", GRN, (860, 830))]

def s2(t, T):  # всё в разных местах
    c = DARK.copy()
    paste_c(c, pill(["Всё в разных местах"], F("Black", 72), (255, 255, 255), PUR + (255,)), W / 2, 230, pop(t / .3))
    for i, (s, col, (x, y)) in enumerate(ICONS):
        k = (t - .3 - i * T * .15) / .3
        if k > 0: paste_c(c, pill([s], F("Black", 56), (255, 255, 255), col + (255,)), x, y + math.sin(t * 3 + i) * 10, pop(k))
    paste_c(c, LAP[("wide", talking(t) and t < T - .4)], W / 2, 1180, 0.6)
    return c

def cap_phone(k):
    im, d = phone_frame("My Capital", "вся семья · в сумах")
    for i, (a, v, col) in enumerate(ASSETS):
        if k > i * .14: card(d, 40, 220 + i * 150, 540, 128, a, v, col)
    if k > .85:
        d.rounded_rectangle([40, 990, 580, 1120], 28, fill=(20, 20, 24))
        d.text((70, 1008), "Итого", font=F("SemiBold", 28), fill=(170, 170, 180))
        d.text((70, 1050), "1,2 млрд сум", font=F("Black", 46), fill=(120, 230, 140))
    return im

def s3(t, T):
    c = GLOW.copy()
    paste_c(c, pill(["Один экран"], F("Black", 64), (255, 255, 255), GRN + (255,)), W / 2, 210, pop(t / .3))
    paste_c(c, cap_phone(t / (T * .85)), 640, 930, 0.95)
    paste_c(c, UP, 190, 1300, 0.42)
    return c

def s4(t, T):  # рост/падение + ИИ
    c = DARK.copy()
    paste_c(c, pill(["Золото  +14% ▲"], F("Black", 64), (20, 20, 24), GOLD + (255,)), W / 2, 300, pop(t / .3))
    if t > T * .25: paste_c(c, pill(["Nexia  −9% ▼"], F("Black", 64), (255, 255, 255), RED + (255,)), W / 2, 460, pop((t - T * .25) / .3))
    if t > T * .5:
        b = Image.new("RGBA", (880, 260), (0, 0, 0, 0)); d = ImageDraw.Draw(b)
        d.rounded_rectangle([0, 0, 879, 259], 44, fill=(255, 255, 255))
        d.rounded_rectangle([36, 34, 150, 84], 20, fill=PUR); d.text((58, 38), "ИИ", font=F("Black", 36), fill=(255, 255, 255))
        d.text((170, 40), "советчик", font=F("SemiBold", 34), fill=(140, 140, 150))
        d.text((40, 130), "Машина дешевеет. Что делать?", font=F("Black", 46), fill=(20, 20, 24))
        paste_c(c, b, W / 2, 680, 1, min(1, (t - T * .5) / .3))
    paste_c(c, LAP[("smug", talking(t) and t < T - .4)], W / 2, 1180, 0.6)
    return c

def s5(t, T):
    c = DARK.copy()
    paste_c(c, pill(["Отправь папе,", "который хранит", "доллары в шкафу"], F("Black", 84), (255, 255, 255), (0, 0, 0, 0),
                    colors=[(255, 255, 255), (255, 255, 255), (255, 236, 160)]), W / 2, 400, pop(t / .3))
    paste_c(c, WAVE, W / 2, 960, 0.55)
    if t > .6: paste_c(c, pill(["Своё приложение? Пришлите ТЗ"], F("Bold", 46), (255, 255, 255), PUR + (255,)), W / 2, 1290, pop((t - .6) / .3))
    if t > 1.0: paste_c(c, pill(["+998 90 970 06 03"], F("Bold", 40), (210, 210, 225), (0, 0, 0, 0)), W / 2, 1400, 1, min(1, (t - 1.0) / .3))
    return c

if __name__ == "__main__":
    fr = sys.argv[sys.argv.index("--frames") + 1] if "--frames" in sys.argv else False
    make_reel(LINES, [s1, s2, s3, s4, s5], OUT, os.path.dirname(os.path.abspath(OUT)) + "/dad_scenes", seed=233, frames=fr, tail=1.6)
