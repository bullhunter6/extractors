import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { api } from '../../api-client';

export interface ExtractorStats {
  id: number;
  name: string;
  status: string;
  category: string;
  enabled: boolean;
  total_runs: number;
  successful_runs: number;
  failed_runs: number;
  success_rate: number;
  avg_duration_seconds: number;
  last_run_at: string | null;
  last_success_at: string | null;
  last_error: string | null;
  current_task_id: string | null;
  recent_runs: ExtractorRun[];
}

export interface ExtractorRun {
  id: number;
  task_id: string;
  status: string;
  items_extracted: number;
  duration_seconds: number;
  started_at: string;
  completed_at: string | null;
  error_message: string | null;
  logs?: string;
}

export interface RunLogs {
  run_id: number;
  extractor_id: number;
  task_id: string;
  status: string;
  logs: string;
  started_at: string;
  completed_at: string | null;
}

// Get extractor stats
export const useExtractorStats = (extractorId: number) => {
  return useQuery<ExtractorStats>({
    queryKey: ['extractor-stats', extractorId],
    queryFn: async () => {
      const { data } = await api.get(`/extractors/${extractorId}/stats`);
      return data;
    },
    refetchInterval: 5000, // Refetch every 5 seconds
  });
};

// Get run logs
export const useRunLogs = (extractorId: number, runId: number) => {
  return useQuery<RunLogs>({
    queryKey: ['run-logs', extractorId, runId],
    queryFn: async () => {
      const { data } = await api.get(`/extractors/${extractorId}/runs/${runId}/logs`);
      return data;
    },
    enabled: !!runId,
  });
};

// Trigger single extractor
export const useTriggerExtractor = () => {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: async (extractorId: number) => {
      const { data } = await api.post(`/extractors/${extractorId}/trigger`);
      return data;
    },
    onSuccess: (_, extractorId) => {
      queryClient.invalidateQueries({ queryKey: ['extractor-stats', extractorId] });
      queryClient.invalidateQueries({ queryKey: ['extractors'] });
    },
  });
};
