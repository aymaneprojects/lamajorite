import {interpolate, spring, useCurrentFrame, useVideoConfig} from 'remotion';
import {Accent, C, MONO, SANS} from './theme';

// Texte par-dessus l'image : hook d'ouverture ou étiquette
export const Overlay: React.FC<{o: any}> = ({o}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const s = spring({frame, fps, config: {damping: 14}});
  if (o.type === 'hook') {
    return (
      <div style={{position: 'absolute', top: 420, left: 50, right: 50, textAlign: 'center', transform: `scale(${0.85 + 0.15 * s})`, opacity: s}}>
        {o.kicker && <div style={{fontFamily: MONO, color: 'white', fontSize: 26, letterSpacing: 6, marginBottom: 10}}>{o.kicker}</div>}
        <div style={{fontFamily: SANS, fontWeight: 900, color: 'white', fontSize: 132, lineHeight: 1, letterSpacing: -3, textShadow: '0 6px 30px rgba(0,0,0,0.8)'}}>
          {o.big}
        </div>
        <div style={{fontFamily: SANS, fontWeight: 900, color: C.pink, fontSize: 64, marginTop: 12, textShadow: '0 4px 20px rgba(0,0,0,0.8)'}}>{o.accent}</div>
      </div>
    );
  }
  const y = interpolate(s, [0, 1], [20, 0]);
  return (
    <div style={{position: 'absolute', top: 1060, left: 0, right: 0, display: 'flex', justifyContent: 'center', opacity: s, transform: `translateY(${y}px)`}}>
      <div style={{background: 'rgba(10,10,10,0.88)', borderRadius: 10, padding: '10px 22px', fontFamily: SANS, fontWeight: 800, fontSize: 38, color: 'white', letterSpacing: 1}}>
        <Accent text={o.text} />
      </div>
    </div>
  );
};
