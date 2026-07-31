'use client';

interface DocumentOverviewProps {
  title: string;
  description: string;
  metadata?: Record<string, unknown>;
  className?: string;
}

export function DocumentOverview({ title, description, metadata, className = '' }: DocumentOverviewProps) {
  return (
    <div className={`bg-white rounded-lg shadow-sm border p-6 ${className}`}>
      <h1 className="text-2xl font-bold text-gray-900 mb-2">{title}</h1>
      <p className="text-gray-600 mb-4">{description}</p>
      {metadata && Object.keys(metadata).length > 0 && (
        <div className="flex flex-wrap gap-2">
          {Object.entries(metadata).map(([key, value]) => (
            <span
              key={key}
              className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-gray-100 text-gray-800"
            >
              {key}: {String(value)}
            </span>
          ))}
        </div>
      )}
    </div>
  );
}

export default DocumentOverview;