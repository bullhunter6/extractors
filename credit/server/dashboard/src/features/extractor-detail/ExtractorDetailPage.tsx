import React, { useEffect, useRef, useState, useCallback } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { 
  ArrowLeft, 
  Play, 
  Clock, 
  CheckCircle, 
  XCircle, 
  Activity,
  Terminal as TerminalIcon,
  History,
  RefreshCw,
  Loader2,
  AlertTriangle,
  ChevronDown,
  ChevronRight,
  ExternalLink
} from 'lucide-react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { TerminalLogViewer } from '../../components/terminal';

const API_BASE = 'http://localhost:8000/api/v1';
const WS_BASE = 'ws://localhost:8000';

interface Extractor {
  id: number;
  name: string;
  module_path: string;
  category: string;
  region: string | null;
  source: string | null;
  description: string | null;
  status: string;
  is_enabled: boolean;
  last_run_at: string | null;
  last_success_at: string | null;
  last_error: string | null;
  total_runs: number;
  successful_runs: number;
  failed_runs: number;
  average_duration: number | null;
  created_at: string;
  updated_at: string;
}

interface ExtractorRun {
  id: number;
  extractor_id: number;
  task_id: string | null;
  status: string;
  started_at: string | null;
  completed_at: string | null;
  duration: number | null;
  error_message: string | null;
  result: any | null;
  logs: string | null;
  triggered_by: string;
  created_at: string;
}

interface LogEntry {
  timestamp: string;
  level: string;
  message: string;
  extractor_id?: number;
  task_id?: string;
}

interface RunsResponse {
  runs: ExtractorRun[];
  total: number;
}

const StatusBadge: React.FC<{ status: string }> = ({ status }) => {
  const styles: Record<string, string> = {
    idle: 'bg-gray-700 text-gray-300',
    running: 'bg-blue-600/20 text-blue-400 border border-blue-500/50',
    success: 'bg-green-600/20 text-green-400 border border-green-500/50',
    failed: 'bg-red-600/20 text-red-400 border border-red-500/50',
    pending: 'bg-yellow-600/20 text-yellow-400 border border-yellow-500/50',
  };
  
  return (
    <span className={`px-3 py-1 rounded-full text-xs font-medium uppercase tracking-wide ${styles[status] || styles.idle}`}>
      {status}
    </span>
  );
};

const StatCard: React.FC<{ 
  icon: React.ReactNode; 
  label: string; 
  value: string | number;
  subValue?: string;
  color: string;
}> = ({ icon, label, value, subValue, color }) => (
  <div className={`bg-gray-800/50 rounded-xl p-4 border border-gray-700/50 hover:border-${color}-500/50 transition-colors`}>
    <div className="flex items-center gap-3">
      <div className={`p-2 rounded-lg bg-${color}-500/20 text-${color}-400`}>
        {icon}
      </div>
      <div>
        <p className="text-gray-400 text-sm">{label}</p>
        <p className="text-white text-xl font-semibold">{value}</p>
        {subValue && <p className="text-gray-500 text-xs">{subValue}</p>}
      </div>
    </div>
  </div>
);

const RunHistoryItem: React.FC<{ 
  run: ExtractorRun; 
  isExpanded: boolean;
  onToggle: () => void;
  isLoadingLogs: boolean;
}> = ({ run, isExpanded, onToggle, isLoadingLogs }) => {
  const formatDuration = (seconds: number | null) => {
    if (!seconds) return '-';
    if (seconds < 60) return `${seconds.toFixed(1)}s`;
    return `${Math.floor(seconds / 60)}m ${Math.floor(seconds % 60)}s`;
  };

  const formatTime = (dateStr: string | null) => {
    if (!dateStr) return '-';
    return new Date(dateStr).toLocaleString();
  };

  return (
    <motion.div 
      className="border border-gray-700/50 rounded-lg overflow-hidden bg-gray-800/30"
      initial={false}
    >
      <button
        onClick={onToggle}
        className="w-full flex items-center justify-between p-4 hover:bg-gray-700/30 transition-colors"
      >
        <div className="flex items-center gap-4">
          {isExpanded ? (
            <ChevronDown className="w-4 h-4 text-gray-400" />
          ) : (
            <ChevronRight className="w-4 h-4 text-gray-400" />
          )}
          <StatusBadge status={run.status} />
          <span className="text-gray-300 text-sm">
            {formatTime(run.started_at)}
          </span>
        </div>
        <div className="flex items-center gap-6 text-sm">
          <span className="text-gray-400">
            <Clock className="w-4 h-4 inline mr-1" />
            {formatDuration(run.duration)}
          </span>
          <span className="text-gray-500 text-xs font-mono">
            {run.task_id?.substring(0, 8)}...
          </span>
        </div>
      </button>

      {isExpanded && (
        <motion.div
          initial={{ height: 0, opacity: 0 }}
          animate={{ height: 'auto', opacity: 1 }}
          exit={{ height: 0, opacity: 0 }}
          className="border-t border-gray-700/50"
        >
          <div className="p-4">
            {run.error_message && (
              <div className="mb-4 p-3 bg-red-500/10 border border-red-500/30 rounded-lg">
                <p className="text-red-400 text-sm font-mono">{run.error_message}</p>
              </div>
            )}
            
            {isLoadingLogs ? (
              <div className="flex items-center justify-center py-8">
                <Loader2 className="w-6 h-6 text-cyan-400 animate-spin" />
              </div>
            ) : (
              <div className="font-mono text-xs bg-gray-950 rounded-lg p-4 max-h-60 overflow-y-auto">
                {run.logs ? (
                  run.logs.split('\n').map((line, idx) => (
                    <div key={idx} className={`
                      ${line.includes('[ERROR]') ? 'text-red-400' : ''}
                      ${line.includes('[WARNING]') ? 'text-yellow-400' : ''}
                      ${line.includes('[INFO]') ? 'text-cyan-400' : ''}
                      ${!line.includes('[') ? 'text-green-400' : ''}
                    `}>
                      {line}
                    </div>
                  ))
                ) : (
                  <span className="text-gray-500">No logs available</span>
                )}
              </div>
            )}
          </div>
        </motion.div>
      )}
    </motion.div>
  );
};

export const ExtractorDetailPage: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const queryClient = useQueryClient();
  const extractorId = parseInt(id || '0');

  const [liveLogs, setLiveLogs] = useState<LogEntry[]>([]);
  const [isConnected, setIsConnected] = useState(false);
  const [expandedRunId, setExpandedRunId] = useState<number | null>(null);
  const wsRef = useRef<WebSocket | null>(null);

  // Fetch extractor details
  const { data: extractor, isLoading: isLoadingExtractor } = useQuery<Extractor>({
    queryKey: ['extractor', extractorId],
    queryFn: async () => {
      const res = await fetch(`${API_BASE}/extractors/${extractorId}`);
      if (!res.ok) throw new Error('Failed to fetch extractor');
      return res.json();
    },
    refetchInterval: 5000,
  });

  // Fetch run history
  const { data: runsData, isLoading: isLoadingRuns } = useQuery<RunsResponse>({
    queryKey: ['extractor-runs', extractorId],
    queryFn: async () => {
      const res = await fetch(`${API_BASE}/extractors/${extractorId}/runs`);
      if (!res.ok) throw new Error('Failed to fetch runs');
      return res.json();
    },
    refetchInterval: 5000,
  });
  
  const runs = runsData?.runs || [];

  // Trigger extractor mutation
  const triggerMutation = useMutation({
    mutationFn: async () => {
      const res = await fetch(`${API_BASE}/extractors/${extractorId}/trigger`, {
        method: 'POST',
      });
      if (!res.ok) throw new Error('Failed to trigger extractor');
      return res.json();
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['extractor', extractorId] });
      queryClient.invalidateQueries({ queryKey: ['extractor-runs', extractorId] });
      setLiveLogs([]); // Clear live logs for new run
    },
  });

  // WebSocket connection for live logs
  useEffect(() => {
    if (!extractorId) return;
    
    let reconnectTimeout: ReturnType<typeof setTimeout> | null = null;
    let isUnmounting = false;

    const connectWebSocket = () => {
      if (isUnmounting) return;
      
      try {
        const ws = new WebSocket(`${WS_BASE}/ws/logs/${extractorId}`);
        wsRef.current = ws;

        ws.onopen = () => {
          console.log('WebSocket connected');
          setIsConnected(true);
        };

        ws.onmessage = (event) => {
          try {
            const data = JSON.parse(event.data);
            setLiveLogs(prev => [...prev, data]);
          } catch (e) {
            console.error('Failed to parse log message:', e);
          }
        };

        ws.onclose = () => {
          console.log('WebSocket disconnected');
          setIsConnected(false);
          // Reconnect after 5 seconds if not unmounting
          if (!isUnmounting) {
            reconnectTimeout = setTimeout(connectWebSocket, 5000);
          }
        };

        ws.onerror = () => {
          // Silently handle - onclose will be called next
          setIsConnected(false);
        };
      } catch (e) {
        console.error('Failed to create WebSocket:', e);
        setIsConnected(false);
      }
    };

    connectWebSocket();

    return () => {
      isUnmounting = true;
      if (reconnectTimeout) {
        clearTimeout(reconnectTimeout);
      }
      if (wsRef.current) {
        wsRef.current.close();
        wsRef.current = null;
      }
    };
  }, [extractorId]);

  // Calculate success rate
  const successRate = extractor && extractor.total_runs > 0
    ? ((extractor.successful_runs / extractor.total_runs) * 100).toFixed(1)
    : '0';

  const formatDuration = (seconds: number | null) => {
    if (!seconds) return '-';
    if (seconds < 60) return `${seconds.toFixed(1)}s`;
    return `${Math.floor(seconds / 60)}m ${Math.floor(seconds % 60)}s`;
  };

  if (isLoadingExtractor) {
    return (
      <div className="min-h-screen bg-gray-900 flex items-center justify-center">
        <Loader2 className="w-8 h-8 text-cyan-400 animate-spin" />
      </div>
    );
  }

  if (!extractor) {
    return (
      <div className="min-h-screen bg-gray-900 flex items-center justify-center">
        <div className="text-center">
          <AlertTriangle className="w-12 h-12 text-yellow-400 mx-auto mb-4" />
          <h2 className="text-xl text-white mb-2">Extractor not found</h2>
          <button
            onClick={() => navigate('/')}
            className="text-cyan-400 hover:text-cyan-300"
          >
            Go back to dashboard
          </button>
        </div>
      </div>
    );
  }

  const latestRun = runs?.[0];

  return (
    <div className="min-h-screen bg-gray-900 text-white">
      {/* Header */}
      <header className="bg-gray-800/50 border-b border-gray-700/50 sticky top-0 z-10 backdrop-blur-md">
        <div className="w-full px-8 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-4">
              <button
                onClick={() => navigate('/')}
                className="p-2 hover:bg-gray-700/50 rounded-lg transition-colors"
              >
                <ArrowLeft className="w-5 h-5 text-gray-400" />
              </button>
              <div>
                <div className="flex items-center gap-3">
                  <h1 className="text-xl font-semibold">{extractor.name}</h1>
                  <StatusBadge status={extractor.status} />
                </div>
                <p className="text-gray-400 text-sm font-mono mt-1">
                  {extractor.module_path}
                </p>
              </div>
            </div>
            
            <div className="flex items-center gap-3">
              <div className={`flex items-center gap-2 px-3 py-1.5 rounded-lg ${
                isConnected ? 'bg-green-500/20 text-green-400' : 'bg-gray-700 text-gray-400'
              }`}>
                <div className={`w-2 h-2 rounded-full ${isConnected ? 'bg-green-400' : 'bg-gray-500'}`} />
                <span className="text-xs">{isConnected ? 'Connected' : 'Disconnected'}</span>
              </div>
              
              <button
                onClick={() => triggerMutation.mutate()}
                disabled={triggerMutation.isPending || extractor.status === 'running'}
                className="flex items-center gap-2 bg-cyan-600 hover:bg-cyan-500 disabled:bg-gray-700 
                  disabled:text-gray-400 px-4 py-2 rounded-lg transition-colors font-medium"
              >
                {triggerMutation.isPending ? (
                  <Loader2 className="w-4 h-4 animate-spin" />
                ) : (
                  <Play className="w-4 h-4" />
                )}
                Run Now
              </button>
            </div>
          </div>
        </div>
      </header>

      <main className="w-full px-8 py-8">
        {/* Stats Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
          <StatCard
            icon={<Activity className="w-5 h-5" />}
            label="Total Runs"
            value={extractor.total_runs}
            color="blue"
          />
          <StatCard
            icon={<CheckCircle className="w-5 h-5" />}
            label="Successful"
            value={extractor.successful_runs}
            subValue={`${successRate}% success rate`}
            color="green"
          />
          <StatCard
            icon={<XCircle className="w-5 h-5" />}
            label="Failed"
            value={extractor.failed_runs}
            color="red"
          />
          <StatCard
            icon={<Clock className="w-5 h-5" />}
            label="Avg Duration"
            value={formatDuration(extractor.average_duration)}
            color="purple"
          />
        </div>

        {/* Info Cards */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-4 mb-8">
          <div className="bg-gray-800/50 rounded-xl p-4 border border-gray-700/50">
            <h3 className="text-gray-400 text-sm mb-2">Category</h3>
            <p className="text-white capitalize">{extractor.category}</p>
          </div>
          <div className="bg-gray-800/50 rounded-xl p-4 border border-gray-700/50">
            <h3 className="text-gray-400 text-sm mb-2">Region</h3>
            <p className="text-white">{extractor.region || '-'}</p>
          </div>
          <div className="bg-gray-800/50 rounded-xl p-4 border border-gray-700/50">
            <h3 className="text-gray-400 text-sm mb-2">Source</h3>
            <p className="text-white">{extractor.source || '-'}</p>
          </div>
        </div>

        {/* Last Error */}
        {extractor.last_error && (
          <motion.div 
            initial={{ opacity: 0, y: -10 }}
            animate={{ opacity: 1, y: 0 }}
            className="mb-8 p-4 bg-red-500/10 border border-red-500/30 rounded-xl"
          >
            <div className="flex items-start gap-3">
              <AlertTriangle className="w-5 h-5 text-red-400 mt-0.5" />
              <div>
                <h3 className="text-red-400 font-medium mb-1">Last Error</h3>
                <p className="text-red-300/80 text-sm font-mono">{extractor.last_error}</p>
              </div>
            </div>
          </motion.div>
        )}

        {/* Live Logs Terminal - Full Width */}
        <div className="mb-8">
          <div className="flex items-center gap-2 mb-4">
            <TerminalIcon className="w-5 h-5 text-cyan-400" />
            <h2 className="text-lg font-semibold">Live Logs</h2>
          </div>
          <TerminalLogViewer
            logs={latestRun?.logs || ''}
            liveLogs={liveLogs}
            isLive={extractor.status === 'running'}
          />
        </div>

        {/* Run History - Full Width */}
        <div>
          <div className="flex items-center gap-2 mb-4">
            <History className="w-5 h-5 text-purple-400" />
            <h2 className="text-lg font-semibold">Run History</h2>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3 max-h-[400px] overflow-y-auto pr-2">
            {isLoadingRuns ? (
              <div className="col-span-full flex items-center justify-center py-8">
                <Loader2 className="w-6 h-6 text-cyan-400 animate-spin" />
              </div>
            ) : runs?.length === 0 ? (
              <div className="col-span-full text-center py-8 text-gray-500">
                <History className="w-8 h-8 mx-auto mb-2 opacity-50" />
                <p>No run history yet</p>
              </div>
            ) : (
              runs?.map(run => (
                <RunHistoryItem
                  key={run.id}
                  run={run}
                  isExpanded={expandedRunId === run.id}
                  onToggle={() => setExpandedRunId(
                    expandedRunId === run.id ? null : run.id
                  )}
                  isLoadingLogs={false}
                />
              ))
            )}
          </div>
        </div>
      </main>
    </div>
  );
};

export default ExtractorDetailPage;
