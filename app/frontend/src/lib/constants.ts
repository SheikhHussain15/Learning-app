export const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export const SECTION_TYPES = [
  'summary',
  'explanation',
  'translation',
  'diagram',
  'quiz',
  'flashcard',
  'revision_notes',
] as const;

export const SECTION_STATUS = [
  'not_requested',
  'processing',
  'failed',
  'completed',
] as const;

export const DIFFICULTY_RATINGS = ['easy', 'medium', 'hard'] as const;

export const PROGRESS_EVENT_TYPES = [
  'quiz_completed',
  'flashcard_reviewed',
  'chapter_completed',
  'reading_progress',
  'tutor_used',
  'diagram_interacted',
  'revision_completed',
] as const;

export const DIAGRAM_TYPES = [
  'flowchart',
  'mind_map',
  'timeline',
  'concept_map',
  'sequence',
  'class',
  'state',
  'er',
] as const;

export const NAVIGATION_ITEMS = [
  { label: 'Dashboard', href: '/dashboard', icon: 'home' },
  { label: 'Library', href: '/library', icon: 'book' },
  { label: 'AI Tutor', href: '/tutor', icon: 'chat' },
  { label: 'Profile', href: '/profile', icon: 'user' },
] as const;

export const BREAKPOINTS = {
  sm: 640,
  md: 768,
  lg: 1024,
  xl: 1280,
  '2xl': 1536,
} as const;