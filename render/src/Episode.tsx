import {AbsoluteFill, Audio, Sequence, staticFile, useVideoConfig} from 'remotion';
import type {Beat, Timeline} from './types';
import {fontsCss} from './theme';
import {FADE, Scene} from './Scene';
import {Cards} from './Cards';
import {HudBar} from './HudBar';
import {Captions} from './Captions';
import {Overlay} from './Overlay';

type Sfx = {at: number; src: string; vol: number};


// Bruitages placés automatiquement d'après le contenu des beats
const sfxFor = (beats: Beat[]): Sfx[] => {
  // Effets réduits au strict nécessaire (troisième plan sonore) : souffle léger à l'entrée des cartes,
  // « pop » des bulles SMS, tampon. Calés sur les images des cartes (voir Cards.tsx).
  const out: Sfx[] = [];
  beats.forEach((b) => {
    const s = b.start;
    const c = b.card;
    if (c && ['stat', 'fact', 'rule'].includes(c.type)) out.push({at: s, src: 'whoosh', vol: 0.6});
    if (c?.type === 'fact' && c.stamp) out.push({at: s + (FADE + c.lines.length * 5 + 18) / 30, src: 'stamp', vol: 0.8});
    if (c?.type === 'sms') c.msgs.forEach((_: string, k: number) => out.push({at: s + (FADE + k * 20) / 30, src: 'pop', vol: 0.7}));
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
        // chaque plan déborde de FADE images sur le suivant : le suivant apparaît en fondu par-dessus
        <Sequence key={b.i} from={f(b.start)} durationInFrames={Math.max(1, f(b.end) - f(b.start)) + FADE} name={b.id}>
          {b.image && <Scene beat={b} available={tl.available} first={b.i === 0} />}
          {/* textes et cartes posés sur l'image s'arrêtent net à la fin du plan (pas pendant le fondu suivant) */}
          <Sequence durationInFrames={Math.max(1, f(b.end) - f(b.start))} layout="none">
            {b.overlay && <Overlay o={b.overlay} />}
            {b.card && !['stat', 'fact', 'rule'].includes(b.card.type) && <Cards card={b.card} beat={b} available={tl.available} />}
          </Sequence>
          {b.card && ['stat', 'fact', 'rule'].includes(b.card.type) && <Cards card={b.card} beat={b} available={tl.available} />}
        </Sequence>
      ))}
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
