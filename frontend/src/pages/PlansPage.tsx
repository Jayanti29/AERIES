import React, { useState, useEffect } from 'react';
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
