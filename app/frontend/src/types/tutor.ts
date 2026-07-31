export interface SourceReference {
  chunk_id: string;
  document_id: string;
  chapter_title: string;
  topic_title: string;
  content_preview: string;
  relevance_score: number;
}

export interface TutorMessage {
  id: string;
  conversation_id: string;
  role: 'user' | 'assistant';
  content: string;
  sources: SourceReference[];
  created_at: string;
}

export interface TutorConversation {
  id: string;
  document_id: string;
  user_id: string;
  title: string;
  message_count: number;
  created_at: string;
  updated_at: string;
}

export interface TutorMessageInput {
  content: string;
}

export interface TutorResponse {
  message_id: string;
  role: 'assistant';
  content: string;
  sources: SourceReference[];
  is_grounded: boolean;
  confidence: number;
  created_at: string;
}