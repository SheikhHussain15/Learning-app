'use client';

interface ExplanationSectionProps {
  content: string;
  className?: string;
}

export function ExplanationSection({ content, className = '' }: ExplanationSectionProps) {
  return (
    <div className={`prose max-w-none ${className}`}>
      <div className="whitespace-pre-wrap text-gray-700">{content}</div>
    </div>
  );
}

export default ExplanationSection;