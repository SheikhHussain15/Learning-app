'use client';

interface SuggestedQuestionsProps {
  questions: string[];
  onSelect: (question: string) => void;
  className?: string;
}

export function SuggestedQuestions({ questions, onSelect, className = '' }: SuggestedQuestionsProps) {
  if (questions.length === 0) {
    return null;
  }

  return (
    <div className={`bg-blue-50 rounded-lg p-4 ${className}`}>
      <h4 className="text-sm font-medium text-blue-800 mb-2">Suggested Questions</h4>
      <div className="space-y-2">
        {questions.map((question, index) => (
          <button
            key={index}
            onClick={() => onSelect(question)}
            className="w-full text-left text-sm text-blue-700 hover:text-blue-900 hover:bg-blue-100 rounded p-2 transition-colors"
          >
            {question}
          </button>
        ))}
      </div>
    </div>
  );
}

export default SuggestedQuestions;