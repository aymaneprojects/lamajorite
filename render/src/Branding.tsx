import {AbsoluteFill, Img, staticFile} from 'remotion';
import {C, MONO, SANS, fontsCss} from './theme';

const NUM_COLORS = ['#ff2e7e', '#7fb2ff', '#52d68a', '#ffc94a', '#b98cff'];

// Miniature d'épisode (couverture Reels / TikTok). Le texte reste dans la zone 3:4 de la grille Instagram.
export const Cover: React.FC<{n: number; title: string; img: string}> = ({n, title, img}) => (
  <AbsoluteFill style={{background: C.dark}}>
    <style>{fontsCss}</style>
    <AbsoluteFill style={{top: 640}}>
      <Img src={staticFile(img)} style={{width: '100%', height: '100%', objectFit: 'cover', objectPosition: '50% 60%'}} />
      <AbsoluteFill style={{background: `linear-gradient(180deg, ${C.dark} 0%, rgba(20,17,16,0) 22%)`}} />
    </AbsoluteFill>
    <div style={{position: 'absolute', top: 300, left: 70, right: 70}}>
      <div style={{fontFamily: MONO, fontSize: 26, letterSpacing: 5, color: 'rgba(255,255,255,0.7)'}}>CHAQUE BILLET LAISSE UNE TRACE</div>
      <div style={{display: 'flex', alignItems: 'baseline', gap: 22, marginTop: 30}}>
        <span style={{fontFamily: SANS, fontWeight: 800, fontSize: 96, color: 'white', letterSpacing: -2}}>PARTIE</span>
        <span style={{fontFamily: SANS, fontWeight: 800, fontSize: 210, lineHeight: 0.8, color: NUM_COLORS[(n - 1) % NUM_COLORS.length]}}>{n}</span>
      </div>
      <div style={{width: 90, height: 8, background: NUM_COLORS[(n - 1) % NUM_COLORS.length], marginTop: 24}} />
      <div style={{fontFamily: SANS, fontWeight: 800, fontSize: 92, color: 'white', marginTop: 18, lineHeight: 1, letterSpacing: -2, textTransform: 'uppercase'}}>{title}</div>
    </div>
  </AbsoluteFill>
);

const ICONS: Record<string, React.ReactNode> = {
  votes: (
    <svg viewBox="0 0 100 100" width="420">
      <rect x="18" y="48" width="64" height="34" rx="6" fill={C.cream} />
      <rect x="30" y="44" width="40" height="6" rx="3" fill="#2b2522" />
      <rect x="36" y="14" width="28" height="34" rx="3" fill={C.pink} />
      <path d="M42 30 l6 6 l11 -13" stroke="white" strokeWidth="5" fill="none" strokeLinecap="round" strokeLinejoin="round" />
    </svg>
  ),
  youtube: (
    <svg viewBox="0 0 100 100" width="420">
      <rect x="14" y="24" width="72" height="50" rx="10" fill="none" stroke={C.cream} strokeWidth="7" />
      <path d="M43 38 L61 49 L43 60 Z" fill={C.pink} />
      <rect x="36" y="80" width="28" height="6" rx="3" fill={C.cream} />
    </svg>
  ),
  episodes: (
    <svg viewBox="0 0 100 100" width="420">
      <rect x="20" y="30" width="60" height="40" rx="6" fill={C.cream} />
      <path d="M20 30 l10 -12 h12 l-10 12 M42 30 l10 -12 h12 l-10 12" fill={C.pink} />
      <path d="M44 42 L58 50 L44 58 Z" fill="#2b2522" />
    </svg>
  ),
  regles: (
    <svg viewBox="0 0 100 100" width="420">
      <rect x="24" y="16" width="52" height="68" rx="5" fill={C.cream} />
      <rect x="34" y="32" width="32" height="5" rx="2" fill="#2b2522" />
      <rect x="34" y="45" width="32" height="5" rx="2" fill="#2b2522" />
      <rect x="34" y="58" width="20" height="5" rx="2" fill={C.pink} />
    </svg>
  ),
  dossier: (
    <svg viewBox="0 0 100 100" width="420">
      <path d="M14 30 h26 l6 7 h40 v43 h-72 Z" fill={C.cream} />
      <rect x="40" y="48" width="20" height="18" rx="3" fill={C.pink} />
      <path d="M44 48 v-5 a6 6 0 0 1 12 0 v5" stroke={C.pink} strokeWidth="4" fill="none" />
    </svg>
  ),
};

// Couverture de story à la une : icône centrée (Instagram la recadre en cercle)
export const Highlight: React.FC<{icon: string}> = ({icon}) => (
  <AbsoluteFill style={{background: '#1a1615', justifyContent: 'center', alignItems: 'center'}}>
    {ICONS[icon]}
  </AbsoluteFill>
);

// Photo de profil : le héros et le sac, sur fond crème (lisible en tout petit, comme l'original)
export const Avatar: React.FC<{img: string}> = ({img}) => (
  <AbsoluteFill style={{background: C.cream, justifyContent: 'center', alignItems: 'center'}}>
    <style>{fontsCss}</style>
    <div style={{width: 860, height: 860, borderRadius: 430, overflow: 'hidden', border: `14px solid ${C.pink}`}}>
      <Img src={staticFile(img)} style={{width: '100%', height: '100%', objectFit: 'cover', objectPosition: '45% 46%', transform: 'scale(1.12)', transformOrigin: '42% 50%'}} />
    </div>
  </AbsoluteFill>
);
