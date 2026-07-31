'use client';

interface DiagramSectionProps {
  content: Record<string, unknown>;
  className?: string;
}

export function DiagramSection({ content, className = '' }: DiagramSectionProps) {
  return (
    <div className={`${className}`}>
      <pre className="bg-gray-50 p-4 rounded-lg overflow-auto text-sm text-gray-700">
        {JSON.stringify(content, null, 2)}
      </pre>
    </div>
  );
}

export default DiagramSection;