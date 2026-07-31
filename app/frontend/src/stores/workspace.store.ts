'use client';

import { useState, useCallback } from 'react';
import { WorkspaceOverview, SectionType, SectionStatus } from '../types/workspace';

const defaultSectionStatuses: Record<SectionType, SectionStatus> = {
  summary: 'not_requested',
  explanation: 'not_requested',
  translation: 'not_requested',
  diagram: 'not_requested',
  quiz: 'not_requested',
  flashcard: 'not_requested',
  revision_notes: 'not_requested',
};

interface UseWorkspaceStoreReturn {
  workspace: WorkspaceOverview | null;
  sectionStatuses: Record<SectionType, SectionStatus>;
  setWorkspace: (workspace: WorkspaceOverview) => void;
  updateSectionStatus: (sectionType: SectionType, status: SectionStatus) => void;
  reset: () => void;
}

export function useWorkspaceStore(): UseWorkspaceStoreReturn {
  const [workspace, setWorkspaceState] = useState<WorkspaceOverview | null>(null);
  const [sectionStatuses, setSectionStatuses] = useState<Record<SectionType, SectionStatus>>({ ...defaultSectionStatuses });

  const setWorkspace = useCallback((workspace: WorkspaceOverview) => {
    const statuses = { ...defaultSectionStatuses };
    workspace.sections.forEach((section) => {
      statuses[section.section_type] = section.status;
    });
    setWorkspaceState(workspace);
    setSectionStatuses(statuses);
  }, []);

  const updateSectionStatus = useCallback((sectionType: SectionType, status: SectionStatus) => {
    setSectionStatuses(prev => ({ ...prev, [sectionType]: status }));
  }, []);

  const reset = useCallback(() => {
    setWorkspaceState(null);
    setSectionStatuses({ ...defaultSectionStatuses });
  }, []);

  return {
    workspace,
    sectionStatuses,
    setWorkspace,
    updateSectionStatus,
    reset,
  };
}

export default useWorkspaceStore;