import {useCurrentFrame} from 'remotion';
import {Accent, C, SANS} from './theme';
import {plus, reveal} from './motion';

// Accroche : texte fixe, capitales, blanc + mot rose, ombre portée, sans fond ni animation (comme Saveo).
// Étiquette : pastille sombre, blanc + mot rose, apparition sèche.
export const Overlay: React.FC<{o: any}> = ({o}) => {
  const f = useCurrentFrame();
  if (o.type === 'hook') {
    return (
      <div style={{position: 'absolute', top: 360, left: 50, right: 50, textAlign: 'center'}}>
        {o.lines.map((l: string, i: number) => {
          const k = plus() ? reveal(f, 2 + i * 5, 10) : 1;
          return (
            <div key={i} style={{overflow: 'hidden', paddingBottom: 8}}>
              <div style={{fontFamily: SANS, fontWeight: 900, fontSize: 88, lineHeight: 1.05, letterSpacing: -2.5, color: 'white', textTransform: 'uppercase', textShadow: '0 4px 24px rgba(0,0,0,0.7)', transform: `translateY(${(1 - k) * 105}%)`}}>
                <Accent text={l} />
              </div>
            </div>
          );
        })}
      </div>
    );
  }
  return (
    <div style={{position: 'absolute', top: 1172, left: 0, right: 0, display: 'flex', justifyContent: 'center'}}>
      <div style={{background: 'rgba(28,24,24,0.82)', borderRadius: 14, padding: '10px 24px', fontFamily: SANS, fontWeight: 800, fontSize: 39, letterSpacing: -0.5, color: 'white', clipPath: plus() ? `inset(0 ${(1 - reveal(f, 2, 9)) * 100}% 0 0 round 14px)` : undefined}}>
        <Accent text={o.text} color={C.pink} />
      </div>
    </div>
  );
};
