import React, { useState } from 'react';
import { Info } from 'lucide-react';

interface ProvenanceProps {
  value: string | number;
  source?: string;
  observedAt?: string;
  ageSeconds?: number;
  confidence?: number;
  unit?: string;
  className?: string;
}

export const ProvenanceValue: React.FC<ProvenanceProps> = ({
  value,
  source = "maintenance-feed",
  observedAt = "2026-10-05T10:31:24Z",
  ageSeconds = 18,
  confidence = 0.96,
  unit = "",
  className = ""
}) => {
  const [showPopover, setShowPopover] = useState(false);

  const confLabel = confidence >= 0.9 ? 'HIGH' : confidence >= 0.7 ? 'MEDIUM' : 'LOW';
  const confColor = confidence >= 0.9 ? 'text-[#22A06B]' : confidence >= 0.7 ? 'text-[#D99A1B]' : 'text-[#E5484D]';

  return (
    <div className={`relative inline-flex items-center space-x-1.5 font-mono ${className}`}>
      <span className="font-semibold text-[#E8EDF7]">{value}{unit ? ` ${unit}` : ''}</span>
      <button
        onClick={() => setShowPopover(!showPopover)}
        onMouseEnter={() => setShowPopover(true)}
        onMouseLeave={() => setShowPopover(false)}
        className="text-[#7A869C] hover:text-[#3B82F6] transition-colors focus:outline-none"
        title="View data provenance and confidence"
      >
        <Info className="w-3.5 h-3.5" />
      </button>

      {showPopover && (
        <div className="absolute bottom-full left-0 mb-2 w-64 bg-[#111A2E] border border-[#24304A] rounded-lg p-3 shadow-xl z-50 text-left font-mono text-[11px] pointer-events-none">
          <div className="text-[10px] uppercase font-bold text-[#7A869C] border-b border-[#24304A] pb-1 mb-2">
            Data Provenance (Spec §11.7)
          </div>
          <div className="space-y-1">
            <div className="flex justify-between">
              <span className="text-[#9AA7BF]">Feed Source:</span>
              <span className="text-[#E8EDF7] font-semibold">{source}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-[#9AA7BF]">Observed At:</span>
              <span className="text-[#E8EDF7]">{observedAt.replace('T', ' ').substring(0, 19)} UTC</span>
            </div>
            <div className="flex justify-between">
              <span className="text-[#9AA7BF]">Data Age:</span>
              <span className="text-[#E8EDF7]">{ageSeconds}s (live counter)</span>
            </div>
            <div className="flex justify-between pt-1 border-t border-[#24304A]/60">
              <span className="text-[#9AA7BF]">Confidence:</span>
              <span className={`font-bold ${confColor}`}>{Math.round(confidence * 100)}% ({confLabel})</span>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
