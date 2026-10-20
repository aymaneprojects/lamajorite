export type Word = {w: string; t0: number; t1: number};
export type Hud = {cash?: number; bank?: number; susp?: number};
export type Beat = {
  i: number;
  start: number;
  end: number;
  kind: 'img' | 'card';
  id: string;
  image: string | null;
  prompt: string;
  overlay: any;
  card: any;
  hud: Hud | null;
};
export type Timeline = {
  episode: string;
  title: string;
  fps: number;
  duration: number;
  voice: string;
  music: string;
  words: Word[];
  beats: Beat[];
  available: string[];
  layers?: string[];
};
