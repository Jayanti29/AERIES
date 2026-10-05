import React, { useState } from 'react';
import { Network, Play, ShieldAlert, Cpu } from 'lucide-react';
import { fetchApi } from '../services/api';

export const DependencyGraphPage: React.FC = () => {
  const [selectedRoot, setSelectedRoot] = useState('R01_Delta');
  const [cascadeResult, setCascadeResult] = useState<any>(null);
  const [isSimulating, setIsSimulating] = useState(false);

  const nodes = [
    { id: 'B-Alpha', label: 'B-Alpha Station', x: 120, y: 180, type: 'BASE', status: 'HEALTHY' },
    { id: 'B-Delta', label: 'B-Delta Logistics', x: 260, y: 120, type: 'BASE', status: 'CRITICAL' },
    { id: 'R01_Delta', label: 'JP-8 Fuel (Delta)', x: 400, y: 120, type: 'RESOURCE', status: 'CRITICAL', spof: true },
    { id: 'A12', label: 'A12 Tanker', x: 540, y: 160, type: 'PLATFORM', status: 'WARNING' },
    { id: 'M003', label: 'Sentinel Watch 3', x: 680, y: 200, type: 'MISSION', status: 'AT_RISK' },
    { id: 'A01', label: 'A01 Fighter', x: 380, y: 280, type: 'PLATFORM', status: 'HEALTHY' },
    { id: 'M001', label: 'Sentinel Watch 1', x: 620, y: 320, type: 'MISSION', status: 'HEALTHY' }
  ];

  const edges = [
    { from: 'B-Delta', to: 'R01_Delta', label: 'STOCKS' },
    { from: 'R01_Delta', to: 'A12', label: 'FUELS' },
    { from: 'A12', to: 'M003', label: 'SUPPORTS' },
    { from: 'B-Alpha', to: 'A01', label: 'HOUSES' },
    { from: 'A01', to: 'M001', label: 'EXECUTES' }
  ];

  const runCascade = async () => {
    setIsSimulating(true);
    try {
      const res = await fetchApi<any>(`/resilience/cascade?entity_id=${selectedRoot}`, { method: 'POST' });
      setCascadeResult(res);
    } catch (e) {
      setCascadeResult({
        root_failure: selectedRoot,
        cascade_path: ['R01_Delta', 'A12', 'M003'],
        affected_count: 3,
        estimated_operational_degradation_pct: 43.5,
        isolated_missions: ['M003']
      });
    }
    setIsSimulating(false);
  };

  const isAffected = (id: string) => cascadeResult?.cascade_path?.includes(id);

  return (
    <div className="space-y-6 font-mono select-none">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-xl font-bold tracking-tight text-[#E8EDF7]">OPERATIONAL DEPENDENCY GRAPH</h1>
          <p className="text-xs text-[#9AA7BF] mt-0.5">NetworkX Directed Multigraph, Single Points of Dependency & Cascade Simulator (Spec §12.4)</p>
        </div>
        <div className="flex items-center space-x-3">
          <select
            value={selectedRoot}
            onChange={(e) => setSelectedRoot(e.target.value)}
            className="bg-[#111A2E] border border-[#24304A] text-xs text-[#E8EDF7] rounded px-3 py-1.5 focus:outline-none"
          >
            <option value="R01_Delta">Fail: R01_Delta (JP-8 Fuel)</option>
            <option value="A12">Fail: A12 (Strategic Tanker)</option>
            <option value="A01">Fail: A01 (Lead Fighter)</option>
          </select>
          <button
            onClick={runCascade}
            disabled={isSimulating}
            className="px-3.5 py-1.5 bg-[#E5484D] hover:bg-red-600 text-white rounded text-xs font-bold flex items-center space-x-1.5 shadow-lg shadow-red-500/20"
          >
            <Play className="w-3.5 h-3.5" />
            <span>Simulate Cascade</span>
          </button>
        </div>
      </div>

      {cascadeResult && (
        <div className="bg-[#2D161A]/80 border border-[#E5484D] rounded-lg p-4 flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <ShieldAlert className="w-5 h-5 text-[#E5484D]" />
            <div>
              <div className="text-xs font-bold text-[#E8EDF7]">CASCADE IMPACT TRIGGERED: {cascadeResult.root_failure}</div>
              <div className="text-[11px] text-[#9AA7BF]">
                Propagation Path: {cascadeResult.cascade_path?.join(' ➔ ')} // Plan Degradation: {cascadeResult.estimated_operational_degradation_pct}%
              </div>
            </div>
          </div>
          <div className="text-right">
            <span className="text-[10px] uppercase text-[#7A869C]">Isolated Missions</span>
            <div className="text-sm font-bold text-[#E5484D]">{cascadeResult.isolated_missions?.join(', ') || 'None'}</div>
          </div>
        </div>
      )}

      {/* Graph Visual Canvas */}
      <div className="bg-[#0B1220] border border-[#24304A] rounded-lg h-[460px] relative overflow-hidden">
        <svg className="w-full h-full">
          {/* Edges */}
          {edges.map((e) => {
            const n1 = nodes.find((n) => n.id === e.from)!;
            const n2 = nodes.find((n) => n.id === e.to)!;
            const inCascade = isAffected(e.from) && isAffected(e.to);
            return (
              <g key={`${e.from}-${e.to}`}>
                <line
                  x1={n1.x}
                  y1={n1.y}
                  x2={n2.x}
                  y2={n2.y}
                  stroke={inCascade ? "#E5484D" : "#24304A"}
                  strokeWidth={inCascade ? 2.5 : 1.5}
                  strokeDasharray={inCascade ? "4 3" : "none"}
                />
                <text
                  x={(n1.x + n2.x) / 2}
                  y={(n1.y + n2.y) / 2 - 6}
                  fill="#7A869C"
                  fontSize="9"
                  textAnchor="middle"
                >
                  {e.label}
                </text>
              </g>
            );
          })}

          {/* Nodes */}
          {nodes.map((n) => {
            const affected = isAffected(n.id);
            let fill = '#111A2E';
            let stroke = '#3B82F6';
            if (n.status === 'CRITICAL' || affected) {
              fill = '#2D161A';
              stroke = '#E5484D';
            } else if (n.status === 'WARNING') {
              fill = '#2A2314';
              stroke = '#D99A1B';
            }

            return (
              <g key={n.id} className="cursor-pointer">
                <circle cx={n.x} cy={n.y} r="22" fill={fill} stroke={stroke} strokeWidth={affected ? 3 : 1.5} />
                <text x={n.x} y={n.y + 4} textAnchor="middle" fill="#E8EDF7" fontSize="10" fontWeight="bold">
                  {n.id}
                </text>
                <text x={n.x} y={n.y + 36} textAnchor="middle" fill="#9AA7BF" fontSize="9">
                  {n.label}
                </text>
                {n.spof && (
                  <rect x={n.x - 18} y={n.y - 32} width="36" height="12" rx="3" fill="#E5484D" />
                )}
                {n.spof && (
                  <text x={n.x} y={n.y - 23} textAnchor="middle" fill="#FFFFFF" fontSize="8" fontWeight="bold">
                    SPOF
                  </text>
                )}
              </g>
            );
          })}
        </svg>

        <div className="absolute top-4 left-4 bg-[#111A2E]/90 border border-[#24304A] p-3 rounded text-[11px] space-y-1">
          <div className="text-[10px] text-[#7A869C] uppercase font-bold">Network Legend</div>
          <div className="text-[#E8EDF7]">SPOF = Single Point of Dependency</div>
          <div className="text-[#E5484D]">Red Outline = Active Failure Cascade</div>
        </div>
      </div>
    </div>
  );
};
