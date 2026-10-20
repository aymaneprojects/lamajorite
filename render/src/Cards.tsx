import {AbsoluteFill, interpolate, useCurrentFrame} from 'remotion';
import type {Beat} from './types';
import {Accent, C, MONO, SANS} from './theme';
import {FADE} from './Scene';

// Cartes reproduites d'après Saveo : fond uni, surtitre mono gris, lignes qui apparaissent l'une après l'autre
// (≈ 5 images d'écart, sans animation), tampon rose penché. Fondu d'entrée identique aux plans.
const STEP = 5;
const shown = (f: number, i: number, start = FADE) => f >= start + i * STEP;

const Kicker: React.FC<{text: string; color: string}> = ({text, color}) => (
  <div style={{fontFamily: MONO, fontWeight: 600, fontSize: 20, letterSpacing: 4, color, textTransform: 'uppercase'}}>{text}</div>
);

const Lines: React.FC<{lines: string[]; dark: boolean}> = ({lines, dark}) => {
  const f = useCurrentFrame();
  const ink = dark ? 'white' : C.ink;
  return (
    <>
      {lines.map((l, i) => {
        // la ligne du milieu (chiffre / mot clé) est la plus grosse, comme « $10,000 »
        const big = lines.length === 3 && i === 1;
        return (
          <div
            key={i}
            style={{
              fontFamily: SANS,
              fontWeight: 800,
              fontSize: big ? 112 : 46,
              letterSpacing: big ? -3 : -0.8,
              lineHeight: big ? 1.05 : 1.2,
              color: ink,
              marginTop: i === 0 ? 34 : 4,
              visibility: shown(f, i) ? 'visible' : 'hidden',
            }}
          >
            <Accent text={l} />
          </div>
        );
      })}
    </>
  );
};

const Stamp: React.FC<{text: string; at: number}> = ({text, at}) => {
  const f = useCurrentFrame();
  if (f < at) return null;
  return (
    <div style={{marginTop: 46, border: `5px solid ${C.pink}`, color: C.pink, fontFamily: SANS, fontWeight: 900, fontSize: 48, letterSpacing: -0.5, padding: '4px 22px', borderRadius: 10, transform: 'rotate(-5deg)'}}>
      {text}
    </div>
  );
};

// Position mesurée sur Saveo : le contenu des cartes part du haut (fait/stat ≈ 17 %, règle ≈ 34 % de la hauteur)
const Full: React.FC<{bg: string; top: number; children: React.ReactNode}> = ({bg, top, children}) => {
  const f = useCurrentFrame();
  return (
    <AbsoluteFill style={{background: bg, opacity: interpolate(f, [0, FADE], [0, 1], {extrapolateRight: 'clamp'})}}>
      <div style={{position: 'absolute', top, left: 90, right: 90, display: 'flex', flexDirection: 'column', alignItems: 'center', textAlign: 'center'}}>
        {children}
      </div>
    </AbsoluteFill>
  );
};

const Stat: React.FC<{c: any}> = ({c}) => (
  <Full bg={C.dark} top={330}>
    <Kicker text={c.kicker} color="rgba(255,255,255,0.5)" />
    <Lines lines={c.lines} dark />
  </Full>
);

const Fact: React.FC<{c: any}> = ({c}) => (
  <Full bg={C.cream} top={330}>
    <Kicker text={c.kicker} color="rgba(0,0,0,0.42)" />
    <Lines lines={c.lines} dark={false} />
    {c.stamp && <Stamp text={c.stamp} at={FADE + c.lines.length * STEP + 18} />}
  </Full>
);

const Rule: React.FC<{c: any}> = ({c}) => (
  <Full bg={C.dark} top={650}>
    <Kicker text={c.kicker} color={C.pink} />
    <div style={{fontFamily: SANS, fontWeight: 800, fontSize: 64, letterSpacing: -1.5, lineHeight: 1.1, color: 'white', marginTop: 26}}>
      <Accent text={c.text} />
    </div>
  </Full>
);

// SMS par-dessus l'image : en-tête mono + bulles grises, une par une
const Sms: React.FC<{c: any}> = ({c}) => {
  const f = useCurrentFrame();
  return (
    <div style={{position: 'absolute', top: 1180, left: 90, right: 90}}>
      <div style={{fontFamily: MONO, fontWeight: 600, fontSize: 20, letterSpacing: 3, color: 'rgba(255,255,255,0.8)', marginBottom: 14}}>{c.from}</div>
      {c.msgs.map((m: string, i: number) =>
        shown(f, i * 4) ? (
          <div key={i} style={{display: 'flex', marginBottom: 12}}>
            <div style={{background: 'rgba(60,58,62,0.92)', color: 'white', fontFamily: SANS, fontWeight: 700, fontSize: 42, padding: '12px 24px', borderRadius: 22}}>{m}</div>
          </div>
        ) : null,
      )}
    </div>
  );
};

// Vote par-dessus la dernière image : « COMMENTE UN MOT » puis les deux boutons, l'un après l'autre
const Vote: React.FC<{c: any; beat: Beat}> = ({c, beat}) => {
  const f = useCurrentFrame();
  const at = Math.round((c.at ?? 0) * 30);
  if (f < at) return null;
  const btn = (word: string, hot: boolean, i: number) =>
    shown(f, i + 1, at) ? (
      <div style={{background: hot ? C.pink : C.cream, color: hot ? 'white' : C.ink, fontFamily: SANS, fontWeight: 900, fontSize: 60, letterSpacing: -1, padding: '8px 38px', borderRadius: 16}}>{word}</div>
    ) : (
      <div style={{width: 260}} />
    );
  void beat;
  return (
    <div style={{position: 'absolute', top: 1360, left: 0, right: 0, textAlign: 'center'}}>
      <div style={{fontFamily: MONO, fontWeight: 600, fontSize: 20, letterSpacing: 4, color: 'rgba(255,255,255,0.85)'}}>COMMENTE UN MOT</div>
      <div style={{display: 'flex', justifyContent: 'center', gap: 28, marginTop: 18}}>
        {btn(c.left.word, false, 0)}
        {btn(c.right.word, true, 1)}
      </div>
    </div>
  );
};

export const Cards: React.FC<{card: any; beat: Beat; available: string[]}> = ({card, beat}) => {
  switch (card.type) {
    case 'stat':
      return <Stat c={card} />;
    case 'fact':
      return <Fact c={card} />;
    case 'rule':
      return <Rule c={card} />;
    case 'sms':
      return <Sms c={card} />;
    case 'vote':
      return <Vote c={card} beat={beat} />;
    default:
      return null;
  }
};
