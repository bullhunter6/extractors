import React, { useEffect, useRef, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  ArrowLeft,
  Play,
  Pause,
  Square,
  Clock,
  CheckCircle,
  XCircle,
  Activity,
  Terminal as TerminalIcon,
  Calendar,
  TrendingUp,
  TrendingDown,
  AlertTriangle,
  Loader2,
  RefreshCw,
  Settings,
  BarChart3,
  Zap,
  Timer,
  Database,
  Server,
  Award,
  Skull
} from 'lucide-react';
import { useScheduleStatus, useSchedulerStats, useUpdateScheduleConfig, useTriggerAll, useStopAll, useRecentRuns } from './api';
import { formatDistanceToNow, format } from 'date-fns';

interface LogEntry {
  timestamp: string;
  level: string;
  message: string;
  extractor_id?: number;
  extractor_name?: string;
  task_id?: string;
}

const WS_BASE = 'ws://localhost:8000';

// Stat Card Component
const StatCard: React.FC<{
  icon: React.ReactNode;
  label: string;
  value: string | number;
  subValue?: string;
  trend?: 'up' | 'down' | 'neutral';
  color: string;
}> = ({ icon, label, value, subValue, trend, color }) => (
  <motion.div
    initial={{ opacity: 0, y: 20 }}
    animate={{ opacity: 1, y: 0 }}
    className={`bg-gray-800/50 rounded-xl p-4 border border-gray-700/50 hover:border-${color}-500/50 transition-all`}
  >
    <div className="flex items-center justify-between">
      <div className="flex items-center gap-3">
        <div className={`p-2.5 rounded-lg bg-${color}-500/20`}>
          <div className={`text-${color}-400`}>{icon}</div>
        </div>
        <div>
          <p className="text-gray-400 text-sm">{label}</p>
          <p className="text-white text-2xl font-bold">{value}</p>
          {subValue && (
            <p className={`text-xs ${trend === 'up' ? 'text-green-400' : trend === 'down' ? 'text-red-400' : 'text-gray-500'}`}>
              {trend === 'up' && <TrendingUp className="w-3 h-3 inline mr-1" />}
              {trend === 'down' && <TrendingDown className="w-3 h-3 inline mr-1" />}
              {subValue}
            </p>
          )}
        </div>
      </div>
    </div>
  </motion.div>
);

// Progress Ring Component
const ProgressRing: React.FC<{ percentage: number; size?: number; color?: string }> = ({ 
  percentage, 
  size = 120, 
  color = '#22d3ee' 
}) => {
  const strokeWidth = 8;
  const radius = (size - strokeWidth) / 2;
  const circumference = radius * 2 * Math.PI;
  const offset = circumference - (percentage / 100) * circumference;

  return (
    <div className="relative" style={{ width: size, height: size }}>
      <svg className="transform -rotate-90" width={size} height={size}>
        <circle
          cx={size / 2}
          cy={size / 2}
          r={radius}
          fill="transparent"
          stroke="#374151"
          strokeWidth={strokeWidth}
        />
        <motion.circle
          cx={size / 2}
          cy={size / 2}
          r={radius}
          fill="transparent"
          stroke={color}
          strokeWidth={strokeWidth}
          strokeLinecap="round"
          initial={{ strokeDashoffset: circumference }}
          animate={{ strokeDashoffset: offset }}
          transition={{ duration: 1, ease: 'easeOut' }}
          style={{ strokeDasharray: circumference }}
        />
      </svg>
      <div className="absolute inset-0 flex items-center justify-center">
        <span className="text-2xl font-bold text-white">{percentage.toFixed(1)}%</span>
      </div>
    </div>
  );
};

// Live Terminal for All Logs
const GlobalTerminal: React.FC<{ logs: LogEntry[]; isConnected: boolean; onClear: () => void }> = ({ logs, isConnected, onClear }) => {
  const terminalRef = useRef<HTMLDivElement>(null);
  const [autoScroll, setAutoScroll] = useState(true);

  useEffect(() => {
    if (autoScroll && terminalRef.current) {
      terminalRef.current.scrollTop = terminalRef.current.scrollHeight;
    }
  }, [logs, autoScroll]);

  const getLogColor = (level: string) => {
    switch (level?.toUpperCase()) {
      case 'ERROR': return 'text-red-400';
      case 'WARNING': return 'text-yellow-400';
      case 'INFO': return 'text-cyan-400';
      case 'DEBUG': return 'text-gray-500';
      default: return 'text-green-400';
    }
  };

  return (
    <div className="h-full flex flex-col">
      {/* Terminal Header */}
      <div className="flex items-center justify-between px-4 py-2 bg-gray-900 border-b border-gray-700 rounded-t-lg">
        <div className="flex items-center gap-2">
          <div className="flex gap-1.5">
            <div className="w-3 h-3 rounded-full bg-red-500"></div>
            <div className="w-3 h-3 rounded-full bg-yellow-500"></div>
            <div className="w-3 h-3 rounded-full bg-green-500"></div>
          </div>
          <span className="ml-3 text-gray-400 text-sm font-mono">all-extractors-logs</span>
          {isConnected && (
            <motion.div 
              className="flex items-center gap-1 ml-3"
              animate={{ opacity: [1, 0.5, 1] }}
              transition={{ duration: 1.5, repeat: Infinity }}
            >
              <div className="w-2 h-2 rounded-full bg-green-500"></div>
              <span className="text-green-400 text-xs">LIVE</span>
            </motion.div>
          )}
        </div>
        <div className="flex items-center gap-2">
          <span className="text-gray-500 text-xs">{logs.length} entries</span>
          <button 
            onClick={onClear}
            className="text-xs px-2 py-1 rounded bg-red-600/50 text-red-200 hover:bg-red-600 transition-colors"
          >
            Clear
          </button>
          <button 
            onClick={() => setAutoScroll(!autoScroll)}
            className={`text-xs px-2 py-1 rounded ${
              autoScroll ? 'bg-cyan-600 text-white' : 'bg-gray-700 text-gray-400'
            }`}
          >
            Auto-scroll
          </button>
        </div>
      </div>

      {/* Terminal Content */}
      <div 
        ref={terminalRef}
        className="flex-1 overflow-y-auto bg-gray-950 font-mono text-xs p-4 rounded-b-lg border border-t-0 border-gray-800"
        style={{ fontFamily: "'JetBrains Mono', 'Fira Code', 'Consolas', monospace" }}
      >
        {logs.length === 0 ? (
          <div className="text-gray-500 flex items-center gap-2">
            <TerminalIcon className="w-4 h-4" />
            <span>Waiting for logs... Run extractors to see output.</span>
          </div>
        ) : (
          <AnimatePresence>
            {logs.map((log, idx) => (
              <motion.div
                key={`${log.timestamp}-${idx}`}
                initial={{ opacity: 0, x: -10 }}
                animate={{ opacity: 1, x: 0 }}
                className={`${getLogColor(log.level)} whitespace-pre-wrap mb-1`}
              >
                <span className="text-gray-600 select-none">{String(idx + 1).padStart(4, ' ')} │ </span>
                <span className="text-purple-400">[{log.extractor_name || 'system'}]</span>
                {' '}
                <span className="text-gray-500">{log.timestamp?.split('T')[1]?.substring(0, 12) || ''}</span>
                {' '}
                <span className={getLogColor(log.level)}>[{log.level}]</span>
                {' '}
                {log.message}
              </motion.div>
            ))}
          </AnimatePresence>
        )}
      </div>
    </div>
  );
};

// Failed Extractor Card
const FailedExtractorCard: React.FC<{ 
  extractor: { id: number; name: string; last_error: string | null; last_run_at: string | null; failed_runs: number };
  onClick: () => void;
}> = ({ extractor, onClick }) => (
  <motion.button
    onClick={onClick}
    whileHover={{ scale: 1.02 }}
    className="w-full text-left p-3 bg-red-500/10 border border-red-500/30 rounded-lg hover:bg-red-500/20 transition-colors"
  >
    <div className="flex items-start justify-between">
      <div className="flex-1 min-w-0">
        <p className="text-red-400 font-medium truncate">{extractor.name}</p>
        <p className="text-red-300/60 text-xs mt-1 truncate">
          {extractor.last_error || 'Unknown error'}
        </p>
      </div>
      <div className="text-right ml-2">
        <span className="text-red-400 text-sm font-bold">{extractor.failed_runs}</span>
        <p className="text-red-400/60 text-xs">failures</p>
      </div>
    </div>
  </motion.button>
);

// Main Scheduler Page
export const SchedulerPage: React.FC = () => {
  const navigate = useNavigate();
  const [liveLogs, setLiveLogs] = useState<LogEntry[]>([]);
  const [isConnected, setIsConnected] = useState(false);
  const [intervalInput, setIntervalInput] = useState(60);
  const wsRef = useRef<WebSocket | null>(null);

  const { data: status } = useScheduleStatus();
  const { data: stats, isLoading: isLoadingStats } = useSchedulerStats();
  const { data: recentRuns } = useRecentRuns(30);
  const updateConfig = useUpdateScheduleConfig();
  const triggerAll = useTriggerAll();
  const stopAll = useStopAll();

  // WebSocket for all logs
  useEffect(() => {
    let reconnectTimeout: ReturnType<typeof setTimeout> | null = null;
    let isUnmounting = false;

    const connectWebSocket = () => {
      if (isUnmounting) return;
      
      try {
        const ws = new WebSocket(`${WS_BASE}/ws/logs`);
        wsRef.current = ws;

        ws.onopen = () => {
          setIsConnected(true);
        };

        ws.onmessage = (event) => {
          try {
            const data = JSON.parse(event.data);
            setLiveLogs(prev => [...prev, data]); // No limit - keep all logs
          } catch (e) {
            console.error('Failed to parse log:', e);
          }
        };

        ws.onclose = () => {
          setIsConnected(false);
          if (!isUnmounting) {
            reconnectTimeout = setTimeout(connectWebSocket, 5000);
          }
        };

        ws.onerror = () => {
          setIsConnected(false);
        };
      } catch (e) {
        setIsConnected(false);
      }
    };

    connectWebSocket();

    return () => {
      isUnmounting = true;
      if (reconnectTimeout) clearTimeout(reconnectTimeout);
      if (wsRef.current) wsRef.current.close();
    };
  }, []);

  // Set initial interval from status
  useEffect(() => {
    if (status?.interval_minutes) {
      setIntervalInput(status.interval_minutes);
    }
  }, [status?.interval_minutes]);

  const handleTriggerAll = () => {
    triggerAll.mutate();
    setLiveLogs([]); // Clear logs for fresh run
  };

  const handleStopAll = () => {
    stopAll.mutate();
  };

  const handleUpdateSchedule = () => {
    updateConfig.mutate({
      enabled: status?.enabled ?? true,
      interval_minutes: intervalInput,
    });
  };

  const handleToggleSchedule = () => {
    updateConfig.mutate({
      enabled: !status?.enabled,
      interval_minutes: intervalInput,
    });
  };

  if (isLoadingStats) {
    return (
      <div className="min-h-screen bg-gray-900 flex items-center justify-center">
        <Loader2 className="w-8 h-8 text-cyan-400 animate-spin" />
      </div>
    );
  }

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
                <h1 className="text-xl font-semibold flex items-center gap-2">
                  <Calendar className="w-6 h-6 text-purple-400" />
                  Scheduler Dashboard
                </h1>
                <p className="text-gray-400 text-sm mt-1">
                  Manage automated extractor runs
                </p>
              </div>
            </div>
            
            <div className="flex items-center gap-4">
              {/* Connection Status */}
              <div className={`flex items-center gap-2 px-3 py-1.5 rounded-lg ${
                isConnected ? 'bg-green-500/20 text-green-400' : 'bg-gray-700 text-gray-400'
              }`}>
                <div className={`w-2 h-2 rounded-full ${isConnected ? 'bg-green-400' : 'bg-gray-500'}`} />
                <span className="text-xs">{isConnected ? 'Connected' : 'Disconnected'}</span>
              </div>

              {/* Schedule Controls */}
              <div className="flex items-center gap-2 bg-gray-800 rounded-lg p-1">
                <button
                  onClick={handleToggleSchedule}
                  className={`px-3 py-2 rounded-lg flex items-center gap-2 transition-colors ${
                    status?.enabled 
                      ? 'bg-green-600 hover:bg-green-500 text-white' 
                      : 'bg-gray-700 hover:bg-gray-600 text-gray-300'
                  }`}
                >
                  {status?.enabled ? <Pause className="w-4 h-4" /> : <Play className="w-4 h-4" />}
                  {status?.enabled ? 'Pause' : 'Enable'}
                </button>
              </div>

              {/* Stop All Button */}
              <button
                onClick={handleStopAll}
                disabled={stopAll.isPending || (stats?.running_extractors ?? 0) === 0}
                className="flex items-center gap-2 bg-red-700 hover:bg-red-600
                  disabled:bg-gray-700 disabled:text-gray-400 px-5 py-2.5 rounded-lg transition-all font-medium shadow-lg"
              >
                {stopAll.isPending ? (
                  <Loader2 className="w-4 h-4 animate-spin" />
                ) : (
                  <Square className="w-4 h-4" />
                )}
                Stop All
              </button>

              {/* Run All Button */}
              <button
                onClick={handleTriggerAll}
                disabled={triggerAll.isPending || (stats?.running_extractors ?? 0) > 0}
                className="flex items-center gap-2 bg-gradient-to-r from-purple-600 to-cyan-600 hover:from-purple-500 hover:to-cyan-500 
                  disabled:from-gray-700 disabled:to-gray-700 disabled:text-gray-400 px-5 py-2.5 rounded-lg transition-all font-medium shadow-lg"
              >
                {triggerAll.isPending ? (
                  <Loader2 className="w-4 h-4 animate-spin" />
                ) : (
                  <Zap className="w-4 h-4" />
                )}
                Run All Extractors
              </button>
            </div>
          </div>
        </div>
      </header>

      <main className="w-full px-8 py-6">
        {/* Schedule Configuration */}
        <div className="mb-6 flex items-center gap-6 p-4 bg-gray-800/30 rounded-xl border border-gray-700/50">
          <div className="flex items-center gap-3">
            <Timer className="w-5 h-5 text-purple-400" />
            <span className="text-gray-300">Run every</span>
            <input
              type="number"
              value={intervalInput}
              onChange={(e) => {
                const val = parseInt(e.target.value);
                if (!isNaN(val)) setIntervalInput(val);
              }}
              min={1}
              max={1440}
              className="w-20 px-3 py-2 bg-gray-800 border border-gray-600 rounded-lg text-white text-center"
            />
            <span className="text-gray-300">minutes</span>
            <button
              onClick={handleUpdateSchedule}
              disabled={updateConfig.isPending}
              className="px-4 py-2 bg-purple-600 hover:bg-purple-500 rounded-lg text-sm font-medium transition-colors"
            >
              {updateConfig.isPending ? <Loader2 className="w-4 h-4 animate-spin" /> : 'Update'}
            </button>
          </div>
          
          <div className="h-8 w-px bg-gray-700" />
          
          <div className="flex items-center gap-6 text-sm">
            <div>
              <span className="text-gray-500">Next Run:</span>
              <span className="ml-2 text-white">
                {status?.next_run_at 
                  ? formatDistanceToNow(new Date(status.next_run_at), { addSuffix: true })
                  : 'Not scheduled'}
              </span>
            </div>
            <div>
              <span className="text-gray-500">Last Run:</span>
              <span className="ml-2 text-white">
                {status?.last_run_at 
                  ? formatDistanceToNow(new Date(status.last_run_at), { addSuffix: true })
                  : 'Never'}
              </span>
            </div>
          </div>
        </div>

        {/* Main Stats Grid */}
        <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-6 gap-4 mb-6">
          <StatCard
            icon={<Database className="w-5 h-5" />}
            label="Total Extractors"
            value={stats?.total_extractors || 0}
            subValue={`${stats?.enabled_extractors || 0} enabled`}
            color="blue"
          />
          <StatCard
            icon={<Activity className="w-5 h-5" />}
            label="Running"
            value={stats?.running_extractors || 0}
            color="yellow"
          />
          <StatCard
            icon={<CheckCircle className="w-5 h-5" />}
            label="Idle"
            value={stats?.idle_extractors || 0}
            color="green"
          />
          <StatCard
            icon={<XCircle className="w-5 h-5" />}
            label="Failed"
            value={stats?.failed_extractors || 0}
            color="red"
          />
          <StatCard
            icon={<BarChart3 className="w-5 h-5" />}
            label="Total Runs"
            value={stats?.total_runs || 0}
            subValue={`${stats?.successful_runs || 0} successful`}
            trend="neutral"
            color="purple"
          />
          <StatCard
            icon={<Clock className="w-5 h-5" />}
            label="Avg Duration"
            value={stats?.avg_duration_last_24h ? `${stats.avg_duration_last_24h.toFixed(1)}s` : '-'}
            subValue="last 24h"
            color="cyan"
          />
        </div>

        {/* Today's Stats + Success Rate */}
        <div className="grid grid-cols-1 lg:grid-cols-4 gap-6 mb-6">
          {/* Today's Performance */}
          <div className="lg:col-span-1 bg-gray-800/50 rounded-xl p-6 border border-gray-700/50">
            <h3 className="text-gray-400 text-sm mb-4 flex items-center gap-2">
              <Calendar className="w-4 h-4" />
              Today's Performance
            </h3>
            <div className="flex items-center justify-center mb-4">
              <ProgressRing 
                percentage={stats?.success_rate_today || 0} 
                color={stats?.success_rate_today && stats.success_rate_today > 90 ? '#22c55e' : stats?.success_rate_today && stats.success_rate_today > 70 ? '#eab308' : '#ef4444'}
              />
            </div>
            <div className="grid grid-cols-3 gap-2 text-center">
              <div>
                <p className="text-2xl font-bold text-white">{stats?.runs_today || 0}</p>
                <p className="text-xs text-gray-500">Runs</p>
              </div>
              <div>
                <p className="text-2xl font-bold text-green-400">{stats?.successful_today || 0}</p>
                <p className="text-xs text-gray-500">Success</p>
              </div>
              <div>
                <p className="text-2xl font-bold text-red-400">{stats?.failed_today || 0}</p>
                <p className="text-xs text-gray-500">Failed</p>
              </div>
            </div>
          </div>

          {/* Last 24 Hours */}
          <div className="lg:col-span-1 bg-gray-800/50 rounded-xl p-6 border border-gray-700/50">
            <h3 className="text-gray-400 text-sm mb-4 flex items-center gap-2">
              <Clock className="w-4 h-4" />
              Last 24 Hours
            </h3>
            <div className="space-y-4">
              <div className="flex justify-between items-center">
                <span className="text-gray-400">Total Runs</span>
                <span className="text-xl font-bold text-white">{stats?.runs_last_24h || 0}</span>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-gray-400">Successful</span>
                <span className="text-xl font-bold text-green-400">{stats?.successful_last_24h || 0}</span>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-gray-400">Failed</span>
                <span className="text-xl font-bold text-red-400">{stats?.failed_last_24h || 0}</span>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-gray-400">Avg Duration</span>
                <span className="text-xl font-bold text-cyan-400">
                  {stats?.avg_duration_last_24h ? `${stats.avg_duration_last_24h.toFixed(1)}s` : '-'}
                </span>
              </div>
            </div>
          </div>

          {/* Category Breakdown */}
          <div className="lg:col-span-2 bg-gray-800/50 rounded-xl p-6 border border-gray-700/50">
            <h3 className="text-gray-400 text-sm mb-4 flex items-center gap-2">
              <Server className="w-4 h-4" />
              Extractors by Category
            </h3>
            <div className="grid grid-cols-2 md:grid-cols-3 gap-3">
              {Object.entries(stats?.extractors_by_category || {}).map(([category, count]) => (
                <div key={category} className="bg-gray-900/50 rounded-lg p-3">
                  <p className="text-gray-400 text-xs uppercase tracking-wide truncate">{category}</p>
                  <p className="text-2xl font-bold text-white">{count}</p>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Latest Runs Table */}
        <div className="mb-6 bg-gray-800/50 rounded-xl border border-gray-700/50 overflow-hidden">
          <div className="flex items-center justify-between px-6 py-4 border-b border-gray-700/50">
            <h3 className="text-gray-200 font-medium flex items-center gap-2">
              <Activity className="w-4 h-4 text-cyan-400" />
              Latest Runs
            </h3>
            <span className="text-gray-500 text-xs">{recentRuns?.length || 0} entries</span>
          </div>
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead>
                <tr className="text-gray-500 text-xs uppercase tracking-wide border-b border-gray-700/50">
                  <th className="text-left px-6 py-3">Extractor</th>
                  <th className="text-left px-6 py-3">Status</th>
                  <th className="text-left px-6 py-3">Started</th>
                  <th className="text-right px-6 py-3">Duration</th>
                  <th className="text-right px-6 py-3">Items</th>
                  <th className="text-left px-6 py-3">Error</th>
                </tr>
              </thead>
              <tbody>
                {!recentRuns || recentRuns.length === 0 ? (
                  <tr>
                    <td colSpan={6} className="text-center text-gray-500 py-8">No runs yet</td>
                  </tr>
                ) : recentRuns.map((run) => {
                  const statusColors: Record<string, string> = {
                    success: 'text-green-400 bg-green-400/10',
                    failed: 'text-red-400 bg-red-400/10',
                    running: 'text-cyan-400 bg-cyan-400/10',
                    idle: 'text-gray-400 bg-gray-400/10',
                  };
                  const s = run.status.toLowerCase();
                  const color = statusColors[s] || 'text-gray-400 bg-gray-400/10';
                  return (
                    <tr key={run.id} className="border-b border-gray-700/30 hover:bg-gray-700/20 transition-colors">
                      <td className="px-6 py-3 font-mono text-gray-200 truncate max-w-[200px]">{run.extractor_name}</td>
                      <td className="px-6 py-3">
                        <span className={`px-2 py-0.5 rounded text-xs font-medium ${color}`}>{run.status}</span>
                      </td>
                      <td className="px-6 py-3 text-gray-400 text-xs">
                        {run.started_at ? new Date(run.started_at).toLocaleString() : '-'}
                      </td>
                      <td className="px-6 py-3 text-right text-gray-300">
                        {run.duration_seconds != null ? `${run.duration_seconds}s` : '-'}
                      </td>
                      <td className="px-6 py-3 text-right text-gray-300">{run.items_extracted}</td>
                      <td className="px-6 py-3 text-red-400/70 text-xs truncate max-w-[200px]">
                        {run.error_message || ''}
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        </div>

        {/* Live Terminal + Failed Extractors + Top/Worst */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Live Terminal - Takes 2 columns */}
          <div className="lg:col-span-2 bg-gray-800/30 rounded-xl border border-gray-700/50 h-[500px] flex flex-col">
            <GlobalTerminal logs={liveLogs} isConnected={isConnected} onClear={() => setLiveLogs([])} />
          </div>

          {/* Side Panel */}
          <div className="space-y-6">
            {/* Failed Extractors */}
            <div className="bg-gray-800/50 rounded-xl p-4 border border-red-500/30">
              <h3 className="text-red-400 text-sm mb-3 flex items-center gap-2">
                <AlertTriangle className="w-4 h-4" />
                Recent Failures ({stats?.recent_failed_extractors?.length || 0})
              </h3>
              <div className="space-y-2 max-h-[180px] overflow-y-auto">
                {stats?.recent_failed_extractors?.length === 0 ? (
                  <p className="text-gray-500 text-sm text-center py-4">No failures! 🎉</p>
                ) : (
                  stats?.recent_failed_extractors?.map(ext => (
                    <FailedExtractorCard
                      key={ext.id}
                      extractor={ext}
                      onClick={() => navigate(`/extractor/${ext.id}`)}
                    />
                  ))
                )}
              </div>
            </div>

            {/* Top Performers */}
            <div className="bg-gray-800/50 rounded-xl p-4 border border-green-500/30">
              <h3 className="text-green-400 text-sm mb-3 flex items-center gap-2">
                <Award className="w-4 h-4" />
                Top Performers
              </h3>
              <div className="space-y-2">
                {stats?.top_extractors?.slice(0, 3).map((ext, idx) => (
                  <button
                    key={ext.id}
                    onClick={() => navigate(`/extractor/${ext.id}`)}
                    className="w-full text-left p-2 bg-green-500/10 rounded-lg hover:bg-green-500/20 transition-colors flex items-center justify-between"
                  >
                    <div className="flex items-center gap-2">
                      <span className="text-green-400 font-bold">#{idx + 1}</span>
                      <span className="text-gray-300 text-sm truncate">{ext.name}</span>
                    </div>
                    <span className="text-green-400 text-sm font-medium">{ext.success_rate}%</span>
                  </button>
                ))}
              </div>
            </div>

            {/* Worst Performers */}
            <div className="bg-gray-800/50 rounded-xl p-4 border border-orange-500/30">
              <h3 className="text-orange-400 text-sm mb-3 flex items-center gap-2">
                <Skull className="w-4 h-4" />
                Needs Attention
              </h3>
              <div className="space-y-2">
                {stats?.worst_extractors?.slice(0, 3).map((ext, idx) => (
                  <button
                    key={ext.id}
                    onClick={() => navigate(`/extractor/${ext.id}`)}
                    className="w-full text-left p-2 bg-orange-500/10 rounded-lg hover:bg-orange-500/20 transition-colors flex items-center justify-between"
                  >
                    <div className="flex items-center gap-2 min-w-0">
                      <span className="text-orange-400 font-bold">#{idx + 1}</span>
                      <span className="text-gray-300 text-sm truncate">{ext.name}</span>
                    </div>
                    <span className="text-orange-400 text-sm font-medium">{ext.success_rate}%</span>
                  </button>
                ))}
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
};

export default SchedulerPage;
