import {Easing, interpolate} from 'remotion';

// Niveau d'animation de l'épisode : 'saveo' = copie sobre de Saveo ; 'plus' = motion design en plus (réglable par épisode).
let level: 'saveo' | 'plus' = 'plus';
export const setMotion = (m?: 'saveo' | 'plus') => {
  level = m ?? 'plus';
};
export const plus = () => level === 'plus';

const ease = Easing.bezier(0.22, 1, 0.36, 1); // sortie douce « ease-out quint »
export const reveal = (f: number, start: number, dur = 8) =>
  interpolate(f, [start, start + dur], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp', easing: ease});
export const inOut = (k: number) => Easing.inOut(Easing.cubic)(Math.min(1, Math.max(0, k)));
