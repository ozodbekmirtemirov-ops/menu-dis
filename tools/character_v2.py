"""Озодбек v2: 13 лет, аккуратные кудри, приятное лицо. character(mood, arms) -> RGBA 560x900."""
import math
from PIL import Image, ImageDraw, ImageFilter

SS = 3
SKIN, SKIN_D, SKIN_L = (238, 194, 158), (221, 168, 130), (246, 210, 180)
HAIR, HAIR_M, HAIR_L = (46, 30, 22), (64, 42, 30), (92, 62, 44)
HOOD, HOOD_D, HOOD_L = (66, 122, 255), (46, 94, 220), (96, 146, 255)
EYE, LINE, LIP = (70, 44, 30), (52, 34, 28), (196, 96, 92)


def _curl(d, x, y, r, s):
    d.ellipse([x - r, y - r, x + r, y + r], fill=HAIR)
    d.arc([x - r * .62, y - r * .62, x + r * .62, y + r * .62], 200, 330, fill=HAIR_L, width=max(2, int(2.2 * s)))


def character(mood="neutral", arms="down"):
    s = SS; cw, ch = 560 * s, 900 * s
    im = Image.new("RGBA", (cw, ch), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    cx = cw // 2
    P = lambda v: v * s

    # ---- body (13 y.o.: narrower shoulders) ----
    d.rounded_rectangle([cx - P(150), P(500), cx + P(150), P(900)], P(80), fill=HOOD)
    d.rounded_rectangle([cx - P(150), P(500), cx + P(150), P(560)], P(40), fill=HOOD_L)
    d.ellipse([cx - P(78), P(470), cx + P(78), P(560)], fill=HOOD_D)  # hood collar
    d.ellipse([cx - P(52), P(478), cx + P(52), P(540)], fill=SKIN_D)
    for sg in (-1, 1):
        d.line([(cx + sg * P(26), P(545)), (cx + sg * P(30), P(650))], fill=(250, 250, 255), width=P(6))
        d.ellipse([cx + sg * P(30) - P(7), P(645), cx + sg * P(30) + P(7), P(659)], fill=(250, 250, 255))
    d.rounded_rectangle([cx - P(80), P(720), cx + P(80), P(800)], P(26), fill=HOOD_D)

    # ---- arms ----
    if arms == "up":
        for sg in (-1, 1):
            d.line([(cx + sg * P(130), P(540)), (cx + sg * P(225), P(360))], fill=HOOD, width=P(62))
            d.ellipse([cx + sg * P(225) - P(34), P(318), cx + sg * P(225) + P(34), P(386)], fill=SKIN)
    elif arms == "phone":
        d.line([(cx - P(135), P(540)), (cx - P(178), P(770))], fill=HOOD, width=P(62))
        d.ellipse([cx - P(178) - P(32), P(750), cx - P(178) + P(32), P(814)], fill=SKIN)
        d.line([(cx + P(135), P(540)), (cx + P(60), P(660))], fill=HOOD, width=P(62))
        d.rounded_rectangle([cx + P(8), P(548), cx + P(104), P(720)], P(16), fill=(22, 22, 26))
        d.rounded_rectangle([cx + P(17), P(560), cx + P(95), P(708)], P(10), fill=(130, 196, 255))
        d.ellipse([cx + P(28), P(640), cx + P(96), P(704)], fill=SKIN)
    elif arms == "wave":
        d.line([(cx - P(135), P(540)), (cx - P(178), P(770))], fill=HOOD, width=P(62))
        d.ellipse([cx - P(178) - P(32), P(750), cx - P(178) + P(32), P(814)], fill=SKIN)
        d.line([(cx + P(130), P(540)), (cx + P(235), P(380))], fill=HOOD, width=P(62))
        d.ellipse([cx + P(235) - P(36), P(330), cx + P(235) + P(36), P(402)], fill=SKIN)
    else:
        for sg in (-1, 1):
            d.line([(cx + sg * P(136), P(540)), (cx + sg * P(178), P(770))], fill=HOOD, width=P(62))
            d.ellipse([cx + sg * P(178) - P(32), P(750), cx + sg * P(178) + P(32), P(814)], fill=SKIN)

    # ---- neck, ears, head ----
    d.rounded_rectangle([cx - P(36), P(420), cx + P(36), P(500)], P(14), fill=SKIN_D)
    hx0, hy0, hx1, hy1 = cx - P(132), P(160), cx + P(132), P(462)
    for sg in (-1, 1):
        ex = cx + sg * P(128)
        d.ellipse([ex - P(24), P(292), ex + P(24), P(356)], fill=SKIN)
        d.ellipse([ex - P(12), P(306), ex + P(12), P(342)], fill=SKIN_D)
    d.ellipse([hx0, hy0, hx1, hy1], fill=SKIN)

    # ---- neat curly hair: solid cap + regular curls ----
    d.chord([hx0 - P(12), P(120), hx1 + P(12), P(326)], 180, 360, fill=HAIR)
    d.rectangle([hx0 - P(4), P(222), hx1 + P(4), P(226)], fill=HAIR)
    d.pieslice([hx0 - P(12), P(196), hx0 + P(44), P(296)], 90, 270, fill=HAIR)   # short sides
    d.pieslice([hx1 - P(44), P(196), hx1 + P(12), P(296)], 270, 90, fill=HAIR)
    # top rows of curls (tidy arc)
    for row, (ry, rr, n, spread) in enumerate([(P(150), P(30), 7, 0.82), (P(122), P(28), 6, 0.62), (P(104), P(24), 4, 0.40)]):
        for i in range(n):
            a = math.pi * (1 + (i + .5) / n)
            x = cx + math.cos(a) * P(150) * spread / 0.82 * 0.98
            y = ry + (1 - abs(math.cos(a))) * -P(4) + abs(math.cos(a)) * P(30)
            _curl(d, x, y, rr, s)
    # front fringe: neat curls along the forehead
    for i in range(7):
        x = cx + (i - 3) * P(34)
        y = P(232) - abs(i - 3) ** 1.6 * P(4)
        _curl(d, x, y, P(22), s)

    # ---- face ----
    ey = P(312)
    if mood == "sleepy":
        for sg in (-1, 1):
            ex = cx + sg * P(52)
            d.arc([ex - P(22), ey - P(8), ex + P(22), ey + P(16)], 10, 170, fill=LINE, width=P(5))
    else:
        big = mood == "shock"
        for sg in (-1, 1):
            ex = cx + sg * P(52)
            w, h = (P(25), P(26)) if big else (P(23), P(20))
            d.ellipse([ex - w, ey - h, ex + w, ey + h], fill=(255, 255, 255))
            ir = P(15) if big else P(14)
            ix = ex + sg * -P(1)
            d.ellipse([ix - ir, ey - ir + P(2), ix + ir, ey + ir + P(2)], fill=EYE)
            d.ellipse([ix - P(7), ey - P(5), ix + P(7), ey + P(9)], fill=(22, 14, 10))
            d.ellipse([ix + P(2), ey - P(7), ix + P(8), ey - P(1)], fill=(255, 255, 255))
            d.arc([ex - w - P(2), ey - h - P(3), ex + w + P(2), ey + h + P(6)], 200, 340, fill=LINE, width=P(4))
    # brows: soft
    for sg in (-1, 1):
        bx = cx + sg * P(54); by = ey - P(40)
        if mood == "sad":
            pts = [(bx - P(22), by + (P(4) if sg > 0 else -P(6))), (bx + P(22), by + (-P(6) if sg > 0 else P(4)))]
            pts = [(bx - P(22), by - sg * -P(2) + (P(6) if sg < 0 else -P(6))), (bx + P(22), by + (P(6) if sg > 0 else -P(6)))]
            d.line(pts, fill=HAIR, width=P(7))
        elif mood == "shock":
            d.arc([bx - P(24), by - P(16), bx + P(24), by + P(10)], 200, 340, fill=HAIR, width=P(7))
        else:
            d.arc([bx - P(24), by - P(8), bx + P(24), by + P(14)], 205, 335, fill=HAIR, width=P(7))
    # nose
    d.arc([cx - P(10), P(336), cx + P(10), P(362)], 20, 160, fill=SKIN_D, width=P(4))
    # cheeks
    for sg in (-1, 1):
        cheek = Image.new("RGBA", (P(60), P(36)), (0, 0, 0, 0))
        ImageDraw.Draw(cheek).ellipse([0, 0, P(60), P(36)], fill=(244, 150, 140, 90 if mood != "happy" else 140))
        im.alpha_composite(cheek, (int(cx + sg * P(88) - P(30)), int(P(350))))
    my = P(392)
    if mood == "happy":
        d.chord([cx - P(44), my - P(26), cx + P(44), my + P(30)], 0, 180, fill=(140, 52, 52))
        d.chord([cx - P(34), my - P(18), cx + P(34), my + P(6)], 0, 180, fill=(255, 255, 255))
        d.ellipse([cx - P(20), my + P(8), cx + P(20), my + P(26)], fill=(232, 120, 120))
    elif mood == "sad":
        d.arc([cx - P(26), my - P(2), cx + P(26), my + P(26)], 205, 335, fill=LIP, width=P(6))
    elif mood == "shock":
        d.ellipse([cx - P(17), my - P(16), cx + P(17), my + P(20)], fill=(120, 40, 40))
    elif mood == "sleepy":
        d.arc([cx - P(22), my - P(14), cx + P(22), my + P(8)], 25, 155, fill=LIP, width=P(5))
    else:
        d.arc([cx - P(32), my - P(26), cx + P(32), my + P(12)], 25, 155, fill=LIP, width=P(6))

    return im.resize((cw // s, ch // s), Image.LANCZOS)


if __name__ == "__main__":
    tiles = [character(m) for m in ("neutral", "happy", "sad", "shock", "sleepy")] + [character("happy", "wave"), character("happy", "phone")]
    sheet = Image.new("RGB", (560 * 7, 900), (20, 22, 40))
    for i, t in enumerate(tiles): sheet.alpha_composite if False else sheet.paste(t, (i * 560, 0), t)
    sheet.resize((560 * 7 // 2, 450)).save("char_v2.jpg")
