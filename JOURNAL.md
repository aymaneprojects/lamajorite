# Journal de La Majorité

## 2026-10-20
- Analyse des 5 vidéos de référence (série « saveo », EN). Format adapté en FR : saison 1 « 9,8 MILLIONS ».
- Chaîne nommée « La Majorité ». Pack de 183 prompts d'images + 5 scripts voix livrés.
- Voix P1 reçue (ElevenLabs, Benjamin, 97,6 s), calée mot à mot. Pipeline de montage Remotion codé, animatic P1 rendu.
- Upload-Post : clé ajoutée par le propriétaire (visible à partir d'une nouvelle session). Client + comptage des votes codés.
- Dépôt GitHub `aymaneprojects/lamajorite` créé comme mémoire de la chaîne. Images récupérées depuis le Drive partagé : 180/183 (manquent les 2 photos de profil et la bannière, hors vidéos).
- Partie 1 rendue avec les vraies images.
- Comparaison avec les vidéos Saveo image par image → montage v2 : motion des textes, parallaxe 2.5D (détourage), effets, bruitages, typo proche de l'original.
- Voix P1 remplacée par Paul K (ElevenLabs). Kit profil (photo, miniatures, highlights, bios).
- Rapport Instagram sur @saveo.house intégré → `docs/STRATEGIE.md` : 19h Paris 7j/7, légende modèle, résultat du vote en ouverture.
- Système mis en place : KANBAN.md, RUNBOOK v2, bilan hebdo (`pipeline/report.py`).
- 17h05 : 1re routine (nouvelle session) → pas de publication : clés absentes de l'environnement, pas d'accès en écriture au dépôt, pip ≠ python3. Corrigé : setup.sh (python3 -m pip), routine déplacée dans la session principale (trig_01V2Yo1vLcdPripEHsqgmcKr). Reste : clés à ajouter par le propriétaire.
- 19h45 : publication de la P1 (session principale). Clés toujours absentes (`env` : 0 variable UPLOAD/ELEVEN/OPENROUTER) → pas de publication automatique. setup.sh bloqué au téléchargement des musiques (site Scott Buckley → HTTP 406 sans en-têtes navigateur) : musiques et 180 images récupérées à la main. P1 refabriquée avec la voix validée : 81,7 s, musique 10,8 dB sous la voix, effets 16,9 dB, 0 image manquante, planche OK (alerte voix 89 % = seulement « Trak-fine »/« tracfin » et « 4h12 » dans la transcription). Vidéo, miniature et légende envoyées au propriétaire pour publication manuelle à 21h00.

## 20/10 — 20h25 · Équipe automatique
- Producteur (routine RUNBOOK) + agent **scénariste** + agent **directeur qualité** (`.claude/agents/`), droit de veto.
- `qa.py` compare chaque épisode à la P1 validée (`docs/reference_P1.json`) : accroche, HUD, cartes, vote, textes calés,
  voix de la série, motion, niveaux → `out/PX_qa.json`. `upload_post.py publish` refuse sans contrôle OK + feu vert du directeur.
- Test : le directeur qualité a validé la P1 (synchro vérifiée image par image). Test négatif : 4 défauts plantés, 4 détectés.
- Voix : plus de voix robot en public ; sans ElevenLabs, le texte voix part au propriétaire (dossier Drive `voix/`).

## 20/10 — 21h25 · Partie 1 publiée
- Clé Upload-Post enfin présente. Pas de profil « lamajorite » : les comptes @lamajorite.serie (TikTok), lamajorite.seriee (Instagram), @lamajoriteserie (YouTube) sont sur le profil **affaires-classees** → défaut de `upload_post.py` et MEMOIRE mis à jour.
- setup.sh : musiques encore en HTTP 406 → téléchargées avec en-têtes navigateur ; images Drive 180/180 (P1_10 retéléchargée à part).
- P1 refabriquée à l'identique (81,7 s, QA OK, mêmes niveaux que la référence) ; directeur qualité : publier = true.
- Publication immédiate (21h25, prête après 21h00) : request 9m8-P1-7e1658, job f165182845f941f5b5ab585fb8cb8b0a, 3/3 OK.
  - TikTok : https://www.tiktok.com/@lamajorite.serie/video/7698833455286734113 (1er commentaire posté)
  - Instagram : https://www.instagram.com/reel/DeulFU0jq1V/
  - YouTube : https://www.youtube.com/watch?v=6s3FwNUDcsY
- `upload_post.py record` corrigé (champs `platform_post_id`/`post_url` de l'API) → posts enregistrés dans MEMOIRE pour le vote.
- À vérifier (directeur qualité, non bloquant) : sources officielles des seuils « 1 000 € en espèces » et « 10 000 €/mois → Tracfin » à noter dans docs/.
