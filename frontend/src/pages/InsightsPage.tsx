import React from 'react';
import { AlertOctagon, HelpCircle, AlertTriangle, ShieldCheck, ArrowRight } from 'lucide-react';
import { StatusBadge } from '../components/common/StatusBadge';
import { ProvenanceValue } from '../components/common/ProvenanceValue';

export const InsightsPage: React.FC = () => {
  const insights = [
    {
      id: 'INS-01',
      rule: 'Shared Constrained Resource',
      title: 'B-Delta Jet Fuel JP-8 Depletion Risk',
      severity: 'CRITICAL',
      confidence: 0.94,
      affected: ['M003', 'M007', 'M011', 'Platform A12'],
      observedTime: '2026-10-05T10:31:24Z',
      message: 'Four concurrent missions depend on resource R01 at B-Delta, which is projected to fall below reserve margins in 65 minutes under current sortie rates.'
    },
    {
      id: 'INS-02',
      rule: 'Single Point of Failure',
      title: 'Strategic Tanker Platform A12 Non-Substitutable',
      severity: 'HIGH',
      confidence: 0.91,
      affected: ['Mission M003', 'M007'],
      observedTime: '2026-10-05T10:28:10Z',
      message: 'Substitutability calculation returns 0 alternative airborne refueling platforms capable of servicing extended patrol Sector 4.'
    },
    {
      id: 'INS-03',
      rule: 'Emerging Bottleneck',
      title: 'Composite Airframe Repair Core at B-Echo',
      severity: 'WARNING',
      confidence: 0.88,
      affected: ['Resource R07', 'Base B-Echo'],
      observedTime: '2026-10-05T10:22:00Z',
      message: 'Projected demand crosses 1.0 threshold within 120 minutes as turnaround inspections converge.'
    },
    {
      id: 'INS-04',
      rule: 'Overloaded Person',
      title: 'Avionics Specialist Workload Warning (P-0042)',
      severity: 'WARNING',
      confidence: 0.97,
      affected: ['Crew T3', 'Personnel P-0042'],
      observedTime: '2026-10-05T10:15:00Z',
      message: 'Cumulative duty hours reach 94% of rolling 24-hour limit. Rule rest violation projected if retasked.'
    }
  ];

  return (
    <div className="space-y-6 font-mono select-none">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-xl font-bold tracking-tight text-[#E8EDF7]">OPERATIONAL INSIGHTS</h1>
          <p className="text-xs text-[#9AA7BF] mt-0.5">Automated Rule Engine: "What are we not seeing?" (Spec §12.7)</p>
        </div>
        <div className="text-xs text-[#3B82F6] font-bold bg-[#13233D] px-3 py-1.5 rounded border border-[#3B82F6]/30">
          4 Active Hidden Constraints
        </div>
      </div>

      <div className="space-y-4">
        {insights.map((ins) => (
          <div
            key={ins.id}
            className="bg-[#111A2E] border border-[#24304A] hover:border-[#3B82F6]/50 rounded-lg p-5 space-y-3 transition-colors"
          >
            <div className="flex justify-between items-start">
              <div>
                <div className="flex items-center space-x-2">
                  <StatusBadge status={ins.severity} />
                  <span className="text-xs text-[#7A869C]">{ins.id} // {ins.rule}</span>
                </div>
                <h3 className="text-base font-bold text-[#E8EDF7] mt-1.5">{ins.title}</h3>
              </div>
              <ProvenanceValue value={`${Math.round(ins.confidence * 100)}% Conf`} confidence={ins.confidence} source="Insights Rule Engine" observedAt={ins.observedTime} />
            </div>

            <p className="text-xs text-[#9AA7BF] leading-relaxed">{ins.message}</p>

            <div className="pt-2 border-t border-[#24304A] flex justify-between items-center text-xs">
              <div className="flex items-center space-x-2">
                <span className="text-[#7A869C]">Affected Entities:</span>
                {ins.affected.map((a) => (
                  <span key={a} className="bg-[#172238] px-2 py-0.5 rounded text-[#E8EDF7] border border-[#24304A]">
                    {a}
                  </span>
                ))}
              </div>
              <a
                href="/plans"
                className="text-[#3B82F6] hover:text-blue-400 font-bold flex items-center space-x-1"
              >
                <span>Mitigate in Optimizer</span>
                <ArrowRight className="w-3.5 h-3.5" />
              </a>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
