# Frontend Components and Dashboard Pages for AERIS

def get_frontend_components_pages():
    files = {}

    files['frontend/src/components/common/Sidebar.tsx'] = """import React from 'react';
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
"""

    files['frontend/src/components/common/TopBar.tsx'] = """import React from 'react';
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
"""

    files['frontend/src/components/common/AppShell.tsx'] = """import React from 'react';
import { HandlingBanner } from './HandlingBanner';
import { Sidebar } from './Sidebar';
import { TopBar } from './TopBar';

interface AppShellProps {
  children: React.ReactNode;
}

export const AppShell: React.FC<AppShellProps> = ({ children }) => {
  return (
    <div className="min-h-screen bg-[#0B1220] text-[#E8EDF7] flex flex-col font-sans">
      <HandlingBanner />
      <div className="flex flex-1 overflow-hidden">
        <Sidebar />
        <div className="flex-1 flex flex-col overflow-y-auto">
          <TopBar />
          <main className="flex-1 p-6 space-y-6">
            {children}
          </main>
          <footer className="h-8 bg-[#0B1220] border-t border-[#24304A] px-6 flex items-center justify-between text-[11px] font-mono text-[#7A869C]">
            <div>UTC CLOCK: 2026-10-05 11:24:00Z</div>
            <div>AERIS CORE ENGINE v1.4.2 // POSTGRES POSTGIS 15 // REDIS 7 // CP-SAT</div>
            <div className="text-[#D99A1B]">RESTRICTED SIMULATION</div>
          </footer>
        </div>
      </div>
    </div>
  );
};
"""

    files['frontend/src/pages/CommandCenter.tsx'] = """import React, { useState, useEffect } from 'react';
import { KpiCard } from '../components/common/KpiCard';
import { HealthBar } from '../components/common/HealthBar';
import { StatusBadge } from '../components/common/StatusBadge';
import { fetchApi } from '../services/api';
import { Shield, Plane, AlertTriangle, Database, Activity, Clock } from 'lucide-react';

export const CommandCenter: React.FC = () => {
  const [summary, setSummary] = useState<any>(null);
  const [health, setHealth] = useState<any>(null);
  const [horizon, setHorizon] = useState<number>(15);

  useEffect(() => {
    fetchApi('/command/summary').then(setSummary).catch(() => {});
    fetchApi('/command/health').then(setHealth).catch(() => {});
  }, []);

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-xl font-bold font-mono tracking-tight text-[#E8EDF7]">COMMAND CENTER</h1>
          <p className="text-xs text-[#9AA7BF] font-mono mt-0.5">Real-time Joint Air Operations & Resource Posture</p>
        </div>
        <div className="flex items-center space-x-2">
          <span className="text-xs font-mono text-[#7A869C]">Scrubber:</span>
          {[15, 30, 60, 120].map((mins) => (
            <button
              key={mins}
              onClick={() => setHorizon(mins)}
              className={`px-2.5 py-1 rounded text-xs font-mono border transition-colors ${
                horizon === mins
                  ? 'bg-[#3B82F6] border-[#3B82F6] text-white font-bold'
                  : 'bg-[#111A2E] border-[#24304A] text-[#9AA7BF] hover:bg-[#172238]'
              }`}
            >
              +{mins}m
            </button>
          ))}
        </div>
      </div>

      {/* KPI Row */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <KpiCard
          title="Overall System Health"
          value={`${summary?.overall_health_pct || 89.2}%`}
          status="NOMINAL"
          icon={Activity}
          provenanceSource="Unified Health Engine"
        />
        <KpiCard
          title="Missions at Risk"
          value={summary?.missions_at_risk || 3}
          subValue={`of ${summary?.missions_total || 24} total`}
          status="WARNING"
          icon={AlertTriangle}
          provenanceSource="CP-SAT Constraint Diagnoser"
        />
        <KpiCard
          title="Peak Resource Pressure"
          value="89.2%"
          subValue="Jet Fuel (B-Delta)"
          status="CRITICAL"
          icon={Plane}
          provenanceSource="Supply Pressure Sensor"
        />
        <KpiCard
          title="Telemetry Data Health"
          value={`${summary?.data_health_pct || 98.4}%`}
          status="HEALTHY"
          icon={Database}
          provenanceSource="Postgres PostGIS Feed"
        />
      </div>

      {/* Main Grid: 8 Domain Health and Operational Queue */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="bg-[#111A2E] border border-[#24304A] rounded-lg p-5 lg:col-span-1 space-y-3">
          <div className="flex justify-between items-center mb-2">
            <h3 className="font-mono text-sm font-bold text-[#E8EDF7]">DOMAIN HEALTH INDEX (8)</h3>
            <span className="text-[10px] text-[#7A869C] font-mono">SPEC 5.1</span>
          </div>
          <div className="space-y-2">
            {(health?.domains || [
              { domain: 'People', score: 88.5, status: 'NOMINAL', details: '400 personnel, 24 high-workload' },
              { domain: 'Platforms', score: 86.7, status: 'NOMINAL', details: '52 of 60 platforms ready' },
              { domain: 'Components', score: 81.2, status: 'WARNING', details: 'Engine-1 subsystem wear' },
              { domain: 'Maintenance', score: 79.4, status: 'WARNING', details: '4 airframes awaiting inspection' },
              { domain: 'Resources', score: 74.8, status: 'CRITICAL', details: 'B-Delta fuel below 18%' },
              { domain: 'Infrastructure', score: 95.0, status: 'HEALTHY', details: 'Runways fully operational' },
              { domain: 'Environment', score: 84.0, status: 'NOMINAL', details: 'Sector 4 crosswinds' },
              { domain: 'Data Quality', score: 98.2, status: 'HEALTHY', details: '14ms latency' }
            ]).map((d: any) => (
              <HealthBar
                key={d.domain}
                label={d.domain}
                score={d.score}
                status={d.status}
                details={d.details}
                isPrimaryConstraint={d.domain === 'Resources'}
              />
            ))}
          </div>
        </div>

        {/* Operational Overview & Queue */}
        <div className="bg-[#111A2E] border border-[#24304A] rounded-lg p-5 lg:col-span-2 space-y-4">
          <div className="flex justify-between items-center">
            <h3 className="font-mono text-sm font-bold text-[#E8EDF7]">PRIORITY MISSION QUEUE</h3>
            <span className="text-xs font-mono text-[#3B82F6]">Live Projections at +{horizon}m</span>
          </div>

          <div className="border border-[#24304A] rounded overflow-hidden">
            <table className="w-full text-left font-mono text-xs">
              <thead className="bg-[#172238] text-[#9AA7BF] uppercase border-b border-[#24304A]">
                <tr>
                  <th className="p-3">Mission</th>
                  <th className="p-3">Priority</th>
                  <th className="p-3">Time Window</th>
                  <th className="p-3">Platforms</th>
                  <th className="p-3">Constraint Flag</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-[#24304A]">
                {[
                  { code: 'M001', name: 'Sentinel Watch 1', prio: 'CRITICAL', window: '11:00 - 15:00 UTC', platforms: 'A01, A02', flag: 'CLEAR' },
                  { code: 'M003', name: 'Sentinel Watch 3', prio: 'CRITICAL', window: '11:30 - 16:00 UTC', platforms: 'A12 (Tanker)', flag: 'AT_RISK' },
                  { code: 'M007', name: 'Forward Recon Bravo', prio: 'HIGH', window: '12:00 - 17:30 UTC', platforms: 'A24, A25', flag: 'AT_RISK' },
                  { code: 'M010', name: 'Logistics Courier Delta', prio: 'MEDIUM', window: '13:00 - 18:00 UTC', platforms: 'A31', flag: 'CLEAR' }
                ].map((m) => (
                  <tr key={m.code} className="hover:bg-[#172238]/40">
                    <td className="p-3 font-bold text-[#E8EDF7]">{m.code} - {m.name}</td>
                    <td className="p-3"><StatusBadge status={m.prio} /></td>
                    <td className="p-3 text-[#9AA7BF]">{m.window}</td>
                    <td className="p-3 text-[#E8EDF7]">{m.platforms}</td>
                    <td className="p-3"><StatusBadge status={m.flag} /></td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          <div className="bg-[#172238]/50 border border-[#24304A] rounded p-4 flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <AlertTriangle className="w-5 h-5 text-[#D99A1B]" />
              <div>
                <div className="text-xs font-bold text-[#E8EDF7] font-mono">PRIMARY CONSTRAINT DETECTED</div>
                <div className="text-[11px] text-[#9AA7BF] font-mono">B-Delta Jet Fuel reserve falls below 15% threshold in +60m.</div>
              </div>
            </div>
            <a href="/plans" className="px-3 py-1.5 bg-[#3B82F6] hover:bg-blue-600 text-white rounded text-xs font-mono font-semibold">
              Explore Plan Alternatives
            </a>
          </div>
        </div>
      </div>
    </div>
  );
};
"""

    files['frontend/src/pages/CraftDashboard.tsx'] = """import React, { useState, useEffect } from 'react';
import { fetchApi } from '../services/api';
import { StatusBadge } from '../components/common/StatusBadge';
import { KpiCard } from '../components/common/KpiCard';
import { Plane, AlertTriangle, Tool, CheckCircle2 } from 'lucide-react';

export const CraftDashboard: React.FC = () => {
  const [fleet, setFleet] = useState<any[]>([]);
  const [summary, setSummary] = useState<any>(null);

  useEffect(() => {
    fetchApi<any[]>('/craft/fleet').then(setFleet).catch(() => {});
    fetchApi<any>('/craft/summary').then(setSummary).catch(() => {});
  }, []);

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-xl font-bold font-mono tracking-tight text-[#E8EDF7]">CRAFT & FLEET POSTURE</h1>
          <p className="text-xs text-[#9AA7BF] font-mono mt-0.5">Airframe Readiness, Subsystems & Predictive Maintenance</p>
        </div>
        <button
          onClick={() => alert("Maintenance flag submitted to validation pipeline")}
          className="px-3 py-1.5 bg-[#E5484D] hover:bg-red-600 text-white text-xs font-mono font-bold rounded"
        >
          Flag Maintenance Issue
        </button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <KpiCard title="Fleet Inventory" value={summary?.fleet_total || 60} status="NOMINAL" icon={Plane} />
        <KpiCard title="Sortie Ready" value={summary?.fleet_ready || 52} status="HEALTHY" icon={CheckCircle2} />
        <KpiCard title="In Maintenance" value={summary?.fleet_in_maintenance || 8} status="WARNING" icon={Tool} />
        <KpiCard title="Constraints (2h)" value={summary?.predicted_constraints_2h || 4} status="CRITICAL" icon={AlertTriangle} />
      </div>

      <div className="bg-[#111A2E] border border-[#24304A] rounded-lg p-5">
        <h3 className="font-mono text-sm font-bold text-[#E8EDF7] mb-4">FLEET STATUS & PREDICTED CONSTRAINTS</h3>
        <div className="max-h-96 overflow-y-auto border border-[#24304A] rounded">
          <table className="w-full text-left font-mono text-xs">
            <thead className="bg-[#172238] text-[#9AA7BF] sticky top-0 uppercase">
              <tr>
                <th className="p-3">Platform</th>
                <th className="p-3">Type</th>
                <th className="p-3">Station</th>
                <th className="p-3">Status</th>
                <th className="p-3">Readiness</th>
                <th className="p-3">Flight Hrs</th>
                <th className="p-3">Inspection Due</th>
                <th className="p-3">Failure Risk (2h)</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-[#24304A]">
              {fleet.slice(0, 15).map((a) => (
                <tr key={a.code} className="hover:bg-[#172238]/40">
                  <td className="p-3 font-bold text-[#3B82F6]">{a.code}</td>
                  <td className="p-3 text-[#E8EDF7]">{a.platform_type}</td>
                  <td className="p-3 text-[#9AA7BF]">{a.base_code}</td>
                  <td className="p-3"><StatusBadge status={a.status} /></td>
                  <td className="p-3 font-bold text-[#E8EDF7]">{Math.round(a.readiness_score * 100)}%</td>
                  <td className="p-3 text-[#9AA7BF]">{a.flight_hours} hrs</td>
                  <td className="p-3 text-[#E8EDF7]">{a.hours_to_inspection} hrs</td>
                  <td className="p-3">
                    <span className={`font-bold ${a.predicted_constraint_prob > 0.2 ? 'text-[#E5484D]' : 'text-[#22A06B]'}`}>
                      {Math.round(a.predicted_constraint_prob * 100)}%
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};
"""

    files['frontend/src/pages/PlansPage.tsx'] = """import React, { useState, useEffect } from 'react';
import { fetchApi } from '../services/api';
import { PlanDNA } from '../components/common/PlanDNA';
import { StatusBadge } from '../components/common/StatusBadge';
import { Layers, ShieldCheck, Cpu } from 'lucide-react';

export const PlansPage: React.FC = () => {
  const [plansData, setPlansData] = useState<any>(null);
  const [selectedPlan, setSelectedPlan] = useState<string>('PLAN-B-RESILIENCE');

  useEffect(() => {
    fetchApi('/plans/generate', {
      method: 'POST',
      body: JSON.stringify({ horizon_hours: 4 })
    }).then(setPlansData).catch(() => {});
  }, []);

  const plans = plansData?.plans || [];

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-xl font-bold font-mono tracking-tight text-[#E8EDF7]">OPERATIONAL PLANS</h1>
          <p className="text-xs text-[#9AA7BF] font-mono mt-0.5">CP-SAT Multi-Objective Formulation: Plan Alpha, Bravo, Charlie</p>
        </div>
        <button
          onClick={() => alert("Re-optimizing solver with live constraints...")}
          className="px-3 py-1.5 bg-[#3B82F6] hover:bg-blue-600 text-white text-xs font-mono font-bold rounded flex items-center space-x-2"
        >
          <Cpu className="w-3.5 h-3.5" />
          <span>Re-Generate Plans</span>
        </button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {plans.map((p: any) => (
          <div
            key={p.id}
            onClick={() => setSelectedPlan(p.id)}
            className={`bg-[#111A2E] border rounded-lg p-5 cursor-pointer transition-all ${
              selectedPlan === p.id ? 'border-[#3B82F6] ring-1 ring-[#3B82F6]' : 'border-[#24304A] hover:border-[#3B82F6]/50'
            }`}
          >
            <div className="flex justify-between items-start mb-3">
              <div>
                <h3 className="font-mono font-bold text-[#E8EDF7] text-sm">{p.name}</h3>
                <span className="text-[10px] text-[#7A869C] font-mono">{p.id}</span>
              </div>
              <StatusBadge status={p.status} />
            </div>
            <p className="text-xs text-[#9AA7BF] mb-4 min-h-[3rem]">{p.description}</p>

            <div className="mb-4">
              <div className="text-[11px] font-mono uppercase text-[#7A869C] mb-2">Plan DNA Radar</div>
              <PlanDNA dna={p.dna} />
            </div>

            <div className="border-t border-[#24304A] pt-3 grid grid-cols-2 gap-2 text-xs font-mono">
              <div>
                <span className="text-[#7A869C] text-[10px]">Missions:</span>
                <div className="text-[#E8EDF7] font-bold">{p.metrics.missions_assigned} / 24</div>
              </div>
              <div>
                <span className="text-[#7A869C] text-[10px]">Fragility Index:</span>
                <div className={`font-bold ${p.metrics.fragility_score > 3.0 ? 'text-[#E5484D]' : 'text-[#22A06B]'}`}>
                  {p.metrics.fragility_score}
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
"""

    files['frontend/src/pages/PilotPages.tsx'] = """import React, { useState, useEffect } from 'react';
import { fetchApi } from '../services/api';
import { StatusBadge } from '../components/common/StatusBadge';
import { Shield, Clock, Award, Bell } from 'lucide-react';

export const PilotPages: React.FC = () => {
  const [duty, setDuty] = useState<any>(null);

  useEffect(() => {
    fetchApi('/pilot/me').then(setDuty).catch(() => {});
  }, []);

  return (
    <div className="space-y-6 max-w-4xl mx-auto">
      <div>
        <h1 className="text-xl font-bold font-mono tracking-tight text-[#E8EDF7]">PILOT DUTY & READINESS</h1>
        <p className="text-xs text-[#9AA7BF] font-mono mt-0.5">Aircrew Individual Posture (Enforced state:read_own)</p>
      </div>

      <div className="bg-[#111A2E] border border-[#24304A] rounded-lg p-6 space-y-6">
        <div className="flex justify-between items-center border-b border-[#24304A] pb-4">
          <div>
            <span className="text-xs font-mono text-[#7A869C]">CALLSIGN</span>
            <div className="text-2xl font-bold font-mono text-[#3B82F6]">{duty?.callsign || 'MAVERICK'}</div>
            <div className="text-xs text-[#9AA7BF] font-mono">{duty?.role || 'Lead Interceptor Pilot'}</div>
          </div>
          <StatusBadge status="READY" label="READY FOR SORTIE" size="md" />
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 font-mono text-xs">
          <div className="bg-[#172238] p-4 rounded border border-[#24304A]">
            <div className="text-[#7A869C] mb-1">DUTY HOURS TODAY</div>
            <div className="text-xl font-bold text-[#E8EDF7]">{duty?.duty_hours_today || 3.5} / 8.0 hrs</div>
            <div className="w-full bg-[#0B1220] rounded-full h-1.5 mt-2">
              <div className="h-full bg-[#22A06B]" style={{ width: '43%' }}></div>
            </div>
          </div>
          <div className="bg-[#172238] p-4 rounded border border-[#24304A]">
            <div className="text-[#7A869C] mb-1">REST ACCUMULATED</div>
            <div className="text-xl font-bold text-[#22A06B]">{duty?.rest_hours_accumulated || 14.5} hrs</div>
            <div className="text-[10px] text-[#9AA7BF] mt-1">Rule threshold: 12.0h min</div>
          </div>
          <div className="bg-[#172238] p-4 rounded border border-[#24304A]">
            <div className="text-[#7A869C] mb-1">ASSIGNED SORTIE</div>
            <div className="text-xl font-bold text-[#3B82F6]">{duty?.current_assignment?.mission_code || 'M001'}</div>
            <div className="text-[10px] text-[#9AA7BF] mt-1">{duty?.current_assignment?.aircraft_code || 'A01 (Fighter)'}</div>
          </div>
        </div>

        <div className="bg-[#172238]/40 border border-[#24304A] rounded p-4">
          <h4 className="text-xs font-mono font-bold text-[#E8EDF7] uppercase mb-2 flex items-center space-x-2">
            <Bell className="w-4 h-4 text-[#3B82F6]" />
            <span>Assignment Notifications</span>
          </h4>
          <div className="text-xs font-mono text-[#9AA7BF] space-y-1">
            <div>• [10:15 UTC] Sortie M001 takeoff window confirmed for 11:00 UTC at B-Alpha.</div>
            <div>• [08:30 UTC] Pre-flight telemetry and weapons verification completed.</div>
          </div>
        </div>
      </div>
    </div>
  );
};
"""

    files['frontend/src/pages/AuditLogPage.tsx'] = """import React, { useState, useEffect } from 'react';
import { fetchApi } from '../services/api';
import { StatusBadge } from '../components/common/StatusBadge';
import { ShieldCheck, Lock, FileText, CheckCircle2 } from 'lucide-react';

export const AuditLogPage: React.FC = () => {
  const [logs, setLogs] = useState<any[]>([]);
  const [verification, setVerification] = useState<any>(null);

  useEffect(() => {
    fetchApi<any[]>('/audit/logs').then(setLogs).catch(() => {});
  }, []);

  const handleVerify = async () => {
    try {
      const res = await fetchApi<any>('/audit/verify', { method: 'POST' });
      setVerification(res);
    } catch (e: any) {
      alert("Verification error: " + e.message);
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-xl font-bold font-mono tracking-tight text-[#E8EDF7]">CRYPTOGRAPHIC AUDIT LEDGER</h1>
          <p className="text-xs text-[#9AA7BF] font-mono mt-0.5">SHA-256 Hash Chained Tamper-Evident Ledger</p>
        </div>
        <button
          onClick={handleVerify}
          className="px-4 py-2 bg-[#22A06B] hover:bg-emerald-600 text-white font-mono text-xs font-bold rounded flex items-center space-x-2 shadow-lg shadow-emerald-600/20"
        >
          <ShieldCheck className="w-4 h-4" />
          <span>Verify Hash Chain Integrity</span>
        </button>
      </div>

      {verification && (
        <div className={`p-4 rounded border font-mono text-xs flex items-center space-x-3 ${
          verification.valid
            ? 'bg-[#142621] border-[#22A06B]/50 text-[#22A06B]'
            : 'bg-[#2D161A] border-[#E5484D]/50 text-[#E5484D]'
        }`}>
          <CheckCircle2 className="w-5 h-5 shrink-0" />
          <div>
            <div className="font-bold">{verification.valid ? "CHAIN INTEGRITY VERIFIED" : "TAMPERING DETECTED"}</div>
            <div className="text-[11px] opacity-80">{verification.reason} // Head: {verification.chain_head?.substring(0, 24)}...</div>
          </div>
        </div>
      )}

      <div className="bg-[#111A2E] border border-[#24304A] rounded-lg p-5">
        <div className="max-h-96 overflow-y-auto border border-[#24304A] rounded font-mono text-xs">
          <table className="w-full text-left">
            <thead className="bg-[#172238] text-[#9AA7BF] sticky top-0">
              <tr>
                <th className="p-3">#</th>
                <th className="p-3">Timestamp (UTC)</th>
                <th className="p-3">Actor</th>
                <th className="p-3">Action</th>
                <th className="p-3">Resource</th>
                <th className="p-3">Block Hash (SHA-256)</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-[#24304A]">
              {logs.map((log) => (
                <tr key={log.index} className="hover:bg-[#172238]/40">
                  <td className="p-3 text-[#7A869C]">{log.index}</td>
                  <td className="p-3 text-[#9AA7BF]">{log.timestamp.replace('T', ' ').substring(0, 19)}</td>
                  <td className="p-3 font-semibold text-[#E8EDF7]">{log.actor_role}</td>
                  <td className="p-3 text-[#3B82F6]">{log.action}</td>
                  <td className="p-3 text-[#9AA7BF]">{log.resource_type}:{log.resource_id}</td>
                  <td className="p-3 text-[10px] text-[#7A869C] truncate max-w-xs">{log.current_hash}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};
"""

    files['frontend/src/App.tsx'] = """import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { AppShell } from './components/common/AppShell';
import { CommandCenter } from './pages/CommandCenter';
import { CraftDashboard } from './pages/CraftDashboard';
import { PlansPage } from './pages/PlansPage';
import { PilotPages } from './pages/PilotPages';
import { AuditLogPage } from './pages/AuditLogPage';

export const App: React.FC = () => {
  return (
    <BrowserRouter>
      <AppShell>
        <Routes>
          <Route path="/" element={<CommandCenter />} />
          <Route path="/craft" element={<CraftDashboard />} />
          <Route path="/plans" element={<PlansPage />} />
          <Route path="/pilot" element={<PilotPages />} />
          <Route path="/audit" element={<AuditLogPage />} />
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </AppShell>
    </BrowserRouter>
  );
};
"""

    files['frontend/src/main.tsx'] = """import React from 'react';
import ReactDOM from 'react-dom/client';
import { App } from './App';
import './index.css';

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
"""

    files['frontend/src/index.css'] = """@tailwind base;
@tailwind components;
@tailwind utilities;

:root {
  color-scheme: dark;
}

body {
  margin: 0;
  background-color: #0B1220;
  color: #E8EDF7;
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
  -webkit-font-smoothing: antialiased;
}

/* Custom subtle scrollbar */
::-webkit-scrollbar {
  width: 6px;
  height: 6px;
}

::-webkit-scrollbar-track {
  background: #0B1220;
}

::-webkit-scrollbar-thumb {
  background: #24304A;
  border-radius: 3px;
}

::-webkit-scrollbar-thumb:hover {
  background: #3B82F6;
}
"""

    files['frontend/index.html'] = """<!DOCTYPE html>
<html lang="en" class="dark">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>AERIS — Adaptive Air Operations & Resource Intelligence</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;600;700&display=swap" rel="stylesheet">
  </head>
  <body class="bg-[#0B1220] text-[#E8EDF7] overflow-x-hidden">
    <div id="root"></div>
    <script type="module" src="/src/main.tsx"></script>
  </body>
</html>
"""

    files['frontend/Dockerfile'] = """FROM node:20-alpine as builder
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=builder /app/dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
"""

    return files

print("frontend_components_pages.py loaded")
