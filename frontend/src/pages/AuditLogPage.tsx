import React, { useState, useEffect } from 'react';
import { fetchApi } from '../services/api';
import { StatusBadge } from '../components/common/StatusBadge';
import { ShieldCheck, Lock, FileText, CheckCircle2 } from 'lucide-react';

export const AuditLogPage: React.FC = () => {
  const [logs, setLogs] = useState<any[]>([]);
  const [verification, setVerification] = useState<any>(null);

  useEffect(() => {
    fetchApi<any[]>('/audit/logs').then(setLogs).catch(() => {});
  }, []);

  const handleVerify = async () => {
    try {
      const res = await fetchApi<any>('/audit/verify', { method: 'POST' });
      setVerification(res);
    } catch (e: any) {
      alert("Verification error: " + e.message);
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-xl font-bold font-mono tracking-tight text-[#E8EDF7]">CRYPTOGRAPHIC AUDIT LEDGER</h1>
          <p className="text-xs text-[#9AA7BF] font-mono mt-0.5">SHA-256 Hash Chained Tamper-Evident Ledger</p>
        </div>
        <button
          onClick={handleVerify}
          className="px-4 py-2 bg-[#22A06B] hover:bg-emerald-600 text-white font-mono text-xs font-bold rounded flex items-center space-x-2 shadow-lg shadow-emerald-600/20"
        >
          <ShieldCheck className="w-4 h-4" />
          <span>Verify Hash Chain Integrity</span>
        </button>
      </div>

      {verification && (
        <div className={`p-4 rounded border font-mono text-xs flex items-center space-x-3 ${
          verification.valid
            ? 'bg-[#142621] border-[#22A06B]/50 text-[#22A06B]'
            : 'bg-[#2D161A] border-[#E5484D]/50 text-[#E5484D]'
        }`}>
          <CheckCircle2 className="w-5 h-5 shrink-0" />
          <div>
            <div className="font-bold">{verification.valid ? "CHAIN INTEGRITY VERIFIED" : "TAMPERING DETECTED"}</div>
            <div className="text-[11px] opacity-80">{verification.reason} // Head: {verification.chain_head?.substring(0, 24)}...</div>
          </div>
        </div>
      )}

      <div className="bg-[#111A2E] border border-[#24304A] rounded-lg p-5">
        <div className="max-h-96 overflow-y-auto border border-[#24304A] rounded font-mono text-xs">
          <table className="w-full text-left">
            <thead className="bg-[#172238] text-[#9AA7BF] sticky top-0">
              <tr>
                <th className="p-3">#</th>
                <th className="p-3">Timestamp (UTC)</th>
                <th className="p-3">Actor</th>
                <th className="p-3">Action</th>
                <th className="p-3">Resource</th>
                <th className="p-3">Block Hash (SHA-256)</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-[#24304A]">
              {logs.map((log) => (
                <tr key={log.index} className="hover:bg-[#172238]/40">
                  <td className="p-3 text-[#7A869C]">{log.index}</td>
                  <td className="p-3 text-[#9AA7BF]">{log.timestamp.replace('T', ' ').substring(0, 19)}</td>
                  <td className="p-3 font-semibold text-[#E8EDF7]">{log.actor_role}</td>
                  <td className="p-3 text-[#3B82F6]">{log.action}</td>
                  <td className="p-3 text-[#9AA7BF]">{log.resource_type}:{log.resource_id}</td>
                  <td className="p-3 text-[10px] text-[#7A869C] truncate max-w-xs">{log.current_hash}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};
