"""Emails au propriétaire (Resend) : je ne le dérange que quand j'ai besoin de lui, ou pour le récap du soir.

  python3 notify.py test
  python3 notify.py voix PY                → texte voix à générer (ElevenLabs, Nicolas Petit) → Drive voix/PY.mp3
  python3 notify.py images PY out/pack_images_PY-PZ.zip
  python3 notify.py a_supprimer PX         → liens TikTok/Instagram à supprimer avant 21h (out/PX_a_supprimer.txt)
  python3 notify.py bloque PX              → épisode refusé par le directeur qualité (out/PX_verdict.json)
  python3 notify.py alerte_accroche PX "accroche 1|accroche 2|accroche 3"
  python3 notify.py recap PX               → liens des posts du soir + commentaires
  python3 notify.py bilan                  → bilan de la semaine (out/rapport.json)

Clé : RESEND_API_KEY (ou RESEND). Expéditeur : RESEND_FROM (défaut onboarding@resend.dev : Resend n'envoie alors qu'à l'adresse
du compte Resend). Sans clé : l'email est écrit dans out/email_<type>_<ep>.txt (carte KANBAN à ajouter).
Anti-doublon : un même email (type + épisode) n'est envoyé qu'une fois par jour (MEMOIRE.json → emails).
"""
import base64, datetime, json, os, sys
import requests

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MEM = os.path.join(ROOT, "MEMOIRE.json")
DRIVE = "https://drive.google.com/drive/folders/1yL0YrWBo4h2scNWURoW5bmxDIULyeXin"
SIGNATURE = "\n\n— L'opérateur de La Majorité (automatique)"


def _out(*p):
    return os.path.join(ROOT, "out", *p)


def _read(path, default=""):
    return open(path).read() if os.path.exists(path) else default


def compose(kind, ep=None, extra=None):
    """→ (sujet, texte, [pièces jointes])"""
    if kind == "test":
        return "La Majorité · test d'email", "Si tu lis ceci, je peux t'écrire tout seul. Rien à faire.", []
    if kind == "voix":
        texte = _read(_out(f"{ep}_voix.txt"))
        return (f"[À faire avant 19h] Voix de la {ep}",
                f"Il me faut la voix de la {ep}.\n\n1. Colle le texte ci-dessous dans ElevenLabs, voix « Nicolas Petit ».\n"
                f"2. Dépose le MP3 dans le Drive, dossier « voix », nommé exactement {ep}.mp3 :\n{DRIVE}\n\n"
                f"Je le récupère tout seul à 19h05 (rattrapage à 20h20). Sans voix, l'épisode ne sort pas : "
                f"je ne publie jamais une voix robot.\n\n——— TEXTE ———\n{texte}", [])
    if kind == "images":
        z = extra
        return (f"[À faire] Images à générer ({os.path.basename(z)})",
                f"Il me manque des images. Les prompts sont dans le zip joint (un fichier = un nom d'image).\n"
                f"Génère-les et dépose-les dans le Drive (même nom de fichier) :\n{DRIVE}\n\n"
                f"En attendant, j'utilise l'image existante la plus proche.", [z])
    if kind == "a_supprimer":
        return (f"[À faire avant 21h] Supprimer la {ep} sur TikTok et Instagram",
                _read(_out(f"{ep}_a_supprimer.txt")) +
                "\nYouTube, je l'ai déjà supprimé. TikTok et Instagram ne permettent pas la suppression automatique : "
                "supprime ces 2 posts depuis l'appli. Je republie à 21h00 avec une nouvelle accroche.", [])
    if kind == "bloque":
        v = json.loads(_read(_out(f"{ep}_verdict.json"), "{}"))
        raisons = "\n".join(f"- {r}" for r in v.get("raisons", [])) or "(voir out/" + ep + "_qa.md)"
        return (f"[Bloqué] La {ep} ne sort pas ce soir",
                f"Le directeur qualité a refusé la {ep} après 2 corrections. Je ne publie pas.\n\nRaisons :\n{raisons}", [])
    if kind == "alerte_accroche":
        acc = "\n".join(f"{i}. {a}" for i, a in enumerate((extra or "").split("|"), 1) if a)
        return (f"[À choisir] {ep} : 3 relances sans assez de commentaires",
                f"La {ep} a été republiée 3 fois sans atteindre le minimum de commentaires. Je propose une nouvelle accroche :\n\n{acc}\n\n"
                f"Réponds avec le numéro choisi (ou écris la tienne). En attendant, je ne republie pas.", [])
    if kind == "recap":
        mem = json.load(open(MEM))
        e = next(x for x in mem["episodes"] if x["id"] == ep)
        liens = "\n".join(f"- {p} : {u}" for p, u in (e.get("urls") or {}).items()) or "- (liens pas encore disponibles)"
        c = (e.get("controle_commentaires") or {}).get("commentaires", "?")
        return (f"La Majorité · {ep} en ligne",
                f"{e.get('title', ep)} — publiée {e.get('publie_le', '')}.\n{liens}\n\nCommentaires du public : {c}. "
                f"Rien à faire de ton côté.", [])
    if kind == "bilan":
        return "La Majorité · bilan de la semaine", _read(_out("rapport.md"), _read(_out("rapport.json"), "(rapport absent)")), []
    raise SystemExit(f"type d'email inconnu : {kind}")


def send(kind, ep=None, extra=None, force=False):
    mem = json.load(open(MEM))
    to = mem["chaine"].get("email_proprietaire")
    today = datetime.date.today().isoformat()
    sent = mem.setdefault("emails", [])
    if not force and any(m["type"] == kind and m.get("ep") == ep and m["date"] == today for m in sent):
        return {"statut": "déjà envoyé aujourd'hui", "type": kind, "ep": ep}
    subject, body, files = compose(kind, ep, extra)
    body += SIGNATURE
    key = os.environ.get("RESEND_API_KEY") or os.environ.get("RESEND")
    if not key:
        path = _out(f"email_{kind}_{ep or today}.txt")
        os.makedirs(os.path.dirname(path), exist_ok=True)
        open(path, "w").write(f"À : {to}\nSujet : {subject}\n\n{body}\n" + "".join(f"\nPièce jointe : {f}" for f in files))
        return {"statut": "pas de RESEND_API_KEY : email écrit dans un fichier", "fichier": path}
    payload = {"from": os.environ.get("RESEND_FROM", "La Majorité <onboarding@resend.dev>"), "to": [to],
               "subject": subject, "text": body}
    if files:
        payload["attachments"] = [{"filename": os.path.basename(f), "content": base64.b64encode(open(f, "rb").read()).decode()}
                                  for f in files if os.path.exists(f)]
    r = requests.post("https://api.resend.com/emails", headers={"Authorization": f"Bearer {key}"}, json=payload, timeout=60)
    ok = r.status_code in (200, 201)
    if ok:
        sent.append({"type": kind, "ep": ep, "date": today, "sujet": subject, "id": r.json().get("id")})
        json.dump(mem, open(MEM, "w"), ensure_ascii=False, indent=1)
    return {"statut": "envoyé" if ok else "échec", "http": r.status_code, "reponse": r.text[:300], "sujet": subject}


if __name__ == "__main__":
    a = sys.argv[1:]
    kind = a[0]
    ep = a[1] if len(a) > 1 and kind not in ("test", "bilan") else None
    extra = a[2] if len(a) > 2 else None
    print(json.dumps(send(kind, ep, extra, force="--force" in a or kind == "test"), ensure_ascii=False, indent=1))
