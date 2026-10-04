import React from 'react';
import { PlanDNA as PlanDNAType } from '../../types';

interface PlanDNAProps {
  dna: PlanDNAType;
  compact?: boolean;
}

export const PlanDNA: React.FC<PlanDNAProps> = ({ dna, compact = false }) => {
  const metrics = [
    { label: 'Coverage', value: dna.coverage, color: 'bg-blue-500' },
    { label: 'Efficiency', value: dna.efficiency, color: 'bg-emerald-500' },
    { label: 'Resilience', value: dna.resilience, color: 'bg-indigo-500' },
    { label: 'Flexibility', value: dna.flexibility, color: 'bg-amber-500' },
    { label: 'Speed', value: dna.speed, color: 'bg-cyan-500' },
    { label: 'Reserve', value: dna.resource_reserve, color: 'bg-purple-500' }
  ];

  return (
    <div className="space-y-1.5 font-mono">
      {metrics.map((m) => (
        <div key={m.label} className="text-xs">
          <div className="flex justify-between text-[#9AA7BF] mb-0.5 text-[11px]">
            <span>{m.label}</span>
            <span className="text-[#E8EDF7] font-semibold">{m.value}%</span>
          </div>
          <div className="w-full bg-[#0B1220] rounded-full h-1.5 overflow-hidden">
            <div className={`h-full ${m.color}`} style={{ width: `${m.value}%` }} />
          </div>
        </div>
      ))}
    </div>
  );
};
