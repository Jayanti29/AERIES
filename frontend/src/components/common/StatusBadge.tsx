import React from 'react';
import { CheckCircle2, AlertTriangle, XCircle, Info, HelpCircle } from 'lucide-react';

interface StatusBadgeProps {
  status: 'HEALTHY' | 'NOMINAL' | 'WARNING' | 'CRITICAL' | 'READY' | 'MAINTENANCE' | 'CLEAR' | 'AT_RISK' | string;
  label?: string;
  size?: 'sm' | 'md';
}

export const StatusBadge: React.FC<StatusBadgeProps> = ({ status, label, size = 'sm' }) => {
  const s = status.toUpperCase();
  let bg = 'bg-[#172238] border-[#24304A] text-[#7A869C]';
  let Icon = HelpCircle;

  if (['HEALTHY', 'NOMINAL', 'READY', 'CLEAR', 'OPERATIONAL'].includes(s)) {
    bg = 'bg-[#142621] border-[#22A06B]/30 text-[#22A06B]';
    Icon = CheckCircle2;
  } else if (['WARNING', 'ELEVATED', 'AT_RISK'].includes(s)) {
    bg = 'bg-[#2A2314] border-[#D99A1B]/30 text-[#D99A1B]';
    Icon = AlertTriangle;
  } else if (['CRITICAL', 'GROUNDED', 'FAILED', 'OVERDUE'].includes(s)) {
    bg = 'bg-[#2D161A] border-[#E5484D]/30 text-[#E5484D]';
    Icon = XCircle;
  } else if (['INFO', 'UPCOMING', 'ACTIVE'].includes(s)) {
    bg = 'bg-[#13233D] border-[#4C9AFF]/30 text-[#4C9AFF]';
    Icon = Info;
  }

  const iconSize = size === 'sm' ? 'w-3 h-3' : 'w-4 h-4';
  const textSize = size === 'sm' ? 'text-xs' : 'text-sm';

  return (
    <span className={`inline-flex items-center space-x-1.5 px-2 py-0.5 rounded font-mono font-medium border ${bg} ${textSize}`}>
      <Icon className={iconSize} />
      <span>{label || status}</span>
    </span>
  );
};
