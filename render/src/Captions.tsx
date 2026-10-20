import {useCurrentFrame, useVideoConfig} from 'remotion';
import type {Beat, Word} from './types';
import {SANS} from './theme';

type Chunk = {words: Word[]; t0: number; t1: number};

// Regroupe les mots en petits blocs (3 mots max, coupe sur la ponctuation)
// "9" "840" "000" "€" -> un seul mot "9 840 000 €"
const mergeNumbers = (words: Word[]): Word[] => {
  const out: Word[] = [];
  for (const w of words) {
    const prev = out[out.length - 1];
    if (prev && (prev.w.endsWith("'") || prev.w.endsWith('’') || /^['’]/.test(w.w))) {
      out[out.length - 1] = {w: prev.w + w.w, t0: prev.t0, t1: w.t1};
    } else if (prev && /^[\d ]+$/.test(prev.w) && /^(\d{3}[.,]?|€[.,]?)$/.test(w.w)) {
      out[out.length - 1] = {w: `${prev.w} ${w.w}`, t0: prev.t0, t1: w.t1};
    } else out.push({...w});
  }
  return out;
};

const chunk = (raw: Word[]): Chunk[] => {
  const words = mergeNumbers(raw);
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

export const Captions: React.FC<{words: Word[]; beats: Beat[]}> = ({words, beats}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const t = frame / fps;
  const beat = beats.find((b) => t >= b.start && t < b.end);
  // pas de sous-titres sur les cartes plein écran (elles ont déjà leur texte)
  if (beat?.card) return null;
  const chunks = chunk(words);
  const c = chunks.find((ch, i) => t >= ch.t0 - 0.05 && t < (chunks[i + 1]?.t0 ?? ch.t1 + 0.4) && t < ch.t1 + 0.6);
  if (!c) return null;
  return (
    <div style={{position: 'absolute', top: 1180, left: 70, right: 70, textAlign: 'center'}}>
      <span style={{fontFamily: SANS, fontWeight: 800, fontSize: 66, lineHeight: 1.15, textShadow: '0 4px 18px rgba(0,0,0,0.9), 0 0 4px rgba(0,0,0,0.9)'}}>
        {c.words.map((w, i) => (
          <span key={i} style={{color: t >= w.t0 ? 'white' : 'rgba(255,255,255,0.5)'}}>
            {w.w}{' '}
          </span>
        ))}
      </span>
    </div>
  );
};
