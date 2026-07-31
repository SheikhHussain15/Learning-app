'use client';

interface QuickActionsProps {
  className?: string;
}

export function QuickActions({ className = '' }: QuickActionsProps) {
  const actions = [
    { label: 'Continue Learning', href: '/library', color: 'bg-blue-500 hover:bg-blue-600' },
    { label: 'Take a Quiz', href: '/library', color: 'bg-green-500 hover:bg-green-600' },
    { label: 'Review Flashcards', href: '/library', color: 'bg-purple-500 hover:bg-purple-600' },
    { label: 'Ask AI Tutor', href: '/library', color: 'bg-orange-500 hover:bg-orange-600' },
  ];

  return (
    <div className={`bg-white rounded-lg shadow-sm border p-6 ${className}`}>
      <h3 className="text-lg font-semibold text-gray-900 mb-4">Quick Actions</h3>
      <div className="grid grid-cols-2 gap-3">
        {actions.map((action) => (
          <a
            key={action.label}
            href={action.href}
            className={`${action.color} text-white px-4 py-3 rounded-lg text-sm font-medium text-center transition-colors`}
          >
            {action.label}
          </a>
        ))}
      </div>
    </div>
  );
}

export default QuickActions;