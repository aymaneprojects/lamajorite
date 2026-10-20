import {useCurrentFrame, useVideoConfig} from 'remotion';
import type {Beat, Hud} from './types';
import {C, MONO, SANS} from './theme';

const fmt = (n: number) => Math.round(n).toLocaleString('fr-FR').replace(/ | /g, ' ') + ' €';

// HUD mesuré sur Saveo (720 px → ×1,5) : 3 blocs sombres arrondis, étiquette mono grise, valeur blanche, soupçon rose.
// Au changement : contour rose sur le bloc, et pastille rouge sous le cash quand il baisse.
export const HudBar: React.FC<{beats: Beat[]; episode: string}> = ({beats}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const t = frame / fps;
  const cur = beats.find((b) => t >= b.start && t < b.end) ?? beats[beats.length - 1];
  if (!cur?.hud || ['stat', 'fact', 'rule'].includes(cur.card?.type)) return null;
  const idx = beats.indexOf(cur);
  const changeBeat = beats.find((b) => b.hud && JSON.stringify(b.hud) === JSON.stringify(cur.hud))!;
  const prev: Hud | undefined = beats.slice(0, beats.indexOf(changeBeat)).reverse().find((b) => b.hud)?.hud ?? undefined;
  const since = t - changeBeat.start;
  const flash = (k: keyof Hud) => prev !== undefined && prev[k] !== cur.hud![k] && since < 1.6;
  const box = (label: string, value: string, flex: number, hot: boolean, pink = false) => (
    <div
      style={{
        flex,
        background: 'rgba(24,20,20,0.86)',
        border: `3px solid ${hot ? C.pink : 'transparent'}`,
        borderRadius: 14,
        padding: '15px 20px 14px',
      }}
    >
      <div style={{fontFamily: MONO, fontWeight: 500, fontSize: 18, letterSpacing: 1.5, color: 'rgba(255,255,255,0.62)'}}>{label}</div>
      <div style={{fontFamily: SANS, fontWeight: 800, fontSize: 40, letterSpacing: -0.5, color: pink ? C.pink : 'white', marginTop: 4}}>{value}</div>
    </div>
  );
  const dCash = (cur.hud.cash ?? 0) - (prev?.cash ?? cur.hud.cash ?? 0);
  void idx;
  return (
    <div style={{position: 'absolute', top: 234, left: 60, right: 60}}>
      <div style={{display: 'flex', gap: 12}}>
        {box('CASH', fmt(cur.hud.cash ?? 0), 1.25, flash('cash'))}
        {box('EN BANQUE', fmt(cur.hud.bank ?? 0), 1, flash('bank'))}
        {box('SOUPÇON', `${cur.hud.susp ?? 0} %`, 0.95, flash('susp'), true)}
      </div>
      <div style={{display: 'flex', gap: 12, marginTop: 12}}>
        {dCash < 0 && since < 3 && (
          <div style={{fontFamily: SANS, fontWeight: 800, fontSize: 26, color: 'white', background: '#d81f45', padding: '2px 12px', borderRadius: 6}}>
            −{fmt(-dCash)}
          </div>
        )}
      </div>
    </div>
  );
};
