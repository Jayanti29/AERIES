import React from 'react';
import { NavLink } from 'react-router-dom';
import {
  Shield, Activity, Layers, Compass, Sliders, PlayCircle,
  FileCheck, Database, FileText, Settings, User, AlertOctagon,
  Cpu, Box, Users, Plane
} from 'lucide-react';
import { useAuthStore } from '../../store/authStore';
import { Role } from '../../types';

interface MenuItem {
  name: string;
  path: string;
  icon: any;
  allowedRoles: Role[];
}

const MENU_SECTIONS: { title: string; items: MenuItem[] }[] = [
  {
    title: 'Command',
    items: [
      { name: 'Command Center', path: '/', icon: Activity, allowedRoles: ['Operations Planner', 'Decision Authority', 'Analyst', 'Administrator'] },
      { name: 'Operational Map', path: '/map', icon: Compass, allowedRoles: ['Operations Planner', 'Decision Authority', 'Analyst'] },
      { name: 'Insights', path: '/insights', icon: AlertOctagon, allowedRoles: ['Operations Planner', 'Decision Authority', 'Analyst'] }
    ]
  },
  {
    title: 'Domains',
    items: [
      { name: 'Craft Fleet', path: '/craft', icon: Plane, allowedRoles: ['Craft Officer', 'Operations Planner', 'Decision Authority', 'Analyst'] },
      { name: 'Supply Logistics', path: '/supply', icon: Box, allowedRoles: ['Supply Officer', 'Operations Planner', 'Decision Authority', 'Analyst'] },
      { name: 'People Roster', path: '/people', icon: Users, allowedRoles: ['Personnel Officer', 'Operations Planner', 'Decision Authority', 'Analyst'] },
      { name: 'Pilot Duty', path: '/pilot', icon: Shield, allowedRoles: ['Pilot'] }
    ]
  },
  {
    title: 'Planning & Resilience',
    items: [
      { name: 'Plans & Missions', path: '/plans', icon: Layers, allowedRoles: ['Operations Planner', 'Decision Authority', 'Analyst'] },
      { name: 'Trade-off Explorer', path: '/tradeoffs', icon: Sliders, allowedRoles: ['Operations Planner', 'Decision Authority'] },
      { name: 'Chaos Lab', path: '/chaos', icon: PlayCircle, allowedRoles: ['Operations Planner', 'Decision Authority'] },
      { name: 'Stress Test', path: '/stress', icon: Cpu, allowedRoles: ['Operations Planner', 'Decision Authority'] }
    ]
  },
  {
    title: 'Decisions & Governance',
    items: [
      { name: 'Decision Queue', path: '/decisions', icon: FileCheck, allowedRoles: ['Decision Authority', 'Operations Planner', 'Auditor'] },
      { name: 'Audit Ledger', path: '/audit', icon: FileText, allowedRoles: ['Auditor', 'Administrator'] },
      { name: 'Administration', path: '/admin', icon: Settings, allowedRoles: ['Administrator'] }
    ]
  }
];

export const Sidebar: React.FC = () => {
  const { user } = useAuthStore();
  const currentRole = user?.role || 'Operations Planner';

  return (
    <aside className="w-60 bg-[#111A2E] border-r border-[#24304A] flex flex-col justify-between select-none">
      <div className="py-4">
        <div className="px-5 mb-6 flex items-center space-x-3">
          <div className="w-8 h-8 rounded bg-[#3B82F6] flex items-center justify-center font-bold text-white shadow-lg shadow-blue-500/20">
            A
          </div>
          <div>
            <div className="font-mono font-bold tracking-wider text-[#E8EDF7] text-base leading-none">AERIS</div>
            <div className="text-[10px] text-[#7A869C] font-mono mt-0.5">OPS INTELLIGENCE</div>
          </div>
        </div>

        <nav className="space-y-6 px-3">
          {MENU_SECTIONS.map((section) => {
            const visibleItems = section.items.filter((item) => item.allowedRoles.includes(currentRole));
            if (visibleItems.length === 0) return null;

            return (
              <div key={section.title}>
                <div className="px-3 mb-2 text-[10px] font-mono uppercase tracking-wider text-[#7A869C]">
                  {section.title}
                </div>
                <div className="space-y-1">
                  {visibleItems.map((item) => {
                    const Icon = item.icon;
                    return (
                      <NavLink
                        key={item.path}
                        to={item.path}
                        className={({ isActive }) => `flex items-center space-x-3 px-3 py-2 rounded text-xs font-mono font-medium transition-colors ${
                          isActive
                            ? 'bg-[#172238] text-[#3B82F6] border-l-2 border-[#3B82F6]'
                            : 'text-[#9AA7BF] hover:bg-[#172238]/50 hover:text-[#E8EDF7]'
                        }`}
                      >
                        <Icon className="w-4 h-4 shrink-0" />
                        <span className="truncate">{item.name}</span>
                      </NavLink>
                    );
                  })}
                </div>
              </div>
            );
          })}
        </nav>
      </div>

      <div className="p-3 border-t border-[#24304A] bg-[#0B1220]/50 font-mono text-[11px] text-[#7A869C]">
        <div>CLOCK: <span className="text-[#E8EDF7]">11:24:00 UTC</span></div>
        <div className="truncate mt-0.5">ROLE: <span className="text-[#3B82F6] font-semibold">{currentRole}</span></div>
      </div>
    </aside>
  );
};
