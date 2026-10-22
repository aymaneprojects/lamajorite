# Croissance — La Majorité

Objectif du propriétaire : le plus d'abonnés, de vues et de commentaires possible. Méthode : mesurer chaque jour,
trouver CE qui bloque, changer **une seule chose à la fois**, juger après 48 h, garder ce qui marche.
Tenu par l'agent `analyste` (`.claude/agents/analyste.md`) ; appliqué par le `scenariste` et le producteur.

## Indicateurs (dans l'ordre de l'entonnoir)
| Étape | Indicateur | Où | Cible |
|---|---|---|---|
| 1. Être montré | vues par épisode, par plateforme | report.py | × 2 chaque semaine |
| 2. Accrocher | temps moyen regardé (TikTok) | report.py | > 35 s |
| 3. Aller au bout | % de vidéos vues en entier | report.py | > 15 % |
| 4. Voter | commentaires du public / 1 000 vues | relance.py / votes.py | > 10 |
| 5. Revenir | abonnés gagnés par épisode, partages, enregistrements | report.py | en hausse |

Le **goulot** = la première étape sous sa cible. On ne travaille que sur lui.

## Diagnostic du 22/10 (P1 + P2, 1 846 vues)
- Être montré : correct pour un compte neuf (TikTok ~650, Instagram 146→358). YouTube bloqué (1 vue) → vérifier « conçue pour les
  enfants » dans YouTube Studio (propriétaire) ; `selfDeclaredMadeForKids=false` envoyé désormais.
- **Accrocher : 16–18 s regardées sur 85 s (≈ 20 %) → GOULOT.** 2–3 % vont au bout, donc presque personne ne voit le vote.
- Voter : ~3 commentaires du public / 1 000 vues. Conséquence du goulot (le vote n'est qu'à la fin).

## Règles de format (recherche du 22/10, sources dans JOURNAL.md)
1. **0–3 s : un problème immédiat et chiffré**, texte à l'écran = voix, image lisible sans le son. Pas de retour en arrière
   avant 20 s (la P1 partait dans le passé dès 5 s).
2. **Annoncer le vote dès 0–5 s** (« Ce soir, c'est toi qui décides : PAYER ou REFUSER »), le rappeler au milieu, écran de vote à la fin.
3. **Durée 62–75 s** (~170–200 mots). Un problème numéroté toutes les 10–12 s, relances explicites vers 15 s et 30 s
   (« Et ce n'est pas le pire… »). Image qui change toutes les 3–5 s.
4. **Fin qui boucle** : la dernière phrase relance la première image (re-visionnages).
5. **Dilemme vraiment clivant** (argent contre famille, morale contre sécurité), avec le prix de chaque option.
6. **Communauté** : afficher 2–3 vrais @ de commentateurs dans l'épisode ; légende « Ton pseudo peut apparaître dans la Partie N » ;
   répondre à chaque commentaire dans la 1re heure.
7. **Partage** (signal n°1 d'Instagram) : une phrase « Envoie ça à celui qui choisirait l'autre option ».
8. Légende : le dilemme d'abord, puis le résultat du vote, puis « La majorité écrit la Partie N · ce soir 21h ».

Idées en réserve (une à la fois, après le goulot actuel) : 20h00 sur TikTok au lieu de 21h00 ; 1–2 vidéos de plus par jour
(extrait-accroche, « résultat du vote », réponse vidéo au meilleur commentaire) ; miniature « PARTIE N · 50 000 € ? » ;
compte du cousin @rayan.vote.

## Consigne du jour (écrite par l'analyste, lue par le scénariste)
- Expérience active : **E1 — accroche + vote dès le début + 62–75 s** (règles 1 à 4) à partir de la P3.

## Journal des expériences
| # | Début | Changement (une seule variable) | Hypothèse | Mesure à 48 h | Verdict |
|---|---|---|---|---|---|
| E1 | P3 | Règles 1–4 (accroche problème immédiat, vote annoncé à 0–5 s, 62–75 s, fin en boucle) | temps moyen regardé > 30 s, % vus en entier × 3 | | |
