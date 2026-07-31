'use client';

import { useState, useCallback } from 'react';
import { quizService } from '../services/quiz.service';
import { Question, QuizResults } from '../types/quiz';

interface UseQuizReturn {
  questions: Question[];
  currentIndex: number;
  answers: Record<string, { selected: string; correct: boolean }>;
  loading: boolean;
  error: string | null;
  generating: boolean;
  submitting: boolean;
  result: QuizResults | null;
  generateQuiz: (documentId: string, options?: { difficulty?: string; count?: number }) => Promise<void>;
  selectAnswer: (questionIndex: string, answerId: string) => void;
  submitQuiz: (documentId: string) => Promise<void>;
  nextQuestion: () => void;
  previousQuestion: () => void;
  resetQuiz: () => void;
  score: number;
}

export function useQuiz(): UseQuizReturn {
  const [questions, setQuestions] = useState<Question[]>([]);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [answers, setAnswers] = useState<Record<string, { selected: string; correct: boolean }>>({});
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [generating, setGenerating] = useState(false);
  const [submitting, setSubmitting] = useState(false);
  const [result, setResult] = useState<QuizResults | null>(null);

  const generateQuiz = useCallback(async (documentId: string, options?: { difficulty?: string; count?: number }) => {
    try {
      setGenerating(true);
      setError(null);
      setAnswers({});
      setCurrentIndex(0);
      setResult(null);
      const response: any = await quizService.generateQuiz(documentId, options);
      setQuestions(response.questions || []);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to generate quiz');
    } finally {
      setGenerating(false);
    }
  }, []);

  const selectAnswer = useCallback((questionIndex: string, answerId: string) => {
    setAnswers(prev => ({
      ...prev,
      [questionIndex]: { selected: answerId, correct: false },
    }));
  }, []);

  const submitQuiz = useCallback(async (documentId: string) => {
    try {
      setSubmitting(true);
      setError(null);
      const response = await quizService.submitQuiz({
        document_id: documentId,
        answers,
      });
      setResult(response);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to submit quiz');
    } finally {
      setSubmitting(false);
    }
  }, [answers]);

  const nextQuestion = useCallback(() => {
    if (currentIndex < questions.length - 1) {
      setCurrentIndex(prev => prev + 1);
    }
  }, [currentIndex, questions.length]);

  const previousQuestion = useCallback(() => {
    if (currentIndex > 0) {
      setCurrentIndex(prev => prev - 1);
    }
  }, [currentIndex]);

  const resetQuiz = useCallback(() => {
    setQuestions([]);
    setCurrentIndex(0);
    setAnswers({});
    setResult(null);
    setError(null);
  }, []);

  const score = questions.length > 0
    ? Object.values(answers).filter(a => a.correct).length / questions.length * 100
    : 0;

  return {
    questions,
    currentIndex,
    answers,
    loading,
    error,
    generating,
    submitting,
    result,
    generateQuiz,
    selectAnswer,
    submitQuiz,
    nextQuestion,
    previousQuestion,
    resetQuiz,
    score,
  };
}