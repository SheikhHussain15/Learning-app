export interface Flashcard {
  id: string;
  document_id: string;
  front: string;
  back: string;
  order: number;
  next_review_at: string | null;
  review_count: number;
  created_at: string;
}

export interface FlashcardDeck {
  document_id: string;
  title: string;
  total_cards: number;
  cards: Flashcard[];
  created_at: string;
}

export type DifficultyRating = 'easy' | 'medium' | 'hard';

export interface FlashcardReviewSubmission {
  difficulty: DifficultyRating;
  review_duration?: number;
}

export interface FlashcardReviewResult {
  flashcard_id: string;
  difficulty: DifficultyRating;
  next_review_at: string;
  review_count: number;
  message: string;
}

export interface FlashcardProgress {
  document_id: string;
  total_cards: number;
  reviewed_today: number;
  due_for_review: number;
  mastered: number;
  learning: number;
  new_cards: number;
}

export interface FlashcardReviewHistory {
  id: string;
  flashcard_id: string;
  difficulty: DifficultyRating;
  review_duration: number;
  next_review_at: string;
  reviewed_at: string;
}