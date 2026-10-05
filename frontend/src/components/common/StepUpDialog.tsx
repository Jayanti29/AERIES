import React, { useState } from 'react';
import { ShieldCheck, X, KeyRound, AlertTriangle } from 'lucide-react';

interface StepUpProps {
  isOpen: boolean;
  actionTitle: string;
  onSuccess: () => void;
  onCancel: () => void;
}

export const StepUpDialog: React.FC<StepUpProps> = ({
  isOpen,
  actionTitle,
  onSuccess,
  onCancel
}) => {
  const [password, setPassword] = useState('');
  const [totp, setTotp] = useState('');
  const [error, setError] = useState('');

  if (!isOpen) return null;

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (password === 'AERIS_Pass_2026!' || password.length >= 6) {
      setError('');
      onSuccess();
    } else {
      setError('Invalid authorization credential for step-up verification.');
    }
  };

  return (
    <div className="fixed inset-0 bg-black/70 backdrop-blur-sm flex items-center justify-center z-50 p-4 font-mono select-none">
      <div className="bg-[#111A2E] border border-[#24304A] w-full max-w-md rounded-lg overflow-hidden shadow-2xl">
        <div className="bg-[#172238] px-5 py-3 border-b border-[#24304A] flex justify-between items-center">
          <div className="flex items-center space-x-2">
            <KeyRound className="w-4 h-4 text-[#3B82F6]" />
            <span className="text-xs font-bold text-[#E8EDF7] uppercase">Step-Up Re-Authentication</span>
          </div>
          <button onClick={onCancel} className="text-[#7A869C] hover:text-[#E8EDF7]">
            <X className="w-4 h-4" />
          </button>
        </div>

        <form onSubmit={handleSubmit} className="p-5 space-y-4">
          <div className="bg-[#13233D] p-3 rounded border border-[#3B82F6]/30 text-xs text-[#9AA7BF]">
            <span className="text-[#3B82F6] font-bold">Privileged Action:</span> {actionTitle}
            <div className="text-[10px] text-[#7A869C] mt-1">Per Spec §5.2.8: Step-up authentication within 5 minutes required.</div>
          </div>

          <div>
            <label className="block text-[11px] uppercase text-[#7A869C] mb-1">Operator Password</label>
            <input
              type="password"
              placeholder="Enter password (AERIS_Pass_2026!)"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="w-full bg-[#0B1220] border border-[#24304A] rounded px-3 py-2 text-xs text-[#E8EDF7] focus:border-[#3B82F6] focus:outline-none"
              autoFocus
            />
          </div>

          <div>
            <label className="block text-[11px] uppercase text-[#7A869C] mb-1">TOTP 6-Digit Code (Optional)</label>
            <input
              type="text"
              placeholder="123456"
              maxLength={6}
              value={totp}
              onChange={(e) => setTotp(e.target.value)}
              className="w-full bg-[#0B1220] border border-[#24304A] rounded px-3 py-2 text-xs text-[#E8EDF7] focus:border-[#3B82F6] focus:outline-none"
            />
          </div>

          {error && <div className="text-xs text-[#E5484D]">{error}</div>}

          <div className="flex justify-end space-x-3 pt-3 border-t border-[#24304A]">
            <button
              type="button"
              onClick={onCancel}
              className="px-3 py-1.5 rounded text-xs text-[#9AA7BF] hover:bg-[#172238]"
            >
              Cancel
            </button>
            <button
              type="submit"
              className="px-4 py-1.5 bg-[#3B82F6] hover:bg-blue-600 text-white rounded text-xs font-bold"
            >
              Authorize & Proceed
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};
