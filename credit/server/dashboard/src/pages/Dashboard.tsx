import { useState } from 'react';
import { motion } from 'framer-motion';
import { useSystemMetrics } from '../features/metrics';
import { useExtractors, useTriggerExtractor, useTriggerBatch, useUpdateExtractor } from '../features/extractors';
import type { ExtractorCategory, ExtractorStatus } from '../types';
import Header from '../components/layout/Header';
import MetricsCards from '../components/metrics/MetricsCards';
import Filters from '../components/filters/Filters';
import ExtractorGrid from '../components/extractors/ExtractorGrid';

export default function Dashboard() {
  const [selectedIds, setSelectedIds] = useState<number[]>([]);
  const [filters, setFilters] = useState<{
    category?: ExtractorCategory;
    status?: ExtractorStatus;
    enabledOnly: boolean;
  }>({ enabledOnly: false });

  const { data: metricsData } = useSystemMetrics();
  const { data: extractorsData, isLoading } = useExtractors({
    category: filters.category,
    status: filters.status,
    enabled: filters.enabledOnly || undefined,
  });

  const triggerMutation = useTriggerExtractor();
  const triggerBatchMutation = useTriggerBatch();
  const updateMutation = useUpdateExtractor();

  const handleTrigger = (id: number) => {
    triggerMutation.mutate(id);
  };

  const handleTriggerSelected = () => {
    if (selectedIds.length > 0) {
      triggerBatchMutation.mutate(selectedIds);
      setSelectedIds([]);
    }
  };

  const handleToggleEnabled = (id: number, enabled: boolean) => {
    updateMutation.mutate({ id, data: { enabled } });
  };

  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-background">
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          className="text-center"
        >
          <div className="w-16 h-16 border-4 border-primary border-t-transparent rounded-full animate-spin mx-auto mb-4" />
          <p className="text-gray-400 font-display text-sm tracking-wider">LOADING SYSTEMS</p>
        </motion.div>
      </div>
    );
  }

  return (
    <div className="min-h-screen relative overflow-hidden">
      {/* Background Effects */}
      <div className="fixed inset-0 -z-10">
        <div className="absolute inset-0 bg-gradient-to-br from-background via-surface to-background" />
        <div className="absolute top-0 left-1/4 w-96 h-96 bg-primary/10 rounded-full blur-3xl animate-pulse-slow" />
        <div className="absolute bottom-0 right-1/4 w-96 h-96 bg-accent/10 rounded-full blur-3xl animate-pulse-slow" style={{ animationDelay: '1s' }} />
      </div>

      <div className="relative z-10">
        <Header />

        <main className="max-w-[1920px] mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8">
          <MetricsCards metrics={metricsData} />

          <Filters
            filters={filters}
            onFilterChange={setFilters}
            selectedCount={selectedIds.length}
            onTriggerSelected={handleTriggerSelected}
          />

          <ExtractorGrid
            extractors={extractorsData?.extractors || []}
            selectedIds={selectedIds}
            onSelect={setSelectedIds}
            onTrigger={handleTrigger}
            onToggleEnabled={handleToggleEnabled}
          />
        </main>
      </div>
    </div>
  );
}
