'use client';

interface QuizSectionProps {
  content: Record<string, unknown>;
  onStartQuiz?: () => void;
  className?: string;
}

export function QuizSection({ content, onStartQuiz, className = '' }: QuizSectionProps) {
  const questions = (content.questions as Array<Record<string, unknown>>) || [];

  return (
    <div className={`${className}`}>
      <p className="text-gray-600 mb-4">
        This quiz contains {questions.length} questions.
      </p>
      {onStartQuiz && (
        <button
          onClick={onStartQuiz}
          className="px-4 py-2 bg-blue-500 text-white rounded-md hover:bg-blue-600 transition-colors"
        >
          Start Quiz
        </button>
      )}
    </div>
  );
}

export default QuizSection;