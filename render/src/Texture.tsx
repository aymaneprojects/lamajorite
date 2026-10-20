import {AbsoluteFill, useCurrentFrame, useVideoConfig} from 'remotion';
import {plus} from './motion';

export const Texture: React.FC = () => {
  const f = useCurrentFrame();
  const {width, height} = useVideoConfig();
  if (!plus()) return null;
  const seed = f % 8;
  return (
    <AbsoluteFill style={{pointerEvents: 'none'}}>
      <svg width={width} height={height} style={{position: 'absolute', opacity: 0.07, mixBlendMode: 'overlay'}}>
        <filter id={`n${seed}`}>
          <feTurbulence type="fractalNoise" baseFrequency="0.85" numOctaves="2" seed={seed} />
        </filter>
        <rect width="100%" height="100%" filter={`url(#n${seed})`} />
      </svg>
    </AbsoluteFill>
  );
};
