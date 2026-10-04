import React from 'react';
import { ShieldAlert } from 'lucide-react';

export const HandlingBanner: React.FC = () => {
  return (
    <div className="w-full bg-[#172238] border-b border-[#24304A] text-[#9AA7BF] px-4 py-1 text-xs font-mono flex items-center justify-between tracking-wider select-none z-50">
      <div className="flex items-center space-x-2">
        <ShieldAlert className="w-3.5 h-3.5 text-[#D99A1B]" />
        <span className="font-semibold text-[#D99A1B]">RESTRICTED SIMULATION // UNCLASSIFIED</span>
      </div>
      <div className="bg-[#111A2E] px-3 py-0.5 rounded border border-[#24304A] text-[#E8EDF7] font-bold">
        SYNTHETIC DATA - SIMULATION
      </div>
      <div className="text-[11px] text-[#7A869C]">
        SEC-ENCLAVE: AERIS-GOV-01
      </div>
    </div>
  );
};
