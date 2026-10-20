"""Cale les beats d'un épisode sur la voix off (mots horodatés) → render/public/<EP>/timeline.json

Usage : python3 align.py P1 ../audio/P1.mp3 ../audio/P1_words.json [dossier_images]
"""
import difflib, json, os, re, shutil, subprocess, sys, unicodedata
from story_data import EPISODES
from montage_specs import SPECS, CAPTION_FIXES, CAPTION_PAIR_FIXES

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAUSE = 0.45
TAIL = 2.5  # secondes d'écran de vote après la fin de la voix


def norm(w):
    w = unicodedata.normalize("NFD", w.lower())
    return re.sub(r"[^a-z0-9]", "", "".join(c for c in w if unicodedata.category(c) != "Mn"))


def music_track(key=None):
    """(fichier, gain) de la piste choisie, ou de la piste par défaut du catalogue."""
    cat = json.load(open(os.path.join(ROOT, "render", "public", "music", "catalog.json")))
    key = key or cat["par_defaut"]
    piste = cat["pistes"][key]
    return piste.get("fichier") or f"music/{key}.mp3", piste.get("gain", 1.0)


def beat_text(b):
    return b[2] if b[0] == "img" else b[1]


def main(ep_id, audio, words_path, img_dir=None):
    ep = next(e for e in EPISODES if e["id"] == ep_id)
    spec = SPECS.get(ep_id, {"beats": {}})
    words = json.load(open(words_path))
    out_dir = os.path.join(ROOT, "render", "public", ep_id)
    os.makedirs(os.path.join(out_dir, "img"), exist_ok=True)

    # 1. silences à insérer (voix trop enchaînée)
    cuts = []
    for target in spec.get("pause_after", []):
        for w in words:
            if norm(w["w"]) == norm(target):
                cuts.append(round(w["t1"] + 0.05, 3))
                break
    cuts.sort()
    voice_out = os.path.join(out_dir, "voice.mp3")
    if cuts:
        parts, prev, filt = [], 0.0, []
        for i, c in enumerate(cuts + [None]):
            end = f":end={c}" if c is not None else ""
            filt.append(f"[0:a]atrim=start={prev}{end},asetpts=PTS-STARTPTS[s{i}]")
            parts.append(f"[s{i}]")
            if c is not None:
                filt.append(f"aevalsrc=0:d={PAUSE}:s=44100[z{i}]")
                parts.append(f"[z{i}]")
                prev = c
        filt.append(f"{''.join(parts)}concat=n={len(parts)}:v=0:a=1[out]")
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", audio, "-filter_complex", ";".join(filt),
                        "-map", "[out]", "-ar", "44100", "-b:a", "192k", voice_out], check=True)
        for w in words:
            shift = PAUSE * sum(1 for c in cuts if w["t0"] >= c)
            w["t0"] = round(w["t0"] + shift, 3)
            w["t1"] = round(w["t1"] + shift, 3)
    else:
        shutil.copy(audio, voice_out)
    dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", voice_out],
                               capture_output=True, text=True).stdout)

    # 2. alignement texte du script ↔ mots transcrits
    script_tokens, beat_first = [], []
    for b in ep["beats"]:
        beat_first.append(len(script_tokens))
        script_tokens += [norm(t) for t in beat_text(b).split() if norm(t)]
    heard = [norm(w["w"]) for w in words]
    sm = difflib.SequenceMatcher(None, script_tokens, heard, autojunk=False)
    mapping = {}
    for a, b, n in sm.get_matching_blocks():
        for k in range(n):
            mapping[a + k] = b + k

    def time_of(tok_idx):
        # premier mot du beat ; si non reconnu (ex. nombres), interpolation entre voisins reconnus
        if tok_idx in mapping:
            return words[mapping[tok_idx]]["t0"]
        before = max((i for i in mapping if i < tok_idx), default=None)
        after = min((i for i in mapping if i > tok_idx), default=None)
        if before is None:
            return 0.0
        tb = words[mapping[before]]["t1"]
        if after is None:
            return tb
        ta = words[mapping[after]]["t0"]
        return tb + (ta - tb) * (tok_idx - before) / (after - before)

    starts = [0.0] + [round(time_of(i) - 0.08, 3) for i in beat_first[1:]]
    ends = starts[1:] + [dur + TAIL]

    # 3. images (copie si fournies) + timeline
    beats, hud = [], None
    last_img = None
    for i, b in enumerate(ep["beats"]):
        s = spec["beats"].get(i, {})
        if "hud" in s:
            hud = {**(hud or {}), **s["hud"]}
        img = None
        if b[0] == "img":
            img = b[1]
            last_img = img
        card = s.get("card")
        if card and card["type"] == "sms":
            img = last_img
        if card and card["type"] == "vote":
            for side in ("left", "right"):
                if card[side].get("img"):
                    card[side]["src"] = f"{ep_id}/img/{card[side]['img']}.png"
        beats.append({
            "i": i, "start": max(0.0, starts[i]), "end": ends[i], "kind": "img" if img else "card",
            "id": b[1] if b[0] == "img" else f"card{i}", "image": f"{ep_id}/img/{img}.png" if img else None,
            "prompt": b[4] if b[0] == "img" else "", "overlay": s.get("overlay"), "card": card, "hud": dict(hud) if hud else None,
        })

    have = set()
    if img_dir and os.path.isdir(img_dir):
        needed = {b["id"] for b in beats if b["kind"] == "img"} | {b["image"].split("/")[-1][:-4] for b in beats if b["image"]}
        for f in os.listdir(img_dir):
            stem, ext = os.path.splitext(f)
            if ext.lower() in (".png", ".jpg", ".jpeg", ".webp") and stem in needed:
                subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", os.path.join(img_dir, f),
                                "-vf", "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920",
                                os.path.join(out_dir, "img", stem + ".png")], check=True)
    have = {os.path.splitext(f)[0] for f in os.listdir(os.path.join(out_dir, "img"))}

    caps = []
    for w in words:
        prev = caps[-1] if caps else None
        pair = (norm(prev["w"]), norm(w["w"])) if prev else None
        if pair in CAPTION_PAIR_FIXES:
            punct = re.sub(r"[\w']", "", w["w"])
            caps[-1] = {"w": CAPTION_PAIR_FIXES[pair] + punct, "t0": prev["t0"], "t1": w["t1"]}
        else:
            caps.append({"w": CAPTION_FIXES.get(w["w"].lower(), w["w"]), "t0": w["t0"], "t1": w["t1"]})
    timeline = {"episode": ep_id, "title": ep["title"], "fps": 30, "duration": round(dur + TAIL, 3),
                "voice": f"{ep_id}/voice.mp3", "music": music_track(spec.get("musique"))[0], "musicGain": music_track(spec.get("musique"))[1], "words": caps, "beats": beats,
                "available": sorted(have)}
    json.dump(timeline, open(os.path.join(out_dir, "timeline.json"), "w"), ensure_ascii=False, indent=1)
    missing = [b["image"].split("/")[-1][:-4] for b in beats if b["image"] and b["image"].split("/")[-1][:-4] not in have]
    print(f"{ep_id}: {len(beats)} beats, {dur:.1f}s voix (+{len(cuts)} pause), images manquantes: {len(missing)}")
    for b in beats:
        print(f"  {b['start']:6.2f}-{b['end']:6.2f} {b['id']:8s} {beat_text(ep['beats'][b['i']])[:60]}")


if __name__ == "__main__":
    main(*sys.argv[1:])
