import {AbsoluteFill, Img, interpolate, staticFile, useCurrentFrame} from 'remotion';
import type {Beat} from './types';
import {C, MONO, SANS} from './theme';
import {inOut, plus} from './motion';

// Comme Saveo : image plein cadre, zoom lent continu, fondu enchaîné court à l'entrée. Rien d'autre.
export const FADE = 6;

export const Scene: React.FC<{beat: Beat; available: string[]; first: boolean}> = ({beat, available, first}) => {
  const f = useCurrentFrame();
  const len = Math.max(1, (beat.end - beat.start) * 30 + FADE);
  const opacity = first ? 1 : interpolate(f, [0, FADE], [0, 1], {extrapolateRight: 'clamp'});
  // Saveo : zoom lent unique. Motion plus : 5 mouvements de caméra (avant, arrière, panoramiques, montée), courbe douce,
  // et une mise au point à l'entrée du plan (léger flou + recul qui se résorbent).
  const k = inOut(f / len);
  let scale = interpolate(f, [0, len], [1.0, 1.06], {extrapolateRight: 'clamp'});
  let tx = 0;
  let ty = 0;
  let blur = 0;
  if (plus()) {
    const m = beat.i % 5;
    scale = m === 1 ? 1.16 - 0.1 * k : m === 0 ? 1.04 + 0.12 * k : 1.12;
    tx = m === 2 ? -45 + 90 * k : m === 3 ? 45 - 90 * k : 0;
    ty = m === 4 ? 50 - 100 * k : 0;
    const e = interpolate(f, [0, FADE + 6], [1, 0], {extrapolateRight: 'clamp'});
    if (!first) {
      blur = 10 * e * e;
      scale *= 1 + 0.05 * e * e;
    }
  }
  const id = beat.image!.split('/').pop()!.replace('.png', '');
  const has = available.includes(id);
  return (
    <AbsoluteFill style={{overflow: 'hidden', opacity}}>
      <AbsoluteFill style={{transform: `translate(${tx}px, ${ty}px) scale(${scale})`, filter: blur > 0.3 ? `blur(${blur}px)` : undefined}}>
        {has ? (
          <Img src={staticFile(beat.image!)} style={{width: '100%', height: '100%', objectFit: 'cover'}} />
        ) : (
          <AbsoluteFill style={{background: '#16131c', justifyContent: 'center', alignItems: 'center'}}>
            <div style={{fontFamily: MONO, color: C.pink, fontSize: 40}}>IMAGE {id}</div>
            <div style={{fontFamily: SANS, color: '#666', fontSize: 28}}>{beat.prompt.slice(0, 120)}</div>
          </AbsoluteFill>
        )}
      </AbsoluteFill>
    </AbsoluteFill>
  );
};
