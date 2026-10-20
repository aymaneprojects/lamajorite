import {interpolate, useCurrentFrame, useVideoConfig} from 'remotion';
import type {Beat, Hud} from './types';
import {C, MONO, SANS} from './theme';

const fmt = (n: number) => Math.round(n).toLocaleString('fr-FR').replace(/ | /g, ' ') + ' €';

// HUD façon jeu vidéo : CASH / EN BANQUE / SOUPÇON. Les valeurs glissent quand elles changent.
export const HudBar: React.FC<{beats: Beat[]}> = ({beats}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const t = frame / fps;
  const idx = beats.findIndex((b) => t >= b.start && t < b.end);
  const cur = beats[idx === -1 ? beats.length - 1 : idx];
  if (!cur?.hud) return null;
  const firstHud = beats.find((b) => b.hud)!;
  const prev: Hud = beats
    .slice(0, Math.max(0, beats.indexOf(cur)))
    .reverse()
    .find((b) => b.hud && JSON.stringify(b.hud) !== JSON.stringify(cur.hud))?.hud ?? {cash: 0, bank: 0, susp: 0};
  const k = interpolate(t, [cur.start, cur.start + 0.8], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  // à la première apparition, le cash monte depuis 0
  const startCash = cur === firstHud ? 0 : prev.cash ?? 0;
  const val = (key: keyof Hud, from: number) => from + ((cur.hud![key] ?? 0) - from) * (cur === firstHud && key === 'cash' ? interpolate(t, [cur.start, cur.start + 2], [0, 1], {extrapolateRight: 'clamp'}) : k);
  const changed = (key: keyof Hud) => cur.hud![key] !== prev[key] && k < 1;
  const appear = interpolate(t, [firstHud.start, firstHud.start + 0.4], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  const isFullCard = cur.card && cur.card.type !== 'sms';
  if (isFullCard && cur.card.type === 'vote') return null;

  const box = (label: string, value: string, hot = false, flash = false) => (
    <div
      style={{
        flex: 1,
        background: 'rgba(12,12,14,0.82)',
        border: `2px solid ${flash ? C.pink : 'rgba(255,255,255,0.08)'}`,
        borderRadius: 14,
        padding: '12px 18px 14px',
      }}
    >
      <div style={{fontFamily: MONO, fontSize: 17, letterSpacing: 3, color: 'rgba(255,255,255,0.5)'}}>{label}</div>
      <div style={{fontFamily: SANS, fontWeight: 800, fontSize: 34, color: hot ? C.pink : 'white', marginTop: 2}}>{value}</div>
    </div>
  );
  return (
    <div style={{position: 'absolute', top: 110, left: 44, right: 44, display: 'flex', gap: 12, opacity: appear}}>
      {box('CASH', fmt(val('cash', startCash)), false, changed('cash'))}
      {box('EN BANQUE', fmt(val('bank', prev.bank ?? 0)))}
      {box('SOUPÇON', `${Math.round(val('susp', prev.susp ?? 0))} %`, true, changed('susp'))}
    </div>
  );
};
