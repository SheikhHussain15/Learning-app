'use client';

import { useEffect } from 'react';
import { useParams, useRouter } from 'next/navigation';
import { useAuth } from '../../../contexts/auth-context';
import { useWorkspace } from '../../../hooks/useWorkspace';
import { DocumentOverview } from '../../../components/workspace/DocumentOverview';
import { ChapterNavigation } from '../../../components/workspace/ChapterNavigation';
import { TopicNavigation } from '../../../components/workspace/TopicNavigation';
import { AIContentSection } from '../../../components/workspace/AIContentSection';
import { SummarySection } from '../../../components/workspace/SummarySection';
import { ExplanationSection } from '../../../components/workspace/ExplanationSection';
import { TranslationSection } from '../../../components/workspace/TranslationSection';
import { DiagramSection } from '../../../components/workspace/DiagramSection';
import { QuizSection } from '../../../components/workspace/QuizSection';
import { FlashcardSection } from '../../../components/workspace/FlashcardSection';
import { RevisionNotesSection } from '../../../components/workspace/RevisionNotesSection';
import { LoadingSpinner } from '../../../components/ui/LoadingSpinner';
import { ErrorState } from '../../../components/ui/ErrorState';
import { useState } from 'react';
import { SectionType } from '../../../types/workspace';

export default function WorkspacePage() {
  const { token } = useAuth();
  const router = useRouter();
  const params = useParams();
  const documentId = params.documentId as string;

  useEffect(() => {
    if (!token) router.push('/login');
  }, [token, router]);

  const { workspace, loading, error, requestGeneration, getSectionStatus } = useWorkspace(documentId);
  const [selectedChapterId, setSelectedChapterId] = useState<string | undefined>();
  const [selectedTopicId, setSelectedTopicId] = useState<string | undefined>();

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

  if (!workspace) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <ErrorState message="Workspace not found" />
      </div>
    );
  }

  const selectedChapter = workspace.chapters.find((c) => c.id === selectedChapterId);
  const topics = selectedChapter?.topics || [];

  const sections: Array<{ type: SectionType; title: string }> = [
    { type: 'summary', title: 'Summary' },
    { type: 'explanation', title: 'Explanation' },
    { type: 'translation', title: 'Translation' },
    { type: 'diagram', title: 'Diagrams' },
    { type: 'quiz', title: 'Quiz' },
    { type: 'flashcard', title: 'Flashcards' },
    { type: 'revision_notes', title: 'Revision Notes' },
  ];

  const renderSectionContent = (type: SectionType, content: Record<string, unknown>) => {
    switch (type) {
      case 'summary':
        return <SummarySection content={content.text as string} />;
      case 'explanation':
        return <ExplanationSection content={content.text as string} />;
      case 'translation':
        return <TranslationSection content={content.text as string} />;
      case 'diagram':
        return <DiagramSection content={content} />;
      case 'quiz':
        return <QuizSection content={content} />;
      case 'flashcard':
        return <FlashcardSection content={content} />;
      case 'revision_notes':
        return <RevisionNotesSection content={content.text as string} />;
      default:
        return null;
    }
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <DocumentOverview
          title={workspace.title}
          description={workspace.description}
          metadata={workspace.metadata}
        />

        <div className="mt-8 grid grid-cols-1 lg:grid-cols-4 gap-6">
          <div className="lg:col-span-1 space-y-4">
            <ChapterNavigation
              chapters={workspace.chapters}
              selectedChapterId={selectedChapterId}
              onSelectChapter={setSelectedChapterId}
            />
            {topics.length > 0 && (
              <TopicNavigation
                topics={topics}
                selectedTopicId={selectedTopicId}
                onSelectTopic={setSelectedTopicId}
              />
            )}
          </div>

          <div className="lg:col-span-3 space-y-6">
            {sections.map(({ type, title }) => (
              <AIContentSection
                key={type}
                sectionType={type}
                status={getSectionStatus(type)}
                title={title}
                onRequestGeneration={() => requestGeneration(type)}
                onRetry={() => requestGeneration(type)}
              >
                {workspace.sections.find((s) => s.section_type === type)?.content &&
                  renderSectionContent(
                    type,
                    workspace.sections.find((s) => s.section_type === type)!.content!
                  )}
              </AIContentSection>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}