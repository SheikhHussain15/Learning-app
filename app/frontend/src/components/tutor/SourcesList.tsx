'use client';

interface SourcesListProps {
  sources: string[];
  className?: string;
}

export function SourcesList({ sources, className = '' }: SourcesListProps) {
  if (sources.length === 0) {
    return null;
  }

  return (
    <div className={`bg-gray-50 rounded-lg p-4 ${className}`}>
      <h4 className="text-sm font-medium text-gray-700 mb-2">Sources</h4>
      <ul className="space-y-1">
        {sources.map((source, index) => (
          <li key={index} className="text-sm text-gray-600">
            {source}
          </li>
        ))}
      </ul>
    </div>
  );
}

export default SourcesList;