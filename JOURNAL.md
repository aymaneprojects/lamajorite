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
