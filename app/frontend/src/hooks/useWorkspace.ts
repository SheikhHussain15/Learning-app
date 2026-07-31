'use client';

import { useState, useEffect, useCallback } from 'react';
import { workspaceService } from '../services/workspace.service';
import { WorkspaceOverview, SectionType, SectionStatus } from '../types/workspace';

interface UseWorkspaceReturn {
  workspace: WorkspaceOverview | null;
  loading: boolean;
  error: string | null;
  refresh: () => Promise<void>;
  requestGeneration: (sectionType: SectionType) => Promise<void>;
  getSectionStatus: (sectionType: SectionType) => SectionStatus;
}

export function useWorkspace(documentId: string): UseWorkspaceReturn {
  const [workspace, setWorkspace] = useState<WorkspaceOverview | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchWorkspace = useCallback(async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await workspaceService.getWorkspace(documentId);
      setWorkspace(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load workspace');
    } finally {
      setLoading(false);
    }
  }, [documentId]);

  useEffect(() => {
    fetchWorkspace();
  }, [fetchWorkspace]);

  const requestGeneration = useCallback(async (sectionType: SectionType) => {
    try {
      await workspaceService.requestGeneration(documentId, sectionType);
      await fetchWorkspace();
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to request generation');
    }
  }, [documentId, fetchWorkspace]);

  const getSectionStatus = useCallback((sectionType: SectionType): SectionStatus => {
    const section = workspace?.sections.find(s => s.section_type === sectionType);
    return section?.status || 'not_requested';
  }, [workspace]);

  return {
    workspace,
    loading,
    error,
    refresh: fetchWorkspace,
    requestGeneration,
    getSectionStatus,
  };
}