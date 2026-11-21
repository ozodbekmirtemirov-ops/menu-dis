"""Карусель 1080x1350 «ТЗ на приложение за 5 минут» (21.11). Usage: carousel_tz.py out_dir DATE N"""
import os, sys
from PIL import Image, ImageDraw
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from reel_kit_ep1 import F, pill, text_size
from character_v2 import character
import numpy as np

OUT, DATE, N = sys.argv[1], sys.argv[2], int(sys.argv[3])
CW, CH = 1080, 1350; PUR = (110, 70, 255)
def bg(glow):
    y, x = np.mgrid[0:CH, 0:CW]; d = np.sqrt((x - CW / 2) ** 2 + (y - CH * .4) ** 2) / 900
    k = np.clip(1 - d, 0, 1)[..., None] ** 2
    return Image.fromarray((np.array((10, 10, 16)) * (1 - k) + np.array(glow) * k).astype(np.uint8)).convert("RGBA")
def put(c, im, cx, cy, s=1.0):
    if s != 1: im = im.resize((int(im.width * s), int(im.height * s)), Image.LANCZOS)
    c.alpha_composite(im, (int(cx - im.width / 2), int(cy - im.height / 2)))
def wrap(d, text, f, maxw):
    out, cur = [], ""
    for w in text.split():
        t = (cur + " " + w).strip()
        if text_size(d, t, f)[0] > maxw and cur: out.append(cur); cur = w
        else: cur = t
    return out + [cur]
def footer(c, i, n):
    d = ImageDraw.Draw(c)
    d.text((60, CH - 80), "@exclusive_apps.uz", font=F("SemiBold", 30), fill=(170, 170, 190))
    s = f"{i} / {n}  →" if i < n else f"{i} / {n}"; tw = text_size(d, s, F("Bold", 30))[0]
    d.text((CW - 60 - tw, CH - 80), s, font=F("Bold", 30), fill=(170, 170, 190))

STEPS = [("1", "Для кого приложение?", "Клиенты, сотрудники, ученики? Сколько человек и где — Чиланзар, весь Ташкент, вся страна.", (60, 150, 255), "Пример: «Для клиентов салона, ~300 человек»"),
         ("2", "Какую проблему решает?", "Одно предложение. Что сейчас неудобно и что станет лучше.", (52, 199, 89), "Пример: «Записи теряются в Telegram»"),
         ("3", "3 главные функции", "Только самое нужное для первой версии. Остальное — потом.", (255, 159, 10), "Пример: запись к мастеру, оплата Click, напоминание"),
         ("4", "Где работает?", "iPhone, Android, сайт — или всё сразу. Нужна ли админка для вас.", (255, 69, 58), "Пример: Android + iPhone + админка"),
         ("5", "На что похоже?", "1–2 приложения, которые нравятся, и что в них НЕ нравится.", (180, 120, 255), "Пример: «Как Yandex Go, но для автомойки»")]
n = len(STEPS) + 2; os.makedirs(OUT, exist_ok=True)

c = bg((60, 40, 150)); d = ImageDraw.Draw(c)
put(c, pill(["Сохрани"], F("Bold", 40), (255, 255, 255), PUR + (255,), pad=(30, 14)), CW / 2, 150)
put(c, pill(["Как написать ТЗ", "на приложение", "за 5 минут"], F("Black", 84), (255, 255, 255), (0, 0, 0, 0)), CW / 2, 380)
put(c, pill(["5 вопросов — и разработчик вас поймёт"], F("SemiBold", 40), (255, 236, 160), (0, 0, 0, 0)), CW / 2, 600)
put(c, character("happy", "wave"), CW / 2, 1000, 0.62); footer(c, 1, n)
c.convert("RGB").save(f"{OUT}/{DATE}_car_1.png")

for i, (num, title, body, col, ex) in enumerate(STEPS, 2):
    c = bg(tuple(int(v * .5) for v in col)); d = ImageDraw.Draw(c)
    d.rounded_rectangle([60, 120, 220, 280], 40, fill=col)
    f = F("Black", 110); tw, th, oy = text_size(d, num, f); d.text((140 - tw / 2, 200 - th / 2 - oy), num, font=f, fill=(255, 255, 255))
    y = 340
    for l in wrap(d, title, F("Black", 86), 960): d.text((60, y), l, font=F("Black", 86), fill=(255, 255, 255)); y += 104
    y += 30
    for l in wrap(d, body, F("Medium", 52), 960): d.text((60, y), l, font=F("Medium", 52), fill=(215, 215, 230)); y += 70
    y += 50
    lines = wrap(d, ex, F("Bold", 40), 860); h = 50 + 54 * len(lines)
    d.rounded_rectangle([60, y, CW - 60, y + h], 30, fill=(255, 255, 255))
    d.rounded_rectangle([60, y, 76, y + h], 8, fill=col)
    for k, l in enumerate(lines): d.text((110, y + 25 + k * 54), l, font=F("Bold", 40), fill=(20, 20, 24))
    put(c, character("neutral" if i % 2 else "happy", "phone" if i % 2 else "down"), CW - 300, 1150, 0.34); footer(c, i, n)
    c.convert("RGB").save(f"{OUT}/{DATE}_car_{i}.png")

c = bg((80, 40, 160)); d = ImageDraw.Draw(c)
put(c, pill(["Не получается?", "Пришлите черновик"], F("Black", 74), (255, 255, 255), (0, 0, 0, 0)), CW / 2, 260)
put(c, pill(["Даже 1 строка — поможем", "превратить её в ТЗ"], F("Bold", 46), (20, 20, 24), (255, 255, 255, 255), colors=[(20, 20, 24), PUR]), CW / 2, 480)
put(c, pill(["+998 90 970 06 03"], F("Black", 62), (255, 255, 255), PUR + (255,), pad=(44, 24)), CW / 2, 640)
put(c, pill(["или «ТЗ» в директ"], F("SemiBold", 40), (210, 210, 225), (0, 0, 0, 0)), CW / 2, 740)
put(c, character("happy", "up"), CW / 2, 1010, 0.42)
put(c, pill([f"Подпишись — нас {N}, цель 1000"], F("Bold", 40), (255, 236, 160), (0, 0, 0, 0)), CW / 2, 1210); footer(c, n, n)
c.convert("RGB").save(f"{OUT}/{DATE}_car_{n}.png")
print("ok", n)
