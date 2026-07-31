'use client';

import { Recommendation } from '../../types/dashboard';
import { EmptyState } from '../ui/EmptyState';

interface RecommendationsProps {
  recommendations: Recommendation[];
  className?: string;
}

export function Recommendations({ recommendations, className = '' }: RecommendationsProps) {
  if (recommendations.length === 0) {
    return (
      <div className={`bg-white rounded-lg shadow-sm border p-6 ${className}`}>
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Recommendations</h3>
        <EmptyState
          title="No recommendations yet"
          description="Complete some learning activities to get personalized recommendations."
        />
      </div>
    );
  }

  return (
    <div className={`bg-white rounded-lg shadow-sm border p-6 ${className}`}>
      <h3 className="text-lg font-semibold text-gray-900 mb-4">Recommendations</h3>
      <div className="space-y-3">
        {recommendations.map((rec) => (
          <div
            key={rec.id}
            className="p-3 bg-blue-50 rounded-lg border border-blue-100"
          >
            <p className="font-medium text-blue-900">{rec.title}</p>
            <p className="text-sm text-blue-700 mt-1">{rec.reason}</p>
          </div>
        ))}
      </div>
    </div>
  );
}

export default Recommendations;