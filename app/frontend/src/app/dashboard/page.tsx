'use client';

import { useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { useAuth } from '../../contexts/auth-context';
import { useDashboard } from '../../hooks/useDashboard';
import { RecentLearning } from '../../components/dashboard/RecentLearning';
import { LearningStatistics } from '../../components/dashboard/LearningStatistics';
import { StudyProgress } from '../../components/dashboard/StudyProgress';
import { LearningStreak } from '../../components/dashboard/LearningStreak';
import { Recommendations } from '../../components/dashboard/Recommendations';
import { SavedNotes } from '../../components/dashboard/SavedNotes';
import { RecentlyViewed } from '../../components/dashboard/RecentlyViewed';
import { QuickActions } from '../../components/dashboard/QuickActions';
import { LoadingSpinner } from '../../components/ui/LoadingSpinner';
import { ErrorState } from '../../components/ui/ErrorState';

export default function DashboardPage() {
  const { token } = useAuth();
  const router = useRouter();
  const { dashboard, loading, error } = useDashboard();

  useEffect(() => {
    if (!token) router.push('/login');
  }, [token, router]);

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <LoadingSpinner size="lg" />
      </div>
    );
  }

  if (error) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <ErrorState message={error} />
      </div>
    );
  }

  if (!dashboard) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <ErrorState message="Failed to load dashboard" />
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-8">Dashboard</h1>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          <div className="lg:col-span-2 space-y-6">
            <RecentLearning activities={dashboard.recent_activity} />
            <StudyProgress progress={dashboard.progress} />
            <RecentlyViewed documents={dashboard.recently_viewed} />
          </div>

          <div className="space-y-6">
            <LearningStatistics statistics={dashboard.statistics} />
            <LearningStreak streak={dashboard.streak} />
            <Recommendations recommendations={dashboard.recommendations} />
            <SavedNotes />
            <QuickActions />
          </div>
        </div>
      </div>
    </div>
  );
}