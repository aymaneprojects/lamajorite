"""Effet 2.5D : détoure le sujet de chaque image (personnage, objets) et bouche le décor derrière.
Le montage déplace sujet et décor à des vitesses différentes (parallaxe), comme une vraie caméra.

  python3 layers.py P1      → render/public/P1/layers/<id>_bg.jpg + <id>_fg.png, liste dans timeline.json
Modèles rembg (téléchargés au premier lancement) : isnet-general-use + isnet-anime, masques combinés.
"""
import json, os, sys
import cv2
import numpy as np
from PIL import Image
from rembg import new_session, remove

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def subject_mask(img_pil, sessions):
    # max des deux modèles : l'un attrape mieux les objets, l'autre les corps des personnages
    masks = [np.array(remove(img_pil, session=s, only_mask=True)) for s in sessions]
    m = np.maximum.reduce(masks)
    m = np.where(m > 110, 255, 0).astype(np.uint8)
    m = cv2.morphologyEx(m, cv2.MORPH_CLOSE, np.ones((15, 15), np.uint8))
    n, lab, stats, _ = cv2.connectedComponentsWithStats(m)
    keep = np.zeros_like(m)
    for i in range(1, n):
        if stats[i, cv2.CC_STAT_AREA] > m.size * 0.004:
            keep[lab == i] = 255
    return keep


def main(ep):
    pub = os.path.join(ROOT, "render", "public", ep)
    tl_path = os.path.join(pub, "timeline.json")
    tl = json.load(open(tl_path))
    out = os.path.join(pub, "layers")
    os.makedirs(out, exist_ok=True)
    sessions = [new_session("isnet-general-use"), new_session("isnet-anime")]
    done = {}
    for b in tl["beats"]:
        if not b["image"]:
            continue
        iid = b["image"].split("/")[-1][:-4]
        src = os.path.join(pub, "img", iid + ".png")
        if iid in done or not os.path.exists(src):
            continue
        fg_path, bg_path = os.path.join(out, iid + "_fg.png"), os.path.join(out, iid + "_bg.jpg")
        if os.path.exists(fg_path) and os.path.exists(bg_path):
            done[iid] = True
            continue
        pil = Image.open(src).convert("RGB")
        img = cv2.cvtColor(np.array(pil), cv2.COLOR_RGB2BGR)
        mask = subject_mask(pil, sessions)
        cover = float((mask > 0).mean())
        ok = 0.02 < cover < 0.7  # un sujet ni minuscule ni plein cadre
        if ok:
            alpha = cv2.GaussianBlur(mask, (0, 0), 1.5)
            hole = cv2.dilate(mask, np.ones((31, 31), np.uint8))
            small = cv2.resize(img, None, fx=0.5, fy=0.5)
            bg = cv2.inpaint(small, cv2.resize(hole, None, fx=0.5, fy=0.5), 15, cv2.INPAINT_TELEA)
            bg = cv2.resize(cv2.GaussianBlur(bg, (0, 0), 2), (img.shape[1], img.shape[0]))
            bg = np.where(hole[..., None] > 0, bg, img)
            cv2.imwrite(bg_path, bg, [cv2.IMWRITE_JPEG_QUALITY, 92])
            cv2.imwrite(fg_path, np.dstack([img, alpha]))
        done[iid] = ok
        print(f"{iid}: sujet {cover:.0%} {'✓' if ok else '— image simple'}", flush=True)
    tl["layers"] = sorted(k for k, v in done.items() if v)
    json.dump(tl, open(tl_path, "w"), ensure_ascii=False, indent=1)


if __name__ == "__main__":
    main(sys.argv[1])
