import {staticFile} from 'remotion';

export const C = {
  pink: '#ff2e7e',
  cream: '#efe9de',
  ink: '#16120f',
  dark: '#141110',
  grey: 'rgba(255,255,255,0.45)',
};

export const fontsCss = `
@font-face{font-family:InterTight;font-weight:100 900;src:url(${staticFile('fonts/InterTight-VF.ttf')})}
@font-face{font-family:JBMono;font-weight:100 800;src:url(${staticFile('fonts/JetBrainsMono-VF.ttf')})}
`;

export const SANS = 'InterTight, sans-serif';
export const MONO = 'JBMono, monospace';

// "texte *accent*" -> segments, l'accent en rose
export const Accent: React.FC<{text: string; color?: string}> = ({text, color = C.pink}) => (
  <>
    {text.split(/(\*[^*]+\*)/).map((s, i) =>
      s.startsWith('*') ? (
        <span key={i} style={{color}}>
          {s.slice(1, -1)}
        </span>
      ) : (
        <span key={i}>{s}</span>
      ),
    )}
  </>
);
