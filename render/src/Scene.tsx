import {AbsoluteFill, Img, interpolate, staticFile, useCurrentFrame} from 'remotion';
import type {Beat} from './types';
import {C, MONO, SANS} from './theme';

// Comme Saveo : image plein cadre, zoom lent continu, fondu enchaîné court à l'entrée. Rien d'autre.
export const FADE = 6;

export const Scene: React.FC<{beat: Beat; available: string[]; first: boolean}> = ({beat, available, first}) => {
  const f = useCurrentFrame();
  const len = Math.max(1, (beat.end - beat.start) * 30 + FADE);
  const scale = interpolate(f, [0, len], [1.0, 1.06], {extrapolateRight: 'clamp'});
  const opacity = first ? 1 : interpolate(f, [0, FADE], [0, 1], {extrapolateRight: 'clamp'});
  const id = beat.image!.split('/').pop()!.replace('.png', '');
  const has = available.includes(id);
  return (
    <AbsoluteFill style={{overflow: 'hidden', opacity}}>
      <AbsoluteFill style={{transform: `scale(${scale})`}}>
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
