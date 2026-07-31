import api from './api';
import { Diagram, DiagramRenderData } from '../types/diagram';

export const diagramService = {
  generateDiagram: (documentId: string) =>
    api.post('/diagram/generate', { document_id: documentId }),

  getDiagrams: (documentId: string) =>
    api.get<Diagram[]>(`/diagram/${documentId}`),

  getDiagram: (diagramId: string, documentId?: string) =>
    api.get<Diagram>(`/diagram/${diagramId}/detail?document_id=${documentId || ''}`),

  getDiagramRender: (diagramId: string, format: string = 'mermaid') =>
    api.get<DiagramRenderData>(`/diagram/${diagramId}/render?format=${format}`),

  interactWithDiagram: (diagramId: string, documentId: string) =>
    api.post(`/diagram/${diagramId}/interact?document_id=${documentId}`, {}),
};

export default diagramService;