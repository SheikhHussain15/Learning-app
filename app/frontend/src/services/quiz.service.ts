import api from './api';
import { Question, QuizResults } from '../types/quiz';

export const quizService = {
  generateQuiz: (documentId: string, options?: { difficulty?: string; count?: number }) =>
    api.post('/quiz/generate', {
      document_id: documentId,
      difficulty: options?.difficulty || 'medium',
      count: options?.count || 5,
    }),

  submitQuiz: (request: { document_id: string; answers: Record<string, any> }) =>
    api.post<QuizResults>('/quiz/submit', request),

  getHistory: (limit = 10) =>
    api.get(`/quiz/history?limit=${limit}`),
};

export default quizService;