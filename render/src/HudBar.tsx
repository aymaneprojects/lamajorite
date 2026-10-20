import {interpolate, spring, useCurrentFrame, useVideoConfig} from 'remotion';
import type {Beat, Hud} from './types';
import {C, MONO, SANS} from './theme';

const fmt = (n: number) => Math.round(n).toLocaleString('fr-FR').replace(/ | /g, ' ') + ' €';
const fmtDelta = (n: number) => (n > 0 ? '+' : '−') + Math.abs(Math.round(n)).toLocaleString('fr-FR').replace(/ | /g, ' ');

// HUD façon jeu vidéo : panneaux vitrés, compteur qui défile, jauge de soupçon qui pulse quand elle monte.
export const HudBar: React.FC<{beats: Beat[]; episode: string}> = ({beats, episode}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const t = frame / fps;
  const idx = beats.findIndex((b) => t >= b.start && t < b.end);
  const cur = beats[idx === -1 ? beats.length - 1 : idx];
  if (!cur?.hud || cur.card?.type === 'vote') return null;
  const firstHud = beats.find((b) => b.hud)!;
  const prevBeat = beats
    .slice(0, beats.indexOf(cur))
    .reverse()
    .find((b) => b.hud && JSON.stringify(b.hud) !== JSON.stringify(cur.hud));
  // le changement a lieu au premier beat qui porte les nouvelles valeurs
  const changeBeat = beats.find((b) => b.hud && JSON.stringify(b.hud) === JSON.stringify(cur.hud))!;
  const prev: Hud = prevBeat?.hud ?? {cash: 0, bank: 0, susp: 0};
  const since = t - changeBeat.start;
  const k = interpolate(since, [0, cur === firstHud ? 2 : 0.9], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  const ease = 1 - Math.pow(1 - k, 3);
  const v = (key: keyof Hud) => (prev[key] ?? 0) + ((cur.hud![key] ?? 0) - (prev[key] ?? 0)) * ease;
  const appear = spring({frame: frame - Math.round(firstHud.start * fps), fps, config: {damping: 14}});
  const dSusp = (cur.hud.susp ?? 0) - (prev.susp ?? 0);
  const dCash = (cur.hud.cash ?? 0) - (prev.cash ?? 0);
  const hot = since < 1.6 && dSusp > 0 && changeBeat !== firstHud;
  const pulse = hot ? 0.5 + 0.5 * Math.sin(since * 18) : 0;
  const chip = (txt: string, color: string) => {
    const o = interpolate(since, [0, 0.2, 1.6, 2], [0, 1, 1, 0], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
    return (
      <div style={{position: 'absolute', top: 104, left: 0, fontFamily: SANS, fontWeight: 800, fontSize: 26, color: 'white', background: color, padding: '3px 12px', borderRadius: 8, opacity: o, transform: `translateY(${(1 - o) * -10}px)`}}>
        {txt}
      </div>
    );
  };
  const panel = (label: string, value: string, extra?: React.ReactNode, glow = 0) => (
    <div
      style={{
        position: 'relative',
        flex: 1,
        background: 'linear-gradient(180deg, rgba(30,28,34,0.78), rgba(12,12,14,0.86))',
        border: `2px solid rgba(255,46,126,${0.12 + glow * 0.8})`,
        boxShadow: `0 8px 30px rgba(0,0,0,0.45), 0 0 ${30 * glow}px rgba(255,46,126,${0.6 * glow})`,
        borderRadius: 16,
        padding: '12px 18px 14px',
        backdropFilter: 'blur(10px)',
      }}
    >
      <div style={{fontFamily: MONO, fontSize: 16, letterSpacing: 3, color: 'rgba(255,255,255,0.5)'}}>{label}</div>
      <div style={{fontFamily: SANS, fontWeight: 800, fontSize: 33, color: 'white', marginTop: 3, fontVariantNumeric: 'tabular-nums'}}>{value}</div>
      {extra}
    </div>
  );
  const susp = v('susp');
  return (
    <div style={{position: 'absolute', top: 104, left: 40, right: 40, opacity: appear, transform: `translateY(${(1 - appear) * -40}px)`}}>
      <div style={{display: 'flex', gap: 12}}>
        {panel('CASH', fmt(v('cash')), dCash !== 0 && changeBeat !== firstHud ? chip(fmtDelta(dCash) + ' €', dCash < 0 ? '#e0244f' : '#1f9d5a') : null)}
        {panel('EN BANQUE', fmt(v('bank')))}
        {panel(
          'SOUPÇON',
          `${Math.round(susp)} %`,
          <>
            <div style={{height: 7, borderRadius: 4, background: 'rgba(255,255,255,0.1)', marginTop: 8, overflow: 'hidden'}}>
              <div style={{width: `${susp}%`, height: '100%', background: `linear-gradient(90deg, #ff8a3c, ${C.pink})`, boxShadow: `0 0 12px ${C.pink}`}} />
            </div>
            {dSusp > 0 && changeBeat !== firstHud ? chip(`+${dSusp} %`, C.pink) : null}
          </>,
          pulse,
        )}
      </div>
      <div style={{display: 'inline-block', marginTop: 12, fontFamily: MONO, fontSize: 18, letterSpacing: 4, color: 'white', background: C.pink, padding: '4px 12px', borderRadius: 6}}>
        PARTIE {episode.replace(/\D/g, '')}
      </div>
    </div>
  );
};
