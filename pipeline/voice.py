"""Voix off d'un épisode : ElevenLabs (voix de la série), secours edge-tts si crédits épuisés / clé absente.
Puis horodatage mot à mot (faster-whisper).

  python3 voice.py P6            → audio/P6.mp3 + audio/P6_words.json
"""
import asyncio, json, os, subprocess, sys
import numpy as np, requests
from story_data import EPISODES

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
AUDIO = os.path.join(ROOT, "audio")
VOICE_ID = os.environ.get("ELEVENLABS_VOICE_ID", "")
FALLBACK_VOICE = "fr-FR-HenriNeural"


def script(ep_id):
    ep = next(e for e in EPISODES if e["id"] == ep_id)
    return "\n\n".join(b[2] if b[0] == "img" else b[1] for b in ep["beats"])


def elevenlabs(text, out):
    key = os.environ.get("ELEVENLABS_API_KEY")
    if not key or not VOICE_ID:
        return "pas de clé ElevenLabs / ELEVENLABS_VOICE_ID"
    r = requests.post(f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}",
                      headers={"xi-api-key": key}, timeout=300,
                      json={"text": text, "model_id": os.environ.get("ELEVENLABS_MODEL", "eleven_multilingual_v2"),
                            "voice_settings": {"stability": 0.5, "similarity_boost": 0.75, "style": 0.15}})
    if r.status_code != 200:
        return f"ElevenLabs {r.status_code}: {r.text[:200]}"
    open(out, "wb").write(r.content)


def edge(text, out):
    import edge_tts
    asyncio.run(edge_tts.Communicate(text, FALLBACK_VOICE, rate="+4%").save(out))


def words(mp3, out_json):
    from faster_whisper import WhisperModel
    pcm = subprocess.run(["ffmpeg", "-v", "error", "-i", mp3, "-ac", "1", "-ar", "16000", "-f", "s16le", "-"], capture_output=True).stdout
    audio = np.frombuffer(pcm, np.int16).astype(np.float32) / 32768
    segs, _ = WhisperModel("medium", device="cpu", compute_type="int8").transcribe(
        audio, language="fr", word_timestamps=True, initial_prompt="Marcel, Rayan, Tracfin, Moreau, box 117, Marseille, euros.")
    ws = [{"w": w.word.strip(), "t0": round(w.start, 3), "t1": round(w.end, 3)} for s in segs for w in s.words]
    json.dump(ws, open(out_json, "w"), ensure_ascii=False)
    return len(ws)


def main(ep_id):
    os.makedirs(AUDIO, exist_ok=True)
    mp3 = os.path.join(AUDIO, f"{ep_id}.mp3")
    provider = "existant"
    if not os.path.exists(mp3):
        err = elevenlabs(script(ep_id), mp3)
        provider = "elevenlabs"
        if err:
            print(f"ElevenLabs indisponible ({err}) → voix de secours {FALLBACK_VOICE}")
            edge(script(ep_id), mp3)
            provider = "edge-tts"
    words_json = os.path.join(AUDIO, f"{ep_id}_words.json")
    # transcription déjà validée (voix fournie) : on la garde telle quelle
    if provider == "existant" and os.path.exists(words_json):
        print(json.dumps({"episode": ep_id, "voice": provider, "words": len(json.load(open(words_json)))}))
        return
    n = words(mp3, words_json)
    print(json.dumps({"episode": ep_id, "voice": provider, "words": n}))


if __name__ == "__main__":
    main(sys.argv[1])
