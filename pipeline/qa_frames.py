"""Planche de synchro pour le directeur qualité : pour chaque texte calé sur la voix (lignes de carte, tampon,
étiquette de plan, bulles SMS, vote), l'image 0,1 s AVANT le mot et 0,25 s APRÈS, côte à côte, annotées.

  python3 qa_frames.py P2   → out/qa_P2/synchro_01.jpg, synchro_02.jpg… (8 événements par planche)

Règle : sur l'image « avant », le texte ne doit PAS être là ; sur l'image « après », il doit être là.
Événements sans instant (temps null, SMS, étiquette sans mot) : marqués « début de plan », à juger à l'œil.
"""
import json, os, subprocess, sys
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def events(tl):
    for b in tl["beats"]:
        for label, t in _events(b, tl["words"]):
            yield label, t, b["start"] + 0.3


def _events(b, words):
    if True:
        c, o, s = b.get("card"), b.get("overlay"), b["start"]
        if c:
            for i, (m, t) in enumerate(zip(c.get("mots", []), c.get("temps", []))):
                if m:
                    yield (f"{c.get('kicker') or c['type']} · ligne {i + 1} « {m} »", None if t is None else s + t)
            if c.get("stamp"):
                yield (f"tampon {c['stamp']}", None if c.get("stamp_at") is None else s + c["stamp_at"])
            if c["type"] == "vote":
                yield ("vote « COMMENTE »", None if c.get("at") is None else s + c["at"])
                for k in ("left", "right"):
                    yield (f"vote {c[k]['word']}", None if c[k].get("at") is None else s + c[k]["at"])
            if c["type"] == "sms":
                yield ("SMS (début de plan)", None)
        if o and o.get("type") == "tag":
            mot = o.get("mot")
            t = next((w["t0"] for w in words if mot and w["t0"] >= s - 0.5 and mot.lower() in w["w"].lower()), None)
            yield (f"étiquette {o['text']}" + ("" if t else " (début de plan)"), t)
        if o and o.get("type") == "hook":
            yield ("accroche", 0.6)


def frame(mp4, t, path):
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-ss", f"{max(t, 0):.2f}", "-i", mp4, "-frames:v", "1",
                    "-vf", "scale=270:-1", path], check=True)
    with Image.open(path) as im:
        return im.convert("RGB").copy()


def main(ep):
    tl = json.load(open(os.path.join(ROOT, "render", "public", ep, "timeline.json")))
    mp4 = os.path.join(ROOT, "out", f"{ep}.mp4")
    d = os.path.join(ROOT, "out", f"qa_{ep}")
    os.makedirs(d, exist_ok=True)
    evs, sheets = list(events(tl)), []
    rows = []
    for label, t, debut in evs:
        beat_t = t if t is not None else debut
        a = frame(mp4, beat_t - 0.1, os.path.join(d, "_a.jpg"))
        z = frame(mp4, beat_t + 0.25, os.path.join(d, "_z.jpg"))
        rows.append((label, beat_t, t is not None, a, z))
    for k in range(0, len(rows), 8):
        chunk = rows[k:k + 8]
        w, h = chunk[0][3].size
        img = Image.new("RGB", (4 * (2 * w + 10), (h + 40) * ((len(chunk) + 3) // 4)), "white")
        dr = ImageDraw.Draw(img)
        try:
            font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 13)
        except OSError:
            font = ImageFont.load_default()
        for i, (label, t, cale, a, z) in enumerate(chunk):
            x, y = (i % 4) * (2 * w + 10), (i // 4) * (h + 40)
            dr.text((x + 4, y + 4), f"{label[:44]}", fill="black", font=font)
            dr.text((x + 4, y + 20), f"{t:.2f} s · AVANT | APRÈS" + ("" if cale else " · non calé"), fill="red" if not cale else "gray", font=font)
            img.paste(a, (x, y + 40)); img.paste(z, (x + w, y + 40))
        p = os.path.join(d, f"synchro_{k // 8 + 1:02d}.jpg")
        img.save(p, quality=85)
        sheets.append(p)
    for f in ("_a.jpg", "_z.jpg"):
        if os.path.exists(os.path.join(d, f)):
            os.remove(os.path.join(d, f))
    print(json.dumps({"evenements": len(rows), "non_cales": sum(not r[2] for r in rows), "planches": sheets}, ensure_ascii=False))


if __name__ == "__main__":
    main(sys.argv[1])
