#!/usr/bin/env bash
# Prépare une session neuve : dépendances + images depuis Google Drive.
set -euo pipefail
cd "$(dirname "$0")"
pip install -q -r requirements.txt 2>/dev/null
(cd render && npm ci --no-audit --no-fund --silent)
# Musiques libres (Kevin MacLeod, CC BY 4.0) listées dans render/public/music/catalog.json
python3 - <<'PY'
import json, os, urllib.request
cat = json.load(open("render/public/music/catalog.json"))
for k, v in cat["pistes"].items():
    dst = f"render/public/music/{k}.mp3"
    if v.get("url") and not os.path.exists(dst):
        urllib.request.urlretrieve(v["url"], dst)
PY
# Images : dossier Drive « La Majorité » (sous-dossiers 0-references, P1…P5, bonus…), à plat dans images/
DRIVE_FOLDER=${DRIVE_FOLDER:-1yL0YrWBo4h2scNWURoW5bmxDIULyeXin}
rm -rf drive_dl && mkdir -p drive_dl images
python3 -m gdown "https://drive.google.com/drive/folders/$DRIVE_FOLDER" -O drive_dl -q || \
  echo "!! Drive inaccessible (dossier pas partagé « tous les utilisateurs disposant du lien » ?)"
find drive_dl -type f \( -iname '*.png' -o -iname '*.jpg' -o -iname '*.jpeg' -o -iname '*.webp' \) -exec cp {} images/ \;
echo "images: $(ls images | grep -vc gitkeep)"
