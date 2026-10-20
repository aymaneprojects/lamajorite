# Habillage de chaque épisode, par index de beat dans story_data.EPISODES[i]["beats"].
# hud      : nouvelles valeurs du HUD à partir de ce beat (cash, bank, susp)
# overlay  : texte par-dessus l'image (hook / étiquette)
# card     : carte plein écran (stat, fact, rule, vote) ou sms (par-dessus l'image précédente)
# *texte*  : mot(s) en rose
SPECS = {
    "P1": {
        "pause_after": ["Bercy"],  # silence ajouté après ce mot (enchaînement trop rapide dans la voix)
        "beats": {
            0: {"overlay": {"type": "hook", "big": "9 840 000 €", "accent": "PERSONNE NE SAIT."}},
            4: {"overlay": {"type": "tag", "text": "BOX 117 · *MARSEILLE*"}},
            12: {"hud": {"cash": 9840000, "bank": 0, "susp": 0},
                 "card": {"type": "stat", "kicker": "BOX 117 · INVENTAIRE", "label": "Total", "value": "9 840 000 €", "sub": "en billets de 50 et 100"}},
            14: {"card": {"type": "stat", "kicker": "MARCEL · CHAUFFEUR DE TAXI", "label": "Le plus qu'il ait jamais gagné", "value": "2 000 €/mois", "sub": "pendant 30 ans"}},
            16: {"hud": {"susp": 8}, "overlay": {"type": "tag", "text": "QUELQU'UN *SAIT*"}},
            19: {"card": {"type": "stat", "kicker": "TOI · LIVREUR", "label": "Pour gagner ce qu'il y a dans les sacs", "value": "*500 ANS*", "sub": "de ton salaire"}},
            23: {"card": {"type": "fact", "kicker": "CE QUE TU NE SAIS PAS", "text": "En France, tu ne peux pas payer plus de *1 000 €* en liquide à un commerçant.", "source": "Code monétaire et financier · art. D112-3"}},
            24: {"overlay": {"type": "tag", "text": "*REFUSÉ*"}},
            25: {"hud": {"susp": 12}, "card": {"type": "fact", "kicker": "CE QUE TU NE SAIS PAS", "text": "Dépôt d'espèces de plus de 10 000 € sur un mois", "arrow": True, "text2": "ta banque prévient *Tracfin*", "stamp": "AUTOMATIQUE", "source": "Code monétaire et financier · art. L561-15-1"}},
            26: {"overlay": {"type": "tag", "text": "TRACFIN · *BERCY*"}},
            32: {"hud": {"susp": 25}, "card": {"type": "sms", "from": "NUMÉRO INCONNU · 04:12", "msgs": ["Box 117.", "Tu as fini de compter ?"]}},
            33: {"hud": {"susp": 31}},
            37: {"card": {"type": "vote", "left": {"img": "P1_30", "word": "GARDER", "sub": "et tu joues"},
                          "right": {"img": "P1_31", "word": "POLICE", "sub": "et tu rends tout"},
                          "footer": "La majorité écrit la *Partie 2*."}},
        },
    },
}

# Corrections des mots mal transcrits par Whisper (affichage des sous-titres)
# paires de mots mal découpées par Whisper
CAPTION_PAIR_FIXES = {("track", "fin"): "Tracfin", ("traque", "fin"): "Tracfin"}

CAPTION_FIXES = {
    "traquefins": "Tracfin", "traquefin": "Tracfin", "échauffeur": "chauffeur", "serré,": "serrés,",
}

# Specs des épisodes écrits en JSON (episodes/PX.json → clé "specs", index de beats en chaînes)
from story_data import EPISODES as _EPS
for _e in _EPS:
    if "specs" in _e:
        SPECS[_e["id"]] = {**_e["specs"], "beats": {int(k): v for k, v in _e["specs"].get("beats", {}).items()}}
