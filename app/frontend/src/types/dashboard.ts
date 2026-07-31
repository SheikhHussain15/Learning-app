export type EventType = 'quiz_completed' | 'flashcard_reviewed' | 'chapter_completed' | 'reading_progress' | 'tutor_used' | 'diagram_interacted' | 'revision_completed';

export interface ActivityItem {
  id: string;
  event_type: EventType;
  document_id: string;
  document_title: string;
  description: string;
  created_at: string;
}

export interface LearningStatistics {
  total_study_time: number;
  documents_studied: number;
  quizzes_completed: number;
  average_quiz_score: number;
  flashcards_reviewed: number;
  tutor_conversations: number;
}

export interface DocumentProgress {
  document_id: string;
  title: string;
  progress: number;
  last_studied: string;
}

export interface StudyProgress {
  documents: DocumentProgress[];
  overall_progress: number;
}

export interface LearningStreak {
  current_streak: number;
  longest_streak: number;
  last_activity_date: string;
  streak_active: boolean;
}

export interface Recommendation {
  id: string;
  recommendation_type: 'document' | 'quiz' | 'flashcard' | 'review';
  document_id: string;
  title: string;
  description: string;
  reason: string;
  priority: number;
}

export interface RecentlyViewedDocument {
  document_id: string;
  title: string;
  progress: number;
  last_viewed: string;
}

export interface DashboardData {
  recent_activity: ActivityItem[];
  statistics: LearningStatistics;
  progress: StudyProgress;
  streak: LearningStreak;
  recommendations: Recommendation[];
  recently_viewed: RecentlyViewedDocument[];
}