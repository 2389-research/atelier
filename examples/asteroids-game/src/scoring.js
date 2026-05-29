import { ASTEROID_SCORES } from './constants.js';

export function createScore() {
  return { value: 0, multiplier: 1 };
}

export function scoreForSize(size) {
  return ASTEROID_SCORES[size];
}

export function addPoints(score, size) {
  score.value += scoreForSize(size) * score.multiplier;
}
