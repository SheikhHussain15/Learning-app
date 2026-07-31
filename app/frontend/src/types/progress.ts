export type ProgressEventType = 'quiz_completed' | 'flashcard_reviewed' | 'chapter_completed' | 'reading_progress' | 'tutor_used' | 'diagram_interacted' | 'revision_completed';

export interface ProgressEventInput {
  event_type: ProgressEventType;
  document_id?: string;
  section_id?: string;
  event_data?: Record<string, unknown>;
  duration?: number;
}

export interface ProgressEvent {
  id: string;
  user_id: string;
  event_type: ProgressEventType;
  document_id: string;
  section_id: string | null;
  event_data: Record<string, unknown>;
  duration: number | null;
  created_at: string;
}

export interface ProgressSummary {
  total_events: number;
  total_study_time: number;
  events_by_type: Record<ProgressEventType, number>;
  documents_studied: number;
  average_daily_time: number;
}

export interface LearningStreak {
  current_streak: number;
  longest_streak: number;
  last_activity_date: string;
  streak_active: boolean;
}