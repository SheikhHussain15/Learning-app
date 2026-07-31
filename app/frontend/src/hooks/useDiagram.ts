'use client';

import { useState, useCallback } from 'react';
import { diagramService } from '../services/diagram.service';
import { Diagram } from '../types/diagram';

interface UseDiagramReturn {
  diagrams: Diagram[];
  currentDiagram: Diagram | null;
  loading: boolean;
  error: string | null;
  generating: boolean;
  zoom: number;
  loadDiagrams: (documentId: string) => Promise<void>;
  generateDiagram: (documentId: string) => Promise<void>;
  selectDiagram: (diagramId: string) => void;
  zoomIn: () => void;
  zoomOut: () => void;
  resetZoom: () => void;
}

export function useDiagram(): UseDiagramReturn {
  const [diagrams, setDiagrams] = useState<Diagram[]>([]);
  const [currentDiagram, setCurrentDiagram] = useState<Diagram | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [generating, setGenerating] = useState(false);
  const [zoom, setZoom] = useState(1);

  const loadDiagrams = useCallback(async (documentId: string) => {
    try {
      setLoading(true);
      setError(null);
      const response = await diagramService.getDiagrams(documentId);
      setDiagrams(response);
      if (response.length > 0) {
        setCurrentDiagram(response[0]);
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load diagrams');
    } finally {
      setLoading(false);
    }
  }, []);

  const generateDiagram = useCallback(async (documentId: string) => {
    try {
      setGenerating(true);
      setError(null);
      await diagramService.generateDiagram(documentId);
      await loadDiagrams(documentId);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to generate diagram');
    } finally {
      setGenerating(false);
    }
  }, [loadDiagrams]);

  const selectDiagram = useCallback((diagramId: string) => {
    const diagram = diagrams.find(d => d.id === diagramId);
    if (diagram) {
      setCurrentDiagram(diagram);
      setZoom(1);
    }
  }, [diagrams]);

  const zoomIn = useCallback(() => {
    setZoom(prev => Math.min(prev + 0.25, 3));
  }, []);

  const zoomOut = useCallback(() => {
    setZoom(prev => Math.max(prev - 0.25, 0.25));
  }, []);

  const resetZoom = useCallback(() => {
    setZoom(1);
  }, []);

  return {
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
  };
}