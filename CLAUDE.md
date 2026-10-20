# La Majorité — studio

Ce dépôt est le cerveau de la chaîne « La Majorité » (fictions interactives FR, TikTok/Instagram/YouTube).

À chaque session :
1. Lire `IDENTITE.md` (qui je suis, règles de contenu non négociables), `MEMOIRE.json` (état), la fin de `JOURNAL.md`.
2. Pour la routine de publication, suivre `RUNBOOK.md` à la lettre.
3. `./setup.sh` installe les dépendances et récupère les images depuis Google Drive dans `images/`.

Repères :
- Histoire et prompts : `pipeline/story_data.py` (P1–P5), `episodes/PX.json` (épisodes suivants), habillage : `pipeline/montage_specs.py`.
- Fabriquer un épisode : `./make_episode.sh PX images` → `out/PX.mp4` + `out/PX_meta.json`.
- Publier : `pipeline/upload_post.py` ; votes : `pipeline/votes.py`.
- Clés (variables d'environnement, jamais dans le dépôt) : UPLOAD_POST_API_KEY (ou UPLOADPOST_API), UPLOAD_POST_USER,
  ELEVENLABS_API_KEY, ELEVENLABS_VOICE_ID, OPENROUTER_API_KEY.
- Ne jamais commiter de clé, d'image ni de MP4.
