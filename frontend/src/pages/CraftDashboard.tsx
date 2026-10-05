import React, { useState, useEffect } from 'react';
import { fetchApi } from '../services/api';
import { StatusBadge } from '../components/common/StatusBadge';
import { KpiCard } from '../components/common/KpiCard';
import { Plane, AlertTriangle, Wrench, CheckCircle2 } from 'lucide-react';

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
        <KpiCard title="In Maintenance" value={summary?.fleet_in_maintenance || 8} status="WARNING" icon={Wrench} />
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
