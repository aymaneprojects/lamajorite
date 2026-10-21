# Emploi du temps de l'opérateur — La Majorité

Tout est automatique (tâches planifiées vers la session opérateur, environnement « video-social-media »).
Le propriétaire n'est sollicité **que par email** (aymane.abdennour@gmail.com, `pipeline/notify.py`, Resend),
et répond en déposant les fichiers dans le **Drive** partagé (images : racine / dossiers P* ; voix : dossier `voix/`).

| Heure (Paris) | Passage | Travail | Email au propriétaire si… |
|---|---|---|---|
| 13h05 | Écriture | réponses aux commentaires, votes provisoires, scénario du prochain épisode (agent `scenariste`), images, voix | il manque la voix (texte à générer) ou des images (zip de prompts) |
| 19h05 | Production | règle des 2 commentaires (`relance.py`), puis : republication **ou** fabrication + contrôle (agent `directeur-qa`) + publication 21h00 | liens TikTok/Instagram à supprimer · voix toujours absente (rappel) · épisode bloqué |
| 20h20 | Rattrapage | si rien n'est programmé ce soir et que la voix est arrivée : fabriquer, contrôler, publier dès que prêt | — |
| 23h35 | Après publication | enregistrer les posts, répondre aux premiers commentaires, journal | récap du soir (liens des 3 posts) |
| Dimanche 19h05 | Bilan | `report.py` en plus de la production | bilan de la semaine |
| Lundi 10h05 | Stock d'images | images des 7 prochains épisodes | zip de prompts si des images manquent |

Règles fixes : publication 21h00 · jamais de voix robot · jamais de mention « IA » · pas de publication sans feu vert
du directeur qualité · moins de 2 commentaires après ~22 h → suppression + republication (3 fois max, puis alerte).
Un même email n'est jamais envoyé deux fois le même jour.
