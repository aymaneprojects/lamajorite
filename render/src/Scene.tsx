import {AbsoluteFill, Img, interpolate, staticFile, useCurrentFrame} from 'remotion';
import type {Beat, Word} from './types';
import {C, MONO, SANS} from './theme';
import {Atmos, fxFor, handheld} from './Fx';

// 3 entrées qui alternent : coup de fouet latéral, zoom traversant, glissement vertical
const entry = (kind: number, f: number) => {
  const k = interpolate(f, [0, 7], [1, 0], {extrapolateRight: 'clamp'});
  const e = k * k;
  if (kind === 0) return {tx: 260 * e, ty: 0, s: 1, blur: 24 * e};
  if (kind === 1) return {tx: 0, ty: 0, s: 1 + 0.35 * e, blur: 16 * e};
  return {tx: 0, ty: -220 * e, s: 1, blur: 20 * e};
};

// 4 mouvements de caméra 2.5D : travelling avant, latéral, plongée, recul
const move = (kind: number, k: number) => {
  const e = 0.5 - Math.cos(Math.PI * k) / 2;
  switch (kind) {
    case 0: return {bgS: 1.08 + 0.05 * e, fgS: 1.08 + 0.09 * e, bgX: 0, fgX: 0, bgY: 0, fgY: -6 * e};
    case 1: return {bgS: 1.12, fgS: 1.12, bgX: -16 + 32 * e, fgX: -36 + 72 * e, bgY: 0, fgY: 0};
    case 2: return {bgS: 1.12, fgS: 1.13, bgX: 0, fgX: 0, bgY: -14 + 28 * e, fgY: -32 + 64 * e};
    default: return {bgS: 1.16 - 0.05 * e, fgS: 1.2 - 0.09 * e, bgX: 0, fgX: 0, bgY: 0, fgY: 0};
  }
};

export const Scene: React.FC<{beat: Beat; available: string[]; layers: string[]; words: Word[]}> = ({beat, available, layers, words}) => {
  const f = useCurrentFrame();
  const len = Math.max(1, (beat.end - beat.start) * 30);
  const k = Math.min(1, f / len);
  const id = beat.image!.split('/').pop()!.replace('.png', '');
  const has = available.includes(id);
  const layered = has && layers.includes(id);
  const hh = handheld(f + beat.i * 50);
  const en = entry(beat.i % 3, f);
  const mv = move(beat.i % 4, k);
  const fx = fxFor(beat.prompt);
  // le personnage « vit » : respiration + petit rebond quand la voix parle
  const t = beat.start + f / 30;
  const speaking = words.some((w) => t >= w.t0 && t <= w.t1);
  const breathe = 1 + 0.008 * Math.sin(f / 14);
  const bob = speaking ? Math.abs(Math.sin(f / 2.6)) * -4 : 0;
  const cam = `translate(${hh.x + en.tx}px, ${hh.y + en.ty}px) rotate(${hh.r}deg) scale(${en.s})`;
  const blur = en.blur > 0.5 ? `blur(${en.blur}px)` : undefined;
  return (
    <AbsoluteFill style={{overflow: 'hidden', background: '#000'}}>
      <AbsoluteFill style={{transform: cam, filter: blur}}>
        {layered ? (
          <>
            <AbsoluteFill style={{transform: `translate(${mv.bgX}px, ${mv.bgY}px) scale(${mv.bgS})`}}>
              <Img src={staticFile(`${beat.image!.split('/')[0]}/layers/${id}_bg.jpg`)} style={{width: '100%', height: '100%', objectFit: 'cover'}} />
            </AbsoluteFill>
            <AbsoluteFill style={{transform: `translate(${mv.fgX}px, ${mv.fgY + bob}px) scale(${mv.fgS}) scaleY(${breathe})`, transformOrigin: '50% 90%'}}>
              <Img src={staticFile(`${beat.image!.split('/')[0]}/layers/${id}_fg.png`)} style={{width: '100%', height: '100%', objectFit: 'cover', filter: 'drop-shadow(0 18px 24px rgba(0,0,0,0.45))'}} />
            </AbsoluteFill>
          </>
        ) : has ? (
          <AbsoluteFill style={{transform: `translate(${mv.fgX * 0.4}px, ${mv.fgY * 0.4}px) scale(${mv.bgS})`}}>
            <Img src={staticFile(beat.image!)} style={{width: '100%', height: '100%', objectFit: 'cover'}} />
          </AbsoluteFill>
        ) : (
          <AbsoluteFill style={{background: 'radial-gradient(ellipse at 50% 45%, #2a2340 0%, #120f1a 60%, #080709 100%)', justifyContent: 'center', alignItems: 'center', padding: 110}}>
            <div style={{fontFamily: MONO, color: C.pink, fontSize: 40, letterSpacing: 6}}>IMAGE {id}</div>
            <div style={{fontFamily: SANS, color: 'rgba(255,255,255,0.35)', fontSize: 30, lineHeight: 1.35, marginTop: 30, textAlign: 'center'}}>{beat.prompt.slice(0, 220)}</div>
          </AbsoluteFill>
        )}
      </AbsoluteFill>
      <Atmos kinds={fx} />
      {/* balayage de lumière diagonal à l'entrée du plan */}
      <AbsoluteFill
        style={{
          background: 'linear-gradient(115deg, rgba(255,255,255,0) 40%, rgba(255,220,240,0.16) 50%, rgba(255,255,255,0) 60%)',
          transform: `translateX(${interpolate(f, [0, 22], [-1100, 1100], {extrapolateRight: 'clamp'})}px)`,
          mixBlendMode: 'screen',
        }}
      />
      <AbsoluteFill style={{background: 'linear-gradient(180deg, rgba(0,0,0,0.6) 0%, rgba(0,0,0,0) 17%, rgba(0,0,0,0) 52%, rgba(0,0,0,0.5) 100%)'}} />
      <AbsoluteFill style={{background: 'white', opacity: interpolate(f, [0, 4], [beat.i % 3 === 1 ? 0.35 : 0.12, 0], {extrapolateRight: 'clamp'})}} />
    </AbsoluteFill>
  );
};
