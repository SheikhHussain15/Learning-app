'use client';

interface TranslationSectionProps {
  content: string;
  className?: string;
}

export function TranslationSection({ content, className = '' }: TranslationSectionProps) {
  return (
    <div className={`prose max-w-none ${className}`}>
      <div className="whitespace-pre-wrap text-gray-700">{content}</div>
    </div>
  );
}

export default TranslationSection;