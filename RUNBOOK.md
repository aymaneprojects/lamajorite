# Routine de La Majorité — 2 passages automatiques par jour

Équipe : **producteur** (la session qui suit ce RUNBOOK, de A à Z) · **scénariste** (agent) · **directeur qualité** (agent
indépendant, droit de veto). Objectif : chaque épisode au niveau de la P1 validée — même voix, même son, même motion,
textes calés sur la voix.

Publication : **21h00 heure de Paris**, 7j/7, TikTok + Instagram + YouTube. Lire d'abord `IDENTITE.md`, `MEMOIRE.json`,
`KANBAN.md`, `docs/STRATEGIE.md`, `docs/REALISATION.md` et la fin de `JOURNAL.md`. Toujours `git pull --rebase origin main` avant de travailler.

## Passage 1 — 19h05 : produire et programmer l'épisode du jour
0. **Installer** si besoin : `./setup.sh` (dépendances + images Drive). Vérifier `python3 pipeline/upload_post.py me`.
   Clé absente ou refusée → ne pas publier, préparer quand même la vidéo, l'envoyer au propriétaire, carte « Bloqué » dans KANBAN.
0b. **Règle des 20 commentaires** (dernier épisode publié `PX`) : `python3 pipeline/relance.py PX`.
   - `continuer` (≥ 20 commentaires du public, nos réponses exclues) → suite normale (étape 1).
   - `attendre` (post de moins de 22 h) → suite normale si un épisode doit sortir, sinon rien.
   - `relancer` (< 20 commentaires après 22 h) → **pas de nouvel épisode aujourd'hui** :
     `python3 pipeline/relance.py PX --executer` (archive la tentative dans MEMOIRE, supprime YouTube par l'API,
     nouvelle accroche de légende). TikTok et Instagram n'ont pas d'API de suppression : envoyer au propriétaire
     `out/PX_a_supprimer.txt` (liens à supprimer avant 21h00) + carte KANBAN « À supprimer ». Si `out/PX.mp4` n'existe
     plus, le refabriquer (`./make_episode.sh PX images`) et refaire le contrôle qualité (qa.py + directeur-qa).
     Puis `engage.py PX`, et republier à 21h00 (étape 8 avec `out/PX_meta.json`), puis passer à l'étape 9.
   - `alerte` (3 relances sans 20 commentaires) → ne pas republier ; proposer au propriétaire 3 nouvelles accroches
     et une nouvelle miniature, carte KANBAN « Accroche à revoir », et attendre son choix.
1. **Vote d'hier** (dernier épisode publié `PX`) : `python3 pipeline/votes.py PX` → nombre de commentaires, votes par option,
   gagnant, pseudos (« Personnes d'intérêt »), extraits. Puis `python3 pipeline/engage.py PX` (réponses aux nouveaux commentaires).
2. **Scénario** — déléguer à l'agent **`scenariste`** (`.claude/agents/scenariste.md`, outil Agent) : lui donner Y, le gagnant,
   le %, le nombre de commentaires, le top commentaire, les pseudos. Il écrit `episodes/PY.json` au format de la P1.
3. **Images** : si `out/PY_images_manquantes.md` existe, ou s'il manque des images pour les 3 épisodes suivants :
   zip `out/pack_images_PY-PZ.zip` (prompts .md + .csv + noms de fichiers, style `docs/pack_saison1/PROMPTS_IMAGES_9M8.md`),
   l'envoyer au propriétaire et ajouter une carte KANBAN « Images à générer ». En attendant : l'image existante la plus proche.
4. **Voix** : la voix de la série est Nicolas Petit (ElevenLabs). Ordre de préférence :
   a. `audio/PY.mp3` déposé par le propriétaire (dossier Drive `voix/`, copié par `setup.sh`) ;
   b. `python3 pipeline/voice.py PY` avec `ELEVENLABS_API_KEY` + `ELEVENLABS_VOICE_ID` ;
   c. sinon : NE PAS publier une voix de secours. Envoyer le texte voix au propriétaire (`out/PY_voix.txt`), carte KANBAN
      « Voix à générer », et reprendre dès que le fichier arrive (le directeur qualité refuse toute voix edge-tts).
5. **Fabriquer** : `./make_episode.sh PY images` (calage, recalage des mots, montage, mixage studio, miniature, `qa.py`).
6. **Contrôle qualité indépendant** — déléguer à l'agent **`directeur-qa`** (`.claude/agents/directeur-qa.md`). Il compare à la P1
   (`docs/reference_P1.json`) et écrit `out/PY_verdict.json`.
   - `publier: false` → appliquer SES corrections (script, synchro, images, mixage), refabriquer, redemander son avis.
     **2 boucles maximum.** Toujours refusé → ne pas publier : envoyer la vidéo + le verdict au propriétaire, carte « Bloqué ».
   - `upload_post.py publish` refuse de lui-même de publier sans `out/PY_qa.json` OK ET `out/PY_verdict.json` « publier: true ».
7. **Légende** : `python3 pipeline/pubkit.py PY "NN % d'entre vous ont dit MOT"`.
8. **Publier** : `python3 pipeline/upload_post.py publish out/PY.mp4 out/PY_meta.json` (programmé à 21h00) → noter le `job_id`
   dans MEMOIRE (`episodes[PY].job_id`), statut « programmé ».
9. **Mémoire** : MEMOIRE (statut, HUD, fil de l'histoire, verdict qualité), KANBAN, JOURNAL ; commit + push
   (jamais de MP4, d'image ni de clé). Message court au propriétaire : épisode, vote gagnant, verdict, heure de publication.

## Passage 2 — 23h35 : après la publication
1. `python3 pipeline/upload_post.py record PY <job_id>` → id et URL des posts dans MEMOIRE (indispensable pour les votes).
   Si la publication a échoué sur une plateforme : `POST /api/uploadposts/posts/retry` ou republier, et prévenir.
2. `python3 pipeline/engage.py PY` : premières réponses aux commentaires (12 max, jamais deux fois le même, pas d'insultes).
3. Noter dans JOURNAL : liens, premiers chiffres (commentaires, vues si disponibles). Commit + push.

## Le dimanche (passage 1)
`python3 pipeline/report.py` → bilan de la semaine dans JOURNAL, 3 recommandations dans `docs/STRATEGIE.md` si les chiffres le justifient.
