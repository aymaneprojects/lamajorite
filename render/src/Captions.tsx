import {interpolate, useCurrentFrame, useVideoConfig} from 'remotion';
import type {Beat, Word} from './types';
import {C, SANS} from './theme';

type Chunk = {words: Word[]; t0: number; t1: number};

// "9" "840" "000" "€" -> "9 840 000 €" ; "d'" "un" -> "d'un"
const merge = (words: Word[]): Word[] => {
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

// mots qui claquent en rose : chiffres, montants, noms, mots-clés de l'histoire
const KEY = /(\d|€|marcel|rayan|tracfin|moreau|police|box|million|personne|inconnu|quelqu'un|garder|payer|refuser|fuir|rester|mentir|parler|couper)/i;

export const Captions: React.FC<{words: Word[]; beats: Beat[]}> = ({words, beats}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const t = frame / fps;
  const beat = beats.find((b) => t >= b.start && t < b.end);
  if (beat?.card) return null; // les cartes ont déjà leur texte
  const chunks = chunk(words);
  const c = chunks.find((ch, i) => t >= ch.t0 - 0.05 && t < (chunks[i + 1]?.t0 ?? ch.t1 + 0.4) && t < ch.t1 + 0.6);
  if (!c) return null;
  return (
    <div style={{position: 'absolute', top: 1170, left: 60, right: 60, textAlign: 'center', fontFamily: SANS, fontWeight: 800, fontSize: 70, lineHeight: 1.15, letterSpacing: -1}}>
      {c.words.map((w, i) => {
        const on = t >= w.t0;
        const p = interpolate(t - w.t0, [0, 0.12], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
        const key = KEY.test(w.w);
        return (
          <span
            key={i}
            style={{
              display: 'inline-block',
              marginRight: 16,
              color: on ? (key ? C.pink : 'white') : 'rgba(255,255,255,0.42)',
              transform: `translateY(${on ? (1 - p) * 14 : 6}px) scale(${on ? 1 + (1 - p) * 0.18 : 0.96})`,
              textShadow: '0 4px 20px rgba(0,0,0,0.95), 0 0 3px rgba(0,0,0,0.9)',
            }}
          >
            {w.w}
          </span>
        );
      })}
    </div>
  );
};
