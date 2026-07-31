'use client';

import { Question } from '../../types/quiz';

interface QuizCardProps {
  question: Question;
  selectedAnswer?: string;
  onSelect: (questionIndex: string, answerId: string) => void;
  showResult?: boolean;
}

export function QuizCard({ question, selectedAnswer, onSelect, showResult = false }: QuizCardProps) {
  return (
    <div className="bg-white rounded-lg shadow-sm border p-6">
      <h3 className="text-lg font-semibold text-gray-900 mb-4">{question.text}</h3>
      <div className="space-y-3">
        {question.options.map((option, index) => {
          const isSelected = selectedAnswer === option.id;
          const showCorrect = showResult && isSelected;
          const showIncorrect = showResult && isSelected;

          return (
            <button
              key={option.id}
              onClick={() => !showResult && onSelect(question.id, option.id)}
              disabled={showResult}
              className={`w-full text-left p-4 rounded-lg border-2 transition-colors ${
                showCorrect
                  ? 'border-green-500 bg-green-50'
                  : showIncorrect
                  ? 'border-red-500 bg-red-50'
                  : isSelected
                  ? 'border-blue-500 bg-blue-50'
                  : 'border-gray-200 hover:border-gray-300 hover:bg-gray-50'
              }`}
            >
              <span className="font-medium">{String.fromCharCode(65 + index)}.</span> {option.text}
            </button>
          );
        })}
      </div>
    </div>
  );
}

export default QuizCard;