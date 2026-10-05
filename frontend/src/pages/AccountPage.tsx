import React from 'react';
import { User, Shield, KeyRound, LogOut } from 'lucide-react';
import { useAuthStore } from '../store/authStore';

export const AccountPage: React.FC = () => {
  const { user, clearAuth } = useAuthStore();

  return (
    <div className="space-y-6 max-w-3xl mx-auto font-mono select-none">
      <div>
        <h1 className="text-xl font-bold tracking-tight text-[#E8EDF7]">ACCOUNT SECURITY & IDENTITY</h1>
        <p className="text-xs text-[#9AA7BF] mt-0.5">MFA Credential Tokens, Active Sessions & Credentials (Spec §5)</p>
      </div>

      <div className="bg-[#111A2E] border border-[#24304A] rounded-lg p-6 space-y-6">
        <div className="flex justify-between items-center border-b border-[#24304A] pb-4">
          <div>
            <span className="text-[10px] text-[#7A869C]">AUTHENTICATED OPERATOR</span>
            <div className="text-xl font-bold text-[#E8EDF7] mt-0.5">{user?.username || 'planner'}</div>
            <div className="text-xs text-[#3B82F6] font-semibold">{user?.role} // CALLSIGN: {user?.callsign}</div>
          </div>
          <button
            onClick={() => clearAuth()}
            className="px-3 py-1.5 border border-[#E5484D]/40 text-[#E5484D] hover:bg-[#2D161A] text-xs font-bold rounded flex items-center space-x-1.5"
          >
            <LogOut className="w-3.5 h-3.5" />
            <span>Sign Out Everywhere</span>
          </button>
        </div>

        <div className="space-y-3">
          <h4 className="text-xs font-bold text-[#7A869C] uppercase">Multi-Factor Authentication (MFA)</h4>
          <div className="p-4 bg-[#172238] rounded border border-[#24304A] flex justify-between items-center text-xs">
            <div>
              <div className="text-[#E8EDF7] font-bold">RFC 6238 TOTP Authenticator</div>
              <div className="text-[11px] text-[#9AA7BF]">Enrolled via hardware/app seed: JBSWY3DPEHPK3PXP</div>
            </div>
            <span className="text-[#22A06B] font-bold bg-[#142621] px-2 py-0.5 rounded border border-[#22A06B]/30">ACTIVE</span>
          </div>
        </div>

        <div className="space-y-3">
          <h4 className="text-xs font-bold text-[#7A869C] uppercase">Active Operator Sessions</h4>
          <div className="p-3 bg-[#0B1220] rounded border border-[#24304A] flex justify-between items-center text-xs">
            <div>
              <div className="text-[#E8EDF7]">Current Session (Browser)</div>
              <div className="text-[10px] text-[#7A869C]">IP: 127.0.0.1 // Expires on 15m inactivity // Token: HttpOnly</div>
            </div>
            <span className="text-[#3B82F6] font-bold text-[11px]">ACTIVE NOW</span>
          </div>
        </div>
      </div>
    </div>
  );
};
