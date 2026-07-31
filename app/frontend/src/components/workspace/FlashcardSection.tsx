'use client';

interface FlashcardSectionProps {
  content: Record<string, unknown>;
  onStartReview?: () => void;
  className?: string;
}

export function FlashcardSection({ content, onStartReview, className = '' }: FlashcardSectionProps) {
  const cards = (content.cards as Array<Record<string, unknown>>) || [];

  return (
    <div className={`${className}`}>
      <p className="text-gray-600 mb-4">
        This deck contains {cards.length} flashcards.
      </p>
      {onStartReview && (
        <button
          onClick={onStartReview}
          className="px-4 py-2 bg-blue-500 text-white rounded-md hover:bg-blue-600 transition-colors"
        >
          Start Review
        </button>
      )}
    </div>
  );
}

export default FlashcardSection;