import api from './api';
import { TutorMessageInput, TutorResponse, TutorConversation } from '../types/tutor';

export const tutorService = {
  sendMessage: (documentId: string, message: string) =>
    api.post<TutorResponse>('/tutor/message', {
      document_id: documentId,
      content: message,
    }),

  getConversation: (documentId: string, limit = 50) =>
    api.get<TutorConversation>(`/tutor/conversation/${documentId}?limit=${limit}`),

  clearConversation: (documentId: string) =>
    api.delete(`/tutor/conversation/${documentId}`),
};

export default tutorService;