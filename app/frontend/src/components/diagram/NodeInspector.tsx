'use client';

interface NodeInspectorProps {
  node: { id: string; label: string; description?: string } | null;
  onClose: () => void;
}

export function NodeInspector({ node, onClose }: NodeInspectorProps) {
  if (!node) {
    return null;
  }

  return (
    <div className="bg-white rounded-lg shadow-sm border p-4">
      <div className="flex items-center justify-between mb-2">
        <h4 className="font-medium text-gray-900">{node.label}</h4>
        <button
          onClick={onClose}
          className="text-gray-400 hover:text-gray-600"
        >
          <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
      </div>
      {node.description && (
        <p className="text-sm text-gray-600">{node.description}</p>
      )}
    </div>
  );
}

export default NodeInspector;