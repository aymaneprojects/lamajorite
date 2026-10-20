"""Compte les votes d'un épisode sur toutes les plateformes et met à jour la mémoire.

  python3 votes.py P1   (lit MEMOIRE.json → posts de P1 → commentaires → résultat)
"""
import collections, json, os, re, sys, unicodedata
from upload_post import comments

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MEM = os.path.join(ROOT, "MEMOIRE.json")


def norm(s):
    s = unicodedata.normalize("NFD", s.upper())
    return "".join(c for c in s if unicodedata.category(c) != "Mn")


def count(options, all_comments):
    """1 vote par personne (son dernier commentaire qui contient une option)."""
    opts = {norm(o).replace("'", ""): o for o in options}
    by_user = {}
    for c in all_comments:
        words = re.findall(r"[A-Z0-9']+", norm(c.get("text", "")).replace("'", ""))
        hits = [opts[w] for w in words if w in opts]
        # « L'EMMENER » → EMMENER : accepte aussi le dernier mot d'une option composée
        for o_n, o in opts.items():
            if " " in o_n or len(o_n.split()) > 1:
                if all(p in words for p in o_n.split()):
                    hits.append(o)
        if hits:
            by_user[(c.get("platform"), (c.get("user") or {}).get("username"))] = hits[-1]
    return collections.Counter(by_user.values())


def main(ep_id):
    mem = json.load(open(MEM))
    ep = next(e for e in mem["episodes"] if e["id"] == ep_id)
    allc = []
    for platform, post in ep.get("posts", {}).items():
        try:
            cs = comments(platform, post)
        except Exception as e:  # une plateforme en panne ne bloque pas le vote
            print(f"[{platform}] commentaires indisponibles : {e}")
            continue
        for c in cs:
            c["platform"] = platform
        allc += cs
    res = count(ep["vote"], allc)
    total = sum(res.values())
    winner = res.most_common(1)[0][0] if res else None
    handles = sorted({"@" + c["user"]["username"] for c in allc if (c.get("user") or {}).get("username")})
    ep["result"] = {"counts": dict(res), "total_votes": total, "winner": winner, "comments": len(allc)}
    ep["persons_of_interest"] = handles[:24]
    ep["comment_samples"] = [{"user": (c.get("user") or {}).get("username"), "text": c.get("text"), "platform": c["platform"]}
                             for c in allc if len(c.get("text", "")) > 12][:40]
    json.dump(mem, open(MEM, "w"), ensure_ascii=False, indent=1)
    print(json.dumps(ep["result"], ensure_ascii=False))


if __name__ == "__main__":
    main(sys.argv[1])
