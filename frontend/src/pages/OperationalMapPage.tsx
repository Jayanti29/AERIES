import React, { useState } from 'react';
import { Compass, Layers, Shield, Plane, AlertTriangle, Eye } from 'lucide-react';
import { StatusBadge } from '../components/common/StatusBadge';
import { EntityDrawer } from '../components/common/EntityDrawer';

export const OperationalMapPage: React.FC = () => {
  const [selectedEntity, setSelectedEntity] = useState<any>(null);
  const [showAirspace, setShowAirspace] = useState(true);
  const [showWeather, setShowWeather] = useState(true);

  const bases = [
    { code: 'B-Alpha', name: 'Alpha Forward Station', x: 200, y: 180, platforms: 12, readiness: 94 },
    { code: 'B-Bravo', name: 'Bravo Ridge Airfield', x: 380, y: 140, platforms: 10, readiness: 91 },
    { code: 'B-Charlie', name: 'Charlie Coastal Hub', x: 180, y: 340, platforms: 15, readiness: 88 },
    { code: 'B-Delta', name: 'Delta Desert Logistics', x: 420, y: 320, platforms: 8, readiness: 78, isConstraint: true },
    { code: 'B-Echo', name: 'Echo Highlands Depot', x: 620, y: 200, platforms: 9, readiness: 85 },
    { code: 'B-Foxtrot', name: 'Foxtrot Northern Outpost', x: 260, y: 80, platforms: 6, readiness: 92 }
  ];

  const airborne = [
    { code: 'A01', type: 'Fighter', x: 280, y: 220, mission: 'M001', heading: 45 },
    { code: 'A12', type: 'Tanker', x: 350, y: 280, mission: 'M003', heading: 120, atRisk: true },
    { code: 'A24', type: 'Recon Drone', x: 500, y: 160, mission: 'M007', heading: 270 }
  ];

  return (
    <div className="space-y-6 font-mono select-none">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-xl font-bold tracking-tight text-[#E8EDF7]">OPERATIONAL AIR & BASE MAP</h1>
          <p className="text-xs text-[#9AA7BF] mt-0.5">Geospatial Posture, Station Capacities & Tactical Air Corridors (Spec §18.2)</p>
        </div>
        <div className="flex items-center space-x-3 bg-[#111A2E] p-1.5 rounded border border-[#24304A] text-xs">
          <label className="flex items-center space-x-1.5 cursor-pointer text-[#9AA7BF] hover:text-[#E8EDF7]">
            <input
              type="checkbox"
              checked={showAirspace}
              onChange={(e) => setShowAirspace(e.target.checked)}
              className="accent-[#3B82F6]"
            />
            <span>Airspace Corridors</span>
          </label>
          <span className="text-[#24304A]">|</span>
          <label className="flex items-center space-x-1.5 cursor-pointer text-[#9AA7BF] hover:text-[#E8EDF7]">
            <input
              type="checkbox"
              checked={showWeather}
              onChange={(e) => setShowWeather(e.target.checked)}
              className="accent-[#3B82F6]"
            />
            <span>Weather Severity</span>
          </label>
        </div>
      </div>

      <div className="relative bg-[#0B1220] border border-[#24304A] rounded-lg h-[540px] overflow-hidden">
        {/* Synthetic Tactical Grid Canvas */}
        <svg className="w-full h-full">
          <defs>
            <pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse">
              <path d="M 40 0 L 0 0 0 40" fill="none" stroke="#172238" strokeWidth="0.8" />
            </pattern>
          </defs>
          <rect width="100%" height="100%" fill="url(#grid)" />

          {/* Airspace corridor overlay */}
          {showAirspace && (
            <path
              d="M 200 180 Q 320 250 420 320"
              fill="none"
              stroke="#3B82F6"
              strokeWidth="2"
              strokeDasharray="6 4"
              opacity="0.6"
            />
          )}

          {/* Weather Zone */}
          {showWeather && (
            <ellipse
              cx="540"
              cy="280"
              rx="110"
              ry="70"
              fill="#D99A1B"
              fillOpacity="0.08"
              stroke="#D99A1B"
              strokeWidth="1.5"
              strokeDasharray="4 4"
            />
          )}

          {/* Flight Vectors */}
          {airborne.map((a) => (
            <g
              key={a.code}
              onClick={() => setSelectedEntity({ ...a, readiness_score: 0.94, flight_hours: 1420 })}
              className="cursor-pointer group"
            >
              <circle cx={a.x} cy={a.y} r="8" fill={a.atRisk ? "#E5484D" : "#3B82F6"} fillOpacity="0.3" />
              <circle cx={a.x} cy={a.y} r="3.5" fill={a.atRisk ? "#E5484D" : "#3B82F6"} />
              <text x={a.x + 12} y={a.y + 4} fill="#E8EDF7" fontSize="10" fontWeight="bold">
                {a.code} ({a.type})
              </text>
            </g>
          ))}

          {/* Bases Markers */}
          {bases.map((b) => (
            <g
              key={b.code}
              onClick={() => setSelectedEntity({ ...b, type: 'BASE', status: b.isConstraint ? 'WARNING' : 'OPERATIONAL' })}
              className="cursor-pointer group"
            >
              <polygon
                points={`${b.x},${b.y - 12} ${b.x + 10},${b.y + 8} ${b.x - 10},${b.y + 8}`}
                fill={b.isConstraint ? "#E5484D" : "#22A06B"}
                fillOpacity="0.8"
                stroke="#111A2E"
                strokeWidth="2"
              />
              <text x={b.x + 14} y={b.y + 2} fill="#E8EDF7" fontSize="11" fontWeight="bold">
                {b.code} - {b.name}
              </text>
              <text x={b.x + 14} y={b.y + 14} fill="#9AA7BF" fontSize="9">
                {b.platforms} platforms | {b.readiness}% ready
              </text>
            </g>
          ))}
        </svg>

        {/* Tactical Legend Box */}
        <div className="absolute bottom-4 left-4 bg-[#111A2E]/90 border border-[#24304A] p-3 rounded text-[11px] space-y-1.5 backdrop-blur-sm">
          <div className="text-[10px] text-[#7A869C] uppercase font-bold">Tactical Map Layers</div>
          <div className="flex items-center space-x-2">
            <span className="w-2.5 h-2.5 rounded-full bg-[#22A06B]"></span>
            <span className="text-[#E8EDF7]">Operational Air Base</span>
          </div>
          <div className="flex items-center space-x-2">
            <span className="w-2.5 h-2.5 rounded-full bg-[#E5484D]"></span>
            <span className="text-[#E8EDF7]">Constrained Base / At-Risk Asset</span>
          </div>
          <div className="flex items-center space-x-2">
            <span className="w-2.5 h-2.5 rounded-full bg-[#3B82F6]"></span>
            <span className="text-[#E8EDF7]">Airborne Sortie In Flight</span>
          </div>
        </div>
      </div>

      <EntityDrawer entity={selectedEntity} onClose={() => setSelectedEntity(null)} />
    </div>
  );
};
