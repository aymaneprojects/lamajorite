# Routine de La Majorité — 2 passages automatiques par jour

Publication : **21h00 heure de Paris**, 7j/7, TikTok + Instagram + YouTube. Lire d'abord `IDENTITE.md`, `MEMOIRE.json`,
`KANBAN.md`, `docs/STRATEGIE.md`, `docs/REALISATION.md` et la fin de `JOURNAL.md`. Toujours `git pull --rebase origin main` avant de travailler.

## Passage 1 — 19h05 : produire et programmer l'épisode du jour
0. **Installer** si besoin : `./setup.sh` (dépendances + images Drive). Vérifier `python3 pipeline/upload_post.py me`.
   Clé absente ou refusée → ne pas publier, préparer quand même la vidéo, l'envoyer au propriétaire, carte « Bloqué » dans KANBAN.
1. **Vote d'hier** (dernier épisode publié `PX`) : `python3 pipeline/votes.py PX` → nombre de commentaires, votes par option,
   gagnant, pseudos (« Personnes d'intérêt »), extraits. Puis `python3 pipeline/engage.py PX` (réponses aux nouveaux commentaires).
2. **Écrire `episodes/PY.json`** (Y = X+1) selon le vote, en suivant `docs/REALISATION.md` (style Saveo : phrase d'ouverture fixe,
   rappel, « NN % d'entre vous ont dit MOT », top commentaire, problèmes numérotés, 1 fait réel vérifié, soupçon dit à voix haute,
   vote à 2 mots calé sur la voix, phrase-mystère finale). Champs de synchro : `mots`, `stamp_mot`, `at_word`, `left/right.mot`.
3. **Images** : utiliser `images/`. S'il manque des images pour PY ou pour les 3 épisodes suivants :
   écrire leurs prompts (même style que `docs/pack_saison1/PROMPTS_IMAGES_9M8.md`), faire un zip
   `out/pack_images_PY-PZ.zip` (prompts .md + .csv + liste des noms de fichiers), l'envoyer au propriétaire et ajouter une carte
   KANBAN « Images à générer ». En attendant, prendre l'image existante la plus proche (même personnage, même lieu).
4. **Voix** : `python3 pipeline/voice.py PY` (ElevenLabs, voix de la série ; secours edge-tts si crédits épuisés — le signaler).
5. **Fabriquer** : `./make_episode.sh PY images` (calage, recalage des mots, montage, mixage studio, miniature, contrôle qualité).
   Lire `out/PY_qa.md` et regarder `out/PY_planche.jpg`. Écart musique 8–11 dB, effets ≥ 15 dB, aucun placeholder, durée 80–110 s.
   Sinon corriger avant de publier.
6. **Légende** : `python3 pipeline/pubkit.py PY "NN % d'entre vous ont dit MOT"`.
7. **Publier** : `python3 pipeline/upload_post.py publish out/PY.mp4 out/PY_meta.json` (programmé à 21h00) → noter le `job_id`
   dans MEMOIRE (`episodes[PY].job_id`), statut « programmé ».
8. **Mémoire** : MEMOIRE (statut, HUD, fil de l'histoire), KANBAN, JOURNAL ; commit + push. Message court au propriétaire.

## Passage 2 — 23h35 : après la publication
1. `python3 pipeline/upload_post.py record PY <job_id>` → id et URL des posts dans MEMOIRE (indispensable pour les votes).
   Si la publication a échoué sur une plateforme : `POST /api/uploadposts/posts/retry` ou republier, et prévenir.
2. `python3 pipeline/engage.py PY` : premières réponses aux commentaires (12 max, jamais deux fois le même, pas d'insultes).
3. Noter dans JOURNAL : liens, premiers chiffres (commentaires, vues si disponibles). Commit + push.

## Le dimanche (passage 1)
`python3 pipeline/report.py` → bilan de la semaine dans JOURNAL, 3 recommandations dans `docs/STRATEGIE.md` si les chiffres le justifient.
