import React, { useState, useEffect } from 'react';
import { fetchApi } from '../services/api';
import { StatusBadge } from '../components/common/StatusBadge';
import { KpiCard } from '../components/common/KpiCard';
import { Users, Lock, Unlock, ShieldAlert, Award } from 'lucide-react';
import { StepUpDialog } from '../components/common/StepUpDialog';
import { ReasonDialog } from '../components/common/ReasonDialog';

export const PeopleDashboard: React.FC = () => {
  const [people, setPeople] = useState<any[]>([]);
  const [summary, setSummary] = useState<any>(null);
  const [unmaskTarget, setUnmaskTarget] = useState<string | null>(null);
  const [showStepUp, setShowStepUp] = useState(false);
  const [showReason, setShowReason] = useState(false);
  const [unmaskedName, setUnmaskedName] = useState<string | null>(null);

  useEffect(() => {
    fetchApi<any[]>('/people/roster').then(setPeople).catch(() => {});
    fetchApi<any>('/people/summary').then(setSummary).catch(() => {});
  }, []);

  const handleStartUnmask = (code: string) => {
    setUnmaskTarget(code);
    setShowStepUp(true);
  };

  const handleStepUpSuccess = () => {
    setShowStepUp(false);
    setShowReason(true);
  };

  const handleReasonConfirm = async (reason: string) => {
    setShowReason(false);
    try {
      const res = await fetchApi<any>('/people/unmask', {
        method: 'POST',
        body: JSON.stringify({ person_code: unmaskTarget, justification_reason: reason })
      });
      setUnmaskedName(`${res.callsign}: ${res.real_name}`);
      alert(`PII Unmasked: ${res.real_name} (${res.callsign}). Access recorded in Audit Ledger.`);
    } catch (e: any) {
      alert("Unmasking denied: " + e.message);
    }
  };

  return (
    <div className="space-y-6 font-mono select-none">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-xl font-bold tracking-tight text-[#E8EDF7]">PERSONNEL & AIRCREW ROSTER</h1>
          <p className="text-xs text-[#9AA7BF] mt-0.5">Masked Identities, Workload Distribution & Qualification Coverage (Spec §5.4, §7)</p>
        </div>
        <div className="text-xs text-[#D99A1B] bg-[#2A2314] px-3 py-1.5 rounded border border-[#D99A1B]/30 flex items-center space-x-2">
          <Lock className="w-3.5 h-3.5" />
          <span>PII Masked By Default</span>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <KpiCard title="Total Personnel" value={summary?.personnel_total || 400} status="NOMINAL" icon={Users} />
        <KpiCard title="Available for Duty" value={summary?.personnel_available || 342} status="HEALTHY" icon={Award} />
        <KpiCard title="High Workload (>90%)" value={summary?.personnel_overloaded || 24} status="WARNING" icon={ShieldAlert} />
        <KpiCard title="Qualification Gaps" value={summary?.qualification_gaps || 2} status="CRITICAL" icon={Lock} />
      </div>

      <div className="bg-[#111A2E] border border-[#24304A] rounded-lg p-5">
        <h3 className="text-sm font-bold text-[#E8EDF7] mb-4">PERSONNEL ROSTER (PRIVACY PROTECTED)</h3>
        <div className="max-h-96 overflow-y-auto border border-[#24304A] rounded text-xs">
          <table className="w-full text-left">
            <thead className="bg-[#172238] text-[#9AA7BF] sticky top-0 uppercase">
              <tr>
                <th className="p-3">Code</th>
                <th className="p-3">Callsign</th>
                <th className="p-3">Identity (PII)</th>
                <th className="p-3">Team</th>
                <th className="p-3">Role</th>
                <th className="p-3">Status</th>
                <th className="p-3">Workload</th>
                <th className="p-3">Action</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-[#24304A]">
              {people.slice(0, 16).map((p) => (
                <tr key={p.code} className="hover:bg-[#172238]/40">
                  <td className="p-3 font-bold text-[#3B82F6]">{p.code}</td>
                  <td className="p-3 text-[#E8EDF7] font-semibold">{p.callsign}</td>
                  <td className="p-3 text-[#7A869C]">{p.masked_name}</td>
                  <td className="p-3 text-[#9AA7BF]">{p.team}</td>
                  <td className="p-3 text-[#E8EDF7]">{p.role}</td>
                  <td className="p-3"><StatusBadge status={p.status} /></td>
                  <td className="p-3">
                    <span className={`font-bold ${p.workload_pct > 88 ? 'text-[#E5484D]' : 'text-[#22A06B]'}`}>
                      {p.workload_pct}%
                    </span>
                  </td>
                  <td className="p-3">
                    <button
                      onClick={() => handleStartUnmask(p.code)}
                      className="px-2 py-1 bg-[#172238] hover:bg-[#24304A] text-[#3B82F6] rounded text-[11px] font-bold border border-[#24304A]"
                    >
                      Unmask
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      <StepUpDialog
        isOpen={showStepUp}
        actionTitle="Unmask Classified Personnel Identity (PII)"
        onSuccess={handleStepUpSuccess}
        onCancel={() => setShowStepUp(false)}
      />

      <ReasonDialog
        isOpen={showReason}
        title="Documented Need-to-Know Justification"
        promptText="State operational need-to-know reason per Spec §7.2 for accessing individual real name."
        onConfirm={handleReasonConfirm}
        onCancel={() => setShowReason(false)}
      />
    </div>
  );
};
