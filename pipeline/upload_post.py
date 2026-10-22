"""Client Upload-Post : publication TikTok / Instagram / YouTube et lecture des commentaires.

Clé lue dans l'environnement : UPLOAD_POST_API_KEY (ou UPLOADPOST_API / UPLOADPOST_API_KEY).
Profil : UPLOAD_POST_USER (défaut « lamajorite »).

  python3 upload_post.py me
  python3 upload_post.py publish out/P1.mp4 meta.json [--private]
  python3 upload_post.py status <request_id>
  python3 upload_post.py comments <platform> <post_id|post_url>
  python3 upload_post.py record PX <request_id|job_id>   → range les id/URL des posts dans MEMOIRE.json
"""
import json, os, sys, uuid
import requests

BASE = "https://api.upload-post.com/api"
PLATFORMS = ["tiktok", "instagram", "youtube"]


def key():
    for k in ("UPLOAD_POST_API_KEY", "UPLOADPOST_API", "UPLOADPOST_API_KEY", "UPLOAD_POST_API"):
        if os.environ.get(k):
            return os.environ[k]
    sys.exit("Clé Upload-Post absente : ajoute UPLOAD_POST_API_KEY dans les réglages de l'environnement.")


def user():
    return os.environ.get("UPLOAD_POST_USER") or os.environ.get("UPLOADPOST_USER") or "affaires-classees"  # profil Upload-Post des comptes @lamajorite.serie


def H():
    return {"Authorization": f"Apikey {key()}"}


def me():
    r = requests.get(f"{BASE}/uploadposts/me", headers=H(), timeout=30)
    return r.status_code, r.json()


def profiles():
    r = requests.get(f"{BASE}/uploadposts/users", headers=H(), timeout=30)
    return r.json()


def publish(video, meta, private=False):
    """meta : {title, caption, first_comment, tags, external_id, youtube_title, youtube_description}"""
    data = [("user", user()), ("title", meta["caption"]),
            ("tiktok_title", meta["caption"]), ("instagram_title", meta["caption"]),
            ("youtube_title", meta["youtube_title"][:100]), ("youtube_description", meta["youtube_description"]),
            ("first_comment", meta["first_comment"]),
            # aucune mention « IA » (consigne du propriétaire, 21/10) : style dessin animé non réaliste,
            # que TikTok et YouTube n'obligent pas à étiqueter. Si un jour une image devient photoréaliste, le signaler.
            ("is_aigc", "false"), ("is_ai_generated", "false"), ("containsSyntheticMedia", "false"),
            ("privacy_level", "SELF_ONLY" if private else "PUBLIC_TO_EVERYONE"),
            ("privacyStatus", "private" if private else "public"),
            ("selfDeclaredMadeForKids", "false"),  # sinon YouTube peut couper la diffusion (style dessin animé)
            ("defaultLanguage", "fr"), ("defaultAudioLanguage", "fr"), ("categoryId", "24"),
            ("external_id", meta["external_id"]), ("request_id", meta["external_id"] + "-" + uuid.uuid4().hex[:6]),
            ("async_upload", "true")]
    data += [("platform[]", p) for p in meta.get("platforms", PLATFORMS)]
    # publication programmée à l'heure de Paris si elle est encore à venir (sinon : tout de suite)
    when = meta.get("schedule_paris")
    if when and not private:
        from datetime import datetime
        from zoneinfo import ZoneInfo
        now = datetime.now(ZoneInfo("Europe/Paris"))
        hh, mm = map(int, when.split(":"))
        target = now.replace(hour=hh, minute=mm, second=0, microsecond=0)
        if (target - now).total_seconds() > 120:
            data += [("scheduled_date", target.strftime("%Y-%m-%dT%H:%M:%S")), ("timezone", "Europe/Paris")]
            data = [d for d in data if d[0] != "async_upload"]
    data += [("tags[]", t) for t in meta.get("tags", [])]
    files = {"video": (os.path.basename(video), open(video, "rb"), "video/mp4")}
    cover = meta.get("cover")
    if cover and not os.path.isabs(cover):
        cover = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), cover)
    if cover and os.path.exists(cover):
        # même miniature partout : TikTok, Instagram (couverture du Reel), YouTube (chaîne vérifiée requise)
        for field in ("tiktok_cover_image", "cover_image", "thumbnail"):
            files[field] = (os.path.basename(cover), open(cover, "rb"), "image/png")
    r = requests.post(f"{BASE}/upload", headers={**H(), "Idempotency-Key": meta["external_id"]},
                      data=data, files=files, timeout=600)
    return r.status_code, r.json()


def status(request_id):
    r = requests.get(f"{BASE}/uploadposts/status", headers=H(), params={"request_id": request_id}, timeout=30)
    return r.json()


def status_job(job_id):
    r = requests.get(f"{BASE}/uploadposts/status", headers=H(), params={"job_id": job_id}, timeout=30)
    return r.json()


def record(ep_id, ident):
    """Lit le statut de la publication et range les id/URL des posts dans MEMOIRE.json (pour les votes et les réponses)."""
    import datetime
    st = status(ident)
    if not st.get("results") and not st.get("platforms"):
        st = status_job(ident)
    results = st.get("results") or {}
    if isinstance(results, list):
        results = {r.get("platform"): r for r in results}
    mem_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "MEMOIRE.json")
    mem = json.load(open(mem_path))
    ep = next(e for e in mem["episodes"] if e["id"] == ep_id)
    posts, urls = ep.setdefault("posts", {}), ep.setdefault("urls", {})
    for platform, r in results.items():
        pid = r.get("platform_post_id") or r.get("post_id") or r.get("publish_id") or r.get("container_id")
        if pid:
            posts[platform] = str(pid)
        if r.get("post_url") or r.get("url"):
            urls[platform] = r.get("post_url") or r["url"]
    ep["request_id"] = ident
    if posts and not ep.get("publie_le"):
        ep["publie_le"] = datetime.datetime.now().isoformat(timespec="minutes")
    json.dump(mem, open(mem_path, "w"), ensure_ascii=False, indent=1)
    return {"posts": posts, "urls": urls, "brut": st}


def comments(platform, post, limit=50):
    """Tous les commentaires d'un post (pagination incluse)."""
    params = {"user": user(), "platform": platform, "limit": limit}
    params["post_url" if post.startswith("http") else "post_id"] = post
    out = []
    while True:
        r = requests.get(f"{BASE}/uploadposts/comments", headers=H(), params=params, timeout=60).json()
        if r.get("success") is False:  # une erreur d'API ne doit pas passer pour « 0 commentaire »
            raise RuntimeError(r.get("error") or r.get("message") or r)
        out += r.get("comments", [])
        pg = r.get("pagination") or {}
        if not pg.get("has_next"):
            return out
        params["after"] = pg["next_cursor"]


def feu_vert(video, test=False):
    """Pas de publication publique sans : contrôle automatique OK (out/PX_qa.json) + feu vert du directeur qualité
    (out/PX_verdict.json, écrit par l'agent directeur-qa). --force : uniquement sur ordre explicite du propriétaire."""
    ep = os.path.basename(video).split(".")[0].split("_")[0]
    out = os.path.dirname(os.path.abspath(video))
    qa = json.load(open(os.path.join(out, f"{ep}_qa.json"))) if os.path.exists(os.path.join(out, f"{ep}_qa.json")) else None
    vd = json.load(open(os.path.join(out, f"{ep}_verdict.json"))) if os.path.exists(os.path.join(out, f"{ep}_verdict.json")) else None
    if test:
        return
    if not qa or not qa.get("ok"):
        sys.exit(f"Publication refusée : contrôle automatique non OK ({(qa or {}).get('bloquants', 'out/' + ep + '_qa.json absent')})")
    if not vd or not vd.get("publier"):
        sys.exit(f"Publication refusée : pas de feu vert du directeur qualité ({(vd or {}).get('raisons', 'out/' + ep + '_verdict.json absent')})")


def sans_ia(meta):
    """Consigne du propriétaire : jamais de mention de l'IA dans ce qui est publié."""
    import re
    txt = " ".join(str(meta.get(k, "")) for k in ("caption", "first_comment", "youtube_title", "youtube_description"))
    # « IA » / « AI » seulement en majuscules (sinon « j'ai » déclenche) ; le reste sans tenir compte de la casse
    m = re.search(r"\b(IA|AI)\b", txt) or re.search(r"intelligence artificielle|artificial intelligence|g[ée]n[ée]r[ée]e?s? par", txt, re.I)
    if m:
        sys.exit(f"Publication refusée : mention interdite « {m.group(0)} » dans la légende/description")


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "me":
        print(json.dumps(me(), indent=1, ensure_ascii=False))
        print(json.dumps(profiles(), indent=1, ensure_ascii=False))
    elif cmd == "publish":
        feu_vert(sys.argv[2], "--private" in sys.argv or "--force" in sys.argv)
        sans_ia(json.load(open(sys.argv[3])))
        print(json.dumps(publish(sys.argv[2], json.load(open(sys.argv[3])), "--private" in sys.argv), indent=1, ensure_ascii=False))
    elif cmd == "status":
        print(json.dumps(status(sys.argv[2]), indent=1, ensure_ascii=False))
    elif cmd == "record":
        print(json.dumps(record(sys.argv[2], sys.argv[3]), indent=1, ensure_ascii=False))
    elif cmd == "comments":
        print(json.dumps(comments(sys.argv[2], sys.argv[3]), indent=1, ensure_ascii=False))
