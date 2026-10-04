import React from 'react';
import { LucideIcon } from 'lucide-react';
import { StatusBadge } from './StatusBadge';

interface KpiCardProps {
  title: string;
  value: string | number;
  subValue?: string;
  status?: string;
  icon?: LucideIcon;
  provenanceSource?: string;
}

export const KpiCard: React.FC<KpiCardProps> = ({
  title,
  value,
  subValue,
  status,
  icon: Icon,
  provenanceSource = "Live Telemetry"
}) => {
  return (
    <div className="bg-[#111A2E] border border-[#24304A] rounded-lg p-4 relative overflow-hidden group hover:border-[#3B82F6]/40 transition-colors">
      <div className="flex items-center justify-between mb-2">
        <span className="text-xs font-mono uppercase tracking-wider text-[#9AA7BF]">{title}</span>
        {Icon && <Icon className="w-4 h-4 text-[#7A869C] group-hover:text-[#3B82F6]" />}
      </div>
      <div className="flex items-baseline space-x-2">
        <span className="text-2xl font-bold font-mono text-[#E8EDF7] tracking-tight">{value}</span>
        {subValue && <span className="text-xs text-[#9AA7BF] font-mono">{subValue}</span>}
      </div>
      <div className="mt-3 flex items-center justify-between pt-2 border-t border-[#24304A]/60">
        {status ? <StatusBadge status={status} /> : <div />}
        <span className="text-[10px] text-[#7A869C] font-mono" title={`Verified feed: ${provenanceSource}`}>
          src: {provenanceSource}
        </span>
      </div>
    </div>
  );
};
