import {AbsoluteFill, Audio, Sequence, staticFile, useVideoConfig} from 'remotion';
import type {Timeline} from './types';
import {fontsCss} from './theme';
import {Scene} from './Scene';
import {Cards} from './Cards';
import {HudBar} from './HudBar';
import {Captions} from './Captions';
import {Overlay} from './Overlay';

export const Episode: React.FC<{episode: string; timeline: Timeline}> = ({timeline: tl}) => {
  const {fps} = useVideoConfig();
  const f = (s: number) => Math.round(s * fps);
  return (
    <AbsoluteFill style={{backgroundColor: '#0b0a0a'}}>
      <style>{fontsCss}</style>
      {tl.beats.map((b) => (
        <Sequence key={b.i} from={f(b.start)} durationInFrames={Math.max(1, f(b.end) - f(b.start))} name={b.id}>
          {b.image && <Scene beat={b} available={tl.available} />}
          {b.overlay && <Overlay o={b.overlay} />}
          {b.card && <Cards card={b.card} beat={b} available={tl.available} />}
        </Sequence>
      ))}
      <HudBar beats={tl.beats} />
      <Captions words={tl.words} beats={tl.beats} />
      <Audio src={staticFile(tl.voice)} />
      <Audio src={staticFile(tl.music)} volume={0.18} />
    </AbsoluteFill>
  );
};
