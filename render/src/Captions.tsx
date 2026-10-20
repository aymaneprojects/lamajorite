import {useCurrentFrame, useVideoConfig} from 'remotion';
import type {Beat, Word} from './types';
import {SANS} from './theme';

type Chunk = {words: Word[]; t0: number; t1: number};

// "9" "840" "000" "€" -> "9 840 000 €" ; "d'" "un" -> "d'un"
const merge = (words: Word[]): Word[] => {
  const out: Word[] = [];
  for (const w of words) {
    const prev = out[out.length - 1];
    if (prev && (prev.w.endsWith("'") || prev.w.endsWith('’') || /^['’]/.test(w.w))) {
      out[out.length - 1] = {w: prev.w + w.w, t0: prev.t0, t1: w.t1};
    } else if (prev && /^[\d ]+$/.test(prev.w) && /^(\d{3}[.,]?|€[.,]?|%[.,]?)$/.test(w.w)) {
      out[out.length - 1] = {w: `${prev.w} ${w.w}`, t0: prev.t0, t1: w.t1};
    } else out.push({...w});
  }
  return out;
};

const chunk = (raw: Word[]): Chunk[] => {
  const words = merge(raw);
  const out: Chunk[] = [];
  let cur: Word[] = [];
  words.forEach((w, i) => {
    cur.push(w);
    const punct = /[.,!?:;…»]$/.test(w.w);
    const gap = words[i + 1] ? words[i + 1].t0 - w.t1 > 0.35 : true;
    if (cur.length >= 3 || punct || gap) {
      out.push({words: cur, t0: cur[0].t0, t1: w.t1});
      cur = [];
    }
  });
  if (cur.length) out.push({words: cur, t0: cur[0].t0, t1: cur[cur.length - 1].t1});
  return out;
};

// Comme Saveo : 2–3 mots, blanc gras, mots à venir en gris, aucune animation, aucun mot coloré, vers 76 % de la hauteur.
export const Captions: React.FC<{words: Word[]; beats: Beat[]}> = ({words, beats}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const t = frame / fps;
  const beat = beats.find((b) => t >= b.start && t < b.end);
  if (beat?.card && !(beat.card.type === 'vote' && t < beat.start + (beat.card.at ?? 99))) return null;
  const chunks = chunk(words);
  const c = chunks.find((ch, i) => t >= ch.t0 - 0.05 && t < (chunks[i + 1]?.t0 ?? ch.t1 + 0.4) && t < ch.t1 + 0.6);
  if (!c) return null;
  return (
    <div
      style={{
        position: 'absolute',
        top: 1430,
        left: 60,
        right: 60,
        textAlign: 'center',
        fontFamily: SANS,
        fontWeight: 800,
        fontSize: 50,
        letterSpacing: -0.8,
        lineHeight: 1.15,
        textShadow: '0 2px 10px rgba(0,0,0,0.75)',
      }}
    >
      {c.words.map((w, i) => (
        <span key={i} style={{color: t >= w.t0 ? 'white' : 'rgba(255,255,255,0.5)'}}>
          {w.w}{' '}
        </span>
      ))}
    </div>
  );
};
