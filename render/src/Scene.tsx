import {AbsoluteFill, Img, interpolate, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';
import type {Beat} from './types';
import {C, MONO, SANS} from './theme';

// Image plein écran avec zoom lent (Ken Burns). Placeholder si l'image n'est pas encore fournie.
export const Scene: React.FC<{beat: Beat; available: string[]}> = ({beat, available}) => {
  const frame = useCurrentFrame();
  const {durationInFrames} = useVideoConfig();
  const len = Math.max(1, (beat.end - beat.start) * 30);
  const dir = beat.i % 2 === 0 ? 1 : -1;
  const scale = interpolate(frame, [0, len], [1.06, 1.14], {extrapolateRight: 'clamp'});
  const x = interpolate(frame, [0, len], [0, 18 * dir], {extrapolateRight: 'clamp'});
  const punch = interpolate(frame, [0, 4], [1.03, 1], {extrapolateRight: 'clamp'});
  const id = beat.image!.split('/').pop()!.replace('.png', '');
  const has = available.includes(id);
  void durationInFrames;
  return (
    <AbsoluteFill style={{overflow: 'hidden'}}>
      <AbsoluteFill style={{transform: `scale(${scale * punch}) translateX(${x}px)`}}>
        {has ? (
          <Img src={staticFile(beat.image!)} style={{width: '100%', height: '100%', objectFit: 'cover'}} />
        ) : (
          <AbsoluteFill
            style={{
              background: `radial-gradient(ellipse at 50% 45%, #2a2340 0%, #120f1a 60%, #080709 100%)`,
              justifyContent: 'center',
              alignItems: 'center',
              padding: 110,
            }}
          >
            <div style={{fontFamily: MONO, color: C.pink, fontSize: 40, letterSpacing: 6}}>IMAGE {id}</div>
            <div style={{fontFamily: SANS, color: 'rgba(255,255,255,0.35)', fontSize: 30, lineHeight: 1.35, marginTop: 30, textAlign: 'center'}}>
              {beat.prompt.slice(0, 220)}
            </div>
          </AbsoluteFill>
        )}
      </AbsoluteFill>
      {/* vignette pour la lisibilité du HUD et des sous-titres */}
      <AbsoluteFill
        style={{
          background:
            'linear-gradient(180deg, rgba(0,0,0,0.55) 0%, rgba(0,0,0,0) 16%, rgba(0,0,0,0) 55%, rgba(0,0,0,0.45) 100%)',
        }}
      />
    </AbsoluteFill>
  );
};
