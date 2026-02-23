import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';

const API_BASE = '/api/v1';

export interface ScheduleStatus {
  enabled: boolean;
  interval_minutes: number;
  next_run_at: string | null;
  last_run_at: string | null;
}

export interface SchedulerStats {
  total_extractors: number;
  enabled_extractors: number;
  disabled_extractors: number;
  running_extractors: number;
  idle_extractors: number;
  failed_extractors: number;
  total_runs: number;
  successful_runs: number;
  failed_runs: number;
  success_rate: number;
  runs_today: number;
  successful_today: number;
  failed_today: number;
  success_rate_today: number;
  runs_last_24h: number;
  successful_last_24h: number;
  failed_last_24h: number;
  avg_duration_last_24h: number | null;
  last_scheduled_run_at: string | null;
  last_scheduled_run_success_count: number;
  last_scheduled_run_failure_count: number;
  recent_failed_extractors: Array<{
    id: number;
    name: string;
    last_error: string | null;
    last_run_at: string | null;
    failed_runs: number;
  }>;
  extractors_by_category: Record<string, number>;
  top_extractors: Array<{
    id: number;
    name: string;
    total_runs: number;
    success_rate: number;
    avg_duration: number | null;
  }>;
  worst_extractors: Array<{
    id: number;
    name: string;
    total_runs: number;
    failed_runs: number;
    success_rate: number;
    last_error: string | null;
  }>;
}

export interface BatchTriggerResponse {
  message: string;
  triggered_count: number;
  task_ids: string[];
}

export const useScheduleStatus = () => {
  return useQuery<ScheduleStatus>({
    queryKey: ['schedule-status'],
    queryFn: async () => {
      const res = await fetch(`${API_BASE}/scheduler/status`);
      if (!res.ok) throw new Error('Failed to fetch schedule status');
      return res.json();
    },
    refetchInterval: 10000,
  });
};

export const useSchedulerStats = () => {
  return useQuery<SchedulerStats>({
    queryKey: ['scheduler-stats'],
    queryFn: async () => {
      const res = await fetch(`${API_BASE}/scheduler/stats`);
      if (!res.ok) throw new Error('Failed to fetch scheduler stats');
      return res.json();
    },
    refetchInterval: 5000,
  });
};

export const useUpdateScheduleConfig = () => {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: async (config: { enabled: boolean; interval_minutes: number }) => {
      const res = await fetch(`${API_BASE}/scheduler/config`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(config),
      });
      if (!res.ok) throw new Error('Failed to update schedule config');
      return res.json();
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['schedule-status'] });
    },
  });
};

export interface StopAllResponse {
  message: string;
  revoked_tasks: number;
  purged_tasks: number;
  reset_extractors: number;
}

export interface RecentRun {
  id: number;
  extractor_name: string;
  status: string;
  started_at: string | null;
  duration_seconds: number | null;
  items_extracted: number;
  error_message: string | null;
}

export const useRecentRuns = (limit = 30) => {
  return useQuery<RecentRun[]>({
    queryKey: ['recent-runs', limit],
    queryFn: async () => {
      const res = await fetch(`${API_BASE}/scheduler/recent-runs?limit=${limit}`);
      if (!res.ok) throw new Error('Failed to fetch recent runs');
      return res.json();
    },
    refetchInterval: 10000,
  });
};

export const useStopAll = () => {
  const queryClient = useQueryClient();

  return useMutation<StopAllResponse>({
    mutationFn: async () => {
      const res = await fetch(`${API_BASE}/scheduler/stop-all`, {
        method: 'POST',
      });
      if (!res.ok) throw new Error('Failed to stop all extractors');
      return res.json();
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['scheduler-stats'] });
      queryClient.invalidateQueries({ queryKey: ['extractors'] });
      queryClient.invalidateQueries({ queryKey: ['schedule-status'] });
    },
  });
};

export const useTriggerAll = () => {
  const queryClient = useQueryClient();
  
  return useMutation<BatchTriggerResponse>({
    mutationFn: async () => {
      const res = await fetch(`${API_BASE}/scheduler/trigger-all`, {
        method: 'POST',
      });
      if (!res.ok) throw new Error('Failed to trigger all extractors');
      return res.json();
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['scheduler-stats'] });
      queryClient.invalidateQueries({ queryKey: ['extractors'] });
    },
  });
};
