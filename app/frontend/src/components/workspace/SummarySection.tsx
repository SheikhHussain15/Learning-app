'use client';

interface SummarySectionProps {
  content: string;
  className?: string;
}

export function SummarySection({ content, className = '' }: SummarySectionProps) {
  return (
    <div className={`prose max-w-none ${className}`}>
      <div className="whitespace-pre-wrap text-gray-700">{content}</div>
    </div>
  );
}

export default SummarySection;