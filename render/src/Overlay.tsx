import {Accent, C, SANS} from './theme';

// Accroche : texte fixe, capitales, blanc + mot rose, ombre portée, sans fond ni animation (comme Saveo).
// Étiquette : pastille sombre, blanc + mot rose, apparition sèche.
export const Overlay: React.FC<{o: any}> = ({o}) => {
  if (o.type === 'hook') {
    return (
      <div style={{position: 'absolute', top: 360, left: 50, right: 50, textAlign: 'center'}}>
        {o.lines.map((l: string, i: number) => (
          <div key={i} style={{fontFamily: SANS, fontWeight: 900, fontSize: 88, lineHeight: 1.05, letterSpacing: -2.5, color: 'white', textTransform: 'uppercase', textShadow: '0 4px 24px rgba(0,0,0,0.7)'}}>
            <Accent text={l} />
          </div>
        ))}
      </div>
    );
  }
  return (
    <div style={{position: 'absolute', top: 1172, left: 0, right: 0, display: 'flex', justifyContent: 'center'}}>
      <div style={{background: 'rgba(28,24,24,0.82)', borderRadius: 14, padding: '10px 24px', fontFamily: SANS, fontWeight: 800, fontSize: 39, letterSpacing: -0.5, color: 'white'}}>
        <Accent text={o.text} color={C.pink} />
      </div>
    </div>
  );
};
