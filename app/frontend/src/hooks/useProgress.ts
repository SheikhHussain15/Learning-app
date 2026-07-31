'use client';

import { useState, useCallback } from 'react';
import { progressService } from '../services/progress.service';
import { ProgressEventInput, ProgressSummary } from '../types/progress';

interface UseProgressReturn {
  stats: ProgressSummary | null;
  loading: boolean;
  error: string | null;
  recordEvent: (request: ProgressEventInput) => Promise<void>;
  loadStats: (documentId?: string) => Promise<void>;
}

export function useProgress(): UseProgressReturn {
  const [stats, setStats] = useState<ProgressSummary | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const recordEvent = useCallback(async (request: ProgressEventInput) => {
    try {
      await progressService.recordEvent(request);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to record event');
    }
  }, []);

  const loadStats = useCallback(async (documentId?: string) => {
    try {
      setLoading(true);
      setError(null);
      const response = await progressService.getStats(documentId);
      setStats(response);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load stats');
    } finally {
      setLoading(false);
    }
  }, []);

  return {
    stats,
    loading,
    error,
    recordEvent,
    loadStats,
  };
}