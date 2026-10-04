import React, { useState, useEffect } from 'react';
import { fetchApi } from '../services/api';
import { StatusBadge } from '../components/common/StatusBadge';
import { Shield, Clock, Award, Bell } from 'lucide-react';

export const PilotPages: React.FC = () => {
  const [duty, setDuty] = useState<any>(null);

  useEffect(() => {
    fetchApi('/pilot/me').then(setDuty).catch(() => {});
  }, []);

  return (
    <div className="space-y-6 max-w-4xl mx-auto">
      <div>
        <h1 className="text-xl font-bold font-mono tracking-tight text-[#E8EDF7]">PILOT DUTY & READINESS</h1>
        <p className="text-xs text-[#9AA7BF] font-mono mt-0.5">Aircrew Individual Posture (Enforced state:read_own)</p>
      </div>

      <div className="bg-[#111A2E] border border-[#24304A] rounded-lg p-6 space-y-6">
        <div className="flex justify-between items-center border-b border-[#24304A] pb-4">
          <div>
            <span className="text-xs font-mono text-[#7A869C]">CALLSIGN</span>
            <div className="text-2xl font-bold font-mono text-[#3B82F6]">{duty?.callsign || 'MAVERICK'}</div>
            <div className="text-xs text-[#9AA7BF] font-mono">{duty?.role || 'Lead Interceptor Pilot'}</div>
          </div>
          <StatusBadge status="READY" label="READY FOR SORTIE" size="md" />
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 font-mono text-xs">
          <div className="bg-[#172238] p-4 rounded border border-[#24304A]">
            <div className="text-[#7A869C] mb-1">DUTY HOURS TODAY</div>
            <div className="text-xl font-bold text-[#E8EDF7]">{duty?.duty_hours_today || 3.5} / 8.0 hrs</div>
            <div className="w-full bg-[#0B1220] rounded-full h-1.5 mt-2">
              <div className="h-full bg-[#22A06B]" style={{ width: '43%' }}></div>
            </div>
          </div>
          <div className="bg-[#172238] p-4 rounded border border-[#24304A]">
            <div className="text-[#7A869C] mb-1">REST ACCUMULATED</div>
            <div className="text-xl font-bold text-[#22A06B]">{duty?.rest_hours_accumulated || 14.5} hrs</div>
            <div className="text-[10px] text-[#9AA7BF] mt-1">Rule threshold: 12.0h min</div>
          </div>
          <div className="bg-[#172238] p-4 rounded border border-[#24304A]">
            <div className="text-[#7A869C] mb-1">ASSIGNED SORTIE</div>
            <div className="text-xl font-bold text-[#3B82F6]">{duty?.current_assignment?.mission_code || 'M001'}</div>
            <div className="text-[10px] text-[#9AA7BF] mt-1">{duty?.current_assignment?.aircraft_code || 'A01 (Fighter)'}</div>
          </div>
        </div>

        <div className="bg-[#172238]/40 border border-[#24304A] rounded p-4">
          <h4 className="text-xs font-mono font-bold text-[#E8EDF7] uppercase mb-2 flex items-center space-x-2">
            <Bell className="w-4 h-4 text-[#3B82F6]" />
            <span>Assignment Notifications</span>
          </h4>
          <div className="text-xs font-mono text-[#9AA7BF] space-y-1">
            <div>• [10:15 UTC] Sortie M001 takeoff window confirmed for 11:00 UTC at B-Alpha.</div>
            <div>• [08:30 UTC] Pre-flight telemetry and weapons verification completed.</div>
          </div>
        </div>
      </div>
    </div>
  );
};
