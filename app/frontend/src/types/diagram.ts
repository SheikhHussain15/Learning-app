export type DiagramType = 'flowchart' | 'mind_map' | 'timeline' | 'concept_map' | 'sequence' | 'class' | 'state' | 'er';

export interface Diagram {
  id: string;
  document_id: string;
  title: string;
  description: string;
  diagram_type: DiagramType;
  content: Record<string, unknown>;
  source_refs: string[];
  created_at: string;
}

export type RenderFormat = 'mermaid' | 'svg' | 'json';

export interface DiagramRenderData {
  diagram_id: string;
  format: RenderFormat;
  data: string;
  metadata: {
    width: number;
    height: number;
    node_count: number;
    edge_count: number;
  };
}