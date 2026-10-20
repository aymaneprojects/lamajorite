"""Légende, hashtags, premier commentaire et titre YouTube d'un épisode → out/PX_meta.json"""
import json, os, sys
from story_data import EPISODES

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TAGS = ["histoire", "serie", "tudecides", "storytime", "thriller", "marseille", "argent", "lamajorite"]


def main(ep_id):
    ep = next(e for e in EPISODES if e["id"] == ep_id)
    n = int(ep_id[1:])
    a, b = ep["vote"]
    title = ep["title"].split("—")[-1].strip()
    caption = (f"Partie {n} · 9,8 MILLIONS — {title}. Commente {a} ou {b}, un seul mot. "
               f"La majorité écrit la partie {n + 1}. " + " ".join("#" + t for t in TAGS))
    meta = {
        "external_id": f"9m8-{ep_id}",
        "caption": caption,
        "first_comment": f"🗳️ VOTE : {a} ou {b} ? Un seul mot. La majorité écrit la Partie {n + 1} demain 19h.",
        "youtube_title": f"9,8 MILLIONS · Partie {n} — {title} (tu décides) #shorts",
        "youtube_description": f"Une histoire. Tu votes en commentaire. La majorité écrit la suite.\nVote : {a} ou {b}.\n"
                               f"Fiction. Images et voix générées par IA.\n#shorts #histoire #serie",
        "tags": TAGS,
        "cover": f"out/{ep_id}_cover.png",  # relatif à la racine du dépôt
    }
    out = os.path.join(ROOT, "out", f"{ep_id}_meta.json")
    json.dump(meta, open(out, "w"), ensure_ascii=False, indent=1)
    print(json.dumps(meta, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main(sys.argv[1])
