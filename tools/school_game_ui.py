"""Интерфейс My School ПРАВИЛЬНЫЙ (25.11): игра-урок по QR, админка только у завуча и директора.
qr(size), game_phone(k), admin_phone(k), class_row(k) -> RGBA."""
import os, random, sys
from PIL import Image, ImageDraw
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from reel_speko_kit import F, phone_frame, card, PUR

ORG = (255, 159, 10); GRN = (52, 199, 89); BLU = (60, 150, 255); RED = (230, 60, 70)

def qr(size=420, seed=7):
    n = 25; c = size // n; im = Image.new("RGBA", (c * n + 2 * c, c * n + 2 * c), (255, 255, 255, 255)); d = ImageDraw.Draw(im)
    rnd = random.Random(seed)
    def finder(x, y):
        d.rectangle([c * (x + 1), c * (y + 1), c * (x + 8) - 1, c * (y + 8) - 1], fill=(20, 20, 24))
        d.rectangle([c * (x + 2), c * (y + 2), c * (x + 7) - 1, c * (y + 7) - 1], fill=(255, 255, 255))
        d.rectangle([c * (x + 3), c * (y + 3), c * (x + 6) - 1, c * (y + 6) - 1], fill=(20, 20, 24))
    for i in range(n):
        for j in range(n):
            if (i < 8 and j < 8) or (i > n - 9 and j < 8) or (i < 8 and j > n - 9): continue
            if rnd.random() < .5: d.rectangle([c * (i + 1), c * (j + 1), c * (i + 2) - 1, c * (j + 2) - 1], fill=(20, 20, 24))
    finder(0, 0); finder(n - 7, 0); finder(0, n - 7)
    return im

def game_phone(k, q="Сколько будет 7 × 8?"):
    im, d = phone_frame("My School · игра", "Математика · 8 «Б»", accent=ORG)
    d.rounded_rectangle([40, 220, 580, 300], 22, fill=(255, 244, 225)); d.text((64, 238), "Вопрос 3 / 10  ·  0:12", font=F("Bold", 32), fill=(200, 110, 0))
    d.text((54, 340), q, font=F("Black", 44), fill=(20, 20, 24))
    opts = [("54", RED), ("56", GRN), ("48", BLU), ("64", PUR)]
    for i, (a, col) in enumerate(opts):
        x = 40 + (i % 2) * 280; y = 440 + (i // 2) * 200
        sel = k > .6 and a == "56"
        d.rounded_rectangle([x, y, x + 260, y + 180], 30, fill=col if (k > .2 + i * .08) else (230, 230, 236), outline=(20, 20, 24) if sel else None, width=8)
        d.text((x + 90, y + 52), a, font=F("Black", 64), fill=(255, 255, 255))
    if k > .75:
        d.rounded_rectangle([40, 880, 580, 1120], 30, fill=(240, 250, 242))
        d.text((64, 900), "Рейтинг класса", font=F("Bold", 32), fill=(20, 120, 50))
        for i, (n, p) in enumerate([("Азиз", "+30"), ("Малика", "+28"), ("Тимур", "+25")]):
            d.text((64, 950 + i * 54), f"{i + 1}. {n}", font=F("Bold", 34), fill=(20, 20, 24)); d.text((470, 950 + i * 54), p, font=F("Black", 34), fill=GRN)
    return im

def admin_phone(k):
    im, d = phone_frame("Админка", "только завуч и директор", accent=PUR)
    d.text((54, 230), "Результаты классов · сегодня", font=F("Bold", 30), fill=(120, 120, 130))
    rows = [("8 «А»", .74, BLU), ("8 «Б»", .93, GRN), ("8 «В»", .61, ORG), ("9 «А»", .82, PUR)]
    for i, (n, v, col) in enumerate(rows):
        y = 300 + i * 150; kk = max(0, min(1, (k - i * .12) / .5))
        d.text((54, y), n, font=F("Black", 40), fill=(20, 20, 24))
        d.rounded_rectangle([54, y + 60, 566, y + 100], 20, fill=(236, 236, 242))
        if kk > 0: d.rounded_rectangle([54, y + 60, 54 + int(512 * v * kk), y + 100], 20, fill=col)
        d.text((470, y), f"{int(v * 100 * kk)}%", font=F("Black", 40), fill=col)
    if k > .7: card(d, 40, 920, 540, 136, "Играли сегодня", "27 из 28 учеников", GRN)
    return im

def class_row(k, n=5):
    """Ряд «учеников» (простые фигурки) с телефонами, поднимают руки по мере k."""
    im = Image.new("RGBA", (1000, 300), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    cols = [(255, 190, 120), (230, 170, 130), (210, 150, 110), (240, 200, 150), (200, 140, 100)]
    shirts = [(220, 80, 80), (60, 150, 255), (52, 199, 89), (255, 159, 10), (160, 90, 220)]
    for i in range(n):
        x = 100 + i * 200
        d.rounded_rectangle([x - 60, 150, x + 60, 300], 40, fill=shirts[i % 5])
        d.ellipse([x - 48, 50, x + 48, 146], fill=cols[i % 5]); d.pieslice([x - 50, 40, x + 50, 120], 180, 360, fill=(40, 30, 30))
        if k > i * .15:
            d.line([x + 50, 190, x + 80, 40], fill=shirts[i % 5], width=30); d.ellipse([x + 62, 18, x + 102, 58], fill=cols[i % 5])
    return im
