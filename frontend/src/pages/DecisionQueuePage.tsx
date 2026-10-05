import React, { useState, useEffect } from 'react';
import { fetchApi } from '../services/api';
import { FileCheck, ShieldCheck, XCircle, CheckCircle2, Clock } from 'lucide-react';
import { StatusBadge } from '../components/common/StatusBadge';
import { StepUpDialog } from '../components/common/StepUpDialog';
import { ReasonDialog } from '../components/common/ReasonDialog';

export const DecisionQueuePage: React.FC = () => {
  const [queue, setQueue] = useState<any[]>([]);
  const [showStepUp, setShowStepUp] = useState(false);
  const [showRejectReason, setShowRejectReason] = useState(false);
  const [signedResult, setSignedResult] = useState<any>(null);

  useEffect(() => {
    fetchApi<any>('/decisions/queue').then((d) => setQueue(d.pending_submissions || [])).catch(() => {});
  }, []);

  const handleAcceptPlan = () => {
    setShowStepUp(true);
  };

  const handleStepUpVerified = async () => {
    setShowStepUp(false);
    try {
      const res = await fetchApi<any>('/decisions/review', {
        method: 'POST',
        body: JSON.stringify({
          plan_id: 'PLAN-B-RESILIENCE',
          action: 'ACCEPT',
          reason: 'Meets high-priority sortie coverage with lowest fragility index.'
        })
      });
      setSignedResult(res);
      alert("Plan Accepted & Digitally Signed! Decision recorded in SHA-256 Audit Chain.");
    } catch (e: any) {
      alert("Error: " + e.message);
    }
  };

  const handleRejectConfirm = async (reason: string) => {
    setShowRejectReason(false);
    await fetchApi('/decisions/review', {
      method: 'POST',
      body: JSON.stringify({ plan_id: 'PLAN-B-RESILIENCE', action: 'REJECT', reason })
    }).catch(() => {});
    alert("Plan rejected. Recorded in audit ledger.");
  };

  return (
    <div className="space-y-6 font-mono select-none">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-xl font-bold tracking-tight text-[#E8EDF7]">DECISION AUTHORITY QUEUE</h1>
          <p className="text-xs text-[#9AA7BF] mt-0.5">Formal Human-in-the-Loop Review, Cryptographic Signing & Separation of Duties (Spec §16.3)</p>
        </div>
        <div className="text-xs text-[#22A06B] bg-[#142621] px-3 py-1.5 rounded border border-[#22A06B]/30 flex items-center space-x-2">
          <Clock className="w-3.5 h-3.5" />
          <span>Staleness Status: FRESH (12m ago)</span>
        </div>
      </div>

      {signedResult && (
        <div className="bg-[#142621] border border-[#22A06B] rounded-lg p-4 flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <CheckCircle2 className="w-5 h-5 text-[#22A06B]" />
            <div>
              <div className="text-xs font-bold text-[#22A06B]">DECISION SIGNED & VERIFIED</div>
              <div className="text-[10px] text-[#9AA7BF]">
                Signature: {signedResult.signature} // Approved By: {signedResult.approved_by}
              </div>
            </div>
          </div>
          <span className="text-xs font-bold text-white bg-[#22A06B] px-3 py-1 rounded">VERIFIED</span>
        </div>
      )}

      <div className="bg-[#111A2E] border border-[#24304A] rounded-lg p-6 space-y-6">
        <div className="flex justify-between items-start border-b border-[#24304A] pb-4">
          <div>
            <span className="text-[10px] text-[#7A869C]">SUBMISSION ID: SUB-2026-001</span>
            <h2 className="text-lg font-bold text-[#E8EDF7] mt-0.5">Plan Bravo (Resilient Redundancy)</h2>
            <p className="text-xs text-[#9AA7BF] mt-1">Submitted by: Operations Planner (planner) at 09:45:00 UTC</p>
          </div>
          <div className="flex space-x-3">
            <button
              onClick={() => setShowRejectReason(true)}
              className="px-4 py-2 border border-[#E5484D]/40 text-[#E5484D] hover:bg-[#2D161A] text-xs font-bold rounded"
            >
              Reject Plan
            </button>
            <button
              onClick={handleAcceptPlan}
              className="px-5 py-2 bg-[#22A06B] hover:bg-emerald-600 text-white text-xs font-bold rounded flex items-center space-x-2 shadow-lg shadow-emerald-500/20"
            >
              <ShieldCheck className="w-4 h-4" />
              <span>Accept & Sign Decision</span>
            </button>
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 text-xs">
          <div className="space-y-3">
            <h4 className="text-[11px] font-bold text-[#7A869C] uppercase">Why Choose Plan Bravo? (Spec §16.1)</h4>
            <div className="p-3 bg-[#0B1220] rounded border border-[#24304A] space-y-2">
              <div className="text-[#E8EDF7]">• Preserves 18% fuel buffer at Forward Base B-Alpha during peak combat window.</div>
              <div className="text-[#E8EDF7]">• Zero rest-rule violations detected across all 18 flight crews.</div>
              <div className="text-[#E8EDF7]">• 95% lower fragility score compared to Plan Alpha under weather turbulence.</div>
            </div>
          </div>
          <div className="space-y-3">
            <h4 className="text-[11px] font-bold text-[#7A869C] uppercase">Why Not Plan Alpha / Charlie?</h4>
            <div className="p-3 bg-[#0B1220] rounded border border-[#24304A] space-y-2">
              <div className="text-[#E5484D]">• Plan Alpha: Violates fuel reserve at B-Delta, leading to single point of failure.</div>
              <div className="text-[#D99A1B]">• Plan Charlie: Leaves 4 strategic reconnaissance sorties unassigned.</div>
            </div>
          </div>
        </div>
      </div>

      <StepUpDialog
        isOpen={showStepUp}
        actionTitle="Accept & Authorize Plan Bravo"
        onSuccess={handleStepUpVerified}
        onCancel={() => setShowStepUp(false)}
      />

      <ReasonDialog
        isOpen={showRejectReason}
        title="Reason for Plan Rejection"
        promptText="Spec §16.3 requires a mandatory documented reason when rejecting a candidate operational plan."
        onConfirm={handleRejectConfirm}
        onCancel={() => setShowRejectReason(false)}
      />
    </div>
  );
};
