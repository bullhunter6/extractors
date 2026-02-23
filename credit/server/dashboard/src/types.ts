export type ExtractorStatus = 'idle' | 'running' | 'success' | 'failed' | 'disabled';
export type ExtractorCategory = 
  | 'banks_me' | 'banks_ca' | 'banks_ca_me' | 'banks_rating'
  | 'corporates_me' | 'corporates_ca' | 'corporates_ca_me' | 'corporates_rating'
  | 'sovereigns_me' | 'sovereigns_ca' | 'sovereigns_ca_me' | 'sovereigns_rating'
  | 'global' | 'events' | 'publications' | 'methodologies';

export interface Extractor {
  id: number;
  name: string;
  display_name: string;
  description: string | null;
  category: ExtractorCategory;
  module_path: string;
  function_name: string;
  enabled: boolean;
  status: ExtractorStatus;
  schedule_cron: string | null;
  schedule_interval_minutes: number | null;
  timeout_seconds: number;
  max_retries: number;
  retry_backoff_seconds: number;
  current_task_id: string | null;
  total_runs: number;
  successful_runs: number;
  failed_runs: number;
  last_run_at: string | null;
  last_success_at: string | null;
  last_error: string | null;
  created_at: string;
  updated_at: string;
}

export interface ExtractorRun {
  id: number;
  extractor_id: number;
  extractor_name: string;
  task_id: string;
  status: ExtractorStatus;
  started_at: string;
  completed_at: string | null;
  duration_seconds: number | null;
  items_extracted: number;
  error_message: string | null;
  error_traceback: string | null;
  worker_name: string | null;
  retry_count: number;
}

export interface SystemMetrics {
  timestamp: string;
  total_extractors: number;
  enabled_extractors: number;
  running_extractors: number;
  active_tasks: number;
  pending_tasks: number;
  avg_duration_seconds: number | null;
  success_rate: number | null;
  cpu_percent: number | null;
  memory_percent: number | null;
}

export interface WSMessage {
  type: string;
  data: any;
  timestamp: string;
}
