import {AbsoluteFill, interpolate, random, useCurrentFrame, useVideoConfig} from 'remotion';
import {C} from './theme';

// Effets d'ambiance animés, choisis d'après la description de l'image.
export type FxKind = 'rain' | 'dust' | 'neon' | 'fog' | 'embers';

export const fxFor = (prompt: string): FxKind[] => {
  const p = prompt.toLowerCase();
  const fx: FxKind[] = [];
  if (/rain|wet|storm|drops/.test(p)) fx.push('rain');
  if (/dust|flashlight|storage|attic|bulb|lamp/.test(p)) fx.push('dust');
  if (/neon|pink light|nightclub|kebab/.test(p)) fx.push('neon');
  if (/mist|fog|forest|smoke|dawn|haze/.test(p)) fx.push('fog');
  if (/sparkler|fire|candle|headlights/.test(p)) fx.push('embers');
  return fx;
};

const Rain: React.FC = () => {
  const f = useCurrentFrame();
  const drops = Array.from({length: 90}, (_, i) => {
    const x = random(`rx${i}`) * 1180 - 50;
    const speed = 38 + random(`rs${i}`) * 30;
    const len = 40 + random(`rl${i}`) * 70;
    const y = ((random(`ry${i}`) * 2100 + f * speed) % 2100) - 120;
    return <line key={i} x1={x} y1={y} x2={x - len * 0.18} y2={y + len} stroke="rgba(200,220,255,0.22)" strokeWidth={1.6 + random(`rw${i}`) * 1.4} />;
  });
  return (
    <svg width={1080} height={1920} style={{position: 'absolute', mixBlendMode: 'screen'}}>
      {drops}
    </svg>
  );
};

const Dust: React.FC<{warm?: boolean}> = ({warm}) => {
  const f = useCurrentFrame();
  return (
    <AbsoluteFill style={{mixBlendMode: 'screen'}}>
      {Array.from({length: 46}, (_, i) => {
        const bx = random(`dx${i}`) * 1080;
        const by = random(`dy${i}`) * 1920;
        const s = 2 + random(`ds${i}`) * 5;
        const x = bx + Math.sin(f / (40 + i) + i) * 30;
        const y = (by - f * (0.4 + random(`dv${i}`) * 1.2) + 1920) % 1920;
        const o = 0.25 + 0.5 * Math.abs(Math.sin(f / 25 + i));
        const col = warm ? '255,190,110' : '255,240,220';
        return <div key={i} style={{position: 'absolute', left: x, top: y, width: s, height: s, borderRadius: s, background: `rgba(${col},${o})`, boxShadow: `0 0 ${s * 3}px rgba(${col},${o})`}} />;
      })}
    </AbsoluteFill>
  );
};

const Fog: React.FC = () => {
  const f = useCurrentFrame();
  return (
    <AbsoluteFill style={{mixBlendMode: 'screen', opacity: 0.55}}>
      {[0, 1, 2].map((i) => (
        <div
          key={i}
          style={{
            position: 'absolute',
            left: -400 + ((f * (0.6 + i * 0.3) + i * 500) % 1900) - 300,
            top: 900 + i * 260,
            width: 1300,
            height: 520,
            borderRadius: '50%',
            background: 'radial-gradient(ellipse, rgba(170,180,210,0.28) 0%, rgba(170,180,210,0) 70%)',
            filter: 'blur(30px)',
          }}
        />
      ))}
    </AbsoluteFill>
  );
};

const Neon: React.FC = () => {
  const f = useCurrentFrame();
  // scintillement irrégulier façon néon fatigué
  const flick = random(`n${Math.floor(f / 2)}`) > 0.93 ? 0.05 : 0.16 + 0.05 * Math.sin(f / 7);
  return <AbsoluteFill style={{background: `radial-gradient(ellipse at 80% 20%, ${C.pink} 0%, rgba(0,0,0,0) 55%)`, opacity: flick, mixBlendMode: 'screen'}} />;
};

const Embers: React.FC = () => {
  const f = useCurrentFrame();
  return (
    <AbsoluteFill style={{mixBlendMode: 'screen'}}>
      {Array.from({length: 28}, (_, i) => {
        const x = random(`ex${i}`) * 1080 + Math.sin(f / 15 + i) * 20;
        const y = (random(`ey${i}`) * 1920 - f * (2 + random(`ev${i}`) * 3) + 3840) % 1920;
        return <div key={i} style={{position: 'absolute', left: x, top: y, width: 4, height: 4, borderRadius: 4, background: '#ffb15c', boxShadow: '0 0 12px #ff8a3c', opacity: 0.7}} />;
      })}
    </AbsoluteFill>
  );
};

export const Atmos: React.FC<{kinds: FxKind[]}> = ({kinds}) => (
  <>
    {kinds.includes('fog') && <Fog />}
    {kinds.includes('rain') && <Rain />}
    {kinds.includes('dust') && <Dust warm />}
    {kinds.includes('embers') && <Embers />}
    {kinds.includes('neon') && <Neon />}
  </>
);

// Grain de film + vignette, toujours actifs : donnent la texture « cinéma »
export const Grain: React.FC = () => {
  const f = useCurrentFrame();
  const {width, height} = useVideoConfig();
  const seed = f % 12;
  return (
    <AbsoluteFill style={{pointerEvents: 'none'}}>
      <svg width={width} height={height} style={{position: 'absolute', opacity: 0.09, mixBlendMode: 'overlay'}}>
        <filter id={`g${seed}`}>
          <feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="2" seed={seed} />
        </filter>
        <rect width="100%" height="100%" filter={`url(#g${seed})`} />
      </svg>
      <AbsoluteFill style={{background: 'radial-gradient(ellipse at 50% 50%, rgba(0,0,0,0) 60%, rgba(0,0,0,0.38) 100%)'}} />
    </AbsoluteFill>
  );
};

// Caméra à l'épaule : léger mouvement continu
export const handheld = (f: number, amp = 1) => ({
  x: (Math.sin(f / 23) * 4 + Math.sin(f / 9.7) * 1.5) * amp,
  y: (Math.cos(f / 19) * 4 + Math.sin(f / 13.3) * 1.5) * amp,
  r: Math.sin(f / 31) * 0.25 * amp,
});

export const shake = (f: number, start: number, dur = 10, amp = 18) => {
  const k = interpolate(f - start, [0, dur], [1, 0], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  return {x: Math.sin(f * 2.7) * amp * k, y: Math.cos(f * 3.1) * amp * k};
};
