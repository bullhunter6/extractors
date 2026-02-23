import { motion } from 'framer-motion';
import { Play } from 'lucide-react';
import type { ExtractorCategory, ExtractorStatus } from '../../types';

interface FiltersProps {
  filters: {
    category?: ExtractorCategory;
    status?: ExtractorStatus;
    enabledOnly: boolean;
  };
  onFilterChange: (filters: any) => void;
  selectedCount: number;
  onTriggerSelected: () => void;
}

const CATEGORIES = [
  { value: 'banks_me', label: 'Banks ME' },
  { value: 'banks_ca', label: 'Banks CA' },
  { value: 'corporates_me', label: 'Corporates ME' },
  { value: 'corporates_ca', label: 'Corporates CA' },
  { value: 'sovereigns_me', label: 'Sovereigns ME' },
  { value: 'sovereigns_ca', label: 'Sovereigns CA' },
  { value: 'global', label: 'Global' },
  { value: 'events', label: 'Events' },
  { value: 'publications', label: 'Publications' },
];

const STATUSES = [
  { value: 'idle', label: 'Idle' },
  { value: 'running', label: 'Running' },
  { value: 'success', label: 'Success' },
  { value: 'failed', label: 'Failed' },
];

export default function Filters({ filters, onFilterChange, selectedCount, onTriggerSelected }: FiltersProps) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: 0.2 }}
      className="glass rounded-2xl p-6"
    >
      <div className="flex flex-wrap gap-4 items-center">
        <select
          value={filters.category || ''}
          onChange={(e) => onFilterChange({ ...filters, category: e.target.value || undefined })}
          className="px-4 py-2.5 bg-white/5 border border-white/10 rounded-xl text-gray-300 font-display text-sm focus:ring-2 focus:ring-primary focus:border-transparent outline-none transition-all"
        >
          <option value="">All Categories</option>
          {CATEGORIES.map((cat) => (
            <option key={cat.value} value={cat.value}>{cat.label}</option>
          ))}
        </select>

        <select
          value={filters.status || ''}
          onChange={(e) => onFilterChange({ ...filters, status: e.target.value || undefined })}
          className="px-4 py-2.5 bg-white/5 border border-white/10 rounded-xl text-gray-300 font-display text-sm focus:ring-2 focus:ring-primary focus:border-transparent outline-none transition-all"
        >
          <option value="">All Statuses</option>
          {STATUSES.map((status) => (
            <option key={status.value} value={status.value}>{status.label}</option>
          ))}
        </select>

        <label className="flex items-center space-x-2 cursor-pointer group">
          <input
            type="checkbox"
            checked={filters.enabledOnly}
            onChange={(e) => onFilterChange({ ...filters, enabledOnly: e.target.checked })}
            className="w-4 h-4 rounded border-white/20 bg-white/5 text-primary focus:ring-2 focus:ring-primary focus:ring-offset-0"
          />
          <span className="text-sm text-gray-400 group-hover:text-gray-300 transition-colors font-display">
            ENABLED ONLY
          </span>
        </label>

        {selectedCount > 0 && (
          <motion.button
            initial={{ scale: 0 }}
            animate={{ scale: 1 }}
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            onClick={onTriggerSelected}
            className="ml-auto px-6 py-2.5 bg-gradient-to-r from-green-500 to-emerald-500 rounded-xl font-display text-sm font-semibold flex items-center space-x-2 shadow-lg shadow-green-500/20 hover:shadow-green-500/40 transition-all"
          >
            <Play className="w-4 h-4" />
            <span>RUN SELECTED ({selectedCount})</span>
          </motion.button>
        )}
      </div>
    </motion.div>
  );
}
