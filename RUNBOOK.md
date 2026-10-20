# Routine quotidienne — exécutée chaque jour à 17h05 (Paris) par une session planifiée

But : un épisode publié à **19h00 heure de Paris** sur TikTok, Instagram et YouTube, tous les jours, sans exception.

## 0. Démarrer
1. Lire `IDENTITE.md`, `MEMOIRE.json`, `KANBAN.md`, `docs/STRATEGIE.md` et la fin de `JOURNAL.md`.
2. `./setup.sh` (dépendances + images Drive dans `images/`). 0 image → stop, prévenir le propriétaire.
3. `python3 pipeline/upload_post.py me` → clé et profil OK ? Sinon : ne pas publier, carte « Bloqué » dans KANBAN, prévenir.

## 1. Le vote d'hier
- Dernier épisode publié = `PX` dans MEMOIRE (`publie_le` renseigné). `python3 pipeline/votes.py PX`.
- Résultat → `MEMOIRE.json` (`result`), phrase « NN % d'entre vous ont dit MOT ».
- Si TikTok ne renvoie pas les commentaires, compter avec Instagram + YouTube et le noter.
- Pas de vote exploitable (0 vote) → la majorité « par défaut » est l'option qui fait avancer l'histoire ; le dire dans l'épisode.

## 2. L'épisode du jour (`PY`, Y = X + 1 ; le tout premier jour : P1 déjà prêt)
- Si `pipeline/story_data.py` ou `episodes/PY.json` contient PY et que son hypothèse (`suppose` dans MEMOIRE) = résultat réel → l'utiliser.
- Sinon écrire `episodes/PY.json` (structure de story_data, `specs` pour l'habillage) en respectant IDENTITE et STRATEGIE :
  résultat du vote en ouverture (carte `results` : barres en %), 3–4 problèmes numérotés, 1 carte « Ce que tu ne sais pas » vérifiée,
  1 retournement, carte `persons` (pseudos d'hier), vote final à 2 mots. 80–120 s (≈ 200–280 mots).
- Images : réutiliser la banque `images/` ; si une image manque, prendre la plus proche (même personnage/lieu) et l'ajouter
  à la carte KANBAN « images à générer ».
- Remplacer tous les `[CROCHETS]` (vues, top commentaire) par les vraies valeurs (en lettres dans la voix).

## 3. Fabriquer
`git pull --rebase origin main` juste avant (le propriétaire a pu pousser des réglages pendant la session).
`./make_episode.sh PY images` → voix (ElevenLabs, voix de la série ; secours edge-tts si crédits épuisés), calage, détourage 2.5D,
montage, miniature `out/PY_cover.png`, méta `out/PY_meta.json`.
Puis `python3 pipeline/pubkit.py PY "NN % d'entre vous ont dit MOT"` pour la légende avec le résultat.
Contrôles avant publication (sinon NE PAS publier et prévenir) :
- durée 80–140 s, 1080×1920, son présent ; aucune image « IMAGE PX_xx » (placeholder) visible ;
- regarder 6 images extraites (`ffmpeg -vf fps=1/15`) : texte lisible, rien de choquant, règles d'IDENTITE respectées.

## 4. Publier
`python3 pipeline/upload_post.py publish out/PY.mp4 out/PY_meta.json` → programmé à 19h00 Paris (ou immédiat s'il est plus tard).
Suivre `status <request_id ou job_id>` ; noter dans MEMOIRE : `posts` {plateforme: post_id/URL}, `request_id`, `publie_le`.

## 5. Mémoire, Kanban, journal
- `MEMOIRE.json` : statut, HUD final, fil de l'histoire (2–3 phrases), crédits, images restantes.
- `KANBAN.md` : déplacer les cartes, ajouter ce qui bloque.
- `JOURNAL.md` : une entrée datée (vote d'hier, épisode publié, liens, problèmes).
- `git add -A && git commit && git push` (jamais de clé, d'image ni de MP4).

## 6. Rapport au propriétaire
Message court : épisode publié + liens, résultat du vote d'hier, chiffres de la veille, ce qu'il doit faire (cartes « Bloqué »).

## Le dimanche en plus : bilan de la semaine
`python3 pipeline/report.py` → vues, likes, commentaires par épisode et plateforme, rétention épisode à épisode ;
ajouter le bilan à `JOURNAL.md` et 3 recommandations (durée, accroche, heure) dans `docs/STRATEGIE.md` si les chiffres le justifient.
