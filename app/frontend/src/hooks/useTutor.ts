'use client';

import { useState, useCallback } from 'react';
import { tutorService } from '../services/tutor.service';
import { TutorMessage, SourceReference } from '../types/tutor';

interface UseTutorReturn {
  messages: TutorMessage[];
  loading: boolean;
  error: string | null;
  sending: boolean;
  sendMessage: (documentId: string, message: string) => Promise<void>;
  loadConversation: (documentId: string) => Promise<void>;
  clearConversation: (documentId: string) => Promise<void>;
}

export function useTutor(): UseTutorReturn {
  const [messages, setMessages] = useState<TutorMessage[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [sending, setSending] = useState(false);

  const sendMessage = useCallback(async (documentId: string, message: string) => {
    try {
      setSending(true);
      setError(null);
      
      const userMessage: TutorMessage = {
        id: `temp-${Date.now()}`,
        conversation_id: '',
        content: message,
        role: 'user',
        sources: [],
        created_at: new Date().toISOString(),
      };
      setMessages(prev => [...prev, userMessage]);
      
      const response = await tutorService.sendMessage(documentId, message);
      
      const assistantMessage: TutorMessage = {
        id: response.message_id,
        conversation_id: '',
        content: response.content,
        role: 'assistant',
        sources: response.sources,
        created_at: response.created_at,
      };
      
      setMessages(prev => {
        const withoutTemp = prev.filter(m => !m.id.startsWith('temp-'));
        return [...withoutTemp, userMessage, assistantMessage];
      });
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to send message');
    } finally {
      setSending(false);
    }
  }, []);

  const loadConversation = useCallback(async (documentId: string) => {
    try {
      setLoading(true);
      setError(null);
      const response: any = await tutorService.getConversation(documentId);
      setMessages(response.messages || []);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load conversation');
    } finally {
      setLoading(false);
    }
  }, []);

  const clearConversation = useCallback(async (documentId: string) => {
    try {
      await tutorService.clearConversation(documentId);
      setMessages([]);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to clear conversation');
    }
  }, []);

  return {
    messages,
    loading,
    error,
    sending,
    sendMessage,
    loadConversation,
    clearConversation,
  };
}