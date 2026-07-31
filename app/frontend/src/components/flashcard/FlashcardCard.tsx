'use client';

import { Flashcard } from '../../types/flashcard';

interface FlashcardCardProps {
  card: Flashcard;
  flipped: boolean;
  onFlip: () => void;
}

export function FlashcardCardComponent({ card, flipped, onFlip }: FlashcardCardProps) {
  return (
    <div
      onClick={onFlip}
      className="w-full h-64 cursor-pointer perspective-1000"
    >
      <div
        className={`relative w-full h-full transition-transform duration-500 transform-style-3d ${
          flipped ? 'rotate-y-180' : ''
        }`}
      >
        <div className="absolute inset-0 backface-hidden bg-white rounded-lg shadow-lg border-2 border-blue-200 flex items-center justify-center p-8">
          <p className="text-xl text-center text-gray-800">{card.front}</p>
        </div>
        <div className="absolute inset-0 backface-hidden bg-blue-50 rounded-lg shadow-lg border-2 border-blue-300 flex items-center justify-center p-8 rotate-y-180">
          <p className="text-xl text-center text-gray-800">{card.back}</p>
        </div>
      </div>
    </div>
  );
}

export default FlashcardCardComponent;