import { SectionType, SectionStatus } from '../types/workspace';
import { DifficultyRating } from '../types/flashcard';
import { ProgressEventType } from '../types/progress';

export function isValidSectionType(value: string): value is SectionType {
  return ['summary', 'explanation', 'translation', 'diagram', 'quiz', 'flashcard', 'revision_notes'].includes(value);
}

export function isValidSectionStatus(value: string): value is SectionStatus {
  return ['not_requested', 'processing', 'failed', 'completed'].includes(value);
}

export function isValidDifficultyRating(value: string): value is DifficultyRating {
  return ['easy', 'medium', 'hard'].includes(value);
}

export function isValidProgressEventType(value: string): value is ProgressEventType {
  return [
    'quiz_completed',
    'flashcard_reviewed',
    'chapter_completed',
    'reading_progress',
    'tutor_used',
    'diagram_interacted',
    'revision_completed',
  ].includes(value);
}

export function validateScore(score: number): boolean {
  return score >= 0 && score <= 100;
}

export function validateEmail(email: string): boolean {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return emailRegex.test(email);
}

export function validateRequired(value: unknown): boolean {
  if (value === null || value === undefined) return false;
  if (typeof value === 'string') return value.trim().length > 0;
  if (Array.isArray(value)) return value.length > 0;
  return true;
}