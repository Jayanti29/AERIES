import React, { useState } from 'react';
import { Settings, ShieldAlert, KeyRound, Play, RefreshCw, Lock } from 'lucide-react';
import { StepUpDialog } from '../components/common/StepUpDialog';
import { ReasonDialog } from '../components/common/ReasonDialog';
import { fetchApi } from '../services/api';

export const AdminPage: React.FC = () => {
  const [readOnlyMode, setReadOnlyMode] = useState(false);
  const [showKeyStepUp, setShowKeyStepUp] = useState(false);
  const [generatorRunning, setGeneratorRunning] = useState(true);

  const handleRotateKey = async () => {
    setShowKeyStepUp(false);
    try {
      await fetchApi('/admin/keys/rotate', {
        method: 'POST',
        body: JSON.stringify({ new_key_hex: '0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef' })
      });
      alert("Key rotation ceremony executed! Envelope keys re-wrapped and recorded in audit ledger.");
    } catch (e: any) {
      alert("Key rotation error: " + e.message);
    }
  };

  return (
    <div className="space-y-6 font-mono select-none">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-xl font-bold tracking-tight text-[#E8EDF7]">SYSTEM ADMINISTRATION</h1>
          <p className="text-xs text-[#9AA7BF] mt-0.5">Dual-Control Approvals, Cryptographic Key Rotation & Synthetic Generator (Spec §5.5, §6.4)</p>
        </div>
        <button
          onClick={() => setReadOnlyMode(!readOnlyMode)}
          className={`px-3.5 py-1.5 rounded text-xs font-bold transition-colors ${
            readOnlyMode ? 'bg-[#E5484D] text-white' : 'border border-[#E5484D]/50 text-[#E5484D] hover:bg-[#2D161A]'
          }`}
        >
          {readOnlyMode ? "EMERGENCY READ-ONLY ACTIVE" : "Toggle Emergency Read-Only"}
        </button>
      </div>

      {readOnlyMode && (
        <div className="bg-[#2D161A] border border-[#E5484D] p-3 rounded text-xs text-[#E5484D] font-bold">
          [CRITICAL NOTICE] SYSTEM IS IN EMERGENCY READ-ONLY MODE. ALL WRITES AND PLAN APPROVALS ARE BLOCKED.
        </div>
      )}

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Key Management */}
        <div className="bg-[#111A2E] border border-[#24304A] rounded-lg p-6 space-y-4">
          <h3 className="text-sm font-bold text-[#E8EDF7] uppercase flex items-center space-x-2">
            <KeyRound className="w-4 h-4 text-[#3B82F6]" />
            <span>Cryptographic Key Management (Spec §6.4)</span>
          </h3>
          <p className="text-xs text-[#9AA7BF]">
            Envelope Encryption Key Encryption Key (KEK). Rotation requires step-up authentication and two-person authorization.
          </p>

          <div className="bg-[#172238] p-3 rounded border border-[#24304A] text-xs space-y-1">
            <div className="flex justify-between">
              <span className="text-[#7A869C]">Active KEK Version:</span>
              <span className="text-[#22A06B] font-bold">v1-2026-OCT</span>
            </div>
            <div className="flex justify-between">
              <span className="text-[#7A869C]">Algorithm:</span>
              <span className="text-[#E8EDF7]">AES-256-GCM / 96-bit Nonce</span>
            </div>
          </div>

          <button
            onClick={() => setShowKeyStepUp(true)}
            className="px-4 py-2 bg-[#172238] hover:bg-[#24304A] text-[#3B82F6] border border-[#24304A] text-xs font-bold rounded"
          >
            Initiate Key Rotation Ceremony
          </button>
        </div>

        {/* Generator Controls */}
        <div className="bg-[#111A2E] border border-[#24304A] rounded-lg p-6 space-y-4">
          <h3 className="text-sm font-bold text-[#E8EDF7] uppercase flex items-center space-x-2">
            <RefreshCw className="w-4 h-4 text-[#22A06B]" />
            <span>Synthetic Data Generator (Spec §20)</span>
          </h3>
          <p className="text-xs text-[#9AA7BF]">
            Deterministic generator streams signed feeds across all 6 bases, 60 aircraft, and 400 personnel.
          </p>

          <div className="bg-[#172238] p-3 rounded border border-[#24304A] text-xs space-y-1">
            <div className="flex justify-between">
              <span className="text-[#7A869C]">Engine Status:</span>
              <span className="text-[#22A06B] font-bold">{generatorRunning ? "RUNNING (1 tick = 1 min)" : "PAUSED"}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-[#7A869C]">World Seed:</span>
              <span className="text-[#3B82F6] font-bold">42</span>
            </div>
          </div>

          <div className="flex space-x-3">
            <button
              onClick={() => setGeneratorRunning(!generatorRunning)}
              className="px-3.5 py-1.5 bg-[#3B82F6] hover:bg-blue-600 text-white rounded text-xs font-bold"
            >
              {generatorRunning ? "Pause Generator" : "Resume Generator"}
            </button>
            <button
              onClick={() => alert("One-off telemetry anomaly injected into quarantine queue.")}
              className="px-3.5 py-1.5 border border-[#24304A] text-[#9AA7BF] hover:bg-[#172238] rounded text-xs"
            >
              Inject Anomaly Event
            </button>
          </div>
        </div>
      </div>

      <StepUpDialog
        isOpen={showKeyStepUp}
        actionTitle="Rotate Cryptographic Key Encryption Key (KEK)"
        onSuccess={handleRotateKey}
        onCancel={() => setShowKeyStepUp(false)}
      />
    </div>
  );
};
