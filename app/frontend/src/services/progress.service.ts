import api from './api';
import { ProgressEventInput, ProgressEvent, ProgressSummary } from '../types/progress';

export const progressService = {
  recordEvent: (request: ProgressEventInput) =>
    api.post('/progress/event', request),

  getProgress: (documentId?: string) => {
    const params = documentId ? `?document_id=${documentId}` : '';
    return api.get<ProgressEvent[]>(`/progress${params}`);
  },

  getStats: (documentId?: string) => {
    const params = documentId ? `?document_id=${documentId}` : '';
    return api.get<ProgressSummary>(`/progress/stats${params}`);
  },
};

export default progressService;