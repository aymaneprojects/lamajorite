"""Synthétise la banque de bruitages (aucune licence nécessaire) → render/public/sfx/*.wav"""
import os, wave
import numpy as np

SR = 44100
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "render", "public", "sfx")
rng = np.random.default_rng(7)


def save(name, x):
    x = np.clip(x / (np.abs(x).max() + 1e-9) * 0.9, -1, 1)
    with wave.open(os.path.join(OUT, name + ".wav"), "w") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((x * 32767).astype(np.int16).tobytes())


def env(n, a, d):
    t = np.arange(n) / SR
    return np.minimum(t / a, 1) * np.exp(-t / d)


def lowpass(x, k):
    return np.convolve(x, np.ones(k) / k, mode="same")


t = lambda s: np.arange(int(SR * s)) / SR

# whoosh : bruit filtré dont la « hauteur » monte puis descend
n = int(SR * 0.45); noise = rng.standard_normal(n)
sweep = np.concatenate([lowpass(noise[i:i + 2205], max(2, int(40 - 35 * np.sin(np.pi * i / n)))) for i in range(0, n, 2205)])[:n]
save("whoosh", sweep * np.sin(np.pi * np.arange(n) / n) ** 2)
# impact : sous-basse + claquement
tt = t(1.2); save("impact", np.sin(2 * np.pi * (55 - 25 * tt) * tt) * np.exp(-tt * 3.5) + 0.4 * rng.standard_normal(len(tt)) * np.exp(-tt * 40))
# stamp : coup sec
tt = t(0.35); save("stamp", lowpass(rng.standard_normal(len(tt)), 6) * np.exp(-tt * 25) + 0.6 * np.sin(2 * np.pi * 120 * tt) * np.exp(-tt * 18))
# tick : compteur
tt = t(0.04); save("tick", np.sin(2 * np.pi * 2400 * tt) * np.exp(-tt * 150))
# buzz : vibration de téléphone (2 salves)
tt = t(0.9); buzz = np.sign(np.sin(2 * np.pi * 150 * tt)) * 0.5 * ((tt % 0.45) < 0.32); save("buzz", lowpass(buzz, 8))
# pop : bulle de SMS / carte
tt = t(0.12); save("pop", np.sin(2 * np.pi * (500 + 900 * tt / 0.12) * tt) * np.exp(-tt * 30))
# riser : montée de tension avant le vote
tt = t(3.0); save("riser", (lowpass(rng.standard_normal(len(tt)), 12) * 0.6 + np.sin(2 * np.pi * (80 + 300 * tt ** 2) * tt) * 0.4) * (tt / 3) ** 2)
# heartbeat : deux battements
tt = t(1.0); hb = np.zeros(len(tt))
for s0 in (0.0, 0.22):
    i = int(s0 * SR); seg = t(0.18); hb[i:i + len(seg)] += np.sin(2 * np.pi * 50 * seg) * np.exp(-seg * 22)
save("heartbeat", hb)
# glitch : bruit numérique haché
tt = t(0.3); g = rng.standard_normal(len(tt)) * ((np.floor(tt * 60) % 2) == 0); save("glitch", g * np.exp(-tt * 6))
print(sorted(os.listdir(OUT)))
