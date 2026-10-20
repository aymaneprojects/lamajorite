"""Mixage studio d'un épisode : voix devant, musique dessous (effacement doux), effets en arrière-plan.

  python3 mix.py P1 out/P1_video.mp4 out/P1.mp4

Entrées : la vidéo rendue par Remotion (image + piste d'effets seule), la voix (render/public/PX/voice.mp3)
et la musique de la série (catalogue). Niveaux visés avant la normalisation finale à -14 LUFS :
  1. voix      -16 LUFS  (référence)
  2. musique   -22 LUFS hors voix, ≈ 10 dB sous la voix quand elle parle (compresseur déclenché par la voix, attaque/relâche lentes)
  3. effets    -30 LUFS  (présents mais jamais devant la voix)
"""
import json, os, re, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VOICE_LUFS, MUSIC_LUFS, SFX_LUFS = -16, -19, -34


MUSIC_EQ = "acompressor=threshold=-26dB:ratio=3:attack=300:release=2000:makeup=1"


def loudness(path, stream="0:a", start=0, length=None, pre=""):
    seek = ["-ss", str(start)] + (["-t", str(length)] if length else [])
    af = (pre + "," if pre else "") + "ebur128=framelog=quiet"
    out = subprocess.run(["ffmpeg", "-hide_banner", *seek, "-i", path, "-map", stream, "-af", af, "-f", "null", "-"],
                         capture_output=True, text=True).stderr
    m = re.findall(r"I:\s+(-?[\d.]+) LUFS", out)
    return float(m[-1]) if m else None


def main(ep_id, video, out):
    tl = json.load(open(os.path.join(ROOT, "render", "public", ep_id, "timeline.json")))
    dur = tl["duration"]
    voice = os.path.join(ROOT, "render", "public", ep_id, "voice.mp3")
    music = os.path.join(ROOT, "render", "public", tl["music"])
    cat = json.load(open(os.path.join(ROOT, "render", "public", "music", "catalog.json")))
    debut = cat["pistes"].get(os.path.splitext(os.path.basename(music))[0], {}).get("debut", 0)
    # gains mesurés (statiques) : la normalisation automatique écrasait les musiques calmes
    music_gain = MUSIC_LUFS - loudness(music, start=debut, length=dur, pre=MUSIC_EQ)
    voice_gain = VOICE_LUFS - loudness(voice)
    sfx_lufs = loudness(video)
    sfx_gain = (SFX_LUFS - sfx_lufs) if sfx_lufs and sfx_lufs > -70 else 0
    fc = (
        # voix : gain fixe (pas de normalisation dynamique qui remonte les fins de mots),
        # puis expandeur qui coupe la traîne de réverbération des voix ElevenLabs (effet « écho »)
        f"[1:a]aresample=48000,highpass=f=70,volume={voice_gain:.1f}dB,"
        f"agate=threshold=0.1:ratio=6:range=0.06:attack=3:release=70:knee=3,"
        f"apad,atrim=0:{dur},aresample=48000,asplit=2[v][key];"
        f"[2:a]aresample=48000,atrim={debut}:{debut + dur},asetpts=PTS-STARTPTS,"
        # égalise les montées et creux du morceau pour qu'il reste à niveau constant sous la voix
        f"{MUSIC_EQ},afade=t=in:d=2,afade=t=out:st={dur - 3}:d=3,"
        f"volume={music_gain:.1f}dB[m];"
        # la musique s'efface d'environ 5 dB quand la voix parle, en douceur (pas d'à-coups mot par mot)
        f"[m][key]sidechaincompress=threshold=0.06:ratio=2:attack=250:release=1200:knee=8,aresample=48000[md];"
        f"[0:a]aresample=48000,volume={sfx_gain:.1f}dB[s];"
        f"[v]asplit=2[v1][v2];[md]asplit=2[m1][m2];[s]asplit=2[s1][s2];"
        f"[v1][m1][s1]amix=inputs=3:normalize=0:duration=first,alimiter=limit=0.89,"
        f"loudnorm=I=-14:TP=-1.5:LRA=11[out]"
    )
    # pistes séparées (voix / musique / effets) pour le contrôle qualité : out/PX_stems/
    stems = os.path.join(ROOT, "out", f"{ep_id}_stems")
    os.makedirs(stems, exist_ok=True)
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", video, "-i", voice, "-stream_loop", "-1", "-i", music,
                    "-filter_complex", fc, "-map", "0:v", "-map", "[out]", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
                    "-ar", "48000", "-movflags", "+faststart", "-t", str(dur), out,
                    "-map", "[v2]", "-ac", "1", f"{stems}/voix.wav", "-map", "[m2]", "-ac", "1", f"{stems}/musique.wav",
                    "-map", "[s2]", "-ac", "1", f"{stems}/effets.wav"], check=True)
    print(json.dumps({"episode": ep_id, "musique": tl["music"], "effets_lufs_avant": sfx_lufs, "gain_effets_db": round(sfx_gain, 1), "gain_musique_db": round(music_gain, 1)}))


if __name__ == "__main__":
    main(*sys.argv[1:4])
