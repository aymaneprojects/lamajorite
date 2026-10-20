"""Contrôle qualité « directeur de studio » d'un épisode rendu.

  python3 qa.py P1   → out/P1_qa.md (rapport) + out/P1_planche.jpg (1 image toutes les 3 s)

Vérifie : voix (mots du script manquants / ajoutés / mal prononcés), rythme (plans trop courts ou trop longs),
son (écart voix / musique, saturation, niveau final), image (placeholders, planche à regarder), durée.
"""
import difflib, json, os, re, subprocess, sys, unicodedata, wave
import numpy as np
from story_data import EPISODES

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REF = os.path.join(ROOT, "docs", "reference_P1.json")  # mesures de la P1 validée par le propriétaire (20/10)


def norm(w):
    w = unicodedata.normalize("NFD", w.lower())
    return re.sub(r"[^a-z0-9]", "", "".join(c for c in w if unicodedata.category(c) != "Mn"))


def pcm(path):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-map", "0:a", "-ac", "1", "-ar", "48000", "-f", "s16le", "-"],
                         capture_output=True).stdout
    return np.frombuffer(raw, np.int16).astype(np.float32) / 32768


def loudness(path):
    err = subprocess.run(["ffmpeg", "-v", "info", "-nostats", "-i", path, "-map", "0:a", "-af", "ebur128", "-f", "null", "-"],
                         capture_output=True, text=True).stderr
    m = re.findall(r"I:\s+(-?[\d.]+) LUFS", err)
    return float(m[-1]) if m else None


def conformite(ep_id, tl, dur):
    """Ce qui fait « le même résultat que la P1 » : accroche, HUD, cartes, vote calé sur la voix, voix de la série, son."""
    beats, words = tl["beats"], tl["words"]
    cards = [b["card"] for b in beats if b.get("card")]
    types = [c["type"] for c in cards]
    hud_at = next((b["start"] for b in beats if b.get("hud")), None)
    vote = next((c for c in cards if c["type"] == "vote"), None)
    lufs = loudness(os.path.join(ROOT, "out", f"{ep_id}.mp4"))
    vfile = os.path.join(ROOT, "audio", f"{ep_id}_voice.json")
    voix = json.load(open(vfile))["provider"] if os.path.exists(vfile) else "inconnue"
    # textes calés sur la voix : chaque mot demandé doit avoir trouvé son instant
    non_cales = [f"{c.get('kicker') or c['type']} « {m} »" for c in cards for m, t in zip(c.get("mots", []), c.get("temps", []))
                 if m and t is None]
    if c_stamp := [c for c in cards if c.get("stamp") and c.get("stamp_mot") and c.get("stamp_at") is None]:
        non_cales += [f"tampon « {c['stamp']} »" for c in c_stamp]
    if vote:
        non_cales += [f"vote « {k} »" for k, t in (("Commente", vote.get("at")), (vote["left"]["word"], vote["left"].get("at")),
                                                   (vote["right"]["word"], vote["right"].get("at"))) if t is None]
    m = {"accroche": (beats[0].get("overlay") or {}).get("type") == "hook",
         "hud_des": None if hud_at is None else round(hud_at, 1),
         "cartes": ", ".join(types), "vote": f"{vote['left']['word']} / {vote['right']['word']}" if vote else None,
         "vote_dans_les_20_dernieres_s": bool(vote) and next(b["start"] for b in beats if b.get("card") is vote) > dur - 20,
         "textes_non_cales": len(non_cales), "voix_source": voix, "motion": tl.get("motion"), "musique": tl.get("music"),
         "lufs_final": lufs, "mots_transcrits": len(words)}
    b = []
    if not m["accroche"]:
        b.append("pas d'accroche (overlay hook) sur le premier plan")
    if hud_at is None or hud_at > 30:
        b.append("HUD absent ou trop tardif (> 30 s)")
    if sum(t in ("fact", "stat") for t in types) < 2 or "rule" not in types:
        b.append(f"cartes insuffisantes ({', '.join(types)}) : au moins 2 fait/stat et 1 règle/problème")
    if not vote:
        b.append("pas d'écran de vote")
    elif not m["vote_dans_les_20_dernieres_s"]:
        b.append("le vote n'est pas dans les 20 dernières secondes")
    if non_cales:
        b.append("textes non calés sur la voix : " + ", ".join(non_cales[:6]))
    if voix != "elevenlabs" and voix != "existant":
        b.append(f"voix « {voix} » : ce n'est pas la voix de la série (Nicolas Petit, ElevenLabs)")
    if tl.get("motion") != "plus":
        b.append(f"motion « {tl.get('motion')} » au lieu de « plus »")
    ref = json.load(open(REF)) if os.path.exists(REF) else {}
    if lufs is None or abs(lufs - ref.get("lufs_final", -14)) > 1.2:
        b.append(f"niveau final {lufs} LUFS (P1 : {ref.get('lufs_final', -14)} ± 1,2)")
    if not 70 <= dur <= 115:
        b.append(f"durée {dur:.0f} s hors de 70–115 s")
    return {"mesures": m, "bloquants": b}


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
    def toks(text):
        return [norm(t) for t in re.split(r"[\s'’\-]+", text) if norm(t)]
    script = [t for b in ep["beats"] for t in toks(b[2] if b[0] == "img" else b[1])]
    heard = [t for x in tl["words"] for t in toks(x["w"])]
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
    if sm.ratio() < 0.85:
        alerts.append(f"la voix s'écarte du script ({sm.ratio():.0%}) : vérifier les écarts listés")

    # 3. Rythme des plans
    short = [b["id"] for b in tl["beats"] if b["end"] - b["start"] < 1.0]
    long_ = [f"{b['id']} ({b['end'] - b['start']:.1f} s)" for b in tl["beats"] if b["end"] - b["start"] > 6.5]
    avg = np.mean([b["end"] - b["start"] for b in tl["beats"]])
    lines += ["", "## Rythme", f"- {len(tl['beats'])} plans, {avg:.1f} s en moyenne",
              f"- plans trop courts (< 1 s) : {', '.join(short) or 'aucun'}", f"- plans longs (> 6,5 s) : {', '.join(long_) or 'aucun'}"]
    if short:
        alerts.append(f"{len(short)} plan(s) de moins d'1 s : image à peine visible")

    # 4. Son : niveaux mesurés piste par piste (out/PX_stems, produit par mix.py)
    from stems_report import report
    st = report(ep_id)
    peak = 20 * np.log10(np.abs(pcm(mp4)).max() + 1e-9)
    lines += ["", "## Son (pistes séparées)", f"- voix {st['voix']} dB · musique sous la voix {st['musique_sous_voix']} dB "
              f"(écart {st['ecart_musique']} dB, cible 7–11, P1 10,8) · musique dans les silences {st['musique_silences']} dB",
              f"- effets {st['effets']} dB (écart {st['ecart_effets']} dB, cible ≥ 15) · crête {peak:.1f} dBFS",
              f"- traîne de la voix (écho après les phrases) {st['traine_voix']} dB (P1 : 16,4 ; plus bas = plus d'écho)"]
    if st["ecart_musique"] < 6:
        alerts.append(f"musique trop forte : seulement {st['ecart_musique']} dB sous la voix")
    if st["ecart_musique"] > 11:
        alerts.append(f"musique trop faible : {st['ecart_musique']} dB sous la voix")
    if st["ecart_effets"] < 13:
        alerts.append(f"effets trop forts : {st['ecart_effets']} dB sous la voix")
    if peak > -0.5:
        alerts.append("saturation possible (crête au-dessus de -0,5 dBFS)")

    # 5. Image : placeholders + planche
    missing = [b["id"] for b in tl["beats"] if b["image"] and b["image"].split("/")[-1][:-4] not in tl["available"]]
    if missing:
        alerts.append(f"{len(missing)} image(s) manquante(s), placeholder visible : {', '.join(missing)}")
    sheet = os.path.join(ROOT, "out", f"{ep_id}_planche.jpg")
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", mp4, "-vf", "fps=1/3,scale=180:-1,tile=10x4", "-frames:v", "1", sheet])
    lines += ["", "## Image", f"- images manquantes : {', '.join(missing) or 'aucune'}", f"- planche : `out/{ep_id}_planche.jpg` (1 image / 3 s) à regarder"]

    # 6. Conformité au format validé (référence : P1 du 20/10, docs/reference_P1.json)
    conf = conformite(ep_id, tl, dur)
    alerts += conf["bloquants"]
    lines += ["", "## Conformité au format P1"] + [f"- {k} : {v}" for k, v in conf["mesures"].items()]

    lines = lines[:2] + ["## Verdict", *(f"- ⚠️ {a}" for a in alerts)] + (["- ✅ rien de bloquant détecté automatiquement"] if not alerts else []) + [""] + lines[2:]
    out = os.path.join(ROOT, "out", f"{ep_id}_qa.md")
    open(out, "w").write("\n".join(lines) + "\n")
    mesures = {**conf["mesures"], **st, "duree": round(dur, 1), "crete": round(float(peak), 1), "concordance": round(sm.ratio(), 3)}
    json.dump({"episode": ep_id, "ok": not alerts, "bloquants": alerts, "mesures": mesures},
              open(os.path.join(ROOT, "out", f"{ep_id}_qa.json"), "w"), ensure_ascii=False, indent=1)
    print("\n".join(lines))


if __name__ == "__main__":
    main(sys.argv[1])
