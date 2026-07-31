'use client';

import { useEffect } from 'react';
import { useParams, useRouter } from 'next/navigation';
import { useAuth } from '../../../contexts/auth-context';
import { useTutor } from '../../../hooks/useTutor';
import { TutorChat } from '../../../components/tutor/TutorChat';
import { LoadingSpinner } from '../../../components/ui/LoadingSpinner';
import { ErrorState } from '../../../components/ui/ErrorState';

export default function TutorPage() {
  const { token } = useAuth();
  const router = useRouter();
  const params = useParams();
  const documentId = params.documentId as string;

  useEffect(() => {
    if (!token) router.push('/login');
  }, [token, router]);

  useEffect(() => {
    if (token && documentId) loadConversation(documentId);
  }, [token, documentId]);

  const { messages, loading, error, sending, sendMessage, loadConversation } = useTutor();

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <LoadingSpinner size="lg" />
      </div>
    );
  }

  if (error) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <ErrorState message={error} />
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 flex flex-col">
      <div className="bg-white border-b px-4 py-3">
        <h1 className="text-lg font-semibold text-gray-900">AI Tutor</h1>
        <p className="text-sm text-gray-500">Ask questions about this document</p>
      </div>
      
      <div className="flex-1 max-w-3xl mx-auto w-full">
        <TutorChat
          messages={messages}
          onSendMessage={(message) => sendMessage(documentId, message)}
          sending={sending}
        />
      </div>
    </div>
  );
}