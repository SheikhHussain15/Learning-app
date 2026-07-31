'use client';

import { ProgressBar } from '../ui/ProgressBar';

interface FlashcardProgressProps {
  current: number;
  total: number;
}

export function FlashcardProgress({ current, total }: FlashcardProgressProps) {
  const progress = total > 0 ? ((current + 1) / total) * 100 : 0;

  return (
    <div className="bg-white rounded-lg shadow-sm border p-4">
      <div className="flex items-center justify-between mb-2">
        <span className="text-sm text-gray-600">
          Card {current + 1} of {total}
        </span>
      </div>
      <ProgressBar value={progress} showLabel={false} />
    </div>
  );
}

export default FlashcardProgress;