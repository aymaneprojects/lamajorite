import {AbsoluteFill, Audio, Sequence, staticFile, useVideoConfig} from 'remotion';
import type {Beat, Timeline} from './types';
import {fontsCss} from './theme';
import {Scene} from './Scene';
import {Cards} from './Cards';
import {HudBar} from './HudBar';
import {Captions} from './Captions';
import {Overlay} from './Overlay';
import {Grain} from './Fx';

type Sfx = {at: number; src: string; vol: number};


// Bruitages placés automatiquement d'après le contenu des beats
const sfxFor = (beats: Beat[]): Sfx[] => {
  const out: Sfx[] = [];
  beats.forEach((b, i) => {
    const s = b.start;
    if (i > 0 && b.kind === 'img' && !b.card) out.push({at: s, src: 'whoosh', vol: 0.5});
    if (b.overlay?.type === 'hook') out.push({at: s + 0.05, src: 'impact', vol: 0.6});
    const c = b.card;
    if (c && ['stat', 'fact', 'rule', 'results', 'persons'].includes(c.type)) out.push({at: s, src: 'impact', vol: 0.4});
    if (c?.type === 'fact' && c.stamp) {
      const t2 = 12 + c.text.split(' ').length * 2.2;
      const stampAt = t2 + (c.text2 ? c.text2.split(' ').length * 2.2 + 10 : 6);
      out.push({at: s + (stampAt + 4) / 30, src: 'stamp', vol: 0.6});
    }
    if (c?.type === 'rule' && c.stamp) out.push({at: s + 34 / 30, src: 'stamp', vol: 0.6});
    if (c?.type === 'sms') {
      out.push({at: s, src: 'buzz', vol: 0.5});
      c.msgs.forEach((_: string, k: number) => out.push({at: s + (8 + k * 22) / 30, src: 'pop', vol: 0.4}));
    }
    if (c?.type === 'vote') out.push({at: Math.max(0, s - 3), src: 'riser', vol: 0.35}, {at: s, src: 'impact', vol: 0.5});
  });
  return out;
};

export const Episode: React.FC<{episode: string; timeline: Timeline}> = ({timeline: tl}) => {
  const {fps} = useVideoConfig();
  const f = (s: number) => Math.round(s * fps);
  return (
    <AbsoluteFill style={{backgroundColor: '#0b0a0a'}}>
      <style>{fontsCss}</style>
      {tl.beats.map((b) => (
        <Sequence key={b.i} from={f(b.start)} durationInFrames={Math.max(1, f(b.end) - f(b.start))} name={b.id}>
          {b.image && <Scene beat={b} available={tl.available} layers={tl.layers ?? []} words={tl.words} />}
          {b.overlay && <Overlay o={b.overlay} />}
          {b.card && <Cards card={b.card} beat={b} available={tl.available} />}
        </Sequence>
      ))}
      <Grain />
      <HudBar beats={tl.beats} episode={tl.episode} />
      <Captions words={tl.words} beats={tl.beats} />
      {/* Seule la piste d'effets sort du rendu. Voix + musique + effets sont mixés ensuite par pipeline/mix.py
          (voix devant, musique dessous avec effacement doux, effets en arrière-plan). */}
      {sfxFor(tl.beats).map((s, i) => (
        <Sequence key={`sfx${i}`} from={f(s.at)} durationInFrames={f(3.2)} name={`sfx-${s.src}`}>
          <Audio src={staticFile(`sfx/${s.src}.wav`)} volume={s.vol} />
        </Sequence>
      ))}
    </AbsoluteFill>
  );
};
