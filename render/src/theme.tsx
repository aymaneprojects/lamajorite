import {staticFile} from 'remotion';

export const C = {
  pink: '#ff2e7e',
  cream: '#efe9de',
  ink: '#16120f',
  dark: '#141110',
  grey: 'rgba(255,255,255,0.45)',
};

export const fontsCss = `
@font-face{font-family:Inter;font-weight:500;src:url(${staticFile('fonts/Inter-Medium.otf')})}
@font-face{font-family:Inter;font-weight:700;src:url(${staticFile('fonts/Inter-Bold.otf')})}
@font-face{font-family:Inter;font-weight:800;src:url(${staticFile('fonts/Inter-ExtraBold.otf')})}
@font-face{font-family:Inter;font-weight:900;src:url(${staticFile('fonts/Inter-Black.otf')})}
@font-face{font-family:Mono;src:url(${staticFile('fonts/DejaVuSansMono.ttf')})}
`;

export const SANS = 'Inter, sans-serif';
export const MONO = 'Mono, monospace';

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
