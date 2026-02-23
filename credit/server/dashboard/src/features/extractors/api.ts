import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import type { Extractor, ExtractorRun, ExtractorCategory, ExtractorStatus } from './types';
import { api } from '../../api-client';

export function useExtractors(params?: {
  category?: ExtractorCategory;
  enabled?: boolean;
  status?: ExtractorStatus;
}) {
  return useQuery({
    queryKey: ['extractors', params],
    queryFn: async () => {
      const response = await api.get<{ extractors: Extractor[]; total: number }>('/extractors', { params });
      return response.data;
    },
    refetchInterval: 5000, // Auto-refresh every 5s
  });
}

export function useExtractor(id: number) {
  return useQuery({
    queryKey: ['extractor', id],
    queryFn: async () => {
      const response = await api.get<Extractor>(`/extractors/${id}`);
      return response.data;
    },
  });
}

export function useTriggerExtractor() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async (id: number) => {
      const response = await api.post(`/extractors/${id}/trigger`);
      return response.data;
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['extractors'] });
      queryClient.invalidateQueries({ queryKey: ['metrics'] });
    },
  });
}

export function useTriggerBatch() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async (ids: number[]) => {
      const response = await api.post('/extractors/trigger-batch', { extractor_ids: ids });
      return response.data;
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['extractors'] });
      queryClient.invalidateQueries({ queryKey: ['metrics'] });
    },
  });
}

export function useUpdateExtractor() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async ({ id, data }: { id: number; data: Partial<Extractor> }) => {
      const response = await api.patch(`/extractors/${id}`, data);
      return response.data;
    },
    onSuccess: (_, variables) => {
      queryClient.invalidateQueries({ queryKey: ['extractor', variables.id] });
      queryClient.invalidateQueries({ queryKey: ['extractors'] });
    },
  });
}

export function useExtractorRuns(id: number) {
  return useQuery({
    queryKey: ['extractor-runs', id],
    queryFn: async () => {
      const response = await api.get<{ runs: ExtractorRun[]; total: number }>(`/extractors/${id}/runs`);
      return response.data;
    },
  });
}
