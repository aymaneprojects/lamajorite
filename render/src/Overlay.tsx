import {interpolate, random, spring, useCurrentFrame, useVideoConfig} from 'remotion';
import {Accent, C, MONO, SANS} from './theme';

// Texte par-dessus l'image : hook d'ouverture (lettres qui tombent + glitch) ou étiquette
export const Overlay: React.FC<{o: any}> = ({o}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const s = spring({frame, fps, config: {damping: 14}});
  if (o.type === 'hook') {
    const glitch = frame < 20 && random(`h${frame}`) > 0.6;
    return (
      <div style={{position: 'absolute', top: 470, left: 40, right: 40, textAlign: 'center'}}>
        {o.kicker && <div style={{fontFamily: MONO, color: 'white', fontSize: 26, letterSpacing: 6, marginBottom: 10}}>{o.kicker}</div>}
        <div style={{fontFamily: SANS, fontWeight: 800, color: 'white', fontSize: 138, lineHeight: 1, letterSpacing: -4, textShadow: glitch ? `6px 0 ${C.pink}, -6px 0 #3cf` : '0 8px 40px rgba(0,0,0,0.85)'}}>
          {o.big.split('').map((ch: string, i: number) => {
            const p = spring({frame: frame - i * 1.5, fps, config: {damping: 12}});
            return (
              <span key={i} style={{display: 'inline-block', opacity: p, transform: `translateY(${(1 - p) * -60}px) scale(${1 + (1 - p) * 0.6})`, whiteSpace: 'pre'}}>
                {ch}
              </span>
            );
          })}
        </div>
        <div
          style={{
            display: 'inline-block',
            fontFamily: SANS,
            fontWeight: 800,
            color: 'white',
            background: C.pink,
            fontSize: 58,
            marginTop: 18,
            padding: '4px 20px',
            transform: `scaleX(${interpolate(frame, [18, 26], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'})})`,
            boxShadow: `0 0 40px rgba(255,46,126,0.6)`,
          }}
        >
          {o.accent}
        </div>
      </div>
    );
  }
  const w = interpolate(frame, [0, 8], [0, 1], {extrapolateRight: 'clamp'});
  return (
    <div style={{position: 'absolute', top: 1060, left: 0, right: 0, display: 'flex', justifyContent: 'center', opacity: s}}>
      <div style={{background: 'rgba(10,10,10,0.9)', borderLeft: `6px solid ${C.pink}`, borderRadius: 8, padding: '10px 22px', fontFamily: SANS, fontWeight: 800, fontSize: 38, color: 'white', letterSpacing: 1, clipPath: `inset(0 ${(1 - w) * 100}% 0 0)`}}>
        <Accent text={o.text} />
      </div>
    </div>
  );
};
