import React from 'react';

interface HealthBarProps {
  label: string;
  score: number;
  status: string;
  details?: string;
  isPrimaryConstraint?: boolean;
}

export const HealthBar: React.FC<HealthBarProps> = ({
  label,
  score,
  status,
  details,
  isPrimaryConstraint = false,
}) => {
  let color = 'bg-[#22A06B]';
  if (score < 80) color = 'bg-[#E5484D]';
  else if (score < 85) color = 'bg-[#D99A1B]';

  return (
    <div className={`p-2.5 rounded border transition-all ${
      isPrimaryConstraint ? 'bg-[#2D161A]/40 border-[#E5484D] ring-1 ring-[#E5484D]/40' : 'bg-[#172238]/60 border-[#24304A]'
    }`}>
      <div className="flex justify-between items-center mb-1 text-xs">
        <div className="flex items-center space-x-2">
          <span className="font-semibold text-[#E8EDF7]">{label}</span>
          {isPrimaryConstraint && (
            <span className="px-1.5 py-0.2 bg-[#E5484D] text-white text-[10px] font-bold rounded uppercase">
              Primary Constraint
            </span>
          )}
        </div>
        <span className="font-mono font-bold text-[#E8EDF7]">{score}%</span>
      </div>
      <div className="w-full bg-[#0B1220] rounded-full h-1.5 overflow-hidden">
        <div className={`h-full ${color}`} style={{ width: `${score}%` }}></div>
      </div>
      {details && <div className="text-[11px] text-[#9AA7BF] mt-1 font-mono truncate">{details}</div>}
    </div>
  );
};
