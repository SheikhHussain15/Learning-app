'use client';

import { Chapter } from '../../types/workspace';

interface ChapterNavigationProps {
  chapters: Chapter[];
  selectedChapterId?: string;
  onSelectChapter: (chapterId: string) => void;
  className?: string;
}

export function ChapterNavigation({
  chapters,
  selectedChapterId,
  onSelectChapter,
  className = '',
}: ChapterNavigationProps) {
  return (
    <div className={`bg-white rounded-lg shadow-sm border p-4 ${className}`}>
      <h2 className="text-lg font-semibold text-gray-900 mb-4">Chapters</h2>
      <nav className="space-y-1">
        {chapters.map((chapter) => (
          <button
            key={chapter.id}
            onClick={() => onSelectChapter(chapter.id)}
            className={`w-full text-left px-3 py-2 rounded-md text-sm font-medium transition-colors ${
              selectedChapterId === chapter.id
                ? 'bg-blue-50 text-blue-700'
                : 'text-gray-700 hover:bg-gray-50'
            }`}
          >
            {chapter.title}
          </button>
        ))}
      </nav>
    </div>
  );
}

export default ChapterNavigation;