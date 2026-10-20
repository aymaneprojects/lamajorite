"""Contrôle qualité « directeur de studio » d'un épisode rendu.

  python3 qa.py P1   → out/P1_qa.md (rapport) + out/P1_planche.jpg (1 image toutes les 3 s)

Vérifie : voix (mots du script manquants / ajoutés / mal prononcés), rythme (plans trop courts ou trop longs),
son (écart voix / musique, saturation, niveau final), image (placeholders, planche à regarder), durée.
"""
import difflib, json, os, re, subprocess, sys, unicodedata, wave
import numpy as np
from story_data import EPISODES

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def norm(w):
    w = unicodedata.normalize("NFD", w.lower())
    return re.sub(r"[^a-z0-9]", "", "".join(c for c in w if unicodedata.category(c) != "Mn"))


def pcm(path):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-map", "0:a", "-ac", "1", "-ar", "48000", "-f", "s16le", "-"],
                         capture_output=True).stdout
    return np.frombuffer(raw, np.int16).astype(np.float32) / 32768


def db(x):
    return 20 * np.log10(np.sqrt(np.mean(x ** 2)) + 1e-9)


def main(ep_id):
    ep = next(e for e in EPISODES if e["id"] == ep_id)
    tl = json.load(open(os.path.join(ROOT, "render", "public", ep_id, "timeline.json")))
    mp4 = os.path.join(ROOT, "out", f"{ep_id}.mp4")
    lines, alerts = [f"# Contrôle qualité — {ep['title']}", ""], []

    # 1. Durée et format
    probe = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration:stream=width,height", "-of", "json", mp4],
                           capture_output=True, text=True).stdout
    info = json.loads(probe)
    dur = float(info["format"]["duration"])
    w, h = info["streams"][0]["width"], info["streams"][0]["height"]
    lines += ["## Format", f"- {w}×{h}, {dur:.1f} s"]
    if (w, h) != (1080, 1920):
        alerts.append(f"format {w}×{h} au lieu de 1080×1920")
    if dur > 120:
        alerts.append(f"durée {dur:.0f} s : au-delà de 120 s (cible 80–100 s pour accrocher)")

    # 2. Voix : script ↔ ce qui est réellement dit
    script = [norm(t) for b in ep["beats"] for t in (b[2] if b[0] == "img" else b[1]).split() if norm(t)]
    heard = [norm(x["w"]) for x in tl["words"] if norm(x["w"])]
    sm = difflib.SequenceMatcher(None, script, heard, autojunk=False)
    diffs = []
    for op, a0, a1, b0, b1 in sm.get_opcodes():
        if op != "equal":
            said, wrote = " ".join(heard[b0:b1]), " ".join(script[a0:a1])
            # les nombres écrits en lettres / en chiffres ne sont pas des erreurs
            if re.fullmatch(r"[\d ]*(euros?)?", said.replace(" ", "")) or not (said or wrote):
                continue
            diffs.append(f"- script « {wrote or '∅'} » → entendu « {said or '∅'} »")
    lines += ["", "## Voix (script ↔ voix réelle)", f"- concordance {sm.ratio():.0%}"] + (diffs[:25] or ["- aucun écart"])
    if sm.ratio() < 0.9:
        alerts.append(f"la voix s'écarte du script ({sm.ratio():.0%}) : vérifier les écarts listés")

    # 3. Rythme des plans
    short = [b["id"] for b in tl["beats"] if b["end"] - b["start"] < 1.0]
    long_ = [f"{b['id']} ({b['end'] - b['start']:.1f} s)" for b in tl["beats"] if b["end"] - b["start"] > 6.5]
    avg = np.mean([b["end"] - b["start"] for b in tl["beats"]])
    lines += ["", "## Rythme", f"- {len(tl['beats'])} plans, {avg:.1f} s en moyenne",
              f"- plans trop courts (< 1 s) : {', '.join(short) or 'aucun'}", f"- plans longs (> 6,5 s) : {', '.join(long_) or 'aucun'}"]
    if short:
        alerts.append(f"{len(short)} plan(s) de moins d'1 s : image à peine visible")

    # 4. Son : écart voix / musique+effets, saturation, niveau final
    mix, voice = pcm(mp4), pcm(os.path.join(ROOT, "render", "public", ep_id, "voice.mp3"))
    n = min(len(mix), len(voice))
    m, v = mix[:n], voice[:n]
    g = (m @ v) / (v @ v)
    gap = db(g * v) - db(m - g * v)
    peak = 20 * np.log10(np.abs(mix).max() + 1e-9)
    lines += ["", "## Son", f"- voix {db(g * v):.1f} dB, musique + effets {db(m - g * v):.1f} dB → écart {gap:.1f} dB (cible 7–10)",
              f"- crête {peak:.1f} dBFS"]
    if gap < 6:
        alerts.append(f"musique trop forte : seulement {gap:.1f} dB sous la voix")
    if gap > 11:
        alerts.append(f"musique trop faible : {gap:.1f} dB sous la voix, on ne l'entend presque pas")
    if peak > -0.5:
        alerts.append("saturation possible (crête au-dessus de -0,5 dBFS)")

    # 5. Image : placeholders + planche
    missing = [b["id"] for b in tl["beats"] if b["image"] and b["image"].split("/")[-1][:-4] not in tl["available"]]
    if missing:
        alerts.append(f"{len(missing)} image(s) manquante(s), placeholder visible : {', '.join(missing)}")
    sheet = os.path.join(ROOT, "out", f"{ep_id}_planche.jpg")
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", mp4, "-vf", "fps=1/3,scale=180:-1,tile=10x4", "-frames:v", "1", sheet])
    lines += ["", "## Image", f"- images manquantes : {', '.join(missing) or 'aucune'}", f"- planche : `out/{ep_id}_planche.jpg` (1 image / 3 s) à regarder"]

    lines = lines[:2] + ["## Verdict", *(f"- ⚠️ {a}" for a in alerts)] + (["- ✅ rien de bloquant détecté automatiquement"] if not alerts else []) + [""] + lines[2:]
    out = os.path.join(ROOT, "out", f"{ep_id}_qa.md")
    open(out, "w").write("\n".join(lines) + "\n")
    print("\n".join(lines))


if __name__ == "__main__":
    main(sys.argv[1])
