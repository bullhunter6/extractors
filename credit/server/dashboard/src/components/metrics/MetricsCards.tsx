import { motion } from 'framer-motion';
import { Activity, Database, TrendingUp, Clock } from 'lucide-react';
import type { SystemMetrics } from '../../features/metrics';

interface MetricsCardsProps {
  metrics?: SystemMetrics;
}

export default function MetricsCards({ metrics }: MetricsCardsProps) {
  const cards = [
    {
      label: 'Total Extractors',
      value: metrics?.total_extractors || 0,
      icon: Database,
      color: 'from-blue-500 to-cyan-500',
      bg: 'bg-blue-500/10',
    },
    {
      label: 'Enabled',
      value: metrics?.enabled_extractors || 0,
      icon: Activity,
      color: 'from-green-500 to-emerald-500',
      bg: 'bg-green-500/10',
    },
    {
      label: 'Running',
      value: metrics?.running_extractors || 0,
      icon: TrendingUp,
      color: 'from-purple-500 to-pink-500',
      bg: 'bg-purple-500/10',
    },
    {
      label: 'Success Rate',
      value: metrics?.success_rate ? `${metrics.success_rate.toFixed(1)}%` : 'N/A',
      icon: Clock,
      color: 'from-amber-500 to-orange-500',
      bg: 'bg-amber-500/10',
    },
  ];

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
      {cards.map((card, index) => (
        <motion.div
          key={card.label}
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: index * 0.1 }}
          className="glass rounded-2xl p-6 hover:bg-white/10 transition-all duration-300 group"
        >
          <div className="flex items-start justify-between">
            <div className="flex-1">
              <p className="text-sm font-medium text-gray-400 uppercase tracking-wider mb-2">
                {card.label}
              </p>
              <p className="text-4xl font-bold bg-gradient-to-r {card.color} bg-clip-text text-transparent">
                {card.value}
              </p>
            </div>
            <div className={`${card.bg} p-3 rounded-xl group-hover:scale-110 transition-transform`}>
              <card.icon className="w-6 h-6 text-white" />
            </div>
          </div>
        </motion.div>
      ))}
    </div>
  );
}
