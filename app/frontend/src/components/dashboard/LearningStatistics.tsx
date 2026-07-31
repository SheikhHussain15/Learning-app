'use client';

import { LearningStatistics as LearningStatisticsType } from '../../types/dashboard';
import { formatDuration } from '../../lib/utils';

interface LearningStatisticsProps {
  statistics: LearningStatisticsType;
  className?: string;
}

export function LearningStatistics({ statistics, className = '' }: LearningStatisticsProps) {
  const stats = [
    { label: 'Study Time', value: formatDuration(statistics.total_study_time) },
    { label: 'Documents', value: statistics.documents_studied },
    { label: 'Quizzes', value: statistics.quizzes_completed },
    { label: 'Avg Score', value: `${Math.round(statistics.average_quiz_score)}%` },
    { label: 'Flashcards', value: statistics.flashcards_reviewed },
  ];

  return (
    <div className={`bg-white rounded-lg shadow-sm border p-6 ${className}`}>
      <h3 className="text-lg font-semibold text-gray-900 mb-4">Statistics</h3>
      <div className="grid grid-cols-2 sm:grid-cols-3 gap-4">
        {stats.map((stat) => (
          <div key={stat.label} className="text-center">
            <p className="text-2xl font-bold text-gray-900">{stat.value}</p>
            <p className="text-sm text-gray-500">{stat.label}</p>
          </div>
        ))}
      </div>
    </div>
  );
}

export default LearningStatistics;