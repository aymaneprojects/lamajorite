"""Client Upload-Post : publication TikTok / Instagram / YouTube et lecture des commentaires.

Clé lue dans l'environnement : UPLOAD_POST_API_KEY (ou UPLOADPOST_API / UPLOADPOST_API_KEY).
Profil : UPLOAD_POST_USER (défaut « lamajorite »).

  python3 upload_post.py me
  python3 upload_post.py publish out/P1.mp4 meta.json [--private]
  python3 upload_post.py status <request_id>
  python3 upload_post.py comments <platform> <post_id|post_url>
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
    return os.environ.get("UPLOAD_POST_USER") or os.environ.get("UPLOADPOST_USER") or "lamajorite"


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
            ("is_aigc", "true"), ("is_ai_generated", "true"), ("containsSyntheticMedia", "true"),
            ("privacy_level", "SELF_ONLY" if private else "PUBLIC_TO_EVERYONE"),
            ("privacyStatus", "private" if private else "public"),
            ("defaultLanguage", "fr"), ("defaultAudioLanguage", "fr"), ("categoryId", "24"),
            ("external_id", meta["external_id"]), ("request_id", meta["external_id"] + "-" + uuid.uuid4().hex[:6]),
            ("async_upload", "true")]
    data += [("platform[]", p) for p in meta.get("platforms", PLATFORMS)]
    data += [("tags[]", t) for t in meta.get("tags", [])]
    files = {"video": (os.path.basename(video), open(video, "rb"), "video/mp4")}
    cover = meta.get("cover")
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


def comments(platform, post, limit=100):
    """Tous les commentaires d'un post (pagination incluse)."""
    params = {"user": user(), "platform": platform, "limit": limit}
    params["post_url" if post.startswith("http") else "post_id"] = post
    out = []
    while True:
        r = requests.get(f"{BASE}/uploadposts/comments", headers=H(), params=params, timeout=60).json()
        out += r.get("comments", [])
        pg = r.get("pagination") or {}
        if not pg.get("has_next"):
            return out
        params["after"] = pg["next_cursor"]


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "me":
        print(json.dumps(me(), indent=1, ensure_ascii=False))
        print(json.dumps(profiles(), indent=1, ensure_ascii=False))
    elif cmd == "publish":
        print(json.dumps(publish(sys.argv[2], json.load(open(sys.argv[3])), "--private" in sys.argv), indent=1, ensure_ascii=False))
    elif cmd == "status":
        print(json.dumps(status(sys.argv[2]), indent=1, ensure_ascii=False))
    elif cmd == "comments":
        print(json.dumps(comments(sys.argv[2], sys.argv[3]), indent=1, ensure_ascii=False))
