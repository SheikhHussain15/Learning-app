export interface QuestionOption {
  id: string;
  text: string;
  order: number;
}

export interface Question {
  id: string;
  text: string;
  options: QuestionOption[];
  order: number;
}

export interface Quiz {
  id: string;
  document_id: string;
  title: string;
  description: string;
  questions: Question[];
  total_questions: number;
  created_at: string;
}

export type QuizAttemptStatus = 'in_progress' | 'completed' | 'abandoned';

export interface QuizAttempt {
  id: string;
  quiz_id: string;
  user_id: string;
  status: QuizAttemptStatus;
  current_question_index: number;
  total_questions: number;
  started_at: string;
  completed_at: string | null;
}

export interface AnswerSubmission {
  question_id: string;
  option_id: string;
}

export interface AnswerFeedback {
  question_id: string;
  selected_option_id: string;
  correct_option_id: string;
  is_correct: boolean;
  explanation: string;
}

export interface QuizResults {
  attempt_id: string;
  score: number;
  total_questions: number;
  correct_answers: number;
  time_spent: number;
  completed_at: string;
}

export interface ReviewQuestion {
  question_id: string;
  text: string;
  options: QuestionOption[];
  selected_option_id: string;
  correct_option_id: string;
  is_correct: boolean;
  explanation: string;
}

export interface QuizReview {
  attempt_id: string;
  questions: ReviewQuestion[];
  score: number;
  total_questions: number;
}