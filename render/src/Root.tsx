import {Composition, staticFile} from 'remotion';
import {Episode} from './Episode';
import type {Timeline} from './types';

export const Root: React.FC = () => (
  <Composition
    id="Episode"
    component={Episode as any}
    width={1080}
    height={1920}
    fps={30}
    durationInFrames={300}
    defaultProps={{episode: 'P1'}}
    calculateMetadata={async ({props}) => {
      const ep = (props as any).episode as string;
      const tl: Timeline = await fetch(staticFile(`${ep}/timeline.json`)).then((r) => r.json());
      return {durationInFrames: Math.ceil(tl.duration * 30), props: {...props, timeline: tl}};
    }}
  />
);
