#!/usr/bin/env bash
# Prépare une session neuve : dépendances + images depuis Google Drive.
set -euo pipefail
cd "$(dirname "$0")"
python3 -m pip install -q -r requirements.txt 2>/dev/null || pip install -q -r requirements.txt
(cd render && npm ci --no-audit --no-fund --silent)
# Musiques libres (CC BY 4.0) listées dans render/public/music/catalog.json
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
# Voix fournies par le propriétaire (dossier Drive « voix », fichiers PX.mp3) : jamais écrasées
find drive_dl -type f -ipath '*voix*' -iname 'P*.mp3' | while read -r f; do
  n=$(basename "$f" | grep -oiE '^P[0-9]+' | tr p P); [ -n "$n" ] && [ ! -f "audio/$n.mp3" ] && cp "$f" "audio/$n.mp3" && \
    echo '{"provider": "elevenlabs", "source": "proprietaire"}' > "audio/${n}_voice.json" && echo "voix: $n"
done
