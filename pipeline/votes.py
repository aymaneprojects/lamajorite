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


def auteur(c):
    """Pseudo de l'auteur, quel que soit le format de la plateforme (Instagram : user.username, TikTok : display_name,
    YouTube : author)."""
    return ((c.get("user") or {}).get("username") or c.get("username") or c.get("author") or c.get("display_name")
            or c.get("id") or c.get("comment_id") or "").lstrip("@")


def est_a_nous(c, mem):
    """Nos propres commentaires (rappel du vote, réponses) ne comptent ni comme votes ni comme commentaires du public."""
    mine = {h.lstrip("@").lower() for h in mem["chaine"].get("comptes", {}).values()}
    return bool(c.get("owner")) or auteur(c).lower() in mine


def count(options, all_comments):
    """1 vote par personne (son dernier commentaire qui contient une option)."""
    opts = {norm(o).replace("'", ""): o for o in options}
    by_user = {}
    for c in all_comments:
        words = re.findall(r"[A-Z0-9']+", norm(c.get("text", "")).replace("'", ""))
        # « Paye » pour PAYER, « Refuse » pour REFUSER : début du mot, au plus 2 lettres en moins
        hits = [o for w in words for o_n, o in opts.items()
                if w == o_n or (len(w) >= 4 and o_n.startswith(w) and len(o_n) - len(w) <= 2)]
        # « L'EMMENER » → EMMENER : accepte aussi le dernier mot d'une option composée
        for o_n, o in opts.items():
            if " " in o_n or len(o_n.split()) > 1:
                if all(p in words for p in o_n.split()):
                    hits.append(o)
        if hits:
            by_user[(c.get("platform"), auteur(c))] = hits[-1]
    return collections.Counter(by_user.values())


def fetch(ep):
    """Commentaires de toutes les plateformes d'un épisode (une plateforme en panne ne bloque pas)."""
    allc, ok = [], False
    for platform, post in ep.get("posts", {}).items():
        try:
            cs = comments(platform, post)
        except Exception as e:
            print(f"[{platform}] commentaires indisponibles : {e}")
            continue
        ok = True
        for c in cs:
            c["platform"] = platform
        allc += cs
    return allc if ok or not ep.get("posts") else None


def main(ep_id):
    mem = json.load(open(MEM))
    ep = next(e for e in mem["episodes"] if e["id"] == ep_id)
    allc = fetch(ep)
    if allc is None:  # aucune plateforme lisible : on garde le dernier résultat connu plutôt que de l'effacer
        sys.exit("Commentaires illisibles sur toutes les plateformes : résultat précédent conservé.")
    allc = [c for c in allc if not est_a_nous(c, mem)]
    res = count(ep["vote"], allc)
    total = sum(res.values())
    winner = res.most_common(1)[0][0] if res else None
    handles = sorted({"@" + c["user"]["username"] for c in allc if (c.get("user") or {}).get("username")})
    ep["result"] = {"counts": dict(res), "total_votes": total, "winner": winner, "comments": len(allc)}
    ep["persons_of_interest"] = handles[:24]
    ep["comment_samples"] = [{"user": auteur(c), "text": c.get("text"), "platform": c["platform"]}
                             for c in allc if len(c.get("text", "")) > 12][:40]
    json.dump(mem, open(MEM, "w"), ensure_ascii=False, indent=1)
    print(json.dumps(ep["result"], ensure_ascii=False))


if __name__ == "__main__":
    main(sys.argv[1])
