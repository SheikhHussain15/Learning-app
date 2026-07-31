'use client';

import { useEffect } from 'react';
import { useParams, useRouter } from 'next/navigation';
import { useAuth } from '../../../contexts/auth-context';
import { useDiagram } from '../../../hooks/useDiagram';
import { DiagramViewer } from '../../../components/diagram/DiagramViewer';
import { DiagramControls } from '../../../components/diagram/DiagramControls';
import { LoadingSpinner } from '../../../components/ui/LoadingSpinner';
import { ErrorState } from '../../../components/ui/ErrorState';
import { EmptyState } from '../../../components/ui/EmptyState';

export default function DiagramsPage() {
  const { token } = useAuth();
  const router = useRouter();
  const params = useParams();
  const documentId = params.documentId as string;

  const {
    diagrams,
    currentDiagram,
    loading,
    error,
    generating,
    zoom,
    loadDiagrams,
    generateDiagram,
    selectDiagram,
    zoomIn,
    zoomOut,
    resetZoom,
  } = useDiagram();

  useEffect(() => {
    if (!token) router.push('/login');
  }, [token, router]);

  useEffect(() => {
    if (token && documentId) loadDiagrams(documentId);
  }, [token, documentId]);

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
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-7xl mx-auto px-4 py-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-8">Diagrams</h1>
        
        <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
          <div className="lg:col-span-1">
            <DiagramControls
              diagrams={diagrams}
              currentDiagramId={currentDiagram?.id || null}
              onSelect={selectDiagram}
              onGenerate={() => generateDiagram(documentId)}
              generating={generating}
            />
          </div>
          
          <div className="lg:col-span-3">
            {currentDiagram ? (
              <DiagramViewer
                diagram={currentDiagram}
                zoom={zoom}
                onZoomIn={zoomIn}
                onZoomOut={zoomOut}
                onResetZoom={resetZoom}
              />
            ) : (
              <EmptyState
                title="No diagram selected"
                description="Select a diagram from the list or generate a new one."
              />
            )}
          </div>
        </div>
      </div>
    </div>
  );
}