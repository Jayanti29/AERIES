import React, { useState, useEffect } from 'react';
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
