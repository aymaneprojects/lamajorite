# Bible de réalisation — La Majorité

Mon rôle sur chaque épisode : scénariste, réalisateur et ingénieur du son. Rien ne sort sans être passé par cette grille.
Sources : pratiques de post-production cinéma/TV (Netflix, études AES), guides de montage, et le rapport Saveo (`docs/rapport_saveo.md`).

## 1. Le son d'abord (c'est lui qui retient le spectateur)
Principe des studios : **la voix est l'ancre**, musique et effets se mixent autour d'elle
(Netflix mesure même son volume sur les dialogues seulement : « dialog-gated »).

| Rang | Piste | Règle |
|---|---|---|
| 1 | Narrateur | Toujours intelligible, jamais couvert. Référence du mix. |
| 2 | Musique | **8 à 10 dB sous la voix** pendant qu'elle parle (une étude AES sur les documentaires TV recommande ≥ 10 LU ; le grand public préfère un peu moins d'écart). Remonte doucement dans les silences. Jamais d'à-coups : effacement lent (attaque 250 ms, relâche ~1,2 s). |
| 3 | Effets | **≥ 15 dB sous la voix** et sous la musique. Ils soulignent, ils ne frappent pas. |

- Livraison réseaux : -14 LUFS intégré, crête ≤ -1,5 dBTP.
- Un seul « coup » fort autorisé par épisode : la révélation finale (avant le vote).
- Les bruitages tombent **pile sur l'image** qu'ils accompagnent (un « sting » qui arrive en retard casse la révélation).
- Musique : un seul morceau par épisode, démarré à un passage où la tension est déjà là ; fondu d'entrée 2 s, sortie 3 s.
- Contrôle à chaque épisode : `pipeline/stems_report.py` (niveaux voix / musique / effets mesurés séparément).

## 2. La voix (direction d'acteur)
- Mots sensibles écrits phonétiquement dans ElevenLabs : Tracfin → « Trak-fine », yonige-ya → « yo-ni-gué-ya ».
- Une phrase = une respiration. Retour à la ligne après chaque réplique forte pour forcer la pause.
- Les chiffres en lettres. Les révélations sur une phrase courte, seule.
- Écoute de contrôle : transcription automatique comparée au script (`pipeline/qa.py`) ; tout mot mal dit est régénéré.

## 3. Le montage
- Format court = **coupes franches** (les fondus enchaînés ralentissent). Les coupes son/image décalées (J-cut / L-cut)
  seulement pour adoucir un passage calme, jamais sur une révélation.
- Un plan = une idée. 2 à 4 s par plan, jamais moins d'1 s (illisible), jamais plus de 6 s sans mouvement.
- Mouvement de caméra lent permanent (zoom/dérive), sans détourage (rendu jugé mal coupé).
- Textes : peu de mots à l'écran, mot prononcé en blanc, mots-clés en rose, animation courte (≤ 0,4 s).

## 4. L'écriture (comme une série)
- **Accroche en 3 s** : qui, quoi, l'enjeu. Le spectateur est le héros (« tu »).
- **« Mais / Donc », jamais « Et puis »** : chaque scène découle de la précédente par une conséquence ou un obstacle
  (règle d'écriture des scénaristes de séries).
- Un problème toutes les 10–15 s, numéroté ; des chiffres précis et visuels.
- Chaque solution crée un problème plus grave.
- Une leçon réelle et vérifiée par épisode (carte « Ce que tu ne sais pas »).
- Fin ouverte sur un choix à 2 mots, au moment de la plus forte tension. Rappel du vote en ouverture de l'épisode suivant.
- Durée cible : 80–100 s (épisode 1), 90–120 s ensuite.

## 5. Validation (règle du propriétaire, 20/10)
Tout essai se fait sur la branche `studio/essais`. Je contrôle moi-même (son, voix, image, rythme) et j'envoie la vidéo
avec mon rapport. **Rien ne passe sur `main` (ce que publie la routine) sans le « c'est bon » du propriétaire.**

## 6. Comment Saveo raconte (transcription des épisodes 2 à 6, `docs/saveo_transcriptions.txt`)
| Procédé | Exemples Saveo | À faire chez nous |
|---|---|---|
| **Même phrase d'ouverture à chaque épisode** | « You stole 10 million dollars. » (5/5 épisodes) | « Tu as 9,8 millions d'euros qui ne sont pas à toi. » puis le rappel en une phrase |
| **Rappel + preuve sociale + résultat du vote dans les 10 premières secondes** | « Almost 2 million people watched you do it. And 61% of them said, hide it. » | « Un million de vous ont regardé. 61 % ont dit GARDER. » |
| **Le public est cité comme un personnage** | « One of you said it best… », « Spend voters, the car would have been worse. » | lire le top commentaire, s'adresser au camp perdant |
| **Tutoiement, phrases très courtes, fragments** | « You swung, hard. He came back harder. » « Three cars back, the whole drive. » | max ~8 mots par phrase, beaucoup de phrases sans verbe |
| **La voix lit le HUD** | « Suspicion, 35%. » « Suspicion just jumped to 52%. » « Every mistake moves the needle. » | « Soupçon : douze pour cent. » à chaque hausse |
| **Problèmes / options / règles numérotés** | « Option one, bury it. » « Rule two, never keep it all in one place. » | « Problème numéro un… », « Règle numéro un… » |
| **Formules fixes pour les faits réels** | « Here's the thing about cash. » « Here's what you don't know. » « And this is a real job. » | « Voilà le truc avec le liquide. » « Ce que tu ne sais pas… » |
| **Répliques des personnages, courtes, en situation** | « I saw what's in the bag, I need 50K. » « Morning, Dre. Nice eyebrow. Where's your chain? » | SMS et dialogues lus comme des répliques, pas racontés |
| **Formule de rappel de la mécanique** | « Every night, the comments decide what you do. » | « Chaque soir, les commentaires décident de ce que tu fais. » |
| **Fin = enjeu + vote + boucle ouverte APRÈS le vote** | « Every choice you make can get you caught or set you free. Comment, pay or move. » puis « There's a third way out. It's cold, it's cruel… » | ajouter une dernière phrase-mystère après « La majorité écrit la partie X. » |
| **Durée** | 92–108 s (147 s pour le 6) ; ~2,6 mots/s | 85–100 s |
