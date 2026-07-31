'use client';

import { EmptyState } from '../ui/EmptyState';

interface SavedNotesProps {
  className?: string;
}

export function SavedNotes({ className = '' }: SavedNotesProps) {
  return (
    <div className={`bg-white rounded-lg shadow-sm border p-6 ${className}`}>
      <h3 className="text-lg font-semibold text-gray-900 mb-4">Saved Notes</h3>
      <EmptyState
        title="No notes yet"
        description="Save notes while studying to review them later."
      />
    </div>
  );
}

export default SavedNotes;