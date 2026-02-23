import { motion } from 'framer-motion';
import { useNavigate } from 'react-router-dom';
import { Play, CheckCircle2, XCircle, Clock, Loader2, Database, ExternalLink } from 'lucide-react';
import { formatDistanceToNow } from 'date-fns';
import type { Extractor } from '../../features/extractors';

interface ExtractorCardProps {
  extractor: Extractor;
  isSelected: boolean;
  onSelect: () => void;
  onTrigger: () => void;
  onToggleEnabled: (enabled: boolean) => void;
  delay: number;
}

const STATUS_CONFIG = {
  idle: { icon: Clock, color: 'text-gray-400', bg: 'bg-gray-500/20', label: 'IDLE' },
  running: { icon: Loader2, color: 'text-blue-400', bg: 'bg-blue-500/20', label: 'RUNNING' },
  success: { icon: CheckCircle2, color: 'text-green-400', bg: 'bg-green-500/20', label: 'SUCCESS' },
  failed: { icon: XCircle, color: 'text-red-400', bg: 'bg-red-500/20', label: 'FAILED' },
  disabled: { icon: XCircle, color: 'text-gray-600', bg: 'bg-gray-700/20', label: 'DISABLED' },
};

export default function ExtractorCard({
  extractor,
  isSelected,
  onSelect,
  onTrigger,
  onToggleEnabled,
  delay
}: ExtractorCardProps) {
  const navigate = useNavigate();
  const statusConfig = STATUS_CONFIG[extractor.status];
  const StatusIcon = statusConfig.icon;
  const successRate = extractor.total_runs > 0
    ? ((extractor.successful_runs / extractor.total_runs) * 100).toFixed(1)
    : '0.0';

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay }}
      whileHover={{ y: -4 }}
      className={`glass rounded-2xl p-6 hover:bg-white/10 transition-all duration-300 border ${
        isSelected ? 'border-primary shadow-lg shadow-primary/20' : 'border-white/10'
      }`}
    >
      {/* Header */}
      <div className="flex items-start justify-between mb-4">
        <div className="flex items-center space-x-3">
          <input
            type="checkbox"
            checked={isSelected}
            onChange={onSelect}
            disabled={!extractor.enabled}
            className="w-4 h-4 rounded border-white/20 bg-white/5 text-primary focus:ring-2 focus:ring-primary focus:ring-offset-0 disabled:opacity-30"
          />
          <div className={`${statusConfig.bg} p-2 rounded-lg`}>
            <Database className="w-4 h-4 text-white" />
          </div>
        </div>

        <div className="flex items-center space-x-2">
          <label className="relative inline-flex items-center cursor-pointer">
            <input
              type="checkbox"
              checked={extractor.enabled}
              onChange={(e) => onToggleEnabled(e.target.checked)}
              className="sr-only peer"
            />
            <div className="w-9 h-5 bg-white/10 peer-focus:ring-2 peer-focus:ring-primary rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:rounded-full after:h-4 after:w-4 after:transition-all peer-checked:bg-primary"></div>
          </label>
        </div>
      </div>

      {/* Title & Category */}
      <div className="mb-4">
        <button
          onClick={() => navigate(`/extractor/${extractor.id}`)}
          className="group flex items-center gap-2 hover:text-primary transition-colors text-left"
        >
          <h3 className="text-lg font-bold text-white group-hover:text-primary mb-1 line-clamp-1 font-display transition-colors">
            {extractor.display_name}
          </h3>
          <ExternalLink className="w-4 h-4 text-gray-500 group-hover:text-primary opacity-0 group-hover:opacity-100 transition-all" />
        </button>
        <p className="text-xs text-gray-400 font-mono uppercase tracking-wider">
          {extractor.category.replace(/_/g, ' ')}
        </p>
      </div>

      {/* Status */}
      <div className="flex items-center space-x-2 mb-4">
        <div className={`${statusConfig.bg} px-3 py-1.5 rounded-lg flex items-center space-x-2`}>
          <StatusIcon className={`w-3.5 h-3.5 ${statusConfig.color} ${extractor.status === 'running' ? 'animate-spin' : ''}`} />
          <span className={`text-xs font-display font-semibold ${statusConfig.color}`}>
            {statusConfig.label}
          </span>
        </div>
      </div>

      {/* Stats */}
      <div className="space-y-2 mb-4 text-sm">
        <div className="flex justify-between items-center">
          <span className="text-gray-400">Success Rate</span>
          <span className="font-bold text-green-400">{successRate}%</span>
        </div>
        <div className="flex justify-between items-center">
          <span className="text-gray-400">Total Runs</span>
          <span className="font-bold text-white">{extractor.total_runs}</span>
        </div>
        <div className="flex justify-between items-center">
          <span className="text-gray-400">Last Run</span>
          <span className="text-xs text-gray-500">
            {extractor.last_run_at
              ? formatDistanceToNow(new Date(extractor.last_run_at), { addSuffix: true })
              : 'Never'}
          </span>
        </div>
      </div>

      {/* Action Button */}
      <motion.button
        whileHover={{ scale: 1.02 }}
        whileTap={{ scale: 0.98 }}
        onClick={onTrigger}
        disabled={!extractor.enabled || extractor.status === 'running'}
        className="w-full py-3 bg-gradient-to-r from-primary to-accent rounded-xl font-display text-sm font-semibold flex items-center justify-center space-x-2 disabled:opacity-30 disabled:cursor-not-allowed shadow-lg shadow-primary/20 hover:shadow-primary/40 transition-all"
      >
        <Play className="w-4 h-4" />
        <span>RUN NOW</span>
      </motion.button>
    </motion.div>
  );
}
