"""Reel: знакомство — Озодбек открыл Exclusive Apps. Timed to voiceover."""
import math, os, subprocess, sys
from PIL import Image, ImageDraw
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from reel_kit_ep1 import (W, H, FPS, F, ease, pop, pill, paste_c, text_size, radial, vgrad, character,
                        CHAR, CHAR_UP_HAPPY, app_icon, render, TMP)

CHAR_WAVE = character("happy", "up")
CHAR_PH = character("happy", "phone")
DARK = radial((10, 10, 14), (24, 40, 90)).convert("RGBA")
PURPLE = radial((10, 8, 16), (70, 40, 140)).convert("RGBA")
GREEN = radial((8, 12, 10), (20, 90, 50)).convert("RGBA")
LIGHT = vgrad((236, 240, 248), (250, 250, 252)).convert("RGBA")

def ea_logo(size=260):
    im = Image.new("RGBA", (size, size), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, size - 1, size - 1], int(size * .24), fill=(110, 70, 255))
    f = F("Black", int(size * .42)); tw, th, oy = text_size(d, "EA", f)
    d.text(((size - tw) / 2, (size - th) / 2 - oy), "EA", font=f, fill=(255, 255, 255)); return im

def mini_icon(col, glyph, size=170):
    im = Image.new("RGBA", (size, size), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, size - 1, size - 1], int(size * .24), fill=col)
    f = F("Black", int(size * .42)); tw, th, oy = text_size(d, glyph, f)
    d.text(((size - tw) / 2, (size - th) / 2 - oy), glyph, font=f, fill=(255, 255, 255)); return im

def phone_frame(title, sub, rows, t, dark=False):
    """rows: list of (left_text, right_text, color) appearing one by one."""
    pw, ph = 640, 1180
    im = Image.new("RGBA", (pw, ph), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    bg, fg, card, mute = ((14, 14, 18), (255, 255, 255), (30, 30, 36), (150, 150, 160)) if dark else ((248, 248, 250), (20, 20, 24), (255, 255, 255), (140, 140, 150))
    d.rounded_rectangle([0, 0, pw - 1, ph - 1], 90, fill=(18, 18, 22))
    d.rounded_rectangle([18, 18, pw - 19, ph - 19], 74, fill=bg)
    d.rounded_rectangle([pw / 2 - 90, 40, pw / 2 + 90, 82], 21, fill=(18, 18, 22))
    d.text((56, 120), title, font=F("Black", 44), fill=fg)
    d.text((56, 178), sub, font=F("Medium", 28), fill=mute)
    y = 250
    for i, (a_, b_, col) in enumerate(rows):
        k = ease((t - 0.25 - i * 0.3) / 0.3)
        if k <= 0: break
        c = Image.new("RGBA", (pw - 112, 140), (0, 0, 0, 0)); cd = ImageDraw.Draw(c)
        cd.rounded_rectangle([0, 0, c.width - 1, 139], 28, fill=card, outline=None if dark else (232, 232, 238), width=2)
        cd.ellipse([24, 35, 94, 105], fill=col)
        f = F("Bold", 34); cd.text((118, 30), a_, font=f, fill=fg)
        cd.text((118, 80), b_, font=F("Medium", 26), fill=mute)
        if k < 1: c.putalpha(c.getchannel("A").point(lambda v: int(v * k)))
        im.alpha_composite(c, (56, int(y + (1 - k) * 50))); y += 160
    return im

def head_caption(c, text, t, y=330, color=(255, 255, 255), size=64, delay=0.0):
    paste_c(c, pill([text], F("Black", size), color, (0, 0, 0, 0)), W / 2, y, pop((t - delay) / 0.35) if t > delay else 0, min(1, max(0, (t - delay) / 0.2)))

def sub_caption(c, lines, t, y=1700, delay=0.15, colors=None):
    p = pill(lines, F("Bold", 48), (20, 20, 24), (255, 255, 255, 245), colors=colors)
    paste_c(c, p, W / 2, y, pop((t - delay) / 0.35) if t > delay else 0)

# ---- scenes (durations from voiceover pauses) ----
def s1(t, T):  # Привет! Меня зовут Озодбек, 14
    c = DARK.copy()
    wave = abs(math.sin(t * 7)) * 25
    paste_c(c, CHAR_WAVE if int(t * 4) % 2 == 0 else CHAR["happy"], W / 2, 1150 - wave * (t < 1.2), 1.05, ease(t / 0.25))
    head_caption(c, "Привет!", t, 330)
    sub_caption(c, ["Меня зовут Озодбек,", "мне 14 лет"], t, delay=0.9)
    return c

def s2(t, T):  # открыл компанию Exclusive Apps
    c = PURPLE.copy()
    paste_c(c, ea_logo(300), W / 2, 560, pop(t / 0.4))
    head_caption(c, "Exclusive Apps", t, 820, size=82, delay=0.5)
    paste_c(c, CHAR["happy"], W / 2, 1380, 0.75, ease((t - 0.2) / 0.3))
    sub_caption(c, ["Я открыл свою компанию"], t, y=1750, delay=0.1)
    return c

ICONS = [((60, 150, 255), "Aa"), ((52, 199, 89), "$"), ((255, 159, 10), "★"), ((255, 69, 58), "♥"),
         ((175, 82, 222), "✓"), ((90, 200, 250), "@"), ((255, 204, 0), "7"), ((48, 209, 88), "%"), ((10, 132, 255), "+")]
ICON_IM = [mini_icon(c_, g) for c_, g in ICONS]
def s3(t, T):  # любое приложение
    c = DARK.copy()
    head_caption(c, "Любое приложение", t, 360, size=74)
    for i, im in enumerate(ICON_IM):
        r, col = divmod(i, 3); st = 0.25 + i * 0.12
        if t < st: continue
        paste_c(c, im, 290 + col * 250, 640 + r * 250 + math.sin(t * 3 + i) * 6, pop((t - st) / 0.3))
    sub_caption(c, ["какое вы захотите"], t, y=1520, delay=0.6)
    return c

def s4(t, T):  # офис — сотрудники
    c = LIGHT.copy()
    head_caption(c, "Для офиса", t, 250, color=(20, 20, 24))
    ph = phone_frame("Сотрудники", "Сегодня в офисе: 3 из 4", [
        ("Азиз", "Пришёл 08:58", (52, 199, 89)), ("Мадина", "Пришла 09:02", (52, 199, 89)),
        ("Жасур", "Опоздал 09:41", (255, 159, 10)), ("Камила", "Нет на месте", (255, 69, 58))], t)
    paste_c(c, ph, W / 2, 1020, 1.0, ease(t / 0.3))
    sub_caption(c, ["Отслеживание сотрудников"], t, y=1730, delay=0.4)
    return c

def s5(t, T):  # школа — ученики
    c = LIGHT.copy()
    head_caption(c, "Для школы", t, 250, color=(20, 20, 24))
    ph = phone_frame("7 «Б» класс", "Средний балл: 4.6", [
        ("Алишер", "Математика: 5", (60, 150, 255)), ("Сабина", "Физика: 5", (60, 150, 255)),
        ("Тимур", "Английский: 4", (90, 200, 250)), ("Нигора", "История: 5", (60, 150, 255))], t)
    paste_c(c, ph, W / 2, 1020, 1.0, ease(t / 0.3))
    sub_caption(c, ["Ученики и оценки"], t, y=1730, delay=0.4)
    return c

def s6(t, T):  # лично для вас
    c = GREEN.copy()
    head_caption(c, "Для вас лично", t, 330, size=72)
    paste_c(c, CHAR_PH, W / 2, 1150, 1.0)
    for i, (col, g) in enumerate([((255, 159, 10), "★"), ((52, 199, 89), "$"), ((255, 69, 58), "♥")]):
        st = 0.2 + i * 0.2
        if t > st: paste_c(c, mini_icon(col, g, 150), 230 + i * 310, 600 + math.sin(t * 4 + i) * 10, pop((t - st) / 0.3))
    return c

ICON_W = app_icon(230)
def cap_icon():
    im = Image.new("RGBA", (230, 230), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, 229, 229], 54, fill=(30, 140, 70))
    for i, h in enumerate([60, 95, 130, 160]):
        d.rounded_rectangle([40 + i * 40, 190 - h, 66 + i * 40, 190], 8, fill=(255, 255, 255))
    d.line([(40, 120), (90, 90), (130, 100), (190, 45)], fill=(255, 214, 10), width=12); return im
def school_icon():
    im = Image.new("RGBA", (230, 230), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, 229, 229], 54, fill=(60, 120, 255))
    d.polygon([(115, 50), (200, 95), (115, 140), (30, 95)], fill=(255, 255, 255))
    d.rectangle([70, 115, 160, 170], fill=(255, 255, 255)); d.line([(190, 100), (190, 160)], fill=(255, 214, 10), width=8); return im
APPS = [(ICON_W, "My Week", 2.15), (cap_icon(), "My Capital", 2.9), (school_icon(), "My School", 3.85)]
def s7(t, T):  # три готовых приложения
    c = DARK.copy()
    head_caption(c, "3 готовых приложения", t, 420, size=66)
    for i, (im, name, st) in enumerate(APPS):
        if t < st - 0.1: continue
        k = pop((t - st + 0.1) / 0.35); y = 760 + i * 330
        paste_c(c, im, 330, y, k)
        paste_c(c, pill([name], F("Black", 62), (255, 255, 255), (0, 0, 0, 0)), 640, y, 1, min(1, (t - st + 0.1) / 0.25))
    return c

def s8(t, T):  # Хотите своё? Пишите в директ
    c = PURPLE.copy()
    paste_c(c, CHAR_UP_HAPPY, W / 2, 1340 - abs(math.sin(t * 5)) * 25, 0.8)
    head_caption(c, "Хотите своё?", t, 330, size=84)
    p = pill(["Пишите нам в директ!"], F("Bold", 54), (20, 20, 24), (255, 255, 255, 255), colors=[(110, 70, 255)])
    paste_c(c, p, W / 2, 500, pop((t - 0.35) / 0.35) if t > 0.35 else 0)
    if t > 0.9:
        a = min(1, (t - 0.9) / 0.3)
        paste_c(c, pill(["+998 90 970 06 03"], F("SemiBold", 46), (255, 255, 255), (0, 0, 0, 0)), W / 2, 640, 1, a)
        paste_c(c, pill(["Пришлите ТЗ — сделаем"], F("Medium", 38), (190, 180, 230), (0, 0, 0, 0)), W / 2, 720, 1, a)
    return c

CUTS = [0, 3.40, 6.43, 9.75, 12.80, 16.10, 17.97, 22.59, 27.0]
SCENES = list(zip([s1, s2, s3, s4, s5, s6, s7, s8], [CUTS[i + 1] - CUTS[i] for i in range(8)]))

if __name__ == "__main__":
    if "--frames" in sys.argv:
        tiles = [fn(dur * 0.85, dur).convert("RGB").resize((270, 480)) for fn, dur in SCENES]
        s = Image.new("RGB", (270 * 4, 480 * 2))
        for i, im in enumerate(tiles): s.paste(im, ((i % 4) * 270, (i // 4) * 480))
        s.save("peek_intro.jpg"); sys.exit()
    files = []
    for i, (fn, dur) in enumerate(SCENES):
        pth = f"{TMP}/i{i:02d}.mp4"; render(fn, dur, pth, fade=0.12); files.append(pth)
    open(f"{TMP}/ilist.txt", "w").write("".join(f"file '{os.path.basename(f)}'\n" for f in files))
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", f"{TMP}/ilist.txt", "-c", "copy", "intro_noaudio.mp4"], check=True)
    print("done")
