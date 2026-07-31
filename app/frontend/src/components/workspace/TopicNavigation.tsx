'use client';

import { Topic } from '../../types/workspace';

interface TopicNavigationProps {
  topics: Topic[];
  selectedTopicId?: string;
  onSelectTopic: (topicId: string) => void;
  className?: string;
}

export function TopicNavigation({
  topics,
  selectedTopicId,
  onSelectTopic,
  className = '',
}: TopicNavigationProps) {
  return (
    <div className={`bg-white rounded-lg shadow-sm border p-4 ${className}`}>
      <h3 className="text-md font-semibold text-gray-900 mb-3">Topics</h3>
      <nav className="space-y-1">
        {topics.map((topic) => (
          <button
            key={topic.id}
            onClick={() => onSelectTopic(topic.id)}
            className={`w-full text-left px-3 py-2 rounded-md text-sm transition-colors ${
              selectedTopicId === topic.id
                ? 'bg-blue-50 text-blue-700 font-medium'
                : 'text-gray-600 hover:bg-gray-50'
            }`}
          >
            {topic.title}
          </button>
        ))}
      </nav>
    </div>
  );
}

export default TopicNavigation;