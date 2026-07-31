'use client';

interface ZoomControlsProps {
  zoom: number;
  onZoomIn: () => void;
  onZoomOut: () => void;
  onResetZoom: () => void;
}

export function ZoomControls({ zoom, onZoomIn, onZoomOut, onResetZoom }: ZoomControlsProps) {
  return (
    <div className="absolute top-2 right-2 z-10 flex items-center space-x-2 bg-white rounded-lg shadow-sm border p-1">
      <button
        onClick={onZoomOut}
        className="p-1 hover:bg-gray-100 rounded"
        title="Zoom out"
      >
        <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M20 12H4" />
        </svg>
      </button>
      <span className="text-sm text-gray-600 min-w-[40px] text-center">
        {Math.round(zoom * 100)}%
      </span>
      <button
        onClick={onZoomIn}
        className="p-1 hover:bg-gray-100 rounded"
        title="Zoom in"
      >
        <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
        </svg>
      </button>
      <button
        onClick={onResetZoom}
        className="p-1 hover:bg-gray-100 rounded text-xs"
        title="Reset zoom"
      >
        Reset
      </button>
    </div>
  );
}

export default ZoomControls;