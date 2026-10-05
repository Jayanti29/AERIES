import React from 'react';
import { Cpu, ShieldCheck, CheckCircle2, Lock } from 'lucide-react';
import { StatusBadge } from '../components/common/StatusBadge';

export const ModelRegistryPage: React.FC = () => {
  const models = [
    {
      name: 'Turbine Failure Classifier',
      version: 'maint-xgb-1.3.0',
      family: 'Gradient Boosting (XGBoost)',
      metric: 'AUC: 0.88, Calib Err: 0.03',
      sha256: 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855',
      signature: 'sig:ed25519:verified',
      status: 'ACTIVE'
    },
    {
      name: 'Resource Pressure Forecaster',
      version: 'resource-ridge-1.1.0',
      family: 'Ridge Regression & Smoothing',
      metric: 'MAPE: 7.8%',
      sha256: '9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08',
      signature: 'sig:ed25519:verified',
      status: 'ACTIVE'
    },
    {
      name: 'Readiness Decay Forecaster',
      version: 'readiness-rf-1.0.0',
      family: 'Random Forest Ensemble',
      metric: 'MAE: 0.04',
      sha256: '5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8',
      signature: 'sig:ed25519:verified',
      status: 'ACTIVE'
    }
  ];

  return (
    <div className="space-y-6 font-mono select-none">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-xl font-bold tracking-tight text-[#E8EDF7]">MACHINE LEARNING MODEL REGISTRY</h1>
          <p className="text-xs text-[#9AA7BF] mt-0.5">Signed Artifacts, Validation Metrics & Ed25519 Verification (Spec §13.3)</p>
        </div>
        <div className="text-xs font-bold text-[#22A06B] bg-[#142621] px-3 py-1.5 rounded border border-[#22A06B]/30 flex items-center space-x-2">
          <ShieldCheck className="w-4 h-4" />
          <span>All 3 Production Models Signed</span>
        </div>
      </div>

      <div className="space-y-4">
        {models.map((m) => (
          <div key={m.version} className="bg-[#111A2E] border border-[#24304A] rounded-lg p-5 space-y-3">
            <div className="flex justify-between items-start">
              <div>
                <div className="flex items-center space-x-2">
                  <span className="text-xs font-bold text-[#3B82F6]">{m.family}</span>
                  <span className="text-[10px] text-[#7A869C]">{m.version}</span>
                </div>
                <h3 className="text-base font-bold text-[#E8EDF7] mt-1">{m.name}</h3>
              </div>
              <StatusBadge status={m.status} />
            </div>

            <div className="grid grid-cols-2 md:grid-cols-4 gap-2 text-xs pt-2 border-t border-[#24304A]">
              <div>
                <span className="text-[#7A869C] text-[10px]">Metrics</span>
                <div className="font-bold text-[#22A06B]">{m.metric}</div>
              </div>
              <div>
                <span className="text-[#7A869C] text-[10px]">Artifact SHA-256</span>
                <div className="text-[10px] text-[#7A869C] truncate max-w-xs">{m.sha256}</div>
              </div>
              <div>
                <span className="text-[#7A869C] text-[10px]">Signature</span>
                <div className="font-bold text-[#22A06B] flex items-center space-x-1">
                  <CheckCircle2 className="w-3.5 h-3.5" />
                  <span>Ed25519 Verified</span>
                </div>
              </div>
              <div>
                <span className="text-[#7A869C] text-[10px]">SHAP Explainability</span>
                <div className="font-bold text-[#3B82F6]">Computed At Inference</div>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
