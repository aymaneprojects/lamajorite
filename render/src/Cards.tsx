import {AbsoluteFill, Img, interpolate, spring, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';
import type {Beat} from './types';
import {Accent, C, MONO, SANS} from './theme';
import {shake} from './Fx';

const usePop = (delay = 0, damping = 13) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  return spring({frame: frame - delay, fps, config: {damping, mass: 0.7}});
};

const Kicker: React.FC<{children: React.ReactNode; color?: string}> = ({children, color = 'rgba(255,255,255,0.5)'}) => {
  const f = useCurrentFrame();
  const txt = String(children);
  const n = Math.floor(interpolate(f, [0, 14], [0, txt.length], {extrapolateRight: 'clamp'}));
  return (
    <div style={{fontFamily: MONO, fontSize: 26, letterSpacing: 6, color, textTransform: 'uppercase'}}>
      {txt.slice(0, n)}
      <span style={{opacity: f % 16 < 8 ? 1 : 0}}>▍</span>
    </div>
  );
};

// fond sombre vivant : halo qui respire
const DarkBg: React.FC<{children: React.ReactNode}> = ({children}) => {
  const f = useCurrentFrame();
  return (
    <AbsoluteFill style={{background: C.dark}}>
      <AbsoluteFill style={{background: `radial-gradient(circle at 50% ${45 + Math.sin(f / 30) * 4}%, rgba(255,46,126,0.13) 0%, rgba(0,0,0,0) 55%)`}} />
      {children}
    </AbsoluteFill>
  );
};

// "9 840 000 €" défile depuis 0 ; texte non numérique = pop simple
const CountUp: React.FC<{value: string; delay: number}> = ({value, delay}) => {
  const f = useCurrentFrame();
  const raw = value.replace(/\*/g, '');
  const m = raw.match(/^([\d  ]*\d)(.*)$/);
  if (!m) return <Accent text={value} />;
  const target = parseInt(m[1].replace(/\D/g, ''), 10);
  const k = interpolate(f - delay, [0, 22], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  const n = Math.round(target * (1 - Math.pow(1 - k, 3)));
  const accent = value.startsWith('*');
  return <span style={{color: accent ? C.pink : undefined}}>{n.toLocaleString('fr-FR').replace(/ | /g, ' ')}{m[2]}</span>;
};

const Stat: React.FC<{c: any}> = ({c}) => {
  const f = useCurrentFrame();
  const p = usePop(4);
  const p2 = usePop(10, 10);
  const sh = shake(f, 10, 8, 10);
  return (
    <DarkBg>
      <AbsoluteFill style={{justifyContent: 'center', alignItems: 'center', textAlign: 'center', padding: 80}}>
        <Kicker>{c.kicker}</Kicker>
        <div style={{fontFamily: SANS, fontWeight: 700, color: 'rgba(255,255,255,0.8)', fontSize: 40, marginTop: 50, opacity: p, transform: `translateY(${(1 - p) * 20}px)`}}>{c.label}</div>
        <div style={{fontFamily: SANS, fontWeight: 800, color: 'white', fontSize: 150, letterSpacing: -4, marginTop: 10, transform: `translate(${sh.x}px, ${sh.y}px) scale(${0.6 + 0.4 * p2})`, opacity: p2, fontVariantNumeric: 'tabular-nums', textShadow: '0 0 40px rgba(255,46,126,0.25)'}}>
          <CountUp value={c.value} delay={10} />
        </div>
        {c.sub && <div style={{fontFamily: SANS, fontWeight: 700, color: 'rgba(255,255,255,0.6)', fontSize: 40, marginTop: 10, opacity: usePop(24)}}>{c.sub}</div>}
      </AbsoluteFill>
    </DarkBg>
  );
};

// texte qui apparaît mot par mot
const Words: React.FC<{text: string; delay: number; style: React.CSSProperties}> = ({text, delay, style}) => {
  const f = useCurrentFrame();
  // découpe sur les espaces hors *accent* : « *Partie 2*. » reste un seul bloc
  const parts = text.match(/(?:\*[^*]+\*|[^\s*])+/g) ?? [];
  return (
    <div style={style}>
      {parts.map((w, i) => {
        const p = interpolate(f - delay - i * 2.2, [0, 6], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
        return (
          <span key={i} style={{display: 'inline-block', marginRight: '0.25em', opacity: p, transform: `translateY(${(1 - p) * 18}px)`}}>
            <Accent text={w} />
          </span>
        );
      })}
    </div>
  );
};

const Stamp: React.FC<{text: string; delay: number; size?: number}> = ({text, delay, size = 64}) => {
  const st = usePop(delay, 9);
  return (
    <div style={{marginTop: 60, border: `6px solid ${C.pink}`, color: C.pink, fontFamily: SANS, fontWeight: 800, fontSize: size, padding: '8px 30px', borderRadius: 12, transform: `rotate(-6deg) scale(${interpolate(st, [0, 1], [2.4, 1])})`, opacity: Math.min(1, st * 1.5)}}>
      {text}
    </div>
  );
};

const Fact: React.FC<{c: any}> = ({c}) => {
  const f = useCurrentFrame();
  const t2 = 12 + c.text.split(' ').length * 2.2;
  const stampAt = Math.round(t2 + (c.text2 ? c.text2.split(' ').length * 2.2 + 10 : 6));
  const sh = c.stamp ? shake(f, stampAt + 4, 10, 14) : {x: 0, y: 0};
  return (
    <AbsoluteFill style={{background: C.cream, transform: `translate(${sh.x}px, ${sh.y}px)`}}>
      <AbsoluteFill style={{justifyContent: 'center', alignItems: 'center', textAlign: 'center', padding: 90}}>
        <Kicker color="rgba(0,0,0,0.5)">{c.kicker}</Kicker>
        <Words text={c.text} delay={12} style={{fontFamily: SANS, fontWeight: 800, color: C.ink, fontSize: 70, lineHeight: 1.12, marginTop: 50}} />
        {c.arrow && <div style={{fontFamily: SANS, fontWeight: 800, fontSize: 80, color: C.ink, margin: '24px 0', opacity: interpolate(f, [t2, t2 + 6], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'}), transform: `translateY(${Math.sin(f / 5) * 6}px)`}}>↓</div>}
        {c.text2 && <Words text={c.text2} delay={t2 + 6} style={{fontFamily: SANS, fontWeight: 800, color: C.ink, fontSize: 70, lineHeight: 1.12}} />}
        {c.stamp && <Stamp text={c.stamp} delay={stampAt} />}
        {c.source && <div style={{position: 'absolute', bottom: 330, fontFamily: MONO, fontSize: 22, color: 'rgba(0,0,0,0.4)'}}>{c.source}</div>}
      </AbsoluteFill>
    </AbsoluteFill>
  );
};

const Rule: React.FC<{c: any}> = ({c}) => (
  <DarkBg>
    <AbsoluteFill style={{justifyContent: 'center', alignItems: 'center', textAlign: 'center', padding: 90}}>
      <Kicker color={C.pink}>{c.kicker}</Kicker>
      <Words text={c.text} delay={10} style={{fontFamily: SANS, fontWeight: 800, color: 'white', fontSize: 84, lineHeight: 1.1, marginTop: 30}} />
      {c.stamp && <Stamp text={c.stamp} delay={30} size={70} />}
    </AbsoluteFill>
  </DarkBg>
);

const Sms: React.FC<{c: any}> = ({c}) => {
  const frame = useCurrentFrame();
  const sh = shake(frame, 0, 14, 9);
  return (
    <div style={{position: 'absolute', top: 680, left: 80, right: 80, transform: `translate(${sh.x}px, ${sh.y}px)`}}>
      <div style={{fontFamily: MONO, fontSize: 24, letterSpacing: 4, color: 'rgba(255,255,255,0.8)', marginBottom: 18, textShadow: '0 2px 10px #000'}}>{c.from}</div>
      {c.msgs.map((m: string, i: number) => {
        const at = 8 + i * 22;
        const typing = frame >= at - 12 && frame < at;
        const p = spring({frame: frame - at, fps: 30, config: {damping: 13}});
        return (
          <div key={i} style={{display: 'flex', marginBottom: 14}}>
            {typing ? (
              <div style={{background: 'rgba(235,235,240,0.9)', borderRadius: 26, padding: '22px 28px', display: 'flex', gap: 10}}>
                {[0, 1, 2].map((d) => (
                  <div key={d} style={{width: 14, height: 14, borderRadius: 7, background: '#666', transform: `translateY(${Math.sin((frame + d * 4) / 3) * 4}px)`}} />
                ))}
              </div>
            ) : frame >= at ? (
              <div style={{background: 'rgba(240,240,245,0.95)', color: '#111', fontFamily: SANS, fontWeight: 700, fontSize: 50, padding: '16px 28px', borderRadius: 26, transform: `scale(${0.7 + 0.3 * p})`, transformOrigin: 'left center', boxShadow: '0 10px 30px rgba(0,0,0,0.5)'}}>{m}</div>
            ) : null}
          </div>
        );
      })}
    </div>
  );
};

const Vote: React.FC<{c: any; available: string[]}> = ({c, available}) => {
  const f = useCurrentFrame();
  const p = usePop(2);
  const p2 = usePop(12, 9);
  const panel = (side: any, hot: boolean, i: number) => {
    const has = available.includes(side.img);
    const pulse = hot ? 1 + 0.05 * Math.sin(f / 4) : 1;
    const zoom = interpolate(f, [0, 200], [1.05, 1.2], {extrapolateRight: 'clamp'});
    return (
      <div style={{flex: 1, display: 'flex', flexDirection: 'column', alignItems: 'center', transform: `translateY(${(1 - p) * (i ? 120 : -120)}px)`, opacity: p}}>
        <div style={{width: '100%', height: 760, borderRadius: 26, overflow: 'hidden', background: '#221d2c', border: hot ? `4px solid ${C.pink}` : '4px solid rgba(255,255,255,0.15)', boxShadow: hot ? `0 0 ${30 + 20 * Math.sin(f / 4)}px rgba(255,46,126,0.5)` : 'none'}}>
          {has && <Img src={staticFile(side.src)} style={{width: '100%', height: '100%', objectFit: 'cover', transform: `scale(${zoom})`}} />}
        </div>
        <div style={{marginTop: -50, background: hot ? C.pink : C.cream, color: hot ? 'white' : C.ink, fontFamily: SANS, fontWeight: 800, fontSize: 66, padding: '10px 34px', borderRadius: 18, transform: `scale(${(0.5 + 0.5 * p2) * pulse})`, boxShadow: '0 10px 30px rgba(0,0,0,0.5)'}}>
          {side.word}
        </div>
        <div style={{fontFamily: MONO, fontSize: 22, color: 'rgba(255,255,255,0.6)', marginTop: 14}}>{side.sub}</div>
      </div>
    );
  };
  return (
    <DarkBg>
      <AbsoluteFill style={{padding: '220px 60px 0', alignItems: 'center'}}>
        <Kicker>Commente un seul mot</Kicker>
        <div style={{display: 'flex', gap: 34, width: '100%', marginTop: 36}}>
          {panel(c.left, false, 0)}
          {panel(c.right, true, 1)}
        </div>
        <Words text={c.footer} delay={22} style={{fontFamily: SANS, fontWeight: 800, color: 'white', fontSize: 60, marginTop: 70}} />
        <div style={{fontSize: 70, marginTop: 10, transform: `translateY(${Math.abs(Math.sin(f / 6)) * 16}px)`, opacity: usePop(34), color: C.pink}}>↓</div>
      </AbsoluteFill>
    </DarkBg>
  );
};

// résultats du vote précédent : barres qui se remplissent
const Results: React.FC<{c: any}> = ({c}) => {
  const f = useCurrentFrame();
  return (
    <AbsoluteFill style={{background: C.cream, padding: '0 90px', justifyContent: 'center'}}>
      <div style={{textAlign: 'center'}}>
        <Kicker color="rgba(0,0,0,0.5)">{c.kicker}</Kicker>
      </div>
      {c.rows.map((r: any, i: number) => {
        const k = interpolate(f - 10 - i * 4, [0, 30], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
        const pct = Math.round(r.pct * (1 - Math.pow(1 - k, 3)));
        return (
          <div key={i} style={{marginTop: 50}}>
            <div style={{display: 'flex', justifyContent: 'space-between', fontFamily: SANS, fontWeight: 800, fontSize: 56, color: i === 0 ? C.pink : C.ink}}>
              <span>{r.label}</span>
              <span style={{fontVariantNumeric: 'tabular-nums'}}>{pct} %</span>
            </div>
            <div style={{height: 22, background: 'rgba(0,0,0,0.1)', borderRadius: 11, marginTop: 12, overflow: 'hidden'}}>
              <div style={{width: `${pct}%`, height: '100%', background: i === 0 ? C.pink : C.ink, borderRadius: 11}} />
            </div>
          </div>
        );
      })}
      {c.stamp && (
        <div style={{display: 'flex', justifyContent: 'center'}}>
          <Stamp text={c.stamp} delay={48} />
        </div>
      )}
    </AbsoluteFill>
  );
};

const Persons: React.FC<{c: any}> = ({c}) => {
  const f = useCurrentFrame();
  const p = usePop(2);
  return (
    <AbsoluteFill style={{background: '#2a221c', justifyContent: 'center', alignItems: 'center'}}>
      <div style={{background: '#f3eddf', width: 860, padding: '40px 50px', transform: `rotate(${-1.5 + (1 - p) * -8}deg) scale(${0.8 + 0.2 * p})`, opacity: p, boxShadow: '0 20px 60px rgba(0,0,0,0.6)'}}>
        <div style={{position: 'absolute', top: -14, left: '50%', width: 28, height: 28, borderRadius: 14, background: C.pink, boxShadow: '0 4px 8px rgba(0,0,0,0.4)'}} />
        <div style={{fontFamily: MONO, fontSize: 24, letterSpacing: 4, color: 'rgba(0,0,0,0.55)'}}>{c.kicker}</div>
        <div style={{columnCount: 2, marginTop: 24}}>
          {c.names.map((n: string, i: number) => (
            <div key={i} style={{fontFamily: MONO, fontSize: 30, color: '#1d1a17', lineHeight: 1.5, opacity: interpolate(f - 8 - i * 1.5, [0, 5], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'})}}>{n}</div>
          ))}
        </div>
      </div>
    </AbsoluteFill>
  );
};

const Comment: React.FC<{c: any}> = ({c}) => {
  const p = usePop(4);
  return (
    <div style={{position: 'absolute', top: 960, left: 60, right: 60, opacity: p, transform: `translateY(${(1 - p) * 60}px) scale(${0.9 + 0.1 * p})`}}>
      <div style={{fontFamily: MONO, fontSize: 22, letterSpacing: 4, color: 'rgba(255,255,255,0.8)', marginBottom: 12}}>{c.kicker}</div>
      <div style={{background: 'rgba(15,15,18,0.92)', borderRadius: 22, padding: '24px 28px', display: 'flex', gap: 20, alignItems: 'flex-start', boxShadow: '0 20px 50px rgba(0,0,0,0.6)'}}>
        <div style={{width: 64, height: 64, borderRadius: 32, background: 'linear-gradient(135deg,#555,#333)', flexShrink: 0}} />
        <div style={{flex: 1}}>
          <div style={{fontFamily: SANS, fontWeight: 700, fontSize: 26, color: 'rgba(255,255,255,0.55)'}}>{c.user}</div>
          <Words text={c.text} delay={10} style={{fontFamily: SANS, fontWeight: 700, fontSize: 40, color: 'white', marginTop: 4}} />
        </div>
        <div style={{fontFamily: SANS, fontWeight: 700, fontSize: 26, color: C.pink}}>♥ {c.likes}</div>
      </div>
    </div>
  );
};

export const Cards: React.FC<{card: any; beat: Beat; available: string[]}> = ({card, available}) => {
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
      return <Vote c={card} available={available} />;
    case 'results':
      return <Results c={card} />;
    case 'persons':
      return <Persons c={card} />;
    case 'comment':
      return <Comment c={card} />;
    default:
      return null;
  }
};
