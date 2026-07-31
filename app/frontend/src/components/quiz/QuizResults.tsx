'use client';

import { QuizResults as QuizResultsType } from '../../types/quiz';

interface QuizResultsProps {
  result: QuizResultsType;
  onRetake: () => void;
  onFinish: () => void;
}

export function QuizResults({ result, onRetake, onFinish }: QuizResultsProps) {
  const passed = result.score >= 70;

  return (
    <div className="bg-white rounded-lg shadow-sm border p-8 text-center">
      <div className={`text-6xl font-bold mb-4 ${passed ? 'text-green-500' : 'text-orange-500'}`}>
        {Math.round(result.score)}%
      </div>
      <p className="text-lg text-gray-600 mb-2">
        {passed ? 'Great job!' : 'Keep practicing!'}
      </p>
      <p className="text-sm text-gray-500 mb-6">
        You got {result.correct_answers} out of {result.total_questions} correct
      </p>
      <div className="flex justify-center space-x-4">
        <button
          onClick={onRetake}
          className="px-6 py-2 border border-gray-300 rounded-lg text-gray-700 hover:bg-gray-50"
        >
          Retake Quiz
        </button>
        <button
          onClick={onFinish}
          className="px-6 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600"
        >
          Finish
        </button>
      </div>
    </div>
  );
}

export default QuizResults;