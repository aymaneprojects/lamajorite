"""Musique de suspense synthétisée (libre de droits) → render/public/sfx/suspense.mp3
Basse pulsée à 72 BPM, tic-tac, nappe sombre en mineur, montée toutes les 16 mesures."""
import os, subprocess, wave
import numpy as np

SR = 44100
DUR = 170
BPM = 72
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "render", "public", "sfx")
rng = np.random.default_rng(3)
t = np.arange(SR * DUR) / SR
beat = 60 / BPM
mix = np.zeros_like(t)

# nappe : accords de ré mineur / si bémol / sol mineur / la, filtrés, lente respiration
chords = [[73.4, 110, 146.8, 174.6], [58.3, 116.5, 146.8, 174.6], [49.0, 98, 146.8, 196], [55, 110, 138.6, 164.8]]
bar = beat * 4
for i, ch in enumerate(chords * int(DUR / bar / 4 + 1)):
    s0, s1 = int(i * bar * 2 * SR), int((i + 1) * bar * 2 * SR)
    if s0 >= len(t):
        break
    seg = t[s0:s1] - t[s0]
    pad = sum(np.sin(2 * np.pi * f * seg + np.sin(2 * np.pi * 0.3 * seg)) for f in ch) / len(ch)
    env = np.minimum(seg / 1.5, 1) * np.minimum((seg[-1] - seg) / 1.5 + 0.01, 1)
    mix[s0:s1] += 0.22 * pad * env

# basse pulsée sur chaque temps (battement de cœur grave)
for k in range(int(DUR / beat)):
    s0 = int(k * beat * SR)
    seg = np.arange(int(0.35 * SR)) / SR
    hit = np.sin(2 * np.pi * (60 - 30 * seg) * seg) * np.exp(-seg * 9)
    e = min(len(hit), len(mix) - s0)
    mix[s0:s0 + e] += (0.55 if k % 2 == 0 else 0.35) * hit[:e]

# tic-tac sur les croches
for k in range(int(DUR / (beat / 2))):
    s0 = int(k * beat / 2 * SR)
    seg = np.arange(int(0.03 * SR)) / SR
    tick = np.sin(2 * np.pi * (3200 if k % 2 else 2600) * seg) * np.exp(-seg * 220)
    e = min(len(tick), len(mix) - s0)
    mix[s0:s0 + e] += 0.06 * tick[:e]

# montée de tension toutes les 16 mesures
period = bar * 16
for k in range(int(DUR / period)):
    s1 = int((k + 1) * period * SR)
    s0 = max(0, s1 - int(4 * SR))
    seg = np.arange(s1 - s0) / SR
    noise = np.convolve(rng.standard_normal(len(seg)), np.ones(30) / 30, mode="same")
    mix[s0:s1] += 0.25 * (seg / 4) ** 2 * (noise + 0.5 * np.sin(2 * np.pi * (100 + 400 * (seg / 4) ** 2) * seg))

mix *= np.minimum(t / 3, 1) * np.minimum((DUR - t) / 4, 1)
mix = mix / np.abs(mix).max() * 0.85
wav = os.path.join(OUT, "suspense.wav")
with wave.open(wav, "w") as w:
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((mix * 32767).astype(np.int16).tobytes())
subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", wav, "-af", "lowpass=f=6000,aecho=0.6:0.5:60:0.25", "-b:a", "160k",
                os.path.join(OUT, "suspense.mp3")], check=True)
os.remove(wav)
print("ok", os.path.join(OUT, "suspense.mp3"))
