"""Общий движок рилса с голосом Speko (21.11): реплики WAV -> склейка с паузами -> сцена на каждую реплику (PIL) ->
субтитры с обводкой -> музыка music.py (0.2) -> loudnorm голоса -> mp4. Основан на reel_speko_local.py.
make_reel(lines, scenes, out, wd, seed): lines=[(wav, subtitle_text, who)], scenes=[fn(t, T) на каждую реплику]."""
import math, os, subprocess, sys, wave
import numpy as np
from PIL import Image, ImageDraw
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from reel_kit_ep1 import W, H, F, ease, pop, pill, paste_c, text_size, render, radial, vgrad
from make_plov import BG, BG2, LAP, subtitle
from character_v2 import character

SR = 44100
PUR = (110, 70, 255)
TOOLS = os.path.dirname(os.path.abspath(__file__))

def read(p):
    with wave.open(p) as w: return np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32) / 32768

def build_dialog(lines, pre=0.3, gap=0.35, tail=0.9):
    parts, t, cues = [np.zeros(int(pre * SR))], pre, []
    for i, (p, txt, who) in enumerate(lines):
        a = read(p); cues.append((t, t + len(a) / SR, txt, who)); parts.append(a); t += len(a) / SR
        g = tail if i == len(lines) - 1 else gap; parts.append(np.zeros(int(g * SR))); t += g
    return np.concatenate(parts), cues

def bounds(cues, dur):
    out = []
    for i in range(len(cues)):
        a = 0 if i == 0 else (cues[i - 1][1] + cues[i][0]) / 2
        b = dur if i == len(cues) - 1 else (cues[i][1] + cues[i + 1][0]) / 2
        out.append((a, b))
    return out

def talking(t, rate=7): return int(t * rate) % 2 == 0

def phone_frame(title, sub=None, pw=620, ph=1180, accent=PUR):
    im = Image.new("RGBA", (pw, ph), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, pw - 1, ph - 1], 86, fill=(18, 18, 22))
    d.rounded_rectangle([18, 18, pw - 19, ph - 19], 70, fill=(248, 248, 250))
    d.rounded_rectangle([pw / 2 - 86, 40, pw / 2 + 86, 80], 20, fill=(18, 18, 22))
    d.text((54, 112), title, font=F("Black", 44), fill=(20, 20, 24))
    if sub: d.text((54, 168), sub, font=F("Medium", 28), fill=(140, 140, 150))
    return im, d

def card(d, x, y, w, h, label, value, col=PUR, vcol=(20, 20, 24)):
    d.rounded_rectangle([x, y, x + w, y + h], 28, fill=(255, 255, 255), outline=(230, 230, 236), width=2)
    d.rounded_rectangle([x + 22, y + 26, x + 32, y + h - 26], 5, fill=col)
    d.text((x + 54, y + 24), label, font=F("SemiBold", 26), fill=(150, 150, 160))
    d.text((x + 54, y + 64), value, font=F("Bold", 34), fill=vcol)

def make_reel(lines, scenes, out, wd, seed, frames=False, tail=0.9):
    os.makedirs(wd, exist_ok=True)
    voice, cues = build_dialog(lines, tail=tail)
    dur = len(voice) / SR; bs = bounds(cues, dur)
    def wrap(i):
        a, b = bs[i]; st, en, txt, who = cues[i]
        col = (190, 220, 255) if who == "L" else (255, 236, 160)
        def g(t, T):
            c = scenes[i](t, T)
            if txt: subtitle(c, txt, t - (st - a), col=col)
            return c
        return g, b - a
    fns = [wrap(i) for i in range(len(cues))]
    if frames:
        n = len(fns); cols = min(n, 6); rows = math.ceil(n / cols)
        sheet = Image.new("RGB", (270 * cols, 480 * rows))
        for i, (fn, T) in enumerate(fns):
            sheet.paste(fn(T * 0.8, T).convert("RGB").resize((270, 480)), ((i % cols) * 270, (i // cols) * 480))
        sheet.save(frames); print("frames ->", frames, "dur", round(dur, 2)); return
    files = []
    for i, (fn, T) in enumerate(fns):
        p = f"{wd}/sc{i:02d}.mp4"; render(fn, T, p, fade=0.06); files.append(p); print("scene", i, flush=True)
    open(f"{wd}/list.txt", "w").write("".join(f"file '{os.path.basename(f)}'\n" for f in files))
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", f"{wd}/list.txt", "-c", "copy", f"{wd}/noaudio.mp4"], check=True)
    with wave.open(f"{wd}/voice.wav", "w") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((np.clip(voice, -1, 1) * 32767).astype(np.int16).tobytes())
    subprocess.run([sys.executable, os.path.join(TOOLS, "music.py"), str(dur), f"{wd}/mus.wav", str(seed)], check=True)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", f"{wd}/noaudio.mp4", "-i", f"{wd}/voice.wav", "-i", f"{wd}/mus.wav",
                    "-filter_complex", "[1:a]loudnorm=I=-16:TP=-1.5,aresample=44100[v];[2:a]volume=0.2[m];[v][m]amix=inputs=2:duration=first:normalize=0[a]",
                    "-map", "0:v", "-map", "[a]", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-t", f"{dur:.2f}", "-movflags", "+faststart", out], check=True)
    print("done", out, "dur", round(dur, 2), "cues", [(round(a, 2), round(b, 2)) for a, b, _, _ in cues])
