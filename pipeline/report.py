"""Bilan des épisodes publiés : vues, likes, commentaires par plateforme (Upload-Post post-analytics).

  python3 report.py   → tableau + out/rapport.json
"""
import json, os
import requests
from upload_post import BASE, H

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def main():
    mem = json.load(open(os.path.join(ROOT, "MEMOIRE.json")))
    rows = []
    for ep in mem["episodes"]:
        rid = ep.get("request_id")
        if not rid:
            continue
        r = requests.get(f"{BASE}/uploadposts/post-analytics/{rid}", headers=H(), timeout=60).json()
        rows.append({"episode": ep["id"], "publie_le": ep.get("publie_le"), "analytics": r})
        print(ep["id"], json.dumps(r, ensure_ascii=False)[:400])
    json.dump(rows, open(os.path.join(ROOT, "out", "rapport.json"), "w"), ensure_ascii=False, indent=1)


if __name__ == "__main__":
    main()
