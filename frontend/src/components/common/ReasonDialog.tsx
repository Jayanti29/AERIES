import React, { useState } from 'react';
import { AlertCircle, X } from 'lucide-react';

interface ReasonProps {
  isOpen: boolean;
  title: string;
  promptText: string;
  onConfirm: (reason: string) => void;
  onCancel: () => void;
}

export const ReasonDialog: React.FC<ReasonProps> = ({
  isOpen,
  title,
  promptText,
  onConfirm,
  onCancel
}) => {
  const [reason, setReason] = useState('');
  const [err, setErr] = useState('');

  if (!isOpen) return null;

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (reason.trim().length < 8) {
      setErr('A specific, documented operational justification (min 8 chars) is required for audit recording.');
      return;
    }
    setErr('');
    onConfirm(reason);
    setReason('');
  };

  return (
    <div className="fixed inset-0 bg-black/70 backdrop-blur-sm flex items-center justify-center z-50 p-4 font-mono select-none">
      <div className="bg-[#111A2E] border border-[#24304A] w-full max-w-md rounded-lg overflow-hidden shadow-2xl">
        <div className="bg-[#172238] px-5 py-3 border-b border-[#24304A] flex justify-between items-center">
          <div className="flex items-center space-x-2">
            <AlertCircle className="w-4 h-4 text-[#D99A1B]" />
            <span className="text-xs font-bold text-[#E8EDF7] uppercase">{title}</span>
          </div>
          <button onClick={onCancel} className="text-[#7A869C] hover:text-[#E8EDF7]">
            <X className="w-4 h-4" />
          </button>
        </div>

        <form onSubmit={handleSubmit} className="p-5 space-y-4">
          <p className="text-xs text-[#9AA7BF]">{promptText}</p>
          <div>
            <textarea
              rows={3}
              placeholder="State formal operational justification for audit ledger..."
              value={reason}
              onChange={(e) => setReason(e.target.value)}
              className="w-full bg-[#0B1220] border border-[#24304A] rounded p-2.5 text-xs text-[#E8EDF7] focus:border-[#3B82F6] focus:outline-none"
              autoFocus
            />
          </div>

          {err && <div className="text-xs text-[#E5484D]">{err}</div>}

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
              Confirm & Audit
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};
