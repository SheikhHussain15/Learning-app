import api from './api';
import { Flashcard, FlashcardReviewResult } from '../types/flashcard';

export const flashcardService = {
  generateFlashcards: (documentId: string, count = 10) =>
    api.post<Flashcard[]>('/flashcard/generate', {
      document_id: documentId,
      count,
    }),

  getFlashcards: (documentId: string) =>
    api.get<Flashcard[]>(`/flashcard/${documentId}`),

  reviewFlashcard: (request: { document_id: string; card_id: string; quality: number }) =>
    api.post<FlashcardReviewResult>('/flashcard/review', request),

  getDueCards: (documentId: string) =>
    api.get<Flashcard[]>(`/flashcard/${documentId}/due`),

  getReviewStats: (documentId: string) =>
    api.get(`/flashcard/${documentId}/stats`),
};

export default flashcardService;