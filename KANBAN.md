# Kanban — La Majorité

Mis à jour par moi à chaque session (routine quotidienne et sessions avec le propriétaire).
Format : `- [ ] tâche — (qui) — détail`. Le propriétaire peut ajouter des cartes dans « À faire ».

## 🔴 Bloqué — action du propriétaire
- [ ] Vérifier les variables d'environnement (Upload-Post et OpenRouter OK le 20/10) : `ELEVENLABS_API_KEY`, `ELEVENLABS_VOICE_ID` (voix Paul K), `OPENROUTER_API_KEY` — (propriétaire)
- [ ] Mettre photo de profil, bio et stories à la une (kit `La_Majorite_profil.zip`) — (propriétaire)
- [ ] Épingler la Partie 1 sur les 3 plateformes après sa publication — (propriétaire)
- [ ] Générer les 2 photos de profil et la bannière manquantes (facultatif) — (propriétaire)

## 📋 À faire
- [ ] Mesure de « traîne de la voix » (`stems_report.py`) : fausse alerte si les fins de mots sont transcrites trop tôt (P2 : 7,5 alors que la voix est sèche) → mesurer après la vraie fin d'énergie — (moi)
- [ ] Carte « TU DIVISES » (P2) : ligne 3 à retoucher, remarque facultative du directeur — (moi)
- [ ] Compter le vote P1 (`votes.py P1`, posts enregistrés dans MEMOIRE), écrire/adapter la P2, publier — 21/10 21h00 (passage 19h05) — (moi)
- [ ] Animation « bouche ouverte / fermée » des personnages via OpenRouter (variantes d'expression) — (moi)
- [ ] Pack d'images du mois (banque réutilisable + 15 images/épisode, P6 → P30) — (moi : prompts ; propriétaire : génération)
- [ ] Ouvrir @rayan.vote quand la P1 dépasse ~300 K vues — (propriétaire + moi)
- [ ] setup.sh : ajouter des en-têtes navigateur au téléchargement des musiques (HTTP 406) — à faire valider (branche studio/essais) — (moi)
- [ ] Rapport hebdo du dimanche (vues, rétention, commentaires, abonnés) — (moi, automatisation)

## 🟡 En cours

## ✅ Fait
- [x] **P2 programmée** 21/10 21h00 (job 868127bebc2840a19b03c9b34e69d2a0) ; vote P1 = GARDER 3/3 ; directeur qualité OK en boucle 2 — 21/10
- [x] **P1 publiée** 20/10 21h25 sur TikTok, Instagram, YouTube (Upload-Post, profil `affaires-classees`, label IA, 1er commentaire de vote) ; verdict directeur qualité : publier — 20/10
- [x] P1 fabriquée et contrôlée (81,7 s ; musique −10,8 dB ; effets −16,9 dB ; 0 image manquante), envoyée au propriétaire — 20/10
- [x] Analyse des vidéos Saveo + rapport Instagram → `docs/STRATEGIE.md`
- [x] Bible saison 1, scripts P1–P5, 183 prompts d'images
- [x] Pipeline : voix, calage, montage Remotion (HUD, cartes, motion, parallaxe 2.5D, bruitages), miniatures
- [x] Publication Upload-Post (TikTok/Instagram/YouTube, label IA, miniature, programmation 19h) + comptage des votes
- [x] Mémoire de la chaîne : IDENTITE, MEMOIRE, JOURNAL, RUNBOOK, KANBAN
- [x] Kit profil : photo, miniatures P1–P5, highlights, bios

- [ ] Étiquettes de plan (overlay tag) calées sur le mot dit, comme les cartes (`align.py`, champ `mot`) — remarque du directeur qualité sur la P1, à appliquer dès la P2 (P1 inchangée).

- [ ] P1 déjà en ligne : retirer « Images et voix générées par IA » de la description YouTube (Upload-Post, édition de post YouTube) ; TikTok/Instagram : étiquette IA posée au 1er post, disparaît à la republication.
- [ ] Propriétaire : ajouter RESEND_API_KEY dans l'environnement « video-social-media » → nouvelle session opérateur + test email.
