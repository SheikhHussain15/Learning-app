'use client';

import { LearningStreak as LearningStreakType } from '../../types/dashboard';

interface LearningStreakProps {
  streak: LearningStreakType;
  className?: string;
}

export function LearningStreak({ streak, className = '' }: LearningStreakProps) {
  return (
    <div className={`bg-white rounded-lg shadow-sm border p-6 ${className}`}>
      <h3 className="text-lg font-semibold text-gray-900 mb-4">Learning Streak</h3>
      <div className="text-center">
        <div className={`text-5xl font-bold mb-2 ${streak.streak_active ? 'text-orange-500' : 'text-gray-400'}`}>
          {streak.current_streak}
        </div>
        <p className="text-sm text-gray-600">day streak</p>
        {streak.longest_streak > 0 && (
          <p className="text-xs text-gray-500 mt-2">
            Longest: {streak.longest_streak} days
          </p>
        )}
      </div>
    </div>
  );
}

export default LearningStreak;