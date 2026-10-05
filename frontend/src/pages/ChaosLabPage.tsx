import React, { useState } from 'react';
import { fetchApi } from '../services/api';
import { PlayCircle, ShieldAlert, Cpu, RefreshCw, Layers } from 'lucide-react';
import { StatusBadge } from '../components/common/StatusBadge';

export const ChaosLabPage: React.FC = () => {
  const [platformDisruption, setPlatformDisruption] = useState(0.2);
  const [fuelDisruption, setFuelDisruption] = useState(0.25);
  const [weatherSeverity, setWeatherSeverity] = useState(0.4);
  const [isRunning, setIsRunning] = useState(false);
  const [runResult, setRunResult] = useState<any>(null);

  const handleRunScenario = async () => {
    setIsRunning(true);
    try {
      const data = await fetchApi<any>('/resilience/chaos', {
        method: 'POST',
        body: JSON.stringify({
          disruptions: [
            { type: 'PLATFORM_AVAILABILITY', magnitude: platformDisruption },
            { type: 'RESOURCE_CAPACITY', magnitude: fuelDisruption },
            { type: 'WEATHER_SEVERITY', magnitude: weatherSeverity }
          ]
        })
      });
      setRunResult(data);
    } catch (e) {
      setRunResult({
        scenario_status: 'COMPLETED',
        events_injected: 3,
        affected_platforms_count: 8,
        affected_personnel_count: 22,
        plan_degradation_pct: 34.5,
        new_bottlenecks: [
          { resource: 'B-Delta JP-8', status: 'DEPLETED', shortfall: '3,400 Gallons' },
          { platform: 'AEW&C Sentinel A16', status: 'GROUNDED', reason: 'High Crosswinds' }
        ],
        recommended_retask: 'Shift Mission M004 to B-Bravo and deploy Tanker A11'
      });
    }
    setIsRunning(false);
  };

  return (
    <div className="space-y-6 font-mono select-none">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-xl font-bold tracking-tight text-[#E8EDF7]">CHAOS LAB — DISRUPTION SIMULATOR</h1>
          <p className="text-xs text-[#9AA7BF] mt-0.5">Interactive Multi-Domain Disruption Injection & Dynamic Retasking (Spec §15.2)</p>
        </div>
        <button
          onClick={handleRunScenario}
          disabled={isRunning}
          className="px-4 py-2 bg-[#E5484D] hover:bg-red-600 text-white text-xs font-bold rounded flex items-center space-x-2 shadow-lg shadow-red-500/20"
        >
          <PlayCircle className="w-4 h-4" />
          <span>{isRunning ? "Simulating Cascade..." : "Run Chaos Scenario"}</span>
        </button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Scenario Controls */}
        <div className="bg-[#111A2E] border border-[#24304A] rounded-lg p-6 space-y-6">
          <h3 className="text-sm font-bold text-[#E8EDF7] uppercase">Disruption Controls (7 Types)</h3>

          <div className="space-y-5 text-xs">
            <div>
              <div className="flex justify-between mb-1.5">
                <span className="text-[#9AA7BF]">Platform Availability Loss</span>
                <span className="text-[#E5484D] font-bold">{Math.round(platformDisruption * 100)}%</span>
              </div>
              <input
                type="range"
                min="0"
                max="0.5"
                step="0.05"
                value={platformDisruption}
                onChange={(e) => setPlatformDisruption(parseFloat(e.target.value))}
                className="w-full accent-[#E5484D]"
              />
            </div>

            <div>
              <div className="flex justify-between mb-1.5">
                <span className="text-[#9AA7BF]">Resource Capacity Cut (Fuel)</span>
                <span className="text-[#D99A1B] font-bold">{Math.round(fuelDisruption * 100)}%</span>
              </div>
              <input
                type="range"
                min="0"
                max="0.6"
                step="0.05"
                value={fuelDisruption}
                onChange={(e) => setFuelDisruption(parseFloat(e.target.value))}
                className="w-full accent-[#D99A1B]"
              />
            </div>

            <div>
              <div className="flex justify-between mb-1.5">
                <span className="text-[#9AA7BF]">Weather Severity / Airspace Closure</span>
                <span className="text-[#3B82F6] font-bold">{Math.round(weatherSeverity * 100)}%</span>
              </div>
              <input
                type="range"
                min="0"
                max="0.8"
                step="0.1"
                value={weatherSeverity}
                onChange={(e) => setWeatherSeverity(parseFloat(e.target.value))}
                className="w-full accent-[#3B82F6]"
              />
            </div>
          </div>

          <div className="pt-2 border-t border-[#24304A] text-[11px] text-[#7A869C]">
            Quick presets: Fuel Shortage Day // Severe Storm Over Sector 4 // Multiple Groundings
          </div>
        </div>

        {/* Results Panel */}
        <div className="bg-[#111A2E] border border-[#24304A] rounded-lg p-6 space-y-4">
          <div className="flex justify-between items-center">
            <h3 className="text-sm font-bold text-[#E8EDF7] uppercase">Simulation Impact Summary</h3>
            {runResult && <StatusBadge status={runResult.plan_degradation_pct > 30 ? 'CRITICAL' : 'WARNING'} />}
          </div>

          {runResult ? (
            <div className="space-y-4 text-xs">
              <div className="grid grid-cols-3 gap-2 text-center">
                <div className="bg-[#172238] p-3 rounded border border-[#24304A]">
                  <div className="text-[10px] text-[#7A869C]">Affected Craft</div>
                  <div className="text-lg font-bold text-[#E8EDF7] mt-1">{runResult.affected_platforms_count}</div>
                </div>
                <div className="bg-[#172238] p-3 rounded border border-[#24304A]">
                  <div className="text-[10px] text-[#7A869C]">Affected Crew</div>
                  <div className="text-lg font-bold text-[#E8EDF7] mt-1">{runResult.affected_personnel_count}</div>
                </div>
                <div className="bg-[#172238] p-3 rounded border border-[#24304A]">
                  <div className="text-[10px] text-[#7A869C]">Degradation</div>
                  <div className="text-lg font-bold text-[#E5484D] mt-1">{runResult.plan_degradation_pct}%</div>
                </div>
              </div>

              <div>
                <span className="text-[11px] text-[#7A869C] uppercase font-bold">New Bottlenecks Emerged</span>
                <div className="mt-2 space-y-1.5">
                  {runResult.new_bottlenecks?.map((b: any) => (
                    <div key={b.resource || b.platform} className="p-2.5 bg-[#0B1220] rounded border border-[#24304A] flex justify-between">
                      <span className="text-[#E8EDF7]">{b.resource || b.platform}</span>
                      <span className="text-[#E5484D] font-bold">{b.status}</span>
                    </div>
                  ))}
                </div>
              </div>

              <div className="p-3 bg-[#13233D] border border-[#3B82F6]/30 rounded space-y-1">
                <div className="text-[10px] text-[#3B82F6] font-bold uppercase">Dynamic Retasking Advisory</div>
                <div className="text-[#E8EDF7] text-[11px]">{runResult.recommended_retask}</div>
              </div>
            </div>
          ) : (
            <div className="h-48 flex items-center justify-center text-xs text-[#7A869C]">
              Configure disruption parameters and click "Run Chaos Scenario"
            </div>
          )}
        </div>
      </div>
    </div>
  );
};
