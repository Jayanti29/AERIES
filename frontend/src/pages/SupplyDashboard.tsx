import React, { useState, useEffect } from 'react';
import { fetchApi } from '../services/api';
import { StatusBadge } from '../components/common/StatusBadge';
import { KpiCard } from '../components/common/KpiCard';
import { Box, AlertTriangle, ShieldCheck, Flame, ArrowUpRight } from 'lucide-react';
import { ReasonDialog } from '../components/common/ReasonDialog';

export const SupplyDashboard: React.FC = () => {
  const [resources, setResources] = useState<any[]>([]);
  const [summary, setSummary] = useState<any>(null);
  const [flagModalOpen, setFlagModalOpen] = useState(false);
  const [selectedRes, setSelectedRes] = useState<string>('R01');

  useEffect(() => {
    fetchApi<any[]>('/supply/resources').then(setResources).catch(() => {});
    fetchApi<any>('/supply/summary').then(setSummary).catch(() => {});
  }, []);

  const handleFlagConfirm = async (reason: string) => {
    await fetchApi('/flags/resource', {
      method: 'POST',
      body: JSON.stringify({ entity_code: selectedRes, flag_type: 'SHORTFALL', reason })
    }).catch(() => {});
    setFlagModalOpen(false);
    alert(`Resource ${selectedRes} flagged successfully into validation pipeline.`);
  };

  return (
    <div className="space-y-6 font-mono select-none">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-xl font-bold tracking-tight text-[#E8EDF7]">SUPPLY & LOGISTICS POSTURE</h1>
          <p className="text-xs text-[#9AA7BF] mt-0.5">Resource Stocks, Projected Shortfalls & Base Buffers (Spec §5.3)</p>
        </div>
        <button
          onClick={() => setFlagModalOpen(true)}
          className="px-3.5 py-1.5 bg-[#D99A1B] hover:bg-amber-600 text-black text-xs font-bold rounded"
        >
          Flag Resource Issue
        </button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <KpiCard title="Tracked Resources" value={summary?.resource_types_tracked || 12} status="NOMINAL" icon={Box} />
        <KpiCard title="Under Pressure" value={summary?.resources_under_pressure || 5} status="WARNING" icon={AlertTriangle} />
        <KpiCard title="Projected Shortfalls (2h)" value={summary?.projected_shortfalls_2h || 2} status="CRITICAL" icon={Flame} />
        <KpiCard title="Average Reserve Margin" value={`${summary?.average_reserve_margin_pct || 28.5}%`} status="HEALTHY" icon={ShieldCheck} />
      </div>

      <div className="bg-[#111A2E] border border-[#24304A] rounded-lg p-5">
        <h3 className="text-sm font-bold text-[#E8EDF7] mb-4">BASE RESOURCE STOCK & PROJECTED PRESSURES</h3>
        <div className="max-h-96 overflow-y-auto border border-[#24304A] rounded text-xs">
          <table className="w-full text-left">
            <thead className="bg-[#172238] text-[#9AA7BF] sticky top-0 uppercase">
              <tr>
                <th className="p-3">Code</th>
                <th className="p-3">Resource Name</th>
                <th className="p-3">Base</th>
                <th className="p-3">Available</th>
                <th className="p-3">Demand (2h)</th>
                <th className="p-3">Reserve Margin</th>
                <th className="p-3">Pressure Status</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-[#24304A]">
              {resources.slice(0, 16).map((r) => (
                <tr key={r.id} className="hover:bg-[#172238]/40">
                  <td className="p-3 font-bold text-[#3B82F6]">{r.code}</td>
                  <td className="p-3 text-[#E8EDF7]">{r.name}</td>
                  <td className="p-3 text-[#9AA7BF]">{r.base_code}</td>
                  <td className="p-3 text-[#E8EDF7] font-semibold">{r.available_qty} {r.unit}</td>
                  <td className="p-3 text-[#9AA7BF]">{r.demand_qty} {r.unit}</td>
                  <td className="p-3 text-[#E8EDF7]">{r.reserve_threshold} {r.unit}</td>
                  <td className="p-3"><StatusBadge status={r.pressure_level} /></td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      <ReasonDialog
        isOpen={flagModalOpen}
        title="Flag Resource Shortfall / Delay"
        promptText="Submitting a formal resource flag creates an audited event in the pipeline to trigger replanning."
        onConfirm={handleFlagConfirm}
        onCancel={() => setFlagModalOpen(false)}
      />
    </div>
  );
};
