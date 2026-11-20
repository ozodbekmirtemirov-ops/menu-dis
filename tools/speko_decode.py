"""Speko audio.synthesize -> локальный WAV 44.1k mono. Usage: speko_decode.py <tool-result.txt> <out.wav>
MCP сохраняет ответ в файл: [0] — путь к .wav-блобу, [1] — JSON с audio_base64. Берём base64 (или блоб)."""
import sys, json, base64, subprocess, re
arr = json.load(open(sys.argv[1])); out = sys.argv[2]; src = None
for it in arr:
    t = it.get("text", "")
    if t.lstrip().startswith("{"):
        d = json.loads(t)
        if d.get("audio_base64"):
            src = out + ".src"; open(src, "wb").write(base64.b64decode(d["audio_base64"]))
            print(d.get("provider"), d.get("model"), d.get("duration_seconds"))
    m = re.search(r"saved to (\S+\.(wav|mp3))", t)
    if m and not src: src = m.group(1)
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", src, "-ar", "44100", "-ac", "1", out], check=True)
