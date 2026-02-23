import React, { useEffect, useRef, useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  Terminal
} from 'lucide-react';

interface LogEntry {
  timestamp: string;
  level: string;
  message: string;
  extractor_id?: number;
  task_id?: string;
  [key: string]: any;
}

interface TerminalLogViewerProps {
  logs: string;
  liveLogs: LogEntry[];
  isLive: boolean;
}

export const TerminalLogViewer: React.FC<TerminalLogViewerProps> = ({ 
  logs, 
  liveLogs,
  isLive 
}) => {
  const terminalRef = useRef<HTMLDivElement>(null);
  const [autoScroll, setAutoScroll] = useState(true);

  // Auto-scroll to bottom when new logs arrive
  useEffect(() => {
    if (autoScroll && terminalRef.current) {
      terminalRef.current.scrollTop = terminalRef.current.scrollHeight;
    }
  }, [logs, liveLogs, autoScroll]);

  // Parse log line to extract level and colorize
  const getLogLineClass = (line: string): string => {
    if (line.includes('[ERROR]') || line.includes('error')) return 'text-red-400';
    if (line.includes('[WARNING]') || line.includes('warning')) return 'text-yellow-400';
    if (line.includes('[INFO]') || line.includes('info')) return 'text-cyan-400';
    if (line.includes('[DEBUG]')) return 'text-gray-500';
    return 'text-green-400';
  };

  const formatLiveLog = (log: LogEntry): string => {
    const ts = log.timestamp?.split('T')[1]?.substring(0, 12) || '';
    const level = log.level?.toUpperCase() || 'INFO';
    const msg = log.message || '';
    return `[${ts}] [${level}] ${msg}`;
  };

  const logLines = logs?.split('\n').filter(l => l.trim()) || [];

  return (
    <div className="relative h-full">
      {/* Terminal Header */}
      <div className="flex items-center justify-between px-4 py-2 bg-gray-900 border-b border-gray-700 rounded-t-lg">
        <div className="flex items-center gap-2">
          <div className="flex gap-1.5">
            <div className="w-3 h-3 rounded-full bg-red-500"></div>
            <div className="w-3 h-3 rounded-full bg-yellow-500"></div>
            <div className="w-3 h-3 rounded-full bg-green-500"></div>
          </div>
          <span className="ml-3 text-gray-400 text-sm font-mono">
            extractor-logs
          </span>
          {isLive && (
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
        <button 
          onClick={() => setAutoScroll(!autoScroll)}
          className={`text-xs px-2 py-1 rounded ${
            autoScroll ? 'bg-cyan-600 text-white' : 'bg-gray-700 text-gray-400'
          }`}
        >
          Auto-scroll
        </button>
      </div>

      {/* Terminal Content */}
      <div 
        ref={terminalRef}
        className="h-[500px] overflow-y-auto bg-gray-950 font-mono text-sm p-4 rounded-b-lg border border-t-0 border-gray-800"
        style={{ 
          fontFamily: "'JetBrains Mono', 'Fira Code', 'Consolas', monospace",
          lineHeight: '1.7'
        }}
      >
        {logLines.length === 0 && liveLogs.length === 0 ? (
          <div className="text-gray-500 flex items-center gap-2">
            <Terminal className="w-4 h-4" />
            <span>No logs available. Run the extractor to see output.</span>
          </div>
        ) : (
          <>
            {/* Persisted logs */}
            {logLines.map((line, idx) => (
              <div key={`log-${idx}`} className={`${getLogLineClass(line)} whitespace-pre-wrap`}>
                <span className="text-gray-600 select-none">{String(idx + 1).padStart(4, ' ')} │ </span>
                {line}
              </div>
            ))}
            
            {/* Live logs */}
            <AnimatePresence>
              {liveLogs.map((log, idx) => (
                <motion.div
                  key={`live-${idx}-${log.timestamp}`}
                  initial={{ opacity: 0, x: -20 }}
                  animate={{ opacity: 1, x: 0 }}
                  className={`${getLogLineClass(log.level || '')} whitespace-pre-wrap`}
                >
                  <span className="text-gray-600 select-none">
                    {String(logLines.length + idx + 1).padStart(4, ' ')} │ 
                  </span>
                  {formatLiveLog(log)}
                </motion.div>
              ))}
            </AnimatePresence>
          </>
        )}

        {/* Cursor */}
        {isLive && (
          <motion.span 
            className="inline-block w-2 h-4 bg-green-400 ml-1"
            animate={{ opacity: [1, 0] }}
            transition={{ duration: 0.8, repeat: Infinity }}
          />
        )}
      </div>
    </div>
  );
};

export default TerminalLogViewer;
