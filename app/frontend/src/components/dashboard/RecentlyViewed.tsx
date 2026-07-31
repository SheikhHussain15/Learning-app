'use client';

import { RecentlyViewedDocument } from '../../types/dashboard';
import { EmptyState } from '../ui/EmptyState';
import { ProgressBar } from '../ui/ProgressBar';

interface RecentlyViewedProps {
  documents: RecentlyViewedDocument[];
  className?: string;
}

export function RecentlyViewed({ documents, className = '' }: RecentlyViewedProps) {
  if (documents.length === 0) {
    return (
      <div className={`bg-white rounded-lg shadow-sm border p-6 ${className}`}>
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Recently Viewed</h3>
        <EmptyState
          title="No documents viewed"
          description="Start studying to see your recently viewed documents here."
        />
      </div>
    );
  }

  return (
    <div className={`bg-white rounded-lg shadow-sm border p-6 ${className}`}>
      <h3 className="text-lg font-semibold text-gray-900 mb-4">Recently Viewed</h3>
      <div className="space-y-3">
        {documents.map((doc) => (
          <div key={doc.document_id} className="p-3 bg-gray-50 rounded-lg">
            <p className="font-medium text-gray-900 truncate">{doc.title}</p>
            <div className="mt-2">
              <ProgressBar value={doc.progress} showLabel={false} />
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

export default RecentlyViewed;