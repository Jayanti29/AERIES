import React from 'react';
import { Database, ShieldCheck, AlertTriangle, Clock } from 'lucide-react';
import { StatusBadge } from '../components/common/StatusBadge';

export const DataHealthPage: React.FC = () => {
  const sources = [
    { name: 'Aircraft Telemetry Feed', status: 'HEALTHY', freshness: 99.4, completeness: 100, latency: 14, confidence: 'HIGH' },
    { name: 'Personnel & Roster System', status: 'HEALTHY', freshness: 98.2, completeness: 99.1, latency: 42, confidence: 'HIGH' },
    { name: 'Maintenance Log System', status: 'HEALTHY', freshness: 97.5, completeness: 98.0, latency: 38, confidence: 'HIGH' },
    { name: 'Base Resource Depot Sensors', status: 'WARNING', freshness: 88.0, completeness: 92.4, latency: 120, confidence: 'MEDIUM' },
    { name: 'Tactical Weather Radar Feed', status: 'HEALTHY', freshness: 99.1, completeness: 100, latency: 22, confidence: 'HIGH' },
    { name: 'Airspace NOTAM & Restrictions', status: 'WARNING', freshness: 84.5, completeness: 89.0, latency: 240, confidence: 'MEDIUM' }
  ];

  return (
    <div className="space-y-6 font-mono select-none">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-xl font-bold tracking-tight text-[#E8EDF7]">DATA HEALTH & SOURCES</h1>
          <p className="text-xs text-[#9AA7BF] mt-0.5">Telemetry Ingestion, Source Latency, Freshness & Anomaly Quarantine (Spec §11.6)</p>
        </div>
        <div className="text-xs font-bold text-[#22A06B] bg-[#142621] px-3 py-1.5 rounded border border-[#22A06B]/30">
          Global Quality: 98.4%
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {sources.map((s) => (
          <div key={s.name} className="bg-[#111A2E] border border-[#24304A] rounded-lg p-5 space-y-3">
            <div className="flex justify-between items-start">
              <h3 className="text-xs font-bold text-[#E8EDF7] max-w-[12rem]">{s.name}</h3>
              <StatusBadge status={s.status} />
            </div>

            <div className="grid grid-cols-2 gap-2 text-xs pt-2 border-t border-[#24304A]/60">
              <div>
                <span className="text-[#7A869C] text-[10px]">Freshness</span>
                <div className="font-bold text-[#E8EDF7]">{s.freshness}%</div>
              </div>
              <div>
                <span className="text-[#7A869C] text-[10px]">Completeness</span>
                <div className="font-bold text-[#E8EDF7]">{s.completeness}%</div>
              </div>
              <div>
                <span className="text-[#7A869C] text-[10px]">Latency</span>
                <div className="font-bold text-[#3B82F6]">{s.latency} ms</div>
              </div>
              <div>
                <span className="text-[#7A869C] text-[10px]">Confidence</span>
                <div className={`font-bold ${s.confidence === 'HIGH' ? 'text-[#22A06B]' : 'text-[#D99A1B]'}`}>{s.confidence}</div>
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* Quarantine Review Table */}
      <div className="bg-[#111A2E] border border-[#24304A] rounded-lg p-5 space-y-3">
        <h3 className="text-sm font-bold text-[#E8EDF7] uppercase">Anomaly Quarantine Queue (Spec §11.4)</h3>
        <p className="text-xs text-[#9AA7BF]">Out-of-range or anomalous feed values (z-score &gt; 6) quarantined to prevent state poisoning.</p>

        <div className="border border-[#24304A] rounded text-xs overflow-hidden">
          <table className="w-full text-left">
            <thead className="bg-[#172238] text-[#9AA7BF]">
              <tr>
                <th className="p-3">Event ID</th>
                <th className="p-3">Source</th>
                <th className="p-3">Received (UTC)</th>
                <th className="p-3">Quarantine Reason</th>
                <th className="p-3">Action</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-[#24304A]">
              <tr className="hover:bg-[#172238]/40">
                <td className="p-3 font-bold text-[#E8EDF7]">EVT-8921</td>
                <td className="p-3 text-[#9AA7BF]">airspace-feed-02</td>
                <td className="p-3 text-[#7A869C]">10:24:12</td>
                <td className="p-3 text-[#E5484D]">Timestamp in future (+45 mins) rejected by domain validator</td>
                <td className="p-3">
                  <span className="text-[11px] text-[#7A869C]">Held for review</span>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};
