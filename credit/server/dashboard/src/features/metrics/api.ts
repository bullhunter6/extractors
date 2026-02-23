import { useQuery } from '@tanstack/react-query';
import type { SystemMetrics } from './types';
import { api } from '../../api-client';

export function useSystemMetrics() {
  return useQuery({
    queryKey: ['metrics', 'system'],
    queryFn: async () => {
      const response = await api.get<SystemMetrics>('/metrics/system');
      return response.data;
    },
    refetchInterval: 10000, // Refresh every 10s
  });
}

export function useExtractorMetrics(days = 7) {
  return useQuery({
    queryKey: ['metrics', 'extractors', days],
    queryFn: async () => {
      const response = await api.get('/metrics/extractors', { params: { days } });
      return response.data;
    },
  });
}

export function useRecentRuns(limit = 20) {
  return useQuery({
    queryKey: ['metrics', 'recent-runs', limit],
    queryFn: async () => {
      const response = await api.get('/metrics/runs/recent', { params: { limit } });
      return response.data;
    },
  });
}
