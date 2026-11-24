"""5 историй дня, 1080x1920, текст в пределах y=250..1600. Usage: stories_daily.py DATE N_FOLLOWERS out_dir"""
import os, sys, math
from PIL import Image, ImageDraw
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from reel_kit_ep1 import W, H, F, pill, paste_c, text_size, radial, app_icon
from character_v2 import character

DATE, N, OUT = sys.argv[1], int(sys.argv[2]), sys.argv[3]
PUR = (110, 70, 255)
def bg(glow): return radial((10, 10, 16), glow, cy=0.42, r=1000).convert("RGBA")
def txt(c, lines, y, size=64, col=(255, 255, 255), w="Black"):
    paste_c(c, pill(lines, F(w, size), col, (0, 0, 0, 0)), W / 2, y)
def badge(c, y=300):
    paste_c(c, pill([f"{N} / 1000"], F("Black", 54), (255, 255, 255), PUR + (255,), pad=(40, 18)), W / 2, y)
def tile(col, glyph, size=200):
    im = Image.new("RGBA", (size, size), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, size - 1, size - 1], int(size * .24), fill=col)
    f = F("Black", int(size * .4)); tw, th, oy = text_size(d, glyph, f)
    d.text(((size - tw) / 2, (size - th) / 2 - oy), glyph, font=f, fill=(255, 255, 255)); return im

def s1(plan):  # счётчик
    c = bg((40, 30, 110)); badge(c, 300)
    txt(c, ["Нас уже " + str(N) + "!"], 470, 84)
    d = ImageDraw.Draw(c); x0, x1, y = 140, 940, 600
    d.rounded_rectangle([x0, y, x1, y + 44], 22, fill=(50, 50, 70))
    d.rounded_rectangle([x0, y, x0 + max(44, (x1 - x0) * N / 1000), y + 44], 22, fill=PUR)
    txt(c, ["Цель — 1000 до 31 декабря"], 700, 42, (190, 190, 205), "SemiBold")
    paste_c(c, character("happy", "wave"), W / 2, 1110, 0.62)
    paste_c(c, pill(["Подпишись —", f"ты будешь {N + 1}-м"], F("Bold", 54), (20, 20, 24), (255, 255, 255, 255), colors=[(20, 20, 24), PUR]), W / 2, 1480)
    return c

def s2(plan):  # анонс рилсов
    c = bg((20, 70, 140)); badge(c, 280)
    txt(c, ["Сегодня в ленте"], 420, 76)
    y = 560
    for tm, title in plan:
        p = pill([f"{tm}  {title}"], F("Bold", 44), (20, 20, 24), (255, 255, 255, 245), pad=(36, 22), radius=28)
        paste_c(c, p, W / 2, y); y += 130
    paste_c(c, character("happy", "phone"), W / 2, 1270, 0.55)
    txt(c, ["Не пропусти!"], 1560, 56, (255, 236, 160))
    return c

def s3(plan):  # вопрос
    c = bg((90, 30, 120)); badge(c, 280)
    txt(c, ["Какое приложение", "нужно ВАМ?"], 470, 76)
    for i, (col, g) in enumerate([((60, 150, 255), "Офис"), ((52, 199, 89), "Школа"), ((255, 159, 10), "Магазин"), ((255, 69, 58), "Своё?")]):
        paste_c(c, pill([g], F("Bold", 40), (255, 255, 255), col + (255,), pad=(30, 16)), 200 + i * 227, 680)
    paste_c(c, character("neutral", "phone"), W / 2, 1110, 0.6)
    paste_c(c, pill(["Напишите в директ —", "лучшую идею покажем в рилсе"], F("Bold", 46), (20, 20, 24), (255, 255, 255, 255), colors=[PUR, (20, 20, 24)]), W / 2, 1490)
    return c

def s4(plan):  # портфолио
    c = bg((20, 90, 60)); badge(c, 280)
    txt(c, ["Что мы уже сделали"], 420, 72)
    apps = [(app_icon(200), "My Week", "планировщик"), (tile((52, 199, 89), "$"), "My Capital", "учёт капитала"),
            (tile((255, 159, 10), "5"), "My School", "игра-урок по QR")]
    for i, (ic, name, sub) in enumerate(apps):
        x = W / 2 if i == 2 else (300 if i == 0 else 780); y = 680 + (i // 2) * 420
        paste_c(c, ic, x, y, 0.95)
        paste_c(c, pill([name], F("Bold", 44), (255, 255, 255), (0, 0, 0, 0)), x, y + 145)
        paste_c(c, pill([sub], F("Medium", 34), (180, 200, 190), (0, 0, 0, 0)), x, y + 200)
    paste_c(c, character("happy", "wave"), 860, 1180, 0.3)
    txt(c, ["Следующее — ваше?"], 1560, 56, (255, 236, 160))
    return c

def s5(plan):  # ТЗ + телефон
    c = bg((80, 40, 160)); badge(c, 280)
    txt(c, ["Как заказать приложение"], 410, 64)
    steps = ["1. Пришлите ТЗ", "2. Дизайн и план", "3. Разработка", "4. Правки — готово!"]
    for i, s in enumerate(steps):
        paste_c(c, pill([s], F("Bold", 48), (20, 20, 24), (255, 255, 255, 245), pad=(40, 22)), W / 2, 560 + i * 125)
    paste_c(c, character("happy", "up"), W / 2, 1230, 0.42)
    paste_c(c, pill(["+998 90 970 06 03"], F("Black", 62), (255, 255, 255), PUR + (255,), pad=(44, 24)), W / 2, 1470)
    txt(c, ["или «ТЗ» в директ"], 1575, 40, (210, 210, 225), "SemiBold")
    return c

if __name__ == "__main__":
    plan = [p.split("|") for p in sys.argv[4:]] or [("12:40", "Серия 1"), ("16:10", "Рилс 2"), ("19:10", "Рилс 3")]
    os.makedirs(OUT, exist_ok=True)
    for i, fn in enumerate([s1, s2, s3, s4, s5], 1):
        fn(plan).convert("RGB").save(f"{OUT}/{DATE}_{i}.png")
    print("ok")

def teaser(title, hook, sub, path):
    """Доп. история-анонс отдельного рилса (не портфолио). teaser('Плов за час', '6 недель или 1 час?', 'Новый рилс уже в ленте', path)"""
    c = bg((150, 70, 30)); badge(c, 280)
    txt(c, ["Новый рилс"], 420, 50, (255, 236, 160), "Bold")
    txt(c, [f"«{title}»"], 510, 80)
    paste_c(c, pill([hook], F("Bold", 56), (20, 20, 24), (255, 255, 255, 255)), W / 2, 680)
    paste_c(c, character("shock", "up"), W / 2, 1130, 0.6)
    paste_c(c, pill([sub], F("Bold", 50), (255, 255, 255), PUR + (255,), pad=(40, 22)), W / 2, 1500)
    c.convert("RGB").save(path)
