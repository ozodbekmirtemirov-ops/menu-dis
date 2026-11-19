"""Рилс «Плов за час»: Озодбек + ноутбук-помощник. Тайминги по диалогу (41.6 c)."""
import math, os, subprocess, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
sys.path.insert(0, "/home/claude/menu-dis/tools")
from reel_kit_ep1 import W, H, FPS, F, ease, pop, pill, paste_c, text_size, render, TMP
from character_v2 import character

# ---------- assets ----------
def bokeh_bg(seed=3, warm=True):
    rng = np.random.default_rng(seed)
    y = np.linspace(0, 1, H)[:, None, None]
    top = np.array([16, 20, 52]); bot = np.array([40, 30, 70])
    arr = (top * (1 - y) + bot * y) * np.ones((1, W, 1))
    im = Image.fromarray(arr.astype(np.uint8), "RGB").convert("RGBA")
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    for _ in range(38):
        x, yy, r = rng.uniform(0, W), rng.uniform(0, H * .75), rng.uniform(14, 60)
        col = (255, 190, 90, int(rng.uniform(40, 120))) if warm and rng.random() < .7 else (140, 170, 255, int(rng.uniform(30, 90)))
        d.ellipse([x - r, yy - r, x + r, yy + r], fill=col)
    lay = lay.filter(ImageFilter.GaussianBlur(10))
    im.alpha_composite(lay)
    d = ImageDraw.Draw(im); d.rectangle([0, 1500, W, H], fill=(38, 26, 40))
    return im
BG = bokeh_bg()
BG2 = bokeh_bg(9)

O = {m: character(m) for m in ("neutral", "happy", "shock", "sad")}
O_UP_SHOCK = character("shock", "up"); O_WAVE = character("happy", "wave"); O_UP_HAPPY = character("happy", "up")

def laptop(expr="neutral", talk=False):
    S = 2; w, h = 700 * S, 620 * S
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle([40 * S, 0, 660 * S, 430 * S], 40 * S, fill=(44, 44, 52))
    d.rounded_rectangle([64 * S, 24 * S, 636 * S, 406 * S], 26 * S, fill=(110, 70, 255))
    d.polygon([(0, 470 * S), (700 * S, 470 * S), (650 * S, 430 * S), (50 * S, 430 * S)], fill=(190, 190, 200))
    d.rounded_rectangle([0, 466 * S, 700 * S, 500 * S], 14 * S, fill=(160, 160, 172))
    d.rounded_rectangle([290 * S, 470 * S, 410 * S, 484 * S], 6 * S, fill=(140, 140, 150))
    # face
    for sg in (-1, 1):
        ex = 350 * S + sg * 120 * S
        if expr == "smug" and sg == -1:
            d.rounded_rectangle([ex - 34 * S, 170 * S, ex + 34 * S, 196 * S], 10 * S, fill=(20, 16, 40))
        elif expr == "wide":
            d.rounded_rectangle([ex - 36 * S, 120 * S, ex + 36 * S, 240 * S], 16 * S, fill=(20, 16, 40))
        else:
            d.rounded_rectangle([ex - 32 * S, 130 * S, ex + 32 * S, 230 * S], 14 * S, fill=(20, 16, 40))
    if talk:
        d.rounded_rectangle([300 * S, 290 * S, 400 * S, 340 * S], 18 * S, fill=(20, 16, 40))
    elif expr == "smug":
        d.arc([280 * S, 250 * S, 420 * S, 330 * S], 20, 160, fill=(20, 16, 40), width=12 * S)
    else:
        d.rounded_rectangle([300 * S, 300 * S, 400 * S, 318 * S], 9 * S, fill=(20, 16, 40))
    f = F("Black", 34 * S); d.text((80 * S, 350 * S), "EA", font=f, fill=(255, 255, 255, 160))
    return im.resize((w // S, h // S), Image.LANCZOS)
LAP = {(e, t): laptop(e, t) for e in ("neutral", "smug", "wide") for t in (False, True)}

def subtitle(c, text, t, y=1620, col=(255, 236, 160)):
    """Outlined subtitle, wraps to 2 lines."""
    f = F("Bold", 50); d = ImageDraw.Draw(c)
    words = text.split(); lines = []; cur = ""
    for w_ in words:
        tst = (cur + " " + w_).strip()
        if text_size(d, tst, f)[0] > 940 and cur: lines.append(cur); cur = w_
        else: cur = tst
    lines.append(cur)
    a = min(1, t / 0.15)
    for i, l in enumerate(lines):
        tw = text_size(d, l, f)[0]; x = (W - tw) / 2; yy = y + i * 64 - (len(lines) - 1) * 32
        d.text((x, yy), l, font=f, fill=col + (int(255 * a),), stroke_width=6, stroke_fill=(10, 8, 20, int(230 * a)))

def talking(t, rate=7): return int(t * rate) % 2 == 0

# ---------- scenes ----------
def s_ask(t, T):
    c = BG.copy()
    char = O_WAVE if talking(t, 6) else O["neutral"]
    paste_c(c, char, W / 2, 1180, 1.25)
    if t < 2.6:
        paste_c(c, pill(["6 недель работы"], F("Black", 76), (255, 255, 255), (0, 0, 0, 0)), W / 2, 300, pop(t / .3))
        paste_c(c, pill(["за 1 час?"], F("Black", 84), (120, 230, 140), (0, 0, 0, 0)), W / 2, 400, pop((t - .3) / .3) if t > .3 else 0)
    subtitle(c, "Слушай! Сделай мне приложение для доставки плова по Ташкенту!", t)
    return c

def s_lap(text, expr="neutral", talk_until=None, bg=None):
    def fn(t, T):
        c = (bg or BG).copy()
        tk = (talk_until is None or t < talk_until) and talking(t, 6)
        paste_c(c, LAP[(expr, tk)], W / 2, 960 + math.sin(t * 2) * 6, 1.25, ease(t / .2))
        subtitle(c, text, t)
        return c
    return fn

def s_shock6(t, T):
    c = BG.copy()
    z = 1.25 + 0.35 * ease(t / .25)
    paste_c(c, O["shock"], W / 2, 1150 + (z - 1.25) * 300, z)
    subtitle(c, "Шесть недель?!", t, col=(255, 120, 110))
    return c

PLAN = [("Меню и казаны", "2 недели", 0.15), ("Оплата Click / Payme", "1 неделя", 2.45), ("Приложение курьеров", "2 недели", 4.8), ("Проверка", "1 неделя", 7.1)]
def window(title):
    im = Image.new("RGBA", (900, 1000), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, 899, 999], 34, fill=(246, 246, 250))
    d.rounded_rectangle([0, 0, 899, 70], 34, fill=(228, 228, 234)); d.rectangle([0, 40, 899, 70], fill=(228, 228, 234))
    for i, col in enumerate([(255, 95, 86), (255, 189, 46), (39, 201, 63)]): d.ellipse([28 + i * 36, 24, 50 + i * 36, 46], fill=col)
    d.text((150, 20), title, font=F("Medium", 26), fill=(120, 120, 130))
    return im
WIN = window("План — Доставка плова")
def s_plan(t, T):
    c = BG2.copy()
    win = WIN.copy(); d = ImageDraw.Draw(win)
    d.text((50, 110), "План работы", font=F("Black", 56), fill=(20, 20, 24))
    y = 220
    for name, dur, st in PLAN:
        if t < st: break
        k = ease((t - st) / .3)
        row = Image.new("RGBA", (800, 130), (0, 0, 0, 0)); rd = ImageDraw.Draw(row)
        rd.rounded_rectangle([0, 0, 799, 129], 26, fill=(255, 255, 255), outline=(230, 230, 236), width=2)
        rd.text((36, 40), name, font=F("Bold", 40), fill=(20, 20, 24))
        tw = text_size(rd, dur, F("Bold", 40))[0]; rd.text((764 - tw, 40), dur, font=F("Bold", 40), fill=(90, 80, 230))
        row.putalpha(row.getchannel("A").point(lambda v: int(v * k)))
        win.alpha_composite(row, (50, int(y + (1 - k) * 30))); y += 156
    if t > 8.6:
        d.text((50, 880), "Итого: 6 недель", font=F("Black", 50), fill=(230, 60, 60))
    paste_c(c, win, W / 2, 820, 1.0, ease(t / .25))
    lines = ["Меню и казаны — две недели.", "Оплата через Click и Payme — неделя.", "Приложение для курьеров — две недели.", "И проверка — ещё неделя."]
    idx = max(i for i, (_, _, st) in enumerate(PLAN) if t >= st - 0.15) if t >= 0 else 0
    subtitle(c, lines[idx], t - PLAN[idx][2] + .2)
    return c

TASKS = ["Меню и казаны", "Оплата", "Курьеры", "Проверка"]
def s_timer(t, T):
    c = Image.new("RGBA", (W, H), (12, 12, 16, 255))
    win = Image.new("RGBA", (920, 1100), (0, 0, 0, 0)); d = ImageDraw.Draw(win)
    d.rounded_rectangle([0, 0, 919, 1099], 34, fill=(22, 22, 28))
    for i, col in enumerate([(255, 95, 86), (255, 189, 46), (39, 201, 63)]): d.ellipse([28 + i * 36, 24, 50 + i * 36, 46], fill=col)
    d.text((150, 20), "Exclusive Apps работает…", font=F("Medium", 26), fill=(140, 140, 150))
    p = min(1, t / (T - .4)); sec = int(p * 3598)
    s = f"0:{sec // 60:02d}:{sec % 60:02d}"
    f = F("Black", 150); tw = text_size(d, s, f)[0]; d.text(((920 - tw) / 2, 140), s, font=f, fill=(255, 255, 255))
    f2 = F("Medium", 32); tw = text_size(d, "прошло времени", f2)[0]; d.text(((920 - tw) / 2, 340), "прошло времени", font=f2, fill=(140, 140, 150))
    for i, name in enumerate(TASKS):
        y = 470 + i * 140; pi = max(0, min(1, p * 4 - i))
        col = (52, 199, 89) if pi >= 1 else (90, 120, 255)
        d.text((60, y), name, font=F("Bold", 40), fill=(255, 255, 255))
        if pi >= 1: d.text((800, y), "✓", font=F("Bold", 44), fill=col)
        else: d.text((760, y), f"{int(pi * 100)}%", font=F("Bold", 36), fill=(170, 170, 180))
        d.rounded_rectangle([60, y + 64, 860, y + 80], 8, fill=(50, 50, 60))
        if pi > 0: d.rounded_rectangle([60, y + 64, 60 + int(800 * pi), y + 80], 8, fill=col)
    paste_c(c, win, W / 2, 900)
    return c

def s_done(t, T):
    c = BG.copy()
    paste_c(c, O["shock"] if t < 1.0 else O["neutral"], W / 2, 1180, 1.25)
    subtitle(c, "Всё… уже готово?", t)
    return c

def plov_phone():
    pw, ph = 640, 1280
    im = Image.new("RGBA", (pw, ph), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, pw - 1, ph - 1], 90, fill=(18, 18, 22))
    d.rounded_rectangle([18, 18, pw - 19, ph - 19], 74, fill=(250, 248, 244))
    d.rounded_rectangle([pw / 2 - 90, 40, pw / 2 + 90, 82], 21, fill=(18, 18, 22))
    d.text((56, 110), "Плов Экспресс", font=F("Black", 46), fill=(20, 20, 24))
    # map
    d.rounded_rectangle([40, 190, pw - 40, 800], 30, fill=(232, 236, 230))
    for gx in range(70, pw - 40, 90): d.rectangle([gx, 190, gx + 14, 800], fill=(255, 255, 255))
    for gy in range(230, 800, 110): d.rectangle([40, gy, pw - 40, gy + 14], fill=(255, 255, 255))
    d.rectangle([340, 420, 420, 520], fill=(176, 220, 170)); d.rectangle([110, 600, 200, 700], fill=(176, 220, 170))
    pts = [(140, 740), (140, 560), (330, 560), (330, 360), (480, 360), (480, 260)]
    for a, b in zip(pts, pts[1:]): d.line([a, b], fill=(90, 80, 230), width=10)
    d.ellipse([462, 232, 498, 268], fill=(255, 69, 58)); d.ellipse([122, 722, 158, 758], fill=(52, 199, 89))
    # card
    d.rounded_rectangle([40, 830, pw - 40, 1230], 34, fill=(255, 255, 255), outline=(230, 230, 236), width=2)
    d.text((76, 860), "Курьер будет через 25 минут", font=F("Medium", 26), fill=(140, 140, 150))
    d.text((76, 910), "Чиланзар → Юнусабад", font=F("Bold", 36), fill=(20, 20, 24))
    d.text((76, 966), "Плов чайханский × 2", font=F("Medium", 30), fill=(90, 90, 100))
    d.text((390, 1030), "85 000 сум", font=F("Black", 34), fill=(20, 20, 24))
    d.text((76, 1034), "Click · Payme", font=F("SemiBold", 28), fill=(90, 80, 230))
    d.rounded_rectangle([76, 1110, pw - 76, 1196], 28, fill=(255, 196, 0))
    f = F("Black", 36); tw = text_size(d, "Заказать плов", f)[0]; d.text(((pw - tw) / 2, 1130), "Заказать плов", font=f, fill=(20, 20, 24))
    return im
PHONE = plov_phone()
def s_app(t, T):
    c = BG2.copy()
    paste_c(c, PHONE, W / 2, 850 + 80 * (1 - ease(t / .35)), 1.05, ease(t / .25))
    subtitle(c, "Меню, оплата, курьеры. Один час.", t, y=1690)
    return c

def s_angry(t, T):
    c = BG.copy()
    shake = math.sin(t * 40) * 6 if t < 1.2 else 0
    paste_c(c, O_UP_SHOCK if talking(t, 5) else O["shock"], W / 2 + shake, 1180, 1.25)
    subtitle(c, "Если ты можешь за час, зачем сказал шесть недель?!", t)
    return c

def s_end(t, T):
    c = BG2.copy()
    paste_c(c, O_UP_HAPPY if talking(t, 5) and t < 3.1 else O["happy"], 330, 1200, 0.95)
    paste_c(c, LAP[("smug", False)], 790, 1260, 0.62)
    paste_c(c, pill(["Хотите своё приложение?"], F("Black", 62), (255, 255, 255), (0, 0, 0, 0)), W / 2, 330, pop(t / .35))
    paste_c(c, pill(["Пришлите ТЗ в директ"], F("Bold", 54), (20, 20, 24), (255, 255, 255, 255), colors=[(110, 70, 255)]), W / 2, 460, pop((t - .4) / .35) if t > .4 else 0)
    if t > 1.0:
        a = min(1, (t - 1) / .3)
        paste_c(c, pill(["Exclusive Apps · +998 90 970 06 03"], F("SemiBold", 38), (255, 255, 255), (0, 0, 0, 0)), W / 2, 580, 1, a)
    return c

CUTS = [0, 4.24, 7.66, 9.11, 19.0, 19.85, 23.12, 25.25, 28.71, 32.36, 36.75, 41.59]
FNS = [s_ask, s_lap("Хорошо. Это займёт примерно шесть недель."), s_shock6, s_plan,
       s_lap("Начинаю.", "wide", bg=BG2), s_timer, s_done, s_app, s_angry,
       s_lap("Шесть недель — это у других. В Exclusive Apps — быстро.", "smug", talk_until=3.6), s_end]
SCENES = list(zip(FNS, [CUTS[i + 1] - CUTS[i] for i in range(len(FNS))]))

if __name__ == "__main__":
    if "--frames" in sys.argv:
        tiles = [fn(min(dur * .7, dur - .1), dur).convert("RGB").resize((240, 427)) for fn, dur in SCENES]
        s = Image.new("RGB", (240 * 6, 427 * 2))
        for i, im in enumerate(tiles): s.paste(im, ((i % 6) * 240, (i // 6) * 427))
        s.save("peek_plov.jpg"); sys.exit()
    files = []
    for i, (fn, dur) in enumerate(SCENES):
        pth = f"{TMP}/p{i:02d}.mp4"; render(fn, dur, pth, fade=0.08); files.append(pth)
    open(f"{TMP}/plist.txt", "w").write("".join(f"file '{os.path.basename(f)}'\n" for f in files))
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", f"{TMP}/plist.txt", "-c", "copy", "plov_noaudio.mp4"], check=True)
    print("done")
