import api from './api';
import { WorkspaceOverview, SectionRequestResponse, SectionStatusResponse, SectionContentResponse, SectionType } from '../types/workspace';

export const workspaceService = {
  getWorkspace: (documentId: string) =>
    api.get<WorkspaceOverview>(`/workspace/${documentId}`),

  getSectionStatus: (documentId: string, sectionType: SectionType) =>
    api.get<SectionStatusResponse>(`/workspace/${documentId}/sections/${sectionType}/status`),

  requestGeneration: (documentId: string, sectionType: SectionType) =>
    api.post<SectionRequestResponse>(`/workspace/${documentId}/sections/${sectionType}/request`, {}),

  getSectionContent: (documentId: string, sectionType: SectionType) =>
    api.get<SectionContentResponse>(`/workspace/${documentId}/sections/${sectionType}/content`),
};

export default workspaceService;