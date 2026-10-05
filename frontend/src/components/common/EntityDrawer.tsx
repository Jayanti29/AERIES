import React, { useState } from 'react';
import { X, Plane, User, Box, Landmark, Shield, Cpu, History, Link, Activity } from 'lucide-react';
import { StatusBadge } from './StatusBadge';
import { ProvenanceValue } from './ProvenanceValue';

interface EntityDrawerProps {
  entity: any | null;
  onClose: () => void;
}

export const EntityDrawer: React.FC<EntityDrawerProps> = ({ entity, onClose }) => {
  const [activeTab, setActiveTab] = useState<'overview' | 'assignments' | 'maintenance' | 'components' | 'prediction' | 'history'>('overview');

  if (!entity) return null;

  return (
    <div className="fixed inset-y-0 right-0 w-96 bg-[#111A2E] border-l border-[#24304A] shadow-2xl z-50 flex flex-col font-mono select-none">
      {/* Drawer Header */}
      <div className="p-4 bg-[#172238] border-b border-[#24304A] flex justify-between items-start">
        <div>
          <div className="flex items-center space-x-2">
            <span className="text-xs font-bold text-[#3B82F6] uppercase">{entity.type || 'AIRCRAFT'}</span>
            <span className="text-[10px] text-[#7A869C]">UUID: {entity.id || 'uuid-001'}</span>
          </div>
          <div className="text-lg font-bold text-[#E8EDF7] mt-0.5">{entity.code || entity.name || 'ENTITY-01'}</div>
          <div className="text-xs text-[#9AA7BF]">{entity.platform_type || entity.role || entity.unit || 'Platform Subsystem'}</div>
        </div>
        <button onClick={onClose} className="text-[#7A869C] hover:text-[#E8EDF7] p-1">
          <X className="w-5 h-5" />
        </button>
      </div>

      {/* Drawer Navigation Tabs */}
      <div className="flex border-b border-[#24304A] bg-[#0B1220] overflow-x-auto text-[11px]">
        {(['overview', 'assignments', 'maintenance', 'prediction', 'history'] as const).map((tab) => (
          <button
            key={tab}
            onClick={() => setActiveTab(tab)}
            className={`px-3 py-2 border-b-2 font-semibold capitalize whitespace-nowrap transition-colors ${
              activeTab === tab
                ? 'border-[#3B82F6] text-[#3B82F6] bg-[#111A2E]'
                : 'border-transparent text-[#7A869C] hover:text-[#E8EDF7]'
            }`}
          >
            {tab}
          </button>
        ))}
      </div>

      {/* Drawer Body Content */}
      <div className="flex-1 p-5 overflow-y-auto space-y-4 text-xs">
        {activeTab === 'overview' && (
          <div className="space-y-4">
            <div className="bg-[#172238]/60 p-3 rounded border border-[#24304A] space-y-2">
              <div className="flex justify-between">
                <span className="text-[#9AA7BF]">Operational Status:</span>
                <StatusBadge status={entity.status || 'READY'} />
              </div>
              <div className="flex justify-between">
                <span className="text-[#9AA7BF]">Readiness Score:</span>
                <ProvenanceValue value={`${Math.round((entity.readiness_score || 0.94) * 100)}%`} source="telemetry-feed" confidence={0.98} />
              </div>
              <div className="flex justify-between">
                <span className="text-[#9AA7BF]">Station / Base:</span>
                <span className="text-[#E8EDF7] font-semibold">{entity.base_code || 'B-Alpha'}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-[#9AA7BF]">Total Flight Hours:</span>
                <span className="text-[#E8EDF7]">{entity.flight_hours || 1240.5} hrs</span>
              </div>
            </div>

            <div>
              <h4 className="text-[11px] font-bold text-[#7A869C] uppercase mb-2">Primary Components</h4>
              <div className="space-y-1.5">
                {[
                  { name: 'Engine Core 1', health: 94, status: 'STABLE' },
                  { name: 'APG-81 Radar', health: 88, status: 'STABLE' },
                  { name: 'Avionics Bus', health: 98, status: 'STABLE' }
                ].map((c) => (
                  <div key={c.name} className="flex justify-between items-center p-2 rounded bg-[#0B1220] border border-[#24304A]">
                    <span className="text-[#E8EDF7]">{c.name}</span>
                    <span className="font-bold text-[#22A06B]">{c.health}%</span>
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}

        {activeTab === 'prediction' && (
          <div className="space-y-4">
            <div className="bg-[#172238]/60 p-3 rounded border border-[#24304A]">
              <div className="text-[11px] font-bold text-[#7A869C] uppercase mb-1">XGBoost Forecast (Spec §13)</div>
              <div className="flex justify-between items-center my-2">
                <span className="text-[#9AA7BF]">P(Failure @ 120m):</span>
                <span className="text-base font-bold text-[#D99A1B]">18.4%</span>
              </div>
              <div className="w-full bg-[#0B1220] rounded-full h-1.5 overflow-hidden">
                <div className="h-full bg-[#D99A1B]" style={{ width: '18.4%' }}></div>
              </div>
            </div>

            <div>
              <h4 className="text-[11px] font-bold text-[#7A869C] uppercase mb-2">SHAP Feature Importances</h4>
              <div className="space-y-1.5">
                {[
                  { feature: 'Exhaust Gas Temp Differential', delta: '+0.24', color: 'text-[#E5484D]' },
                  { feature: 'High Vibration Cycles', delta: '+0.11', color: 'text-[#E5484D]' },
                  { feature: 'Hydraulic Pressure Stability', delta: '-0.07', color: 'text-[#22A06B]' }
                ].map((s) => (
                  <div key={s.feature} className="flex justify-between items-center p-2 rounded bg-[#0B1220] border border-[#24304A]">
                    <span className="text-[#9AA7BF]">{s.feature}</span>
                    <span className={`font-bold ${s.color}`}>{s.delta}</span>
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}

        {activeTab === 'assignments' && (
          <div className="space-y-3">
            <div className="bg-[#172238]/60 p-3 rounded border border-[#24304A]">
              <div className="text-[11px] text-[#7A869C] uppercase">Active Mission</div>
              <div className="text-sm font-bold text-[#3B82F6] mt-1">{entity.current_mission || 'M001 - Operation Sentinel Watch'}</div>
              <div className="text-[11px] text-[#9AA7BF] mt-1">Slot: 11:00 - 15:00 UTC // Station: B-Alpha</div>
            </div>
          </div>
        )}

        {activeTab === 'maintenance' && (
          <div className="space-y-3">
            <div className="p-3 rounded bg-[#0B1220] border border-[#24304A]">
              <div className="text-[#7A869C] text-[11px]">Next Inspection Due In</div>
              <div className="text-base font-bold text-[#E8EDF7] mt-1">{entity.hours_to_inspection || 32.0} flight hours</div>
              <div className="text-[10px] text-[#22A06B] mt-0.5">Status: Within Safe Flight Envelope</div>
            </div>
          </div>
        )}

        {activeTab === 'history' && (
          <div className="space-y-2">
            <div className="text-[11px] text-[#7A869C]">State History (valid_from / valid_to)</div>
            <div className="p-2.5 rounded bg-[#0B1220] border border-[#24304A] space-y-1">
              <div className="text-[10px] text-[#7A869C]">2026-10-05 10:31:24 UTC</div>
              <div className="text-[#E8EDF7]">Telemetry ingestion merged from source maintenance-feed.</div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};
