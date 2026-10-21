"""Règle du seuil de commentaires (SEUIL) : un épisode qui n'en a pas assez est supprimé et republié.

  python3 relance.py PX              → décision (attendre / continuer / relancer / alerte), écrite dans MEMOIRE.json
  python3 relance.py PX --executer   → archive la tentative, supprime YouTube (API), liste TikTok/Instagram à supprimer
                                       par le propriétaire (out/PX_a_supprimer.txt), nouvelle légende → out/PX_meta.json

Délai : contrôle au passage de 19h05 le lendemain (~22 h après une publication de 21h00), car l'essentiel des
commentaires d'une vidéo courte arrive dans les 24 premières heures. TikTok et Instagram n'ont pas d'API de
suppression (doc Upload-Post) : c'est le propriétaire qui les supprime.
"""
import datetime, json, os, sys
from zoneinfo import ZoneInfo
import requests
from upload_post import BASE, H, user
from votes import fetch

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MEM = os.path.join(ROOT, "MEMOIRE.json")
SEUIL = 2           # commentaires du public, toutes plateformes (propriétaire, 21/10 : 2 suffisent pour avancer)
DELAI_H = 22        # âge minimal du post avant de juger
MAX_RELANCES = 3    # au-delà : le propriétaire décide (nouvelle accroche / miniature)
PARIS = ZoneInfo("Europe/Paris")
# accroches de légende pour les republications (la vidéo, validée, ne change pas)
ACCROCHES = ["Tu trouves 9 840 000 € dans un box. Personne ne sait. Tu fais quoi ?",
             "Ton grand-oncle te laisse une clé. Derrière : 9 840 000 € en liquide.",
             "Un seul mot en commentaire décide de la suite. GARDER ou POLICE ?"]


def own_handles(mem):
    return {h.lstrip("@").lower() for h in mem["chaine"].get("comptes", {}).values()}


def public_comments(ep, mem):
    mine = own_handles(mem)
    return [c for c in fetch(ep) if ((c.get("user") or {}).get("username") or "").lower() not in mine]


def decide(ep_id):
    mem = json.load(open(MEM))
    ep = next(e for e in mem["episodes"] if e["id"] == ep_id)
    if not ep.get("posts") or not ep.get("publie_le"):
        return {"decision": "attendre", "raison": "épisode pas encore publié"}
    pub = datetime.datetime.fromisoformat(ep["publie_le"])
    pub = pub if pub.tzinfo else pub.replace(tzinfo=PARIS)
    age = (datetime.datetime.now(PARIS) - pub).total_seconds() / 3600
    n = len(public_comments(ep, mem))
    tent = len(ep.get("tentatives", []))
    if n >= SEUIL:
        d = "continuer"
    elif age < DELAI_H:
        d = "attendre"
    elif tent >= MAX_RELANCES:
        d = "alerte"
    else:
        d = "relancer"
    res = {"decision": d, "commentaires": n, "seuil": SEUIL, "age_h": round(age, 1), "relances_faites": tent,
           "le": datetime.datetime.now(PARIS).isoformat(timespec="minutes")}
    ep["controle_commentaires"] = res
    json.dump(mem, open(MEM, "w"), ensure_ascii=False, indent=1)
    return res


def unpublish(platform, post_id):
    r = requests.post(f"{BASE}/uploadposts/posts/unpublish", headers=H(), timeout=60,
                      json={"platform": platform, "user": user(), "post_id": post_id})
    return r.status_code, r.text[:200]


def executer(ep_id):
    mem = json.load(open(MEM))
    ep = next(e for e in mem["episodes"] if e["id"] == ep_id)
    k = len(ep.get("tentatives", [])) + 1
    a_supprimer, supprimes = [], {}
    for platform, pid in ep.get("posts", {}).items():
        if platform == "youtube":
            supprimes[platform] = unpublish(platform, pid)
        else:  # TikTok / Instagram : pas d'API de suppression
            a_supprimer.append(f"{platform} : {ep.get('urls', {}).get(platform, pid)}")
    ep.setdefault("tentatives", []).append({"n": k, "posts": ep.get("posts"), "urls": ep.get("urls"),
                                            "publie_le": ep.get("publie_le"), "controle": ep.get("controle_commentaires"),
                                            "youtube_supprime": supprimes.get("youtube"), "a_supprimer_proprietaire": a_supprimer})
    for f in ("posts", "urls", "publie_le", "job_id", "request_id"):
        ep.pop(f, None)
    ep["statut"] = f"relance_{k}_programmee"
    json.dump(mem, open(MEM, "w"), ensure_ascii=False, indent=1)
    txt = os.path.join(ROOT, "out", f"{ep_id}_a_supprimer.txt")
    os.makedirs(os.path.dirname(txt), exist_ok=True)
    open(txt, "w").write(f"{ep_id} : moins de {SEUIL} commentaires → republication ce soir 21h00 (tentative {k + 1}).\n"
                         "À supprimer avant 21h00 (pas d'API pour ces plateformes) :\n" + "\n".join(a_supprimer) + "\n")
    # nouvelle légende (accroche différente) + identifiant neuf : sinon Upload-Post refuse le doublon
    mp = os.path.join(ROOT, "out", f"{ep_id}_meta.json")
    meta = json.load(open(mp))
    base = meta.get("caption_base") or meta["caption"]
    meta.update({"caption_base": base, "caption": ACCROCHES[(k - 1) % len(ACCROCHES)] + " " + base,
                 "external_id": f"9m8-{ep_id}-r{k}", "schedule_paris": "21:00"})
    json.dump(meta, open(mp, "w"), ensure_ascii=False, indent=1)
    from notify import send
    mail = send("a_supprimer", ep_id) if a_supprimer else None
    return {"tentative": k + 1, "youtube": supprimes.get("youtube"), "email": mail, "proprietaire_doit_supprimer": a_supprimer,
            "fichier": txt, "nouvelle_legende": meta["caption"][:120]}


if __name__ == "__main__":
    ep_id = sys.argv[1]
    out = executer(ep_id) if "--executer" in sys.argv else decide(ep_id)
    print(json.dumps(out, ensure_ascii=False, indent=1))
