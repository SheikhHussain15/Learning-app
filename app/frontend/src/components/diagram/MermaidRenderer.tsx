'use client';

import { useEffect, useRef } from 'react';

interface MermaidRendererProps {
  code: string;
  zoom?: number;
}

export function MermaidRenderer({ code, zoom = 1 }: MermaidRendererProps) {
  const containerRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (containerRef.current && code) {
      containerRef.current.innerHTML = `
        <div class="mermaid" style="transform: scale(${zoom}); transform-origin: top left;">
          ${code}
        </div>
      `;
    }
  }, [code, zoom]);

  return (
    <div
      ref={containerRef}
      className="mermaid-container"
      style={{ minHeight: '200px' }}
    />
  );
}

export default MermaidRenderer;