"""Эп.3 «Среда, которую никто не планировал» (22.11, 12:40). Разгадка: задачу поставил ноутбук-помощник, ждал учитель
информатики (первый клиент). Клиффхэнгер: «Четверг, 8:00 — зайди к директору». Голос Speko: Озодбек Dmitry, ноутбук cartesia.
Usage: reel_ep3.py voice_dir out.mp4 [--frames sheet.jpg]"""
import math, os, sys
from PIL import Image, ImageDraw, ImageFilter
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from reel_speko_kit import *
import reel_kit_ep1 as rk

VD, OUT = sys.argv[1], sys.argv[2]
SUBS = [("Серия 3. Среда. И сразу сюрприз: контрольную перенесли на сегодня!", "O"),
        ("План рухнул. Но в My Week я просто перетащил задачи. Минута — и всё сходится.", "O"),
        ("Контрольная — пять! А ровно в 15:00 я у школы. С ноутбуком.", "O"),
        ("Признаюсь: задачу поставил я. Тебе написал клиент — я назначил встречу.", "L"),
        ("Клиент?! Это же наш учитель информатики!", "O"),
        ("Он увидел мой My Week и хочет приложение для всей школы. Наш первый клиент!", "O"),
        ("Но в конце ТЗ приписка: «Четверг, 8:00. Зайди к директору». Зачем?!", "O"),
        ("Серия 4 — завтра в 12:40. Подпишись!", "O")]
LINES = [(f"{VD}/o{i + 1}.wav", s, w) for i, (s, w) in enumerate(SUBS)]

ROOM = rk.ROOM.convert("RGBA"); DARK = rk.DARK
NIGHT = vgrad((8, 10, 30), (24, 22, 60)).convert("RGBA")
SKY = vgrad((120, 170, 230), (210, 225, 245)).convert("RGBA")
C = {m: character(m) for m in ("neutral", "happy", "shock", "sad")}
UP = character("happy", "up"); UP_SH = character("shock", "up"); PH = character("happy", "phone"); PH_SH = character("shock", "phone")
Q = rk.qmark()

def school_bg():
    c = SKY.copy(); d = ImageDraw.Draw(c)
    d.rectangle([90, 520, 990, 1300], fill=(236, 214, 180)); d.polygon([(60, 530), (540, 330), (1020, 530)], fill=(190, 70, 60))
    for r in range(3):
        for k in range(5):
            x = 150 + k * 170; y = 620 + r * 200; d.rounded_rectangle([x, y, x + 110, y + 130], 10, fill=(140, 190, 240))
    d.rounded_rectangle([470, 1100, 610, 1300], 14, fill=(120, 80, 50))
    d.rectangle([340, 470, 740, 530], fill=(255, 255, 255)); f = F("Black", 44); tw = text_size(d, "ШКОЛА", f)[0]
    d.text((540 - tw / 2, 474), "ШКОЛА", font=f, fill=(190, 70, 60))
    d.rectangle([0, 1300, W, H], fill=(120, 120, 130))
    return c
SCH = school_bg()

def s1(t, T):
    c = ROOM.copy()
    paste_c(c, pill(["Серия 3"], F("Black", 56), (255, 255, 255), PUR + (255,), pad=(36, 18)), W / 2, 300, pop(t / .35))
    paste_c(c, pill(["Среда"], F("Black", 76), (20, 20, 24), (0, 0, 0, 0)), W / 2, 420, pop((t - .2) / .35) if t > .2 else 0)
    if t > T * .45:
        sh = math.sin(t * 45) * 10 if t < T * .45 + .8 else 0
        paste_c(c, pill(["Контрольная — СЕГОДНЯ!"], F("Black", 56), (255, 255, 255), (220, 50, 50, 255)), W / 2 + sh, 560, pop((t - T * .45) / .3))
    paste_c(c, C["neutral"] if t < T * .45 else UP_SH, W / 2, 1200, 1.0)
    return c

TASKS = [("15:00", "Встреча у школы ???", (220, 50, 50)), ("09:00", "Контрольная", (255, 159, 10)),
         ("17:00", "Футбол", (140, 110, 255)), ("19:00", "Домашка", (52, 199, 89))]
ORDER0 = [2, 3, 0, 1]   # было: контрольная внизу
ORDER1 = [1, 0, 2, 3]   # стало
def task_row(tm, name, col, w=760):
    im = Image.new("RGBA", (w, 150), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, w - 1, 149], 30, fill=(255, 255, 255), outline=(230, 230, 236), width=2)
    d.rounded_rectangle([24, 28, 34, 122], 5, fill=col)
    d.text((58, 26), tm, font=F("SemiBold", 30), fill=(150, 150, 160))
    d.text((58, 70), name, font=F("Bold", 40), fill=(20, 20, 24))
    return im
ROWS = [task_row(*x) for x in TASKS]

def s2(t, T):
    c = NIGHT.copy(); d = ImageDraw.Draw(c)
    d.rounded_rectangle([120, 250, 960, 1130], 50, fill=(248, 248, 250))
    d.text((170, 285), "MY WEEK · Среда", font=F("Black", 46), fill=(20, 20, 24))
    k = ease((t - T * .3) / (T * .4))
    for idx in range(4):
        y0 = 420 + ORDER0.index(idx) * 170; y1 = 420 + ORDER1.index(idx) * 170
        y = y0 + (y1 - y0) * k; x = W / 2 + (40 * math.sin(k * math.pi) if idx == 1 else 0)
        paste_c(c, ROWS[idx], x, y + 75)
    if k >= 1: paste_c(c, pill(["Готово за 1 минуту ✓"], F("Bold", 44), (255, 255, 255), (52, 199, 89, 255)), W / 2, 1210, pop((t - T * .7) / .3))
    paste_c(c, PH, 880, 1420, 0.42)
    return c

def s3(t, T):
    c = SCH.copy()
    paste_c(c, pill(["Контрольная: 5"], F("Black", 58), (255, 255, 255), (52, 199, 89, 255)), W / 2, 290, pop(t / .35))
    if t > T * .45: paste_c(c, pill(["15:00"], F("Black", 72), (255, 255, 255), (220, 50, 50, 255)), 800, 1190, pop((t - T * .45) / .35))
    paste_c(c, C["happy"], 380, 1330, 0.85)
    paste_c(c, LAP[("neutral", False)], 790, 1440, 0.45)
    return c

def chat(sender, lines, w=900):
    f = F("Bold", 40); lh = 54; h = 120 + lh * len(lines)
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, w - 1, h - 1], 40, fill=(245, 245, 250, 248))
    d.text((40, 28), sender, font=F("SemiBold", 30), fill=PUR)
    for i, l in enumerate(lines): d.text((40, 80 + i * lh), l, font=f, fill=(20, 20, 24))
    return im
MSG = chat("Учитель информатики · в 15:00", ["Озодбек, видел твой My Week.", "Сделаешь приложение для школы?"])

def s4(t, T):
    c = BG2.copy()
    paste_c(c, pill(["Задачу поставил я"], F("Black", 58), (255, 255, 255), PUR + (255,)), W / 2, 300, pop(t / .35))
    paste_c(c, LAP[("smug", talking(t) and t < T - .4)], W / 2, 820, 1.1)
    paste_c(c, C["shock"], 870, 1330, 0.45)
    return c

def s5(t, T):
    c = SCH.copy()
    paste_c(c, MSG, W / 2, 330 + 40 * (1 - ease(t / .4)), 1, min(1, t / .3))
    paste_c(c, UP_SH, W / 2, 1250, 0.95)
    return c

def tz_doc(hl=0.0):
    w, h = 820, 860
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, w - 1, h - 1], 36, fill=(255, 255, 255))
    d.text((50, 44), "ТЗ: приложение для школы", font=F("Black", 46), fill=(20, 20, 24))
    d.line([(50, 120), (w - 50, 120)], fill=(230, 230, 236), width=3)
    for i, s in enumerate(["• Расписание уроков", "• Оценки и дневник", "• Чат с родителями", "• Домашка с фото"]):
        d.text((50, 160 + i * 80), s, font=F("SemiBold", 40), fill=(60, 60, 70))
    if hl > 0:
        d.rounded_rectangle([30, 520, w - 30, 820], 28, fill=(255, int(250 - 40 * hl), int(250 - 40 * hl)), outline=(220, 50, 50), width=int(2 + 4 * hl))
    d.text((60, 540), "P.S.", font=F("Bold", 36), fill=(220, 50, 50))
    d.text((60, 600), "Четверг, 8:00 —", font=F("Black", 52), fill=(20, 20, 24))
    d.text((60, 680), "зайди к директору.", font=F("Black", 52), fill=(220, 50, 50))
    return im
DOC0 = tz_doc(0); DOC1 = tz_doc(1)

def s6(t, T):
    c = DARK.copy()
    paste_c(c, pill(["Первый клиент!"], F("Black", 74), (255, 236, 160), (0, 0, 0, 0)), W / 2, 290, pop(t / .35))
    paste_c(c, DOC0, W / 2, 800, 0.85 * pop((t - .2) / .35) if t > .2 else 0)
    paste_c(c, UP, 860, 1380, 0.42)
    return c

def s7(t, T):
    c = NIGHT.copy()
    paste_c(c, DOC1, W / 2, 700 - 120 * ease(t / .6), 1.0)
    for i, (x, y) in enumerate([(130, 1250), (950, 1230)]):
        paste_c(c, Q, x, y + math.sin(t * 3 + i) * 14, 0.7 * pop((t - .8 - i * .15) / .3) if t > .8 + i * .15 else 0)
    paste_c(c, C["shock"], W / 2, 1330, 0.62)
    return c

def s8(t, T):
    c = DARK.copy()
    paste_c(c, pill(["Зачем директор?"], F("Black", 86), (255, 255, 255), (0, 0, 0, 0)), W / 2, 320, pop(t / .35))
    paste_c(c, pill(["Четверг · 8:00 · кабинет директора"], F("Bold", 42), (255, 255, 255), (220, 50, 50, 255)), W / 2, 460, pop((t - .3) / .35) if t > .3 else 0)
    paste_c(c, C["shock"], W / 2, 880 + math.sin(t * 7) * 6, 0.6)
    if t > .9: paste_c(c, pill(["Серия 4 — завтра в 12:40"], F("Black", 58), (255, 236, 160), (0, 0, 0, 0)), W / 2, 1250, pop((t - .9) / .35))
    if t > 1.5: paste_c(c, pill(["Подпишись, чтобы не пропустить"], F("Bold", 44), (255, 255, 255), PUR + (255,)), W / 2, 1370, pop((t - 1.5) / .35))
    if t > 2.1: paste_c(c, pill(["Своё приложение? Пришлите ТЗ · +998 90 970 06 03"], F("SemiBold", 32), (200, 200, 215), (0, 0, 0, 0)), W / 2, 1470, 1, min(1, (t - 2.1) / .3))
    return c

if __name__ == "__main__":
    fr = sys.argv[sys.argv.index("--frames") + 1] if "--frames" in sys.argv else False
    make_reel(LINES, [s1, s2, s3, s4, s5, s6, s7, s8], OUT, os.path.dirname(os.path.abspath(OUT)) + "/ep3_scenes", seed=31, frames=fr, tail=2.6)
