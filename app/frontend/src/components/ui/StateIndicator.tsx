'use client';

import { SectionStatus } from '../../types/workspace';

interface StateIndicatorProps {
  status: SectionStatus;
  className?: string;
}

const statusConfig: Record<SectionStatus, { color: string; label: string; icon: string }> = {
  not_requested: { color: 'bg-gray-100 text-gray-600', label: 'Not Requested', icon: '○' },
  processing: { color: 'bg-blue-100 text-blue-600', label: 'Processing', icon: '◎' },
  failed: { color: 'bg-red-100 text-red-600', label: 'Failed', icon: '✕' },
  completed: { color: 'bg-green-100 text-green-600', label: 'Completed', icon: '✓' },
};

export function StateIndicator({ status, className = '' }: StateIndicatorProps) {
  const config = statusConfig[status];

  return (
    <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${config.color} ${className}`}>
      <span className="mr-1">{config.icon}</span>
      {config.label}
    </span>
  );
}

export default StateIndicator;