'use client';

import { ActivityItem } from '../../types/dashboard';
import { getRelativeTime } from '../../lib/utils';

interface RecentLearningProps {
  activities: ActivityItem[];
  className?: string;
}

export function RecentLearning({ activities, className = '' }: RecentLearningProps) {
  if (activities.length === 0) {
    return (
      <div className={`bg-white rounded-lg shadow-sm border p-6 ${className}`}>
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Recent Activity</h3>
        <p className="text-gray-500 text-sm">No recent activity. Start learning to see your progress here.</p>
      </div>
    );
  }

  return (
    <div className={`bg-white rounded-lg shadow-sm border p-6 ${className}`}>
      <h3 className="text-lg font-semibold text-gray-900 mb-4">Recent Activity</h3>
      <div className="space-y-3">
        {activities.map((activity) => (
          <div key={activity.id} className="flex items-start space-x-3">
            <div className="flex-shrink-0 w-2 h-2 mt-2 bg-blue-500 rounded-full" />
            <div className="flex-1 min-w-0">
              <p className="text-sm text-gray-700">{activity.description}</p>
              <p className="text-xs text-gray-500">{getRelativeTime(activity.created_at)}</p>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

export default RecentLearning;