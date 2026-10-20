# Routine quotidienne (exécutée chaque jour par une session planifiée)

0. **Installer** : `./setup.sh` (dépendances + images Drive). Si 0 image → stop, préviens le propriétaire.

Contexte : lis d'abord `IDENTITE.md`, `MEMOIRE.json`, la fin de `JOURNAL.md`.

1. **Vérifs** : `python3 pipeline/upload_post.py me` (clé + profil). Si erreur → stop, préviens le propriétaire.
2. **Votes de la veille** : `python3 pipeline/votes.py PX` (X = dernier épisode publié). Note le gagnant, les pseudos, le top commentaire.
   - Si TikTok ne renvoie pas les commentaires (capability `comments` absente) : compte avec Instagram + YouTube et note-le.
3. **Écrire l'épisode du jour** :
   - Si un script existe déjà et que son hypothèse de vote (`suppose`) = résultat réel → l'utiliser.
   - Sinon écrire `episodes/PX.json` (même structure que story_data.py, champ `specs` pour l'habillage) selon le vote,
     en respectant IDENTITE.md. Réutiliser au maximum les images existantes de `images/` (banque) ; lister les images manquantes.
   - Remplacer les placeholders : nombre de vues (en lettres dans la voix), top commentaire, « Personnes d'intérêt ».
4. **Fabriquer** : `./make_episode.sh PX images` (voix ElevenLabs, secours edge-tts ; calage ; rendu ; méta).
   - Contrôle : durée 80–140 s, 1080×1920, aucune image placeholder visible (sinon NE PAS publier).
5. **Publier** : `python3 pipeline/upload_post.py publish out/PX.mp4 out/PX_meta.json`
   puis `status <request_id>` jusqu'à obtenir les post_id/URL → les écrire dans `MEMOIRE.json` (`posts`: {plateforme: post_id}).
6. **Mémoire** : MAJ `MEMOIRE.json` (statut, HUD, fil de l'histoire, crédits), ajouter une entrée à `JOURNAL.md`, commit + push.
7. **Rapport** au propriétaire : épisode publié, liens, votes de la veille, images à fournir pour les 7 prochains jours.
