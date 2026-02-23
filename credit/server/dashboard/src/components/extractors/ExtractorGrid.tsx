import type { Extractor } from '../../features/extractors';
import ExtractorCard from './ExtractorCard';

interface ExtractorGridProps {
  extractors: Extractor[];
  selectedIds: number[];
  onSelect: (ids: number[]) => void;
  onTrigger: (id: number) => void;
  onToggleEnabled: (id: number, enabled: boolean) => void;
}

export default function ExtractorGrid({
  extractors,
  selectedIds,
  onSelect,
  onTrigger,
  onToggleEnabled
}: ExtractorGridProps) {
  const handleSelectAll = () => {
    if (selectedIds.length === extractors.length) {
      onSelect([]);
    } else {
      onSelect(extractors.filter(e => e.enabled).map(e => e.id));
    }
  };

  const handleSelect = (id: number) => {
    onSelect(
      selectedIds.includes(id)
        ? selectedIds.filter(sid => sid !== id)
        : [...selectedIds, id]
    );
  };

  return (
    <div>
      <div className="flex items-center justify-between mb-6">
        <h2 className="text-2xl font-bold font-display tracking-tight">
          <span className="gradient-text">EXTRACTORS</span>
          <span className="text-gray-400 text-lg ml-3">({extractors.length})</span>
        </h2>

        <button
          onClick={handleSelectAll}
          className="text-sm text-primary hover:text-accent font-display transition-colors"
        >
          {selectedIds.length === extractors.length ? 'DESELECT ALL' : 'SELECT ALL'}
        </button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
        {extractors.map((extractor, index) => (
          <ExtractorCard
            key={extractor.id}
            extractor={extractor}
            isSelected={selectedIds.includes(extractor.id)}
            onSelect={() => handleSelect(extractor.id)}
            onTrigger={() => onTrigger(extractor.id)}
            onToggleEnabled={(enabled) => onToggleEnabled(extractor.id, enabled)}
            delay={index * 0.02}
          />
        ))}
      </div>
    </div>
  );
}
