'use client';

import { useEffect } from 'react';
import { useParams, useRouter } from 'next/navigation';
import { useAuth } from '../../../contexts/auth-context';
import { useQuiz } from '../../../hooks/useQuiz';
import { QuizCard } from '../../../components/quiz/QuizCard';
import { QuizProgress } from '../../../components/quiz/QuizProgress';
import { QuizResults } from '../../../components/quiz/QuizResults';
import { LoadingSpinner } from '../../../components/ui/LoadingSpinner';
import { ErrorState } from '../../../components/ui/ErrorState';
import { EmptyState } from '../../../components/ui/EmptyState';

export default function QuizPage() {
  const { token } = useAuth();
  const params = useParams();
  const router = useRouter();
  const documentId = params.documentId as string;

  useEffect(() => {
    if (!token) router.push('/login');
  }, [token, router]);

  const {
    questions,
    currentIndex,
    answers,
    generating,
    submitting,
    error,
    result,
    generateQuiz,
    selectAnswer,
    submitQuiz,
    nextQuestion,
    previousQuestion,
    resetQuiz,
    score,
  } = useQuiz();

  if (generating) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <LoadingSpinner size="lg" />
      </div>
    );
  }

  if (error) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <ErrorState message={error} />
      </div>
    );
  }

  if (questions.length === 0) {
    return (
      <div className="flex flex-col items-center justify-center min-h-screen">
        <EmptyState
          title="Ready to test your knowledge?"
          description="Start a quiz to check your understanding of this document."
        />
        <button
          onClick={() => generateQuiz(documentId)}
          className="mt-4 px-6 py-3 bg-blue-500 text-white rounded-lg hover:bg-blue-600"
        >
          Start Quiz
        </button>
      </div>
    );
  }

  if (result) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <QuizResults
          result={result}
          onRetake={() => {
            resetQuiz();
            generateQuiz(documentId);
          }}
          onFinish={() => router.push(`/workspace/${documentId}`)}
        />
      </div>
    );
  }

  const currentQuestion = questions[currentIndex];
  const answeredCount = Object.keys(answers).length;

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-2xl mx-auto px-4">
        <QuizProgress
          current={currentIndex}
          total={questions.length}
          answered={answeredCount}
        />

        <div className="mt-6">
          <QuizCard
            question={currentQuestion}
            selectedAnswer={answers[currentQuestion.id]?.selected}
            onSelect={(_questionId, answerId) => selectAnswer(currentQuestion.id, answerId)}
          />
        </div>

        <div className="mt-6 flex justify-between">
          <button
            onClick={previousQuestion}
            disabled={currentIndex === 0}
            className="px-4 py-2 border border-gray-300 rounded-lg text-gray-700 hover:bg-gray-50 disabled:opacity-50"
          >
            Previous
          </button>

          {currentIndex === questions.length - 1 ? (
            <button
              onClick={() => submitQuiz(documentId)}
              disabled={answeredCount < questions.length || submitting}
              className="px-6 py-2 bg-green-500 text-white rounded-lg hover:bg-green-600 disabled:opacity-50"
            >
              {submitting ? 'Submitting...' : 'Submit Quiz'}
            </button>
          ) : (
            <button
              onClick={nextQuestion}
              className="px-6 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600"
            >
              Next
            </button>
          )}
        </div>
      </div>
    </div>
  );
}