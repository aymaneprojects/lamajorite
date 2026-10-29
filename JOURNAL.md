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

## 20/10 — 23h · Règle des 20 commentaires (demande du propriétaire)
- `pipeline/relance.py` : au passage de 19h05 (~22 h après la publication), moins de 20 commentaires du public
  (nos réponses exclues) → l'épisode est supprimé et republié à 21h00 avec une nouvelle accroche ; pas de nouvel épisode ce jour-là.
- YouTube supprimé par l'API ; TikTok et Instagram : pas d'API de suppression → le propriétaire supprime (liens envoyés).
- 3 relances sans succès → alerte au propriétaire (nouvelle accroche / miniature à choisir). Testé sur des commentaires simulés.

## 20/10 — 23h35 · Passage 2 (après publication P1)
- `record P1` : 3/3 posts OK, id et URL confirmés dans MEMOIRE (TikTok 7698833455286734113, Instagram 18130217056829263, YouTube 6s3FwNUDcsY).
- Commentaires à 23h35 (2h10 après la mise en ligne) : TikTok 0, Instagram 0, YouTube 0 → `engage.py P1` : aucune réponse à envoyer.
- Vote P1 (GARDER/POLICE) à compter demain au passage 1 (19h05).

## 21/10 — 16h45 · Emploi du temps + emails + plus aucune mention IA
- `docs/EMPLOI_DU_TEMPS.md` : 13h05 écriture · 19h05 production/relance · 20h20 rattrapage · 23h35 après publication · dim. bilan · lun. stock d'images.
- `pipeline/notify.py` (Resend) : voix, images, à supprimer, bloqué, alerte accroche, récap, bilan ; anti-doublon ; sans clé → out/email_*.txt.
- Consigne propriétaire : jamais de mention « IA » → étiquettes IA retirées, description YouTube nettoyée, verrou `sans_ia` avant publication.

## 21/10 — 17h55 · Seuil abaissé à 2 commentaires (propriétaire)
- La P2 se produit dès 2 commentaires du public ; en dessous (0 ou 1) après ~22 h → suppression + republication.

## 21/10 — 19h05 · Passage 1 : P2 programmée à 21h00
- Règle des 2 commentaires (`relance.py P1`) : **continuer** (4 commentaires du public).
- Vote P1 : **GARDER 3/3 (100 %)** — roou._x (Instagram) + 2 votes TikTok ; 1 commentaire hors vote (« Bête de concept »).
  Bugs corrigés en route (le premier comptage donnait 0 commentaire, puis POLICE gagnant à tort) :
  `comments()` envoyait limit=100 (max 50) et l'erreur passait pour « 0 commentaire » → limit 50 + erreur levée ;
  `votes.py` comptait nos propres rappels « GARDER ou POLICE ? » et fusionnait tous les votants TikTok (pas de user.username)
  → `auteur()` + `est_a_nous()` partagés avec `relance.py` et `engage.py` ; `engage.py` lit aussi `comment_id` (TikTok).
- `engage.py P1` : 3 réponses (1 Instagram, 2 TikTok). Formules « demain 21h » → « à 21h » (l'épisode suivant sort le soir même).
- P2 (script de la session principale, voix Nicolas Petit fournie par le propriétaire) : 1er rendu refusé par qa.py (2 plans < 1 s).
  Directeur qualité, boucle 1 : refus (plans courts + traîne de voix 7,5 dB). Plans fusionnés (16+17, 25+26) et dernier plan coupé (P2_29 puis P2_28 + vote).
  Traîne : gate plus dur sans effet ; enveloppe mesurée = fin réelle des mots (transcription ~0,1 s trop tôt) puis silence numérique → voix sèche, mixage P1 conservé.
  Boucle 2 : **publier = true** (87,4 s, 33 plans, musique −10,4 dB, effets −16,0 dB, 30 textes calés).
- Fait vérifié : identité contrôlée par la banque pour louer un coffre (obligation de vigilance, art. L561-5 CMF).
- Publication programmée 21h00 : request 9m8-P2-f98610, job 868127bebc2840a19b03c9b34e69d2a0. Légende « 100 % d'entre vous ont dit GARDER », sans mention IA.

## 21/10 — 23h35 · Passage 2 (après publication P2)
- P2 publiée à 21h00, 3/3 :
  - TikTok : https://www.tiktok.com/@lamajorite.serie/video/7699198595630664993
  - Instagram : https://www.instagram.com/reel/DexHQzTDI4p/
  - YouTube : https://www.youtube.com/watch?v=LVkWFL419Ns
- Commentaires du public à 23h35 : 2 (Instagram : @mistermarti « Tu les passes », @evil_shrimply), aucun vote PAYER/REFUSER encore.
- `engage.py P2` : 0 réponse envoyée (commentaires sans vote : réponse tirée au sort, pas retenue).
- Récap au propriétaire (`notify.py recap P2`) : pas envoyé, RESEND_API_KEY absente → écrit dans out/email_recap_P2.txt.

## 22/10 — 13h05 → 19h05 · P3 écrite, voix manquante
- Vote P2 : **PAYER 2/2** (TikTok @malvinfontaine « Payer », Instagram @lepro2cfgh « Paye ») ; 5 commentaires du public ; règle des 2 commentaires : continuer.
  `votes.py` accepte maintenant les formes courtes (« Paye » → PAYER, « Refuse » → REFUSER : début du mot, ≤ 2 lettres en moins).
- Réponses : 2 (TikTok « Payer », Instagram @mistermarti).
- P3 « Tout en liquide » écrite par le scénariste (règles docs/CROISSANCE.md) : 192 mots ≈ 71 s, 21 plans, vote PARTAGER/REFUSER, 0 image manquante.
  Fait réel : bijoutiers soumis à déclaration de soupçon à Tracfin (CMF L561-2, L561-15). Box 117 / sac 2 reportés en P4.
- Passage de 13h05 interrompu (redémarrage du conteneur) avant la demande de voix ; reprise à 19h05.
- **Pas de voix P3** : pas de clé ElevenLabs, pas de P3.mp3 dans le Drive (vérifié par recherche Drive), pas de clé Resend → email non envoyé (out/email_voix_P3.txt). P3 non publiée à 21h00.
- Chiffres 22/10 13h : P1 TikTok 688 vues / 60 likes, IG 167, YT 37 ; P2 TikTok 627 / 46 likes, IG 1 173 vues / 41 likes, YT 22 (data/metrics.jsonl).

Texte voix P3 :
```
Tu as trouvé neuf millions huit cent quarante mille euros.

Ce soir, tu décides : partager, ou refuser. Ton cousin en veut la moitié.

Il y a trois jours, il voulait cinquante mille.

Cent pour cent d'entre vous ont dit payer. Top commentaire : « Payer. »

Alors tu paies. Il jure : personne ne saura.

Lui, il s'est tu. Sa nouvelle chaîne, non.

Une chaîne en or. Six mille euros.

Des jantes. Une nuit en boîte. Tout en liquide.

Et ce n'est pas le pire.

Voilà le truc. Un bijoutier qui a un doute doit prévenir Trak-fine. C'est la loi.

Rayan. Quatre cents euros sur son compte. Six mille de bijoux, en billets.

L'analyste tire le fil. Un numéro revient.

Le tien. Soupçon : soixante-deux pour cent.

Problème. Rayan t'a suivi. Jusqu'au sac numéro un.

Deux heures du matin. Il creuse déjà.

Il sourit. « Moitié-moitié. Ou j'appelle quelqu'un. »

Au bout du chemin, des phares s'éteignent. Rayan n'était pas seul.

Tu partages, avec un cousin que Trak-fine surveille ?

Ou tu refuses, et Rayan fait signe à la voiture ?

Commente : partager, ou refuser. La majorité écrit la partie quatre.

Regarde bien son sourire. Ce n'est pas toi qu'il regarde.
```

## 22/10 — 23h35 · Passage 2
- Aucun épisode publié ce soir (voix P3 absente du Drive à 19h05 et à 20h20) → rien à enregistrer.
- `engage.py P2` lancé sur le dernier épisode en ligne ; vote P2 toujours PAYER.

## 22/10 — fin de session
- Conversation complète enregistrée : docs/sessions/2026-10-20_22_conversation.md.
- Retour du propriétaire : les vidéos ne sont pas assez narratives → à retravailler ensemble à la prochaine session.
- Clé Resend (« RESEND ») pas encore visible dans « video-social-media » : emails toujours écrits en fichiers.

## 23/10 — 13h05 · Passage 0
- Vote P2 inchangé : PAYER 2/2 (5 commentaires) ; aucune nouvelle réponse à envoyer.
- P3 déjà écrite → pas de nouveau scénario. Script P3 non retouché : le propriétaire veut retravailler la narration avec moi à la prochaine session (retour du 22/10).
- Voix P3 : toujours ni clé ElevenLabs ni clé Resend dans l'environnement → demande réécrite dans out/email_voix_P3.txt, non envoyée.

## 23/10 — 19h05 · Passage 1 : pas d'épisode (2e soir)
- Règle des 2 commentaires P2 : continuer (5 commentaires) ; vote PAYER 2/2 inchangé ; aucune réponse à envoyer.
- Voix P3 : toujours absente (ni audio/P3.mp3, ni fichier audio récent dans le Drive, ni clé ElevenLabs/Resend) → pas de fabrication ni de publication.
- Script P3 gardé tel quel en attendant la séance « narration » avec le propriétaire.

## 23/10 — soirée · Narration P3 v2 + passage 2
- Le propriétaire veut « une belle narration » : P3 réécrite en scène (pinède à 2 h du matin, retour 3 jours en arrière, face-à-face),
  lien affectif avec Rayan, enquête racontée, fin en boucle — `episodes/P3_voix_v2.txt` (~200 mots ≈ 74 s).
  Proposé aussi : balises de jeu ElevenLabs v3 et une bande-son plan par plan (pelle, forêt, moteur, phares…).
  En attente de son accord avant de recaler `episodes/P3.json` ; bruitages spécifiques à trouver (ElevenLabs Sound Effects ou banque libre).
- 23h35 : aucun épisode publié ce soir (voix P3 absente). P2 : vote PAYER 2/2 inchangé, aucune réponse à envoyer.

## 24/10 — 19h05 · Passage 1 : pas d'épisode (3e soir)
- P2 : vote PAYER 2/2 inchangé, aucun nouveau commentaire. Voix P3 absente (Drive vérifié), pas de clé ElevenLabs/Resend.
- En attente du propriétaire : validation du texte P3 v2, choix des bruitages, dépôt de P3.mp3.
- 24/10 23h35 : aucun épisode publié ce soir (voix P3 absente) ; P2 inchangée (PAYER 2/2), aucune réponse à envoyer.
- 25/10 13h05 : P2 inchangée (PAYER 2/2) ; 1 réponse automatique envoyée à @yassine_9537 (« si c pas du plagiat ça ») avec l'invitation à voter — réponse générique peu adaptée à une critique, à surveiller. P3 toujours en attente (texte v2, bruitages, voix).

## Bilan de la semaine (20–25/10) — dimanche 25/10, 19h05
| Épisode | TikTok vues · likes · comm. · temps moyen · vus en entier | Instagram vues · likes · comm. · partages · enreg. | YouTube vues |
|---|---|---|---|
| P1 (20/10) | 693 · 60 · 5 · 17,7 s · 3,0 % | 170 · 3 · 3 · 0 · 0 | 46 |
| P2 (21/10) | 635 · 46 · 3 · 15,4 s · 2,0 % | 1 299 · 46 · 8 · 2 · 5 | 44 |
- Total : ~2 900 vues, 2 abonnés TikTok gagnés (P2). Votes : P1 GARDER 3/3, P2 PAYER 2/2.
- Instagram a décollé sur la P2 (×7,6 vs P1, portée 1 051) ; TikTok stable ; YouTube marginal.
- Goulot inchangé : on regarde 15–18 s sur ~85 s, 2–3 % vont au bout → presque personne ne voit le vote.
- **Problème n°1 de la semaine : 4 soirs sans épisode (22→25/10)**, faute de voix P3 (ni clé ElevenLabs ni fichier déposé).
  La régularité compte plus que tout le reste : la priorité est de rendre la voix automatique (clés ElevenLabs) ou de
  déposer plusieurs voix d'avance.
- Expérience E1 (accroche + vote dès 5 s + 62–75 s) : pas encore testée (P3 non sortie). Narration P3 v2 en attente de validation.
- Pas de nouvelle recommandation dans docs/STRATEGIE.md : aucune donnée nouvelle depuis le diagnostic du 22/10.
- Récap envoyé ? Non : clé Resend absente (out/email_bilan*.txt).
- 25/10 23h35 : aucun épisode publié ce soir (voix P3 absente) ; P2 inchangée (PAYER 2/2).

## 26/10 — lundi 10h05 · Stock d'images
- P3, P4, P5 : toutes les images présentes (180 dans images/, 0 manquante d'après la bible).
- P6 → P9 : pas encore écrits (dépendent des votes et de la refonte narrative demandée par le propriétaire) → pas de pack de prompts
  ce lundi : le faire dès que l'arc P6+ est validé. Le stock couvre les 3 prochains épisodes (P3 toujours bloquée sur la voix).
- 26/10 19h05 : pas de P3 (voix absente du Drive, 5e soir sans épisode) ; P2 inchangée (PAYER 2/2).
- 26/10 23h35 : aucun épisode publié ce soir (voix P3 absente) ; P2 inchangée (PAYER 2/2).
- 26/10 23h35 (suite) : **Upload-Post refuse désormais le profil affaires-classees** (« not available on your current plan ») →
  commentaires illisibles. `votes.py` avait écrasé le résultat P2 par un résultat vide : restauré (PAYER 2/2).
  Garde-fous : `votes.py` conserve le dernier résultat et `relance.py` ne décide plus rien (pas de suppression) si aucune
  plateforme ne répond. Carte « Bloqué » ajoutée pour le propriétaire.
- 27/10 19h05 : pas de P3 (6e soir) — voix absente, Upload-Post toujours sur le plan Default (profil refusé).
- 27/10 23h35 : aucun épisode publié ; Upload-Post toujours sur le plan Default (commentaires illisibles).
- 28/10 19h05 : pas de P3 (7e soir) — voix absente, Upload-Post toujours sur le plan Default.
- 28/10 23h35 : aucun épisode publié ; Upload-Post toujours sur le plan Default.
- 29/10 19h05 : pas de P3 (8e soir) — voix absente, Upload-Post toujours sur le plan Default.
