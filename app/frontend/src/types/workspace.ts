export type SectionType = 'summary' | 'explanation' | 'translation' | 'diagram' | 'quiz' | 'flashcard' | 'revision_notes';

export type SectionStatus = 'not_requested' | 'processing' | 'failed' | 'completed';

export interface WorkspaceSection {
  id: string;
  document_id: string;
  section_type: SectionType;
  status: SectionStatus;
  content: Record<string, unknown> | null;
  error_message: string | null;
  requested_at: string | null;
  completed_at: string | null;
  created_at: string;
  updated_at: string;
}

export interface Topic {
  id: string;
  title: string;
  order: number;
  chapter_id: string;
}

export interface Chapter {
  id: string;
  title: string;
  order: number;
  topics: Topic[];
}

export interface WorkspaceOverview {
  document_id: string;
  title: string;
  description: string;
  metadata: Record<string, unknown>;
  chapters: Chapter[];
  sections: WorkspaceSection[];
}

export interface SectionRequestResponse {
  section_id: string;
  status: 'processing';
  message: string;
}

export interface SectionStatusResponse {
  section_id: string;
  status: SectionStatus;
  progress: number;
  error_message: string | null;
}

export interface SectionContentResponse {
  section_id: string;
  section_type: SectionType;
  content: Record<string, unknown>;
  metadata: Record<string, unknown>;
}