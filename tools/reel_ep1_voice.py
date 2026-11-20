"""Эп.1 «Неделя без плана» — версия С ГОЛОСОМ (20.11). Сцены из reel_kit_ep1 (персонаж v2), тайминги по озвучке 37.7 c.
Usage: python3 reel_ep1_voice.py out_dir   (--frames для превью)"""
import os, subprocess, sys
from PIL import Image, ImageDraw
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import reel_kit_ep1 as rk
from reel_kit_ep1 import W, H, F, pop, pill, paste_c, text_size, render, DARK, ICON

rk.caption = lambda *a, **k: None   # подписи-пилюли заменяем субтитрами озвучки

def subtitle(c, text, t, y=1680, col=(255, 236, 160)):
    f = F("Bold", 54); d = ImageDraw.Draw(c)
    words = text.split(); lines = []; cur = ""
    for w_ in words:
        tst = (cur + " " + w_).strip()
        if text_size(d, tst, f)[0] > 940 and cur: lines.append(cur); cur = w_
        else: cur = tst
    lines.append(cur)
    a = min(1, max(0, t / 0.15))
    for i, l in enumerate(lines):
        tw = text_size(d, l, f)[0]; x = (W - tw) / 2; yy = y + i * 68 - (len(lines) - 1) * 34
        d.text((x, yy), l, font=f, fill=col + (int(255 * a),), stroke_width=7, stroke_fill=(10, 8, 20, int(235 * a)))

def with_sub(fn, text, y=1680):
    def g(t, T):
        c = fn(t, T); subtitle(c, text, t - 0.1, y=y); return c
    g.__name__ = fn.__name__; return g

def s_end(t, T):
    c = DARK.copy()
    paste_c(c, ICON, W / 2, 560, pop(t / 0.4), min(1, t / 0.2))
    a = min(1, max(0, (t - 0.4) / 0.3))
    paste_c(c, pill(["MY WEEK"], F("Black", 90), (255, 255, 255), (0, 0, 0, 0)), W / 2, 790, 1, a)
    paste_c(c, pill(["by Exclusive Apps"], F("SemiBold", 38), (200, 200, 210), (0, 0, 0, 0)), W / 2, 880, 1, a)
    if t > 0.6:
        p = pill(["Хотите своё приложение?", "Пришлите ТЗ — сделаем!"], F("Bold", 50), (20, 20, 24), (255, 255, 255, 255), colors=[(20, 20, 24), (110, 70, 255)])
        paste_c(c, p, W / 2, 1090, pop((t - 0.6) / 0.35))
    if t > 1.2:
        paste_c(c, pill(["+998 90 970 06 03"], F("SemiBold", 44), (255, 255, 255), (0, 0, 0, 0)), W / 2, 1260, 1, min(1, (t - 1.2) / 0.3))
    if t > 3.4:
        paste_c(c, pill(["Вторник — завтра →"], F("Bold", 48), (255, 236, 160), (0, 0, 0, 0)), W / 2, 1400, pop((t - 3.4) / .35))
    if t > 5.2:
        paste_c(c, pill(["Подпишись, чтобы не пропустить"], F("Bold", 42), (255, 255, 255), (110, 70, 255, 255)), W / 2, 1530, pop((t - 5.2) / .35))
    return c

def s_turn(t, T):
    c = DARK.copy()
    paste_c(c, rk.CHAR_PHONE, W / 2, 1280, 0.95)
    paste_c(c, pill(["И тут друг скинул", "мне одно приложение…"], F("Bold", 56), (255, 255, 255), (0, 0, 0, 0)), W / 2, 540, 1, min(1, t / 0.3))
    return c

CUTS = [0, 5.38, 10.1, 14.28, 17.93, 20.91, 27.12, 29.99, 37.68]
FNS = [with_sub(rk.s_hook, "Привет, я Озодбек, мне 13. И это моя неделя без плана."),
       with_sub(rk.s_monday, "Понедельник. Будильник? Не слышал. Опять проспал!"),
       with_sub(rk.s_school, "В школе спрашивают домашку. А я такой: какая домашка?"),
       with_sub(rk.s_evening, "А вечером — 10 дел. Сделано — ноль."),
       s_turn,
       with_sub(rk.s_app, "My Week. Утро, обед, вечер — всё по полочкам.", y=1700),
       rk.s_happy, s_end]
SCENES = list(zip(FNS, [CUTS[i + 1] - CUTS[i] for i in range(len(FNS))]))

if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "."
    if "--frames" in sys.argv:
        tiles = [fn(min(dur * .75, dur - .1), dur).convert("RGB").resize((270, 480)) for fn, dur in SCENES]
        s = Image.new("RGB", (270 * 4, 480 * 2))
        for i, im in enumerate(tiles): s.paste(im, ((i % 4) * 270, (i // 4) * 480))
        s.save(f"{out}/peek_ep1v.jpg"); sys.exit()
    files = []
    for i, (fn, dur) in enumerate(SCENES):
        p = f"{out}/e{i:02d}.mp4"; render(fn, dur, p, fade=0.08); files.append(p); print("scene", i, flush=True)
    open(f"{out}/elist.txt", "w").write("".join(f"file '{os.path.basename(f)}'\n" for f in files))
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", f"{out}/elist.txt", "-c", "copy", f"{out}/ep1v_noaudio.mp4"], check=True)
    print("done")
