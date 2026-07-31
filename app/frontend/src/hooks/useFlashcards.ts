'use client';

import { useState, useCallback } from 'react';
import { flashcardService } from '../services/flashcard.service';
import { Flashcard, FlashcardReviewResult } from '../types/flashcard';

interface UseFlashcardsReturn {
  cards: Flashcard[];
  currentIndex: number;
  loading: boolean;
  error: string | null;
  generating: boolean;
  reviewing: boolean;
  flipped: boolean;
  stats: { total_cards: number; reviewed_today: number; due_today: number; mastered: number } | null;
  generateFlashcards: (documentId: string, count?: number) => Promise<void>;
  loadFlashcards: (documentId: string) => Promise<void>;
  flipCard: () => void;
  rateCard: (quality: number) => Promise<void>;
  nextCard: () => void;
  previousCard: () => void;
  resetFlashcards: () => void;
}

export function useFlashcards(): UseFlashcardsReturn {
  const [cards, setCards] = useState<Flashcard[]>([]);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [generating, setGenerating] = useState(false);
  const [reviewing, setReviewing] = useState(false);
  const [flipped, setFlipped] = useState(false);
  const [stats, setStats] = useState<{ total_cards: number; reviewed_today: number; due_today: number; mastered: number } | null>(null);

  const generateFlashcards = useCallback(async (documentId: string, count = 10) => {
    try {
      setGenerating(true);
      setError(null);
      setFlipped(false);
      setCurrentIndex(0);
      const response = await flashcardService.generateFlashcards(documentId, count);
      setCards(response);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to generate flashcards');
    } finally {
      setGenerating(false);
    }
  }, []);

  const loadFlashcards = useCallback(async (documentId: string) => {
    try {
      setLoading(true);
      setError(null);
      const response = await flashcardService.getFlashcards(documentId);
      setCards(response);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load flashcards');
    } finally {
      setLoading(false);
    }
  }, []);

  const flipCard = useCallback(() => {
    setFlipped(prev => !prev);
  }, []);

  const rateCard = useCallback(async (quality: number) => {
    if (currentIndex >= cards.length) return;
    
    const card = cards[currentIndex];
    try {
      setReviewing(true);
      await flashcardService.reviewFlashcard({
        document_id: card.document_id,
        card_id: card.id,
        quality,
      });
      setFlipped(false);
      if (currentIndex < cards.length - 1) {
        setCurrentIndex(prev => prev + 1);
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to record review');
    } finally {
      setReviewing(false);
    }
  }, [currentIndex, cards]);

  const nextCard = useCallback(() => {
    if (currentIndex < cards.length - 1) {
      setFlipped(false);
      setCurrentIndex(prev => prev + 1);
    }
  }, [currentIndex, cards.length]);

  const previousCard = useCallback(() => {
    if (currentIndex > 0) {
      setFlipped(false);
      setCurrentIndex(prev => prev - 1);
    }
  }, [currentIndex]);

  const resetFlashcards = useCallback(() => {
    setCards([]);
    setCurrentIndex(0);
    setFlipped(false);
    setError(null);
  }, []);

  return {
    cards,
    currentIndex,
    loading,
    error,
    generating,
    reviewing,
    flipped,
    stats,
    generateFlashcards,
    loadFlashcards,
    flipCard,
    rateCard,
    nextCard,
    previousCard,
    resetFlashcards,
  };
}