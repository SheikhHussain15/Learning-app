'use client';

import { ReactNode } from 'react';
import { SectionType, SectionStatus } from '../../types/workspace';
import { StateIndicator } from '../ui/StateIndicator';
import { LoadingSpinner } from '../ui/LoadingSpinner';
import { ErrorState } from '../ui/ErrorState';

interface AIContentSectionProps {
  sectionType: SectionType;
  status: SectionStatus;
  title: string;
  children: ReactNode;
  onRequestGeneration?: () => void;
  onRetry?: () => void;
  errorMessage?: string | null;
  className?: string;
}

export function AIContentSection({
  sectionType,
  status,
  title,
  children,
  onRequestGeneration,
  onRetry,
  errorMessage,
  className = '',
}: AIContentSectionProps) {
  const renderContent = () => {
    switch (status) {
      case 'not_requested':
        return (
          <div className="text-center py-8">
            <p className="text-gray-500 mb-4">This section has not been generated yet.</p>
            {onRequestGeneration && (
              <button
                onClick={onRequestGeneration}
                className="px-4 py-2 bg-blue-500 text-white rounded-md hover:bg-blue-600 transition-colors"
              >
                Generate {title}
              </button>
            )}
          </div>
        );
      case 'processing':
        return (
          <div className="flex flex-col items-center justify-center py-8">
            <LoadingSpinner size="lg" />
            <p className="mt-4 text-gray-500">Generating content...</p>
          </div>
        );
      case 'failed':
        return (
          <ErrorState
            message={errorMessage || 'Failed to generate content'}
            action={
              onRetry && (
                <button
                  onClick={onRetry}
                  className="px-4 py-2 bg-blue-500 text-white rounded-md hover:bg-blue-600 transition-colors"
                >
                  Retry
                </button>
              )
            }
          />
        );
      case 'completed':
        return <>{children}</>;
      default:
        return null;
    }
  };

  return (
    <div className={`bg-white rounded-lg shadow-sm border p-6 ${className}`}>
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-lg font-semibold text-gray-900">{title}</h3>
        <StateIndicator status={status} />
      </div>
      {renderContent()}
    </div>
  );
}

export default AIContentSection;