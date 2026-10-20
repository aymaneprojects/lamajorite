"""Légende, hashtags, premier commentaire et titre YouTube d'un épisode → out/PX_meta.json"""
import json, os, sys
from story_data import EPISODES

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TAGS = ["ChaqueBilletLaisseUneTrace", "lamajorite", "serie", "histoire", "tudecides"]


def music_credit(ep_id):
    """Crédit exigé par la licence (CC BY 4.0) de la musique de l'épisode."""
    tl_path = os.path.join(ROOT, "render", "public", ep_id, "timeline.json")
    if not os.path.exists(tl_path):
        return None
    music = json.load(open(tl_path)).get("music", "")
    cat = json.load(open(os.path.join(ROOT, "render", "public", "music", "catalog.json")))
    key = os.path.splitext(os.path.basename(music))[0]
    piste = cat["pistes"].get(key, {})
    if not piste.get("titre"):
        return None
    return f"Musique : « {piste['titre']} » {piste['auteur']} ({piste['site']}), licence {piste['licence']}."


def main(ep_id, result=None):
    """result : « 61 % d'entre vous ont dit GARDER » (résultat du vote précédent), facultatif."""
    ep = next(e for e in EPISODES if e["id"] == ep_id)
    n = int(ep_id[1:])
    a, b = ep["vote"]
    title = ep["title"].split("—")[-1].strip()
    # modèle de légende tiré du rapport Saveo : accueil, résultat du vote, vote, abonnement, 1 hashtag de série
    lines = [f"Partie {n} · {title}."]
    if n > 1:
        lines.append("Nouveau ? Commence par la Partie 1 (épinglée).")
    if result:
        lines.append(result + ".")
    lines.append(f"Tu choisis quoi ? Commente {a} ou {b}. La majorité écrit la partie {n + 1}.")
    lines.append(f"Abonne-toi pour ne pas rater la partie {n + 1}, demain 19h.")
    lines.append("#ChaqueBilletLaisseUneTrace #lamajorite #serie #histoire")
    credit = music_credit(ep_id)
    if credit:
        lines.append(credit)
    caption = " ".join(lines)  # TikTok ignore les retours à la ligne
    meta = {
        "external_id": f"9m8-{ep_id}",
        "caption": caption,
        "first_comment": f"🗳️ VOTE : {a} ou {b} ? Un seul mot. La majorité écrit la Partie {n + 1} demain 19h.",
        "youtube_title": f"9,8 MILLIONS · Partie {n} — {title} (c'est toi qui décides) #shorts",
        "youtube_description": f"Une histoire. Tu votes en commentaire. La majorité écrit la suite.\nVote : {a} ou {b}.\n"
                               f"Nouvel épisode chaque jour à 19h. Fiction. Images et voix générées par IA.\n{credit or ''}\n#shorts #ChaqueBilletLaisseUneTrace",
        "tags": TAGS,
        "cover": f"out/{ep_id}_cover.png",  # relatif à la racine du dépôt
        "schedule_paris": "19:00",
    }
    out = os.path.join(ROOT, "out", f"{ep_id}_meta.json")
    json.dump(meta, open(out, "w"), ensure_ascii=False, indent=1)
    print(json.dumps(meta, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else None)
