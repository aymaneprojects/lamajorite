import {AbsoluteFill, Img, interpolate, spring, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';
import type {Beat} from './types';
import {Accent, C, MONO, SANS} from './theme';

const usePop = (delay = 0) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  return spring({frame: frame - delay, fps, config: {damping: 13, mass: 0.7}});
};

const Kicker: React.FC<{children: React.ReactNode; color?: string}> = ({children, color = 'rgba(255,255,255,0.45)'}) => (
  <div style={{fontFamily: MONO, fontSize: 26, letterSpacing: 6, color, textTransform: 'uppercase'}}>{children}</div>
);

const Stat: React.FC<{c: any}> = ({c}) => {
  const p = usePop();
  const p2 = usePop(6);
  return (
    <AbsoluteFill style={{background: C.dark, justifyContent: 'center', alignItems: 'center', textAlign: 'center', padding: 80}}>
      <Kicker>{c.kicker}</Kicker>
      <div style={{fontFamily: SANS, fontWeight: 700, color: 'rgba(255,255,255,0.8)', fontSize: 40, marginTop: 50, opacity: p}}>{c.label}</div>
      <div style={{fontFamily: SANS, fontWeight: 900, color: 'white', fontSize: 150, letterSpacing: -4, marginTop: 10, transform: `scale(${0.7 + 0.3 * p2})`, opacity: p2}}>
        <Accent text={c.value} />
      </div>
      {c.sub && <div style={{fontFamily: SANS, fontWeight: 700, color: 'rgba(255,255,255,0.6)', fontSize: 40, marginTop: 10, opacity: p2}}>{c.sub}</div>}
    </AbsoluteFill>
  );
};

const Fact: React.FC<{c: any}> = ({c}) => {
  const p = usePop();
  const p2 = usePop(14);
  const st = usePop(26);
  return (
    <AbsoluteFill style={{background: C.cream, justifyContent: 'center', alignItems: 'center', textAlign: 'center', padding: 90}}>
      <Kicker color="rgba(0,0,0,0.45)">{c.kicker}</Kicker>
      <div style={{fontFamily: SANS, fontWeight: 900, color: C.ink, fontSize: 70, lineHeight: 1.12, marginTop: 50, opacity: p, transform: `translateY(${(1 - p) * 30}px)`}}>
        <Accent text={c.text} />
      </div>
      {c.arrow && <div style={{fontFamily: SANS, fontWeight: 900, fontSize: 80, color: C.ink, margin: '24px 0', opacity: p2}}>↓</div>}
      {c.text2 && (
        <div style={{fontFamily: SANS, fontWeight: 900, color: C.ink, fontSize: 70, lineHeight: 1.12, opacity: p2}}>
          <Accent text={c.text2} />
        </div>
      )}
      {c.stamp && (
        <div
          style={{
            marginTop: 60,
            border: `6px solid ${C.pink}`,
            color: C.pink,
            fontFamily: SANS,
            fontWeight: 900,
            fontSize: 64,
            padding: '8px 30px',
            borderRadius: 12,
            transform: `rotate(-6deg) scale(${interpolate(st, [0, 1], [2, 1])})`,
            opacity: st,
          }}
        >
          {c.stamp}
        </div>
      )}
      {c.source && <div style={{position: 'absolute', bottom: 330, fontFamily: MONO, fontSize: 22, color: 'rgba(0,0,0,0.4)'}}>{c.source}</div>}
    </AbsoluteFill>
  );
};

const Rule: React.FC<{c: any}> = ({c}) => {
  const p = usePop();
  const st = usePop(20);
  return (
    <AbsoluteFill style={{background: C.dark, justifyContent: 'center', alignItems: 'center', textAlign: 'center', padding: 90}}>
      <Kicker color={C.pink}>{c.kicker}</Kicker>
      <div style={{fontFamily: SANS, fontWeight: 900, color: 'white', fontSize: 84, lineHeight: 1.1, marginTop: 30, opacity: p}}>{c.text}</div>
      {c.stamp && (
        <div style={{marginTop: 70, border: `6px solid ${C.pink}`, color: C.pink, fontFamily: SANS, fontWeight: 900, fontSize: 70, padding: '6px 30px', borderRadius: 12, transform: `rotate(-6deg) scale(${interpolate(st, [0, 1], [2, 1])})`, opacity: st}}>
          {c.stamp}
        </div>
      )}
    </AbsoluteFill>
  );
};

const Sms: React.FC<{c: any}> = ({c}) => {
  const frame = useCurrentFrame();
  return (
    <div style={{position: 'absolute', top: 700, left: 90, right: 90}}>
      <div style={{fontFamily: MONO, fontSize: 24, letterSpacing: 4, color: 'rgba(255,255,255,0.75)', marginBottom: 18}}>{c.from}</div>
      {c.msgs.map((m: string, i: number) => {
        const p = spring({frame: frame - i * 20, fps: 30, config: {damping: 14}});
        return (
          <div key={i} style={{display: 'flex', marginBottom: 14, opacity: p, transform: `translateY(${(1 - p) * 20}px)`}}>
            <div style={{background: 'rgba(235,235,240,0.92)', color: '#111', fontFamily: SANS, fontWeight: 700, fontSize: 48, padding: '16px 28px', borderRadius: 26}}>{m}</div>
          </div>
        );
      })}
    </div>
  );
};

const Vote: React.FC<{c: any; available: string[]}> = ({c, available}) => {
  const p = usePop();
  const p2 = usePop(10);
  const panel = (side: any, hot: boolean) => {
    const has = available.includes(side.img);
    return (
      <div style={{flex: 1, display: 'flex', flexDirection: 'column', alignItems: 'center'}}>
        <div style={{width: '100%', height: 760, borderRadius: 26, overflow: 'hidden', background: '#221d2c', border: hot ? `4px solid ${C.pink}` : '4px solid rgba(255,255,255,0.15)'}}>
          {has && <Img src={staticFile(side.src)} style={{width: '100%', height: '100%', objectFit: 'cover'}} />}
        </div>
        <div
          style={{
            marginTop: -50,
            background: hot ? C.pink : C.cream,
            color: hot ? 'white' : C.ink,
            fontFamily: SANS,
            fontWeight: 900,
            fontSize: 66,
            padding: '10px 34px',
            borderRadius: 18,
            transform: `scale(${0.6 + 0.4 * p2})`,
          }}
        >
          {side.word}
        </div>
        <div style={{fontFamily: MONO, fontSize: 22, color: 'rgba(255,255,255,0.55)', marginTop: 14}}>{side.sub}</div>
      </div>
    );
  };
  return (
    <AbsoluteFill style={{background: C.dark, padding: '230px 60px 0', alignItems: 'center'}}>
      <Kicker>Commente un seul mot</Kicker>
      <div style={{display: 'flex', gap: 34, width: '100%', marginTop: 36, opacity: p}}>
        {panel(c.left, false)}
        {panel(c.right, true)}
      </div>
      <div style={{fontFamily: SANS, fontWeight: 900, color: 'white', fontSize: 60, marginTop: 70, opacity: p2}}>
        <Accent text={c.footer} />
      </div>
    </AbsoluteFill>
  );
};

const Persons: React.FC<{c: any}> = ({c}) => {
  const p = usePop();
  return (
    <AbsoluteFill style={{background: '#2a221c', justifyContent: 'center', alignItems: 'center'}}>
      <div style={{background: '#f3eddf', width: 860, padding: '40px 50px', transform: `rotate(-1.5deg) scale(${0.9 + 0.1 * p})`, opacity: p, boxShadow: '0 20px 60px rgba(0,0,0,0.6)'}}>
        <div style={{fontFamily: MONO, fontSize: 24, letterSpacing: 4, color: 'rgba(0,0,0,0.55)'}}>{c.kicker}</div>
        <div style={{columnCount: 2, marginTop: 24}}>
          {c.names.map((n: string, i: number) => (
            <div key={i} style={{fontFamily: MONO, fontSize: 30, color: '#1d1a17', lineHeight: 1.5}}>{n}</div>
          ))}
        </div>
      </div>
    </AbsoluteFill>
  );
};

const Comment: React.FC<{c: any}> = ({c}) => {
  const p = usePop();
  return (
    <div style={{position: 'absolute', top: 980, left: 60, right: 60, opacity: p, transform: `translateY(${(1 - p) * 30}px)`}}>
      <div style={{fontFamily: MONO, fontSize: 22, letterSpacing: 4, color: 'rgba(255,255,255,0.7)', marginBottom: 12}}>{c.kicker}</div>
      <div style={{background: 'rgba(15,15,18,0.9)', borderRadius: 22, padding: '24px 28px', display: 'flex', gap: 20, alignItems: 'flex-start'}}>
        <div style={{width: 64, height: 64, borderRadius: 32, background: '#555', flexShrink: 0}} />
        <div style={{flex: 1}}>
          <div style={{fontFamily: SANS, fontWeight: 700, fontSize: 26, color: 'rgba(255,255,255,0.55)'}}>{c.user}</div>
          <div style={{fontFamily: SANS, fontWeight: 700, fontSize: 40, color: 'white', marginTop: 4}}>{c.text}</div>
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
    case 'persons':
      return <Persons c={card} />;
    case 'comment':
      return <Comment c={card} />;
    default:
      return null;
  }
};
