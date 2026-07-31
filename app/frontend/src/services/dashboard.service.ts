import api from './api';
import { DashboardData, ActivityItem, LearningStatistics, StudyProgress, LearningStreak, RecentlyViewedDocument } from '../types/dashboard';

export const dashboardService = {
  getDashboard: () => api.get<DashboardData>('/dashboard'),

  getRecentActivity: (limit = 10) =>
    api.get<ActivityItem[]>(`/dashboard/recent-activity?limit=${limit}`),

  getStatistics: () => api.get<LearningStatistics>('/dashboard/statistics'),

  getProgress: () => api.get<StudyProgress>('/dashboard/progress'),

  getStreak: () => api.get<LearningStreak>('/dashboard/streak'),

  getRecentlyViewed: (limit = 5) =>
    api.get<RecentlyViewedDocument[]>(`/dashboard/recently-viewed?limit=${limit}`),
};

export default dashboardService;