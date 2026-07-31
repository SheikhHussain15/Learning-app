'use client';

import { StudyProgress as StudyProgressType } from '../../types/dashboard';
import { ProgressBar } from '../ui/ProgressBar';

interface StudyProgressProps {
  progress: StudyProgressType;
  className?: string;
}

export function StudyProgress({ progress, className = '' }: StudyProgressProps) {
  return (
    <div className={`bg-white rounded-lg shadow-sm border p-6 ${className}`}>
      <h3 className="text-lg font-semibold text-gray-900 mb-4">Study Progress</h3>
      <div className="mb-4">
        <p className="text-sm text-gray-600 mb-2">Overall Progress</p>
        <ProgressBar value={progress.overall_progress} />
      </div>
      {progress.documents.length > 0 && (
        <div className="space-y-3">
          {progress.documents.map((doc) => (
            <div key={doc.document_id}>
              <div className="flex justify-between text-sm mb-1">
                <span className="text-gray-700 truncate">{doc.title}</span>
                <span className="text-gray-500">{Math.round(doc.progress)}%</span>
              </div>
              <ProgressBar value={doc.progress} showLabel={false} />
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default StudyProgress;