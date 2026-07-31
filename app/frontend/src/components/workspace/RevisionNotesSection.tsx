'use client';

interface RevisionNotesSectionProps {
  content: string;
  className?: string;
}

export function RevisionNotesSection({ content, className = '' }: RevisionNotesSectionProps) {
  return (
    <div className={`prose max-w-none ${className}`}>
      <div className="whitespace-pre-wrap text-gray-700">{content}</div>
    </div>
  );
}

export default RevisionNotesSection;