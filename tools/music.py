"""Light upbeat background loop, synthesized. Usage: music.py seconds out.wav [seed]"""
import sys, wave
import numpy as np
dur = float(sys.argv[1]); out = sys.argv[2]; seed = int(sys.argv[3]) if len(sys.argv) > 3 else 0
SR = 44100; bpm = 112; beat = 60 / bpm
n = int(dur * SR); t = np.arange(n) / SR
mix = np.zeros(n)
progs = [[(60, 64, 67), (55, 59, 62), (57, 60, 64), (53, 57, 60)],
         [(57, 60, 64), (53, 57, 60), (60, 64, 67), (55, 59, 62)],
         [(62, 65, 69), (55, 59, 62), (60, 64, 67), (57, 60, 64)]]
prog = progs[seed % len(progs)]
f = lambda m: 440 * 2 ** ((m - 69) / 12)
bar = beat * 4
def env(L, a=0.01, r=0.3):
    e = np.ones(L); A = int(a * SR); e[:A] = np.linspace(0, 1, A)
    e *= np.exp(-np.arange(L) / (r * SR)); return e
# pads
for i in range(int(dur / bar) + 1):
    s = int(i * bar * SR); L = min(int(bar * SR), n - s)
    if L <= 0: break
    ch = prog[i % 4]; tt = np.arange(L) / SR
    pad = sum(np.sin(2 * np.pi * f(m) * tt) + 0.3 * np.sin(2 * np.pi * 2 * f(m) * tt) for m in ch)
    e = np.minimum(1, tt / 0.15) * np.minimum(1, (bar - tt) / 0.15)
    mix[s:s + L] += 0.05 * pad * e
    # bass
    b = np.sin(2 * np.pi * f(ch[0] - 24) * tt); mix[s:s + L] += 0.18 * b * e
    # arpeggio eighths
    for k in range(8):
        ss = s + int(k * beat / 2 * SR); LL = min(int(beat / 2 * SR), n - ss)
        if LL <= 0: break
        m = ch[[0, 1, 2, 1, 0, 2, 1, 2][k]] + 12; tt2 = np.arange(LL) / SR
        mix[ss:ss + LL] += 0.07 * np.sin(2 * np.pi * f(m) * tt2) * env(LL, 0.005, 0.12)
# drums
rng = np.random.default_rng(1)
for k in range(int(dur / beat) + 1):
    s = int(k * beat * SR); L = min(int(0.25 * SR), n - s)
    if L <= 0: break
    tt = np.arange(L) / SR
    kick = np.sin(2 * np.pi * (50 + 90 * np.exp(-tt * 30)) * tt) * np.exp(-tt * 9)
    mix[s:s + L] += 0.35 * kick
    hs = s + int(beat / 2 * SR); HL = min(int(0.05 * SR), n - hs)
    if HL > 0: mix[hs:hs + HL] += 0.05 * rng.standard_normal(HL) * np.exp(-np.arange(HL) / SR * 60)
    if k % 2 == 1:
        SL = min(int(0.18 * SR), n - s)
        mix[s:s + SL] += 0.08 * rng.standard_normal(SL) * np.exp(-np.arange(SL) / SR * 18)
fade = int(1.2 * SR); mix[-fade:] *= np.linspace(1, 0, fade); mix[:int(0.1 * SR)] *= np.linspace(0, 1, int(0.1 * SR))
mix = mix / np.max(np.abs(mix)) * 0.8
with wave.open(out, "w") as w:
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((mix * 32767).astype(np.int16).tobytes())
