'use client';

import { EmptyState } from '../ui/EmptyState';

interface QuizHistoryProps {
  history: any[];
  className?: string;
}

export function QuizHistory({ history, className = '' }: QuizHistoryProps) {
  if (history.length === 0) {
    return (
      <div className={`bg-white rounded-lg shadow-sm border p-6 ${className}`}>
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Quiz History</h3>
        <EmptyState
          title="No quizzes taken"
          description="Complete your first quiz to see your history here."
        />
      </div>
    );
  }

  return (
    <div className={`bg-white rounded-lg shadow-sm border p-6 ${className}`}>
      <h3 className="text-lg font-semibold text-gray-900 mb-4">Quiz History</h3>
      <div className="space-y-3">
        {history.map((attempt, index) => (
          <div key={index} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
            <div>
              <p className="font-medium text-gray-900">Quiz {index + 1}</p>
              <p className="text-sm text-gray-500">{attempt.total_questions} questions</p>
            </div>
            <div className={`text-lg font-bold ${attempt.score >= 70 ? 'text-green-500' : 'text-orange-500'}`}>
              {Math.round(attempt.score)}%
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

export default QuizHistory;