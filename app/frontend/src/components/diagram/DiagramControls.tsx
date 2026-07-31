'use client';

interface DiagramControlsProps {
  diagrams: { id: string; title: string }[];
  currentDiagramId: string | null;
  onSelect: (diagramId: string) => void;
  onGenerate: () => void;
  generating: boolean;
}

export function DiagramControls({
  diagrams,
  currentDiagramId,
  onSelect,
  onGenerate,
  generating,
}: DiagramControlsProps) {
  return (
    <div className="bg-white rounded-lg shadow-sm border p-4">
      <div className="flex items-center justify-between mb-4">
        <h3 className="font-medium text-gray-900">Diagrams</h3>
        <button
          onClick={onGenerate}
          disabled={generating}
          className="px-3 py-1 text-sm bg-blue-500 text-white rounded hover:bg-blue-600 disabled:opacity-50"
        >
          {generating ? 'Generating...' : 'Generate'}
        </button>
      </div>
      
      {diagrams.length === 0 ? (
        <p className="text-sm text-gray-500">No diagrams available</p>
      ) : (
        <div className="space-y-2">
          {diagrams.map((diagram) => (
            <button
              key={diagram.id}
              onClick={() => onSelect(diagram.id)}
              className={`w-full text-left px-3 py-2 rounded text-sm ${
                currentDiagramId === diagram.id
                  ? 'bg-blue-50 text-blue-700 border border-blue-200'
                  : 'hover:bg-gray-50 text-gray-700'
              }`}
            >
              {diagram.title}
            </button>
          ))}
        </div>
      )}
    </div>
  );
}

export default DiagramControls;