"""Répond aux commentaires d'un épisode (vote compté, ton de la série) et like les votes sur TikTok.

  python3 engage.py P1 [--max 12] [--dry]

Garde-fous : jamais deux réponses au même commentaire (ids gardés dans MEMOIRE.json), plafond par passage,
pas de réponse aux commentaires insultants ou hors sujet, messages variés (pas de copier-coller visible).
"""
import json, os, random, re, sys, unicodedata
import requests
from upload_post import BASE, H, comments, user

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MEM = os.path.join(ROOT, "MEMOIRE.json")
BLOCK = re.compile(r"(connard|pute|salope|encul|nique|ntm|fdp|merde|arnaque|bot\b|spam|http)", re.I)

REPONSES = [
    "Vote compté : {mot}. Résultat demain 21h 🗳️",
    "{mot}, noté. La majorité décide demain à 21h.",
    "Ton vote pèse : {mot}. On voit demain si tu as gagné.",
    "{mot} ? Courageux. Réponse demain 21h.",
    "Noté pour {mot}. Le compteur tourne… 🗳️",
    "{mot}. Retiens bien ce choix, il aura des conséquences.",
]
REPONSES_SANS_VOTE = [
    "Commente {a} ou {b} pour que ton vote compte 🗳️",
    "Un seul mot pour voter : {a} ou {b}. La majorité écrit la suite.",
]


def norm(s):
    s = unicodedata.normalize("NFD", s.upper())
    return "".join(c for c in s if unicodedata.category(c) != "Mn")


def reply(platform, post, comment_id, message):
    body = {"platform": platform, "user": user(), "comment_id": comment_id, "message": message}
    if platform in ("tiktok", "youtube"):
        body["post_id"] = post
    return requests.post(f"{BASE}/uploadposts/comments/create", headers={**H(), "Content-Type": "application/json"},
                         json=body, timeout=60).json()


def like(platform, post, comment_id):
    if platform != "tiktok":
        return None
    body = {"platform": platform, "user": user(), "comment_id": comment_id, "action": "like", "post_id": post}
    return requests.post(f"{BASE}/uploadposts/comments/action", headers={**H(), "Content-Type": "application/json"},
                         json=body, timeout=60).json()


def main(ep_id, max_replies=12, dry=False):
    mem = json.load(open(MEM))
    ep = next(e for e in mem["episodes"] if e["id"] == ep_id)
    a, b = ep["vote"]
    done = set(ep.setdefault("repondus", []))
    sent = 0
    for platform, post in ep.get("posts", {}).items():
        try:
            cs = comments(platform, post)
        except Exception as e:
            print(f"[{platform}] commentaires indisponibles : {e}")
            continue
        random.shuffle(cs)
        for c in cs:
            cid, text = c.get("id"), c.get("text", "")
            if not cid or cid in done or sent >= max_replies or BLOCK.search(text):
                continue
            words = re.findall(r"[A-Z']+", norm(text))
            mot = next((o for o in (a, b) if norm(o).replace("'", "") in [w.replace("'", "") for w in words]), None)
            if mot:
                msg = random.choice(REPONSES).format(mot=mot)
            elif len(text) > 8 and random.random() < 0.3:
                msg = random.choice(REPONSES_SANS_VOTE).format(a=a, b=b)
            else:
                continue
            print(f"[{platform}] @{(c.get('user') or {}).get('username')}: {text[:60]!r} → {msg}")
            if not dry:
                r = reply(platform, post, cid, msg)
                if mot:
                    like(platform, post, cid)
                if not r.get("success", True):
                    print("   échec :", r)
                    continue
            done.add(cid)
            sent += 1
    ep["repondus"] = sorted(done)
    if not dry:
        json.dump(mem, open(MEM, "w"), ensure_ascii=False, indent=1)
    print(f"{sent} réponse(s) envoyée(s)")


if __name__ == "__main__":
    args = sys.argv[1:]
    mx = int(args[args.index("--max") + 1]) if "--max" in args else 12
    main(args[0], mx, "--dry" in args)
