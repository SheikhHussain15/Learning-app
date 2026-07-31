'use client';

interface FlashcardControlsProps {
  onRate: (quality: number) => void;
  disabled?: boolean;
}

export function FlashcardControls({ onRate, disabled = false }: FlashcardControlsProps) {
  const ratings = [
    { quality: 1, label: 'Again', color: 'bg-red-500 hover:bg-red-600' },
    { quality: 2, label: 'Hard', color: 'bg-orange-500 hover:bg-orange-600' },
    { quality: 3, label: 'Good', color: 'bg-green-500 hover:bg-green-600' },
    { quality: 4, label: 'Easy', color: 'bg-blue-500 hover:bg-blue-600' },
  ];

  return (
    <div className="flex justify-center space-x-3">
      {ratings.map((rating) => (
        <button
          key={rating.quality}
          onClick={() => onRate(rating.quality)}
          disabled={disabled}
          className={`px-4 py-2 text-white rounded-lg transition-colors ${rating.color} disabled:opacity-50`}
        >
          {rating.label}
        </button>
      ))}
    </div>
  );
}

export default FlashcardControls;