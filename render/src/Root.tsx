import {Composition, staticFile} from 'remotion';
import {Episode} from './Episode';
import {Avatar, Cover, Highlight} from './Branding';
import type {Timeline} from './types';

export const Root: React.FC = () => (
  <>
  <Composition id="Cover" component={Cover as any} width={1080} height={1920} fps={30} durationInFrames={1}
    defaultProps={{n: 1, title: 'Le box 117', img: 'brand/X_cover_P1.png'}} />
  <Composition id="Highlight" component={Highlight as any} width={1080} height={1920} fps={30} durationInFrames={1}
    defaultProps={{icon: 'votes'}} />
  <Composition id="Avatar" component={Avatar as any} width={1080} height={1080} fps={30} durationInFrames={1}
    defaultProps={{img: 'brand/X_cover_P1.png'}} />
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

  </>
);
