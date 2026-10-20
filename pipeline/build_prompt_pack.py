"""Génère le pack de prompts (MD + CSV) et les scripts voix off ElevenLabs à partir de story_data.py."""
import csv, os, sys, zipfile
from story_data import STYLE, CHARACTERS, EPISODES, EXTRAS

OUT = sys.argv[1] if len(sys.argv) > 1 else "../docs/pack_saison1"
os.makedirs(OUT, exist_ok=True)
REF_NAMES = {c[0].split("_")[0]: c for c in CHARACTERS}

def refs_label(refs):
    if not refs:
        return "aucune"
    return " + ".join(f"{r} ({REF_NAMES[r][1].split(' (')[0]})" for r in refs.split(","))

def full_prompt(p):
    style = STYLE
    if p.startswith("Square avatar"):  # photo de profil : carré, pas 9:16
        style = style.split(" Vertical 9:16")[0] + " Square 1:1 format, subject fills the frame. No text, no letters, no watermark, no logos."
    return f"{p} {style}"

rows, md = [], []
n_img = len(CHARACTERS) + sum(1 for e in EPISODES for b in e["beats"] if b[0] == "img") + sum(len(g[1]) for g in EXTRAS)

md += [
    "# 9,8 MILLIONS — Pack de prompts images (Saison 1, Parties 1 à 5)",
    "",
    f"**{n_img} images** au total. Chaque prompt est complet, il suffit de le copier-coller.",
    "",
    "## Mode d'emploi (à lire avant de générer)",
    "",
    "1. **Génère d'abord les 8 images de référence** (section 0). Choisis la meilleure version de chaque personnage : c'est elle qui garantit que le personnage reste le même dans toute la série.",
    "2. Pour chaque image, **joins la ou les références indiquées** (« Réf. à joindre ») :",
    "   - **ChatGPT / gpt-image** : glisse l'image de référence + le prompt.",
    "   - **Midjourney** : `--cref <url de la réf> --cw 80 --ar 9:16` (et `--sref` avec ta plus belle image pour garder le style).",
    "   - **Flux Kontext / Nano Banana / Ideogram** : image de référence en entrée + le prompt.",
    "3. **Format : vertical 9:16** (1080×1920 idéalement, minimum 768×1365).",
    "4. **Nomme chaque fichier exactement comme l'ID** (`P1_01.png`, `C01_toi.png`, `X_cover_P1.png`…) et renvoie-moi tout dans un dossier ou un zip. Je cale tout automatiquement.",
    "5. **Aucun texte dans les images** : les chiffres, le HUD (CASH / EN BANQUE / SOUPÇON), les SMS, les cartes et les boutons de vote sont ajoutés par moi au montage.",
    "6. Si une image sort avec du texte, des doigts bizarres ou un personnage différent, régénère-la. Mieux vaut 2 essais que casser la cohérence.",
    "",
    "Les lignes **🎙️ Voix off** te montrent ce qui est dit pendant l'image, pour vérifier que l'image colle. Les lignes **🟪 CARTE** sont des écrans faits au montage : **rien à générer**.",
    "",
    "Style commun (déjà inclus à la fin de chaque prompt) :",
    "",
    f"> {STYLE}",
    "",
    "---",
    "",
    "## 0. Références personnages et décor (à générer EN PREMIER)",
    "",
]
for cid, name, p in CHARACTERS:
    md += [f"### `{cid}` — {name}", "", "```", full_prompt(p), "```", ""]
    rows.append(["0-references", cid, "", "", full_prompt(p)])

for e in EPISODES:
    n = sum(1 for b in e["beats"] if b[0] == "img")
    md += ["---", "", f"## {e['title']} ({n} images)", "",
           f"HUD : {e['hud']}  ·  Vote final : **{e['vote'][0]}** / **{e['vote'][1]}**", ""]
    for b in e["beats"]:
        if b[0] == "card":
            md += [f"🟪 **CARTE (montage, rien à générer)** — 🎙️ *{b[1]}*  ", f"↳ {b[2]}", ""]
            continue
        _, iid, vo, refs, p = b
        md += [f"### `{iid}`", f"🎙️ *{vo}*  ", f"Réf. à joindre : **{refs_label(refs)}**", "", "```", full_prompt(p), "```", ""]
        rows.append([e["id"], iid, refs, vo, full_prompt(p)])

md += ["---", "", "## Bonus : miniatures, expressions et plans de transition", "",
       "Utiles pour les couvertures TikTok, les hooks, et pour boucher un trou au montage.", ""]
for title, items in EXTRAS:
    md += [f"### {title}", ""]
    for iid, refs, p in items:
        md += [f"#### `{iid}`", f"Réf. à joindre : **{refs_label(refs)}**", "", "```", full_prompt(p), "```", ""]
        rows.append(["bonus", iid, refs, "", full_prompt(p)])

with open(f"{OUT}/PROMPTS_IMAGES_9M8.md", "w") as f:
    f.write("\n".join(md))
with open(f"{OUT}/prompts_images.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["partie", "id_fichier", "references", "voix_off", "prompt"])
    w.writerows(rows)

# --- Scripts voix off ElevenLabs : un fichier par partie + un récap
vo_all = [
    "# 9,8 MILLIONS — Scripts voix off (ElevenLabs)",
    "",
    "## Réglages conseillés",
    "",
    "- **Modèle** : Eleven Multilingual v2 (le plus naturel en français).",
    "- **Voix** : masculine, grave, posée, un peu tendue (style narrateur de thriller). Garde la **même voix pour toute la série**.",
    "- **Réglages** : Stabilité ≈ 45 % · Similarité ≈ 75 % · Style ≈ 15 % · Vitesse 1.0 (1.05 si la partie dépasse 2 min).",
    "- **Colle le script d'une partie en entier** (une ligne = une phrase, garde les retours à la ligne : ils créent les pauses).",
    "- **Exporte 1 MP3 par partie**, nommé `P1.mp3`, `P2.mp3`… et envoie-les-moi. Je cale les images et les sous-titres mot à mot sur ta voix.",
    "- Remplace les `[CROCHETS]` avant de générer (nombre de vues **écrit en lettres**, ex. « sept cent mille »).",
    "- Si un mot sonne mal (Tracfin, Rayan, yonige-ya…), régénère seulement ce paragraphe ou écris-le phonétiquement (« Trak-fine »).",
    "",
]
for e in EPISODES:
    lines = [b[2] if b[0] == "img" else b[1] for b in e["beats"]]
    words = sum(len(l.split()) for l in lines)
    txt = "\n\n".join(lines) + "\n"
    with open(f"{OUT}/voix_{e['id']}.txt", "w") as f:
        f.write(txt)
    vo_all += ["---", "", f"## {e['title']}  (~{words} mots ≈ {round(words / 2.4)} s)", "", "```", txt.strip(), "```", ""]
with open(f"{OUT}/SCRIPTS_VOIX_OFF.md", "w") as f:
    f.write("\n".join(vo_all))

print(f"{len(rows)} prompts -> {OUT}")
