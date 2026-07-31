'use client';

import { ProgressBar } from '../ui/ProgressBar';

interface QuizProgressProps {
  current: number;
  total: number;
  answered: number;
}

export function QuizProgress({ current, total, answered }: QuizProgressProps) {
  const progress = total > 0 ? (answered / total) * 100 : 0;

  return (
    <div className="bg-white rounded-lg shadow-sm border p-4">
      <div className="flex items-center justify-between mb-2">
        <span className="text-sm text-gray-600">
          Question {current + 1} of {total}
        </span>
        <span className="text-sm text-gray-600">
          {answered} answered
        </span>
      </div>
      <ProgressBar value={progress} showLabel={false} />
    </div>
  );
}

export default QuizProgress;