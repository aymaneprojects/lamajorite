"""Niveaux de chaque piste du mix (out/PX_stems) : voix, musique sous la voix / dans les silences, effets."""
import json, os, sys, wave
import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def rd(p):
    # rééchantillonné à 48 kHz quel que soit le fichier (certaines pistes sortent en 192 kHz)
    import subprocess
    pcm = subprocess.run(["ffmpeg", "-v", "error", "-i", p, "-ac", "1", "-ar", "48000", "-f", "s16le", "-"], capture_output=True).stdout
    return np.frombuffer(pcm, np.int16).astype(np.float32) / 32768


def db(x):
    return 20 * np.log10(np.sqrt(np.mean(x ** 2)) + 1e-9)


def report(ep):
    d = os.path.join(ROOT, "out", f"{ep}_stems")
    v, m, s = rd(f"{d}/voix.wav"), rd(f"{d}/musique.wav"), rd(f"{d}/effets.wav")
    n = min(len(v), len(m), len(s))
    v, m, s = v[:n], m[:n], s[:n]
    sr = 48000
    mask = np.zeros(n, bool)
    for w in json.load(open(os.path.join(ROOT, "render", "public", ep, "timeline.json")))["words"]:
        mask[int(w["t0"] * sr):min(n, int(w["t1"] * sr))] = True
    fx = s[np.abs(s) > 1e-3]
    r = {"voix": db(v[mask]), "musique_sous_voix": db(m[mask]), "musique_silences": db(m[~mask]), "effets": db(fx) if len(fx) else -99}
    r["ecart_musique"] = r["voix"] - r["musique_sous_voix"]
    r["ecart_effets"] = r["voix"] - r["effets"]
    # écho : niveau 50–250 ms après la fin des mots (pauses > 0,35 s), par rapport à la parole
    words = json.load(open(os.path.join(ROOT, "render", "public", ep, "timeline.json")))["words"]
    tails = [v[int(w["t1"] * sr) + 2400:int(w["t1"] * sr) + 12000] for w, nx in zip(words, words[1:]) if nx["t0"] - w["t1"] > 0.35]
    r["traine_voix"] = r["voix"] - db(np.concatenate(tails)) if tails else 0
    return {k: round(float(x), 1) for k, x in r.items()}


if __name__ == "__main__":
    print(json.dumps(report(sys.argv[1]), ensure_ascii=False, indent=1))
