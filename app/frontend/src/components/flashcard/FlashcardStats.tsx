'use client';

interface FlashcardStatsProps {
  stats: {
    total_cards: number;
    reviewed_today: number;
    due_today: number;
    mastered: number;
  };
  className?: string;
}

export function FlashcardStats({ stats, className = '' }: FlashcardStatsProps) {
  return (
    <div className={`bg-white rounded-lg shadow-sm border p-6 ${className}`}>
      <h3 className="text-lg font-semibold text-gray-900 mb-4">Review Stats</h3>
      <div className="grid grid-cols-2 gap-4">
        <div className="text-center">
          <p className="text-2xl font-bold text-gray-900">{stats.total_cards}</p>
          <p className="text-sm text-gray-500">Total Cards</p>
        </div>
        <div className="text-center">
          <p className="text-2xl font-bold text-green-500">{stats.mastered}</p>
          <p className="text-sm text-gray-500">Mastered</p>
        </div>
        <div className="text-center">
          <p className="text-2xl font-bold text-blue-500">{stats.reviewed_today}</p>
          <p className="text-sm text-gray-500">Reviewed Today</p>
        </div>
        <div className="text-center">
          <p className="text-2xl font-bold text-orange-500">{stats.due_today}</p>
          <p className="text-sm text-gray-500">Due Today</p>
        </div>
      </div>
    </div>
  );
}

export default FlashcardStats;