#!/usr/bin/env bash
# Fabrique un épisode complet : voix → calage → montage → kit de publication.
#   ./make_episode.sh P1 [dossier_images]
set -euo pipefail
EP=$1; IMG=${2:-images}
cd "$(dirname "$0")"
python3 pipeline/voice.py "$EP"
(cd pipeline && python3 align.py "$EP" "../audio/$EP.mp3" "../audio/${EP}_words.json" "../$IMG" && python3 layers.py "$EP")
BROWSER=$(ls -d /opt/pw-browsers/chromium_headless_shell-*/chrome-linux/headless_shell 2>/dev/null | head -1 || true)
(cd render && npx remotion render src/index.ts Episode "../out/$EP.mp4" --props="{\"episode\":\"$EP\"}" \
   ${BROWSER:+--browser-executable=$BROWSER} --concurrency=4 --log=error)
# volume normalisé pour les réseaux (-14 LUFS)
ffmpeg -y -v error -i "out/$EP.mp4" -c:v libx264 -crf 20 -preset medium -pix_fmt yuv420p -movflags +faststart -af loudnorm=I=-14:TP=-1.5:LRA=11 -ar 44100 -b:a 192k "out/${EP}_n.mp4" && mv "out/${EP}_n.mp4" "out/$EP.mp4"
python3 pipeline/pubkit.py "$EP" >/dev/null
ffprobe -v error -show_entries format=duration:stream=width,height -of compact "out/$EP.mp4"
echo "OK → out/$EP.mp4 + out/${EP}_meta.json"
