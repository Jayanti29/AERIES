import React, { useState } from 'react';
import { fetchApi } from '../services/api';
import { PlanDNA } from '../components/common/PlanDNA';
import { Sliders, Cpu, ArrowRight } from 'lucide-react';

export const TradeoffExplorer: React.FC = () => {
  const [coverageVal, setCoverageVal] = useState(0.5);
  const [resilienceVal, setResilienceVal] = useState(0.5);
  const [flexibilityVal, setFlexibilityVal] = useState(0.5);
  const [result, setResult] = useState<any>({
    candidate_dna: {
      coverage: 92.0,
      efficiency: 85.0,
      resilience: 88.0,
      flexibility: 82.0,
      speed: 86.0,
      resource_reserve: 78.0
    },
    projected_missions_satisfied: 22,
    projected_reserve_margin_pct: 78.0,
    fragility_index: 1.8
  });

  const handleSliderChange = async (cov: number, res: number, flex: number) => {
    setCoverageVal(cov);
    setResilienceVal(res);
    setFlexibilityVal(flex);

    try {
      const data = await fetchApi<any>('/tradeoffs/explore', {
        method: 'POST',
        body: JSON.stringify({
          coverage_vs_conservation: cov,
          efficiency_vs_resilience: res,
          immediate_vs_flexibility: flex
        })
      });
      setResult(data);
    } catch (e) {}
  };

  return (
    <div className="space-y-6 font-mono select-none">
      <div>
        <h1 className="text-xl font-bold tracking-tight text-[#E8EDF7]">TRADE-OFF EXPLORER</h1>
        <p className="text-xs text-[#9AA7BF] mt-0.5">Real-time CP-SAT Objective Weight Tuning & Plan DNA Preview (Spec §14.6)</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Sliders Panel */}
        <div className="bg-[#111A2E] border border-[#24304A] rounded-lg p-6 space-y-6">
          <h3 className="text-sm font-bold text-[#E8EDF7] uppercase flex items-center space-x-2">
            <Sliders className="w-4 h-4 text-[#3B82F6]" />
            <span>Operational Weight Adjusters</span>
          </h3>

          <div className="space-y-5 text-xs">
            <div>
              <div className="flex justify-between mb-1.5">
                <span className="text-[#9AA7BF]">Sortie Coverage</span>
                <span className="text-[#3B82F6] font-bold">Resource Conservation</span>
              </div>
              <input
                type="range"
                min="0"
                max="1"
                step="0.05"
                value={coverageVal}
                onChange={(e) => handleSliderChange(parseFloat(e.target.value), resilienceVal, flexibilityVal)}
                className="w-full accent-[#3B82F6]"
              />
            </div>

            <div>
              <div className="flex justify-between mb-1.5">
                <span className="text-[#9AA7BF]">Operational Efficiency</span>
                <span className="text-[#22A06B] font-bold">Resilience & Redundancy</span>
              </div>
              <input
                type="range"
                min="0"
                max="1"
                step="0.05"
                value={resilienceVal}
                onChange={(e) => handleSliderChange(coverageVal, parseFloat(e.target.value), flexibilityVal)}
                className="w-full accent-[#22A06B]"
              />
            </div>

            <div>
              <div className="flex justify-between mb-1.5">
                <span className="text-[#9AA7BF]">Immediate Sortie Speed</span>
                <span className="text-[#D99A1B] font-bold">Future Dynamic Flexibility</span>
              </div>
              <input
                type="range"
                min="0"
                max="1"
                step="0.05"
                value={flexibilityVal}
                onChange={(e) => handleSliderChange(coverageVal, resilienceVal, parseFloat(e.target.value))}
                className="w-full accent-[#D99A1B]"
              />
            </div>
          </div>
        </div>

        {/* Dynamic Plan DNA Preview */}
        <div className="bg-[#111A2E] border border-[#24304A] rounded-lg p-6 space-y-4">
          <div className="flex justify-between items-center">
            <h3 className="text-sm font-bold text-[#E8EDF7] uppercase">Candidate Plan DNA Result</h3>
            <span className="text-[10px] text-[#22A06B] font-bold">SOLVER FEASIBLE</span>
          </div>

          <PlanDNA dna={result.candidate_dna} />

          <div className="border-t border-[#24304A] pt-4 grid grid-cols-3 gap-2 text-center text-xs">
            <div className="bg-[#172238] p-2.5 rounded border border-[#24304A]">
              <div className="text-[10px] text-[#7A869C]">Missions</div>
              <div className="text-base font-bold text-[#E8EDF7] mt-0.5">{result.projected_missions_satisfied} / 24</div>
            </div>
            <div className="bg-[#172238] p-2.5 rounded border border-[#24304A]">
              <div className="text-[10px] text-[#7A869C]">Reserve Margin</div>
              <div className="text-base font-bold text-[#22A06B] mt-0.5">{result.projected_reserve_margin_pct}%</div>
            </div>
            <div className="bg-[#172238] p-2.5 rounded border border-[#24304A]">
              <div className="text-[10px] text-[#7A869C]">Fragility Index</div>
              <div className="text-base font-bold text-[#3B82F6] mt-0.5">{result.fragility_index}</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
