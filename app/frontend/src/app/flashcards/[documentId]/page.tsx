'use client';

import { useEffect } from 'react';
import { useParams, useRouter } from 'next/navigation';
import { useAuth } from '../../../contexts/auth-context';
import { useFlashcards } from '../../../hooks/useFlashcards';
import { FlashcardCardComponent } from '../../../components/flashcard/FlashcardCard';
import { FlashcardProgress } from '../../../components/flashcard/FlashcardProgress';
import { FlashcardControls } from '../../../components/flashcard/FlashcardControls';
import { LoadingSpinner } from '../../../components/ui/LoadingSpinner';
import { ErrorState } from '../../../components/ui/ErrorState';
import { EmptyState } from '../../../components/ui/EmptyState';

export default function FlashcardsPage() {
  const { token } = useAuth();
  const params = useParams();
  const router = useRouter();
  const documentId = params.documentId as string;

  useEffect(() => {
    if (!token) router.push('/login');
  }, [token, router]);

  useEffect(() => {
    if (token && documentId) loadFlashcards(documentId);
  }, [token, documentId]);

  const {
    cards,
    currentIndex,
    generating,
    loading,
    error,
    flipped,
    generateFlashcards,
    loadFlashcards,
    flipCard,
    rateCard,
    nextCard,
    previousCard,
    resetFlashcards,
  } = useFlashcards();

  if (loading || generating) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <LoadingSpinner size="lg" />
      </div>
    );
  }

  if (error) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <ErrorState message={error} />
      </div>
    );
  }

  if (cards.length === 0) {
    return (
      <div className="flex flex-col items-center justify-center min-h-screen">
        <EmptyState
          title="Ready to review?"
          description="Generate flashcards to start your review session."
        />
        <button
          onClick={() => generateFlashcards(documentId)}
          className="mt-4 px-6 py-3 bg-blue-500 text-white rounded-lg hover:bg-blue-600"
        >
          Generate Flashcards
        </button>
      </div>
    );
  }

  const card = cards[currentIndex];
  const isComplete = currentIndex >= cards.length;

  if (isComplete) {
    return (
      <div className="flex flex-col items-center justify-center min-h-screen">
        <div className="bg-white rounded-lg shadow-sm border p-8 text-center">
          <div className="text-5xl font-bold text-green-500 mb-4">✓</div>
          <h2 className="text-2xl font-bold text-gray-900 mb-2">Session Complete!</h2>
          <p className="text-gray-600 mb-6">You've reviewed all {cards.length} cards.</p>
          <div className="flex justify-center space-x-4">
            <button
              onClick={() => {
                resetFlashcards();
                generateFlashcards(documentId);
              }}
              className="px-6 py-2 border border-gray-300 rounded-lg text-gray-700 hover:bg-gray-50"
            >
              Start Over
            </button>
            <button
              onClick={() => router.push(`/workspace/${documentId}`)}
              className="px-6 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600"
            >
              Back to Workspace
            </button>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-2xl mx-auto px-4">
        <FlashcardProgress current={currentIndex} total={cards.length} />

        <div className="mt-6 flex justify-center">
          <FlashcardCardComponent
            card={card}
            flipped={flipped}
            onFlip={flipCard}
          />
        </div>

        <div className="mt-8">
          <FlashcardControls onRate={rateCard} />
        </div>

        <div className="mt-6 flex justify-between">
          <button
            onClick={previousCard}
            disabled={currentIndex === 0}
            className="px-4 py-2 border border-gray-300 rounded-lg text-gray-700 hover:bg-gray-50 disabled:opacity-50"
          >
            Previous
          </button>
          <button
            onClick={nextCard}
            disabled={currentIndex === cards.length - 1}
            className="px-4 py-2 border border-gray-300 rounded-lg text-gray-700 hover:bg-gray-50 disabled:opacity-50"
          >
            Next
          </button>
        </div>
      </div>
    </div>
  );
}