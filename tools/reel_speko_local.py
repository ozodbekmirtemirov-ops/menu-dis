"""Полностью локальный конвейер (без ElevenLabs): реплики Speko (WAV) -> склейка с паузами -> видео кодом -> музыка 0.2 -> mp4.
Тест 20.11: 11-секундный тизер серии 2. Usage: reel_speko_local.py work_dir out.mp4"""
import math, os, subprocess, sys, wave
import numpy as np
from PIL import Image
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from reel_kit_ep1 import W, H, F, pop, pill, paste_c, render
from make_plov import BG, BG2, LAP, subtitle
from character_v2 import character

WD, OUT = sys.argv[1], sys.argv[2]
SR = 44100
def read(p):
    with wave.open(p) as w: return np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32) / 32768

def build_dialog(lines, pre=0.3, gap=0.35, tail=0.9):
    """lines: [(wav, text, who)] -> (audio, [(start, end, text, who)])"""
    parts, t, cues = [np.zeros(int(pre * SR))], pre, []
    for i, (p, txt, who) in enumerate(lines):
        a = read(p); cues.append((t, t + len(a) / SR, txt, who)); parts.append(a); t += len(a) / SR
        g = tail if i == len(lines) - 1 else gap; parts.append(np.zeros(int(g * SR))); t += g
    return np.concatenate(parts), cues

LINES = [(f"{WD}/o1.wav", "Эй! Кто поставил мне задачу на среду, 15:00?!", "O"),
         (f"{WD}/l1.wav", "Не я. Честно. Но я знаю, кто.", "L"),
         (f"{WD}/o2.wav", "Что?! Серия 2 — завтра. Подпишись!", "O")]
voice, CUES = build_dialog(LINES)
DUR = len(voice) / SR
O_PH = character("shock", "phone"); O_UP = character("shock", "up"); O_N = character("neutral")

def cue_bounds(i):
    a = 0 if i == 0 else (CUES[i - 1][1] + CUES[i][0]) / 2
    b = DUR if i == len(CUES) - 1 else (CUES[i][1] + CUES[i + 1][0]) / 2
    return a, b

def s0(t, T):
    c = BG.copy()
    paste_c(c, pill(["Среда, 15:00 — ???"], F("Black", 64), (255, 255, 255), (220, 50, 50, 255)), W / 2, 380, pop(t / .35))
    paste_c(c, O_PH, W / 2, 1150, 1.15)
    subtitle(c, CUES[0][2], t - (CUES[0][0] - cue_bounds(0)[0]))
    return c

def s1(t, T):
    c = BG2.copy()
    talk = int(t * 7) % 2 == 0 and t < CUES[1][1] - cue_bounds(1)[0]
    paste_c(c, LAP[("smug", talk)], W / 2, 900, 1.15)
    paste_c(c, O_N, 860, 1380, 0.45)
    subtitle(c, CUES[1][2], t - (CUES[1][0] - cue_bounds(1)[0]), col=(190, 220, 255))
    return c

def s2(t, T):
    c = BG.copy()
    paste_c(c, O_UP, W / 2, 1100 + math.sin(t * 9) * 10, 1.05)
    paste_c(c, pill(["Серия 2 — завтра в 12:40"], F("Black", 62), (255, 236, 160), (0, 0, 0, 0)), W / 2, 330, pop(t / .35))
    if t > 1.2:
        paste_c(c, pill(["Подпишись, чтобы не пропустить"], F("Bold", 46), (255, 255, 255), (110, 70, 255, 255)), W / 2, 460, pop((t - 1.2) / .35))
    subtitle(c, CUES[2][2], t - (CUES[2][0] - cue_bounds(2)[0]))
    return c

if __name__ == "__main__":
    files = []
    for i, fn in enumerate([s0, s1, s2]):
        a, b = cue_bounds(i); p = f"{WD}/sp{i}.mp4"; render(fn, b - a, p, fade=0.08); files.append(p)
    if "--frames" in sys.argv: pass
    open(f"{WD}/splist.txt", "w").write("".join(f"file '{os.path.basename(f)}'\n" for f in files))
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", f"{WD}/splist.txt", "-c", "copy", f"{WD}/sp_noaudio.mp4"], check=True)
    with wave.open(f"{WD}/voice.wav", "w") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((np.clip(voice, -1, 1) * 32767).astype(np.int16).tobytes())
    subprocess.run([sys.executable, os.path.join(os.path.dirname(os.path.abspath(__file__)), "music.py"), str(DUR), f"{WD}/mus.wav", "11"], check=True)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", f"{WD}/sp_noaudio.mp4", "-i", f"{WD}/voice.wav", "-i", f"{WD}/mus.wav",
                    "-filter_complex", "[1:a]loudnorm=I=-16:TP=-1.5,aresample=44100[v];[2:a]volume=0.2[m];[v][m]amix=inputs=2:duration=first:normalize=0[a]",
                    "-map", "0:v", "-map", "[a]", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-t", f"{DUR:.2f}", OUT], check=True)
    print("cues", [(round(a, 2), round(b, 2)) for a, b, _, _ in CUES], "dur", round(DUR, 2))
