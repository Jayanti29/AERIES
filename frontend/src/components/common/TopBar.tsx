import React from 'react';
import { Bell, Search, Shield, User, ChevronDown } from 'lucide-react';
import { useAuthStore } from '../../store/authStore';
import { Role } from '../../types';

const DEMO_ROLES: Role[] = [
  'Operations Planner',
  'Decision Authority',
  'Craft Officer',
  'Supply Officer',
  'Personnel Officer',
  'Pilot',
  'Auditor',
  'Administrator',
  'Analyst'
];

export const TopBar: React.FC = () => {
  const { user, switchRole } = useAuthStore();

  return (
    <header className="h-14 bg-[#111A2E] border-b border-[#24304A] px-6 flex items-center justify-between z-40 select-none">
      <div className="flex items-center space-x-4">
        <div className="relative">
          <Search className="w-4 h-4 absolute left-3 top-2.5 text-[#7A869C]" />
          <input
            type="text"
            placeholder="Search entity (A01, P-0012, M001)... [/]"
            className="w-80 bg-[#0B1220] border border-[#24304A] rounded pl-9 pr-3 py-1.5 text-xs text-[#E8EDF7] font-mono focus:outline-none focus:border-[#3B82F6]"
          />
        </div>
        <div className="flex items-center space-x-2">
          <span className="px-2 py-0.5 rounded bg-[#142621] text-[#22A06B] border border-[#22A06B]/30 text-[11px] font-mono">
            SYS: HEALTHY 89.2%
          </span>
          <span className="px-2 py-0.5 rounded bg-[#13233D] text-[#4C9AFF] border border-[#4C9AFF]/30 text-[11px] font-mono">
            DATA: 98.4%
          </span>
        </div>
      </div>

      <div className="flex items-center space-x-4">
        {/* Evaluator Quick Role Switcher */}
        <div className="flex items-center space-x-2 bg-[#0B1220] px-2 py-1 rounded border border-[#24304A]">
          <span className="text-[10px] font-mono text-[#7A869C] uppercase">Switch Role:</span>
          <select
            value={user?.role}
            onChange={(e) => switchRole(e.target.value as Role)}
            className="bg-transparent text-xs font-mono text-[#3B82F6] font-bold focus:outline-none cursor-pointer"
          >
            {DEMO_ROLES.map((r) => (
              <option key={r} value={r} className="bg-[#111A2E] text-[#E8EDF7]">
                {r}
              </option>
            ))}
          </select>
        </div>

        <button className="p-1.5 text-[#9AA7BF] hover:text-[#E8EDF7] rounded hover:bg-[#172238] relative">
          <Bell className="w-4 h-4" />
          <span className="w-2 h-2 rounded-full bg-[#E5484D] absolute top-1 right-1" />
        </button>

        <div className="flex items-center space-x-2 pl-2 border-l border-[#24304A]">
          <div className="w-7 h-7 rounded-full bg-[#172238] border border-[#24304A] flex items-center justify-center text-xs font-mono text-[#E8EDF7]">
            {user?.callsign ? user.callsign.substring(0, 2) : 'OP'}
          </div>
          <div className="text-left font-mono">
            <div className="text-xs font-semibold text-[#E8EDF7] leading-none">{user?.callsign || 'OPERATOR'}</div>
            <div className="text-[10px] text-[#7A869C] mt-0.5">{user?.role}</div>
          </div>
        </div>
      </div>
    </header>
  );
};
