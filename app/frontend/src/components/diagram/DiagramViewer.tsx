'use client';

import { Diagram } from '../../types/diagram';
import { MermaidRenderer } from './MermaidRenderer';
import { ZoomControls } from './ZoomControls';

interface DiagramViewerProps {
  diagram: Diagram;
  zoom: number;
  onZoomIn: () => void;
  onZoomOut: () => void;
  onResetZoom: () => void;
}

export function DiagramViewer({ diagram, zoom, onZoomIn, onZoomOut, onResetZoom }: DiagramViewerProps) {
  return (
    <div className="bg-white rounded-lg shadow-sm border overflow-hidden">
      <div className="p-4 border-b">
        <h3 className="text-lg font-semibold text-gray-900">{diagram.title}</h3>
        {diagram.description && (
          <p className="text-sm text-gray-600 mt-1">{diagram.description}</p>
        )}
      </div>
      
      <div className="relative p-4">
        <ZoomControls
          zoom={zoom}
          onZoomIn={onZoomIn}
          onZoomOut={onZoomOut}
          onResetZoom={onResetZoom}
        />
        
        <div
          className="overflow-auto"
          style={{ maxHeight: '500px' }}
        >
          <MermaidRenderer
            code={JSON.stringify(diagram.content)}
            zoom={zoom}
          />
        </div>
      </div>
      
      {diagram.source_refs && diagram.source_refs.length > 0 && (
        <div className="p-4 border-t bg-gray-50">
          <h4 className="text-sm font-medium text-gray-700 mb-2">References</h4>
          <div className="flex flex-wrap gap-2">
            {diagram.source_refs.map((ref, index) => (
              <span
                key={index}
                className="px-2 py-1 bg-blue-100 text-blue-800 text-xs rounded-full"
              >
                {ref}
              </span>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}

export default DiagramViewer;