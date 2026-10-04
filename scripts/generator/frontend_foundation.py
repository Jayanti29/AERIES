# Frontend Foundation and Shared Components (Part 1) for AERIS

def get_frontend_foundation():
    files = {}

    files['frontend/package.json'] = """{
  "name": "aeris-frontend",
  "private": true,
  "version": "1.0.0",
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "tsc && vite build",
    "preview": "vite preview"
  },
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "react-router-dom": "^6.22.3",
    "zustand": "^4.5.2",
    "lucide-react": "^0.358.0",
    "clsx": "^2.1.0",
    "tailwind-merge": "^2.2.1"
  },
  "devDependencies": {
    "@types/react": "^18.2.66",
    "@types/react-dom": "^18.2.22",
    "@vitejs/plugin-react": "^4.2.1",
    "autoprefixer": "^10.4.18",
    "postcss": "^8.4.35",
    "tailwindcss": "^3.4.1",
    "typescript": "^5.2.2",
    "vite": "^5.1.6"
  }
}
"""

    files['frontend/tsconfig.json'] = """{
  "compilerOptions": {
    "target": "ES2020",
    "useDefineForClassFields": true,
    "lib": ["ES2020", "DOM", "DOM.Iterable"],
    "module": "ESNext",
    "skipLibCheck": true,
    "moduleResolution": "bundler",
    "allowImportingTsExtensions": true,
    "resolveJsonModule": true,
    "isolatedModules": true,
    "noEmit": true,
    "jsx": "react-jsx",
    "strict": true,
    "noUnusedLocals": false,
    "noUnusedParameters": false,
    "noFallthroughCasesInSwitch": true
  },
  "include": ["src"]
}
"""

    files['frontend/vite.config.ts'] = """import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  server: {
    port: 3000,
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true
      },
      '/ws': {
        target: 'ws://localhost:8000',
        ws: true
      }
    }
  }
});
"""

    files['frontend/tailwind.config.js'] = """/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        aeris: {
          bg: '#0B1220',
          surface: '#111A2E',
          raised: '#172238',
          border: '#24304A',
          primary: '#E8EDF7',
          secondary: '#9AA7BF',
          accent: '#3B82F6',
          healthy: '#22A06B',
          warning: '#D99A1B',
          critical: '#E5484D',
          info: '#4C9AFF',
          unknown: '#7A869C'
        }
      },
      fontFamily: {
        sans: ['Inter', 'sans-serif'],
        mono: ['JetBrains Mono', 'monospace'],
      }
    },
  },
  plugins: [],
}
"""

    files['frontend/postcss.config.js'] = """export default {
  plugins: {
    tailwindcss: {},
    autoprefixer: {},
  },
}
"""

    files['frontend/src/tokens/colors.ts'] = """export const AERIS_TOKENS = {
  dark: {
    background: '#0B1220',
    surface: '#111A2E',
    surfaceRaised: '#172238',
    border: '#24304A',
    textPrimary: '#E8EDF7',
    textSecondary: '#9AA7BF',
    accent: '#3B82F6',
    healthy: '#22A06B',
    warning: '#D99A1B',
    critical: '#E5484D',
    info: '#4C9AFF',
    unknown: '#7A869C'
  },
  light: {
    background: '#F4F6FA',
    surface: '#FFFFFF',
    surfaceRaised: '#FFFFFF',
    border: '#D5DBE6',
    textPrimary: '#0F1A2B',
    textSecondary: '#4A586F',
    accent: '#1D4ED8',
    healthy: '#14804F',
    warning: '#A56A00',
    critical: '#C2262B',
    info: '#1F6FD1',
    unknown: '#6B778C'
  }
};
"""

    files['frontend/src/types/index.ts'] = """export type Role =
  | 'Administrator'
  | 'Operations Planner'
  | 'Decision Authority'
  | 'Analyst'
  | 'Auditor'
  | 'Pilot'
  | 'Craft Officer'
  | 'Supply Officer'
  | 'Personnel Officer';

export interface User {
  id: string;
  username: string;
  role: Role;
  callsign: string;
}

export interface DomainHealth {
  domain: string;
  score: number;
  status: 'HEALTHY' | 'NOMINAL' | 'WARNING' | 'CRITICAL';
  details: string;
}

export interface Aircraft {
  code: string;
  base_code: string;
  platform_type: string;
  status: string;
  readiness_score: number;
  flight_hours: number;
  hours_to_inspection: number;
  current_mission: string | null;
  predicted_constraint_prob: number;
}

export interface Resource {
  id: string;
  code: string;
  name: string;
  base_code: string;
  unit: string;
  available_qty: number;
  demand_qty: number;
  projected_shortfall: number;
  reserve_threshold: number;
  pressure_level: string;
}

export interface Personnel {
  code: string;
  callsign: string;
  masked_name: string;
  team: string;
  role: string;
  status: string;
  workload_pct: number;
  duty_hours_today: number;
  qualifications: string[];
}

export interface PlanDNA {
  coverage: number;
  efficiency: number;
  resilience: number;
  flexibility: number;
  speed: number;
  resource_reserve: number;
}

export interface Plan {
  id: string;
  name: string;
  description: string;
  dna: PlanDNA;
  metrics: {
    missions_assigned: number;
    unmet_demand: number;
    fuel_burn_gal: number;
    crew_rest_violations: number;
    fragility_score: number;
  };
  status: string;
}
"""

    files['frontend/src/store/authStore.ts'] = """import { create } from 'zustand';
import { User, Role } from '../types';

interface AuthState {
  user: User | null;
  token: string | null;
  isAuthenticated: boolean;
  theme: 'dark' | 'light';
  setAuth: (user: User, token: string) => void;
  clearAuth: () => void;
  toggleTheme: () => void;
  switchRole: (role: Role) => void;
}

export const useAuthStore = create<AuthState>((set) => ({
  user: {
    id: 'usr-planner',
    username: 'planner',
    role: 'Operations Planner',
    callsign: 'STRATEGIST'
  },
  token: 'mock-initial-token',
  isAuthenticated: true,
  theme: 'dark',
  setAuth: (user, token) => set({ user, token, isAuthenticated: true }),
  clearAuth: () => set({ user: null, token: null, isAuthenticated: false }),
  toggleTheme: () => set((state) => ({ theme: state.theme === 'dark' ? 'light' : 'dark' })),
  switchRole: (role: Role) => set((state) => ({
    user: state.user ? { ...state.user, role, username: role.toLowerCase().replace(/\\s+/g, '_') } : null
  }))
}));
"""

    files['frontend/src/services/api.ts'] = """// AERIS Centralized API Client

const BASE_URL = '/api';

export async function fetchApi<T>(endpoint: string, options: RequestInit = {}): Promise<T> {
  const token = localStorage.getItem('aeris_token');
  const headers = {
    'Content-Type': 'application/json',
    ...(token ? { 'Authorization': `Bearer ${token}` } : {}),
    ...options.headers,
  };

  const response = await fetch(`${BASE_URL}${endpoint}`, {
    ...options,
    headers,
  });

  if (!response.ok) {
    const errorData = await response.json().catch(() => ({ detail: response.statusText }));
    throw new Error(errorData.detail || `HTTP Error ${response.status}`);
  }

  return response.json();
}
"""

    files['frontend/src/components/common/HandlingBanner.tsx'] = """import React from 'react';
import { ShieldAlert } from 'lucide-react';

export const HandlingBanner: React.FC = () => {
  return (
    <div className="w-full bg-[#172238] border-b border-[#24304A] text-[#9AA7BF] px-4 py-1 text-xs font-mono flex items-center justify-between tracking-wider select-none z-50">
      <div className="flex items-center space-x-2">
        <ShieldAlert className="w-3.5 h-3.5 text-[#D99A1B]" />
        <span className="font-semibold text-[#D99A1B]">RESTRICTED SIMULATION // UNCLASSIFIED</span>
      </div>
      <div className="bg-[#111A2E] px-3 py-0.5 rounded border border-[#24304A] text-[#E8EDF7] font-bold">
        SYNTHETIC DATA - SIMULATION
      </div>
      <div className="text-[11px] text-[#7A869C]">
        SEC-ENCLAVE: AERIS-GOV-01
      </div>
    </div>
  );
};
"""

    files['frontend/src/components/common/StatusBadge.tsx'] = """import React from 'react';
import { CheckCircle2, AlertTriangle, XCircle, Info, HelpCircle } from 'lucide-react';

interface StatusBadgeProps {
  status: 'HEALTHY' | 'NOMINAL' | 'WARNING' | 'CRITICAL' | 'READY' | 'MAINTENANCE' | 'CLEAR' | 'AT_RISK' | string;
  label?: string;
  size?: 'sm' | 'md';
}

export const StatusBadge: React.FC<StatusBadgeProps> = ({ status, label, size = 'sm' }) => {
  const s = status.toUpperCase();
  let bg = 'bg-[#172238] border-[#24304A] text-[#7A869C]';
  let Icon = HelpCircle;

  if (['HEALTHY', 'NOMINAL', 'READY', 'CLEAR', 'OPERATIONAL'].includes(s)) {
    bg = 'bg-[#142621] border-[#22A06B]/30 text-[#22A06B]';
    Icon = CheckCircle2;
  } else if (['WARNING', 'ELEVATED', 'AT_RISK'].includes(s)) {
    bg = 'bg-[#2A2314] border-[#D99A1B]/30 text-[#D99A1B]';
    Icon = AlertTriangle;
  } else if (['CRITICAL', 'GROUNDED', 'FAILED', 'OVERDUE'].includes(s)) {
    bg = 'bg-[#2D161A] border-[#E5484D]/30 text-[#E5484D]';
    Icon = XCircle;
  } else if (['INFO', 'UPCOMING', 'ACTIVE'].includes(s)) {
    bg = 'bg-[#13233D] border-[#4C9AFF]/30 text-[#4C9AFF]';
    Icon = Info;
  }

  const iconSize = size === 'sm' ? 'w-3 h-3' : 'w-4 h-4';
  const textSize = size === 'sm' ? 'text-xs' : 'text-sm';

  return (
    <span className={`inline-flex items-center space-x-1.5 px-2 py-0.5 rounded font-mono font-medium border ${bg} ${textSize}`}>
      <Icon className={iconSize} />
      <span>{label || status}</span>
    </span>
  );
};
"""

    files['frontend/src/components/common/KpiCard.tsx'] = """import React from 'react';
import { LucideIcon } from 'lucide-react';
import { StatusBadge } from './StatusBadge';

interface KpiCardProps {
  title: string;
  value: string | number;
  subValue?: string;
  status?: string;
  icon?: LucideIcon;
  provenanceSource?: string;
}

export const KpiCard: React.FC<KpiCardProps> = ({
  title,
  value,
  subValue,
  status,
  icon: Icon,
  provenanceSource = "Live Telemetry"
}) => {
  return (
    <div className="bg-[#111A2E] border border-[#24304A] rounded-lg p-4 relative overflow-hidden group hover:border-[#3B82F6]/40 transition-colors">
      <div className="flex items-center justify-between mb-2">
        <span className="text-xs font-mono uppercase tracking-wider text-[#9AA7BF]">{title}</span>
        {Icon && <Icon className="w-4 h-4 text-[#7A869C] group-hover:text-[#3B82F6]" />}
      </div>
      <div className="flex items-baseline space-x-2">
        <span className="text-2xl font-bold font-mono text-[#E8EDF7] tracking-tight">{value}</span>
        {subValue && <span className="text-xs text-[#9AA7BF] font-mono">{subValue}</span>}
      </div>
      <div className="mt-3 flex items-center justify-between pt-2 border-t border-[#24304A]/60">
        {status ? <StatusBadge status={status} /> : <div />}
        <span className="text-[10px] text-[#7A869C] font-mono" title={`Verified feed: ${provenanceSource}`}>
          src: {provenanceSource}
        </span>
      </div>
    </div>
  );
};
"""

    files['frontend/src/components/common/HealthBar.tsx'] = """import React from 'react';

interface HealthBarProps {
  label: string;
  score: number;
  status: string;
  details?: string;
  isPrimaryConstraint?: boolean;
}

export const HealthBar: React.FC<HealthBarProps> = ({
  label,
  score,
  status,
  details,
  isPrimaryConstraint = false,
}) => {
  let color = 'bg-[#22A06B]';
  if (score < 80) color = 'bg-[#E5484D]';
  else if (score < 85) color = 'bg-[#D99A1B]';

  return (
    <div className={`p-2.5 rounded border transition-all ${
      isPrimaryConstraint ? 'bg-[#2D161A]/40 border-[#E5484D] ring-1 ring-[#E5484D]/40' : 'bg-[#172238]/60 border-[#24304A]'
    }`}>
      <div className="flex justify-between items-center mb-1 text-xs">
        <div className="flex items-center space-x-2">
          <span className="font-semibold text-[#E8EDF7]">{label}</span>
          {isPrimaryConstraint && (
            <span className="px-1.5 py-0.2 bg-[#E5484D] text-white text-[10px] font-bold rounded uppercase">
              Primary Constraint
            </span>
          )}
        </div>
        <span className="font-mono font-bold text-[#E8EDF7]">{score}%</span>
      </div>
      <div className="w-full bg-[#0B1220] rounded-full h-1.5 overflow-hidden">
        <div className={`h-full ${color}`} style={{ width: `${score}%` }}></div>
      </div>
      {details && <div className="text-[11px] text-[#9AA7BF] mt-1 font-mono truncate">{details}</div>}
    </div>
  );
};
"""

    files['frontend/src/components/common/PlanDNA.tsx'] = """import React from 'react';
import { PlanDNA as PlanDNAType } from '../../types';

interface PlanDNAProps {
  dna: PlanDNAType;
  compact?: boolean;
}

export const PlanDNA: React.FC<PlanDNAProps> = ({ dna, compact = false }) => {
  const metrics = [
    { label: 'Coverage', value: dna.coverage, color: 'bg-blue-500' },
    { label: 'Efficiency', value: dna.efficiency, color: 'bg-emerald-500' },
    { label: 'Resilience', value: dna.resilience, color: 'bg-indigo-500' },
    { label: 'Flexibility', value: dna.flexibility, color: 'bg-amber-500' },
    { label: 'Speed', value: dna.speed, color: 'bg-cyan-500' },
    { label: 'Reserve', value: dna.resource_reserve, color: 'bg-purple-500' }
  ];

  return (
    <div className="space-y-1.5 font-mono">
      {metrics.map((m) => (
        <div key={m.label} className="text-xs">
          <div className="flex justify-between text-[#9AA7BF] mb-0.5 text-[11px]">
            <span>{m.label}</span>
            <span className="text-[#E8EDF7] font-semibold">{m.value}%</span>
          </div>
          <div className="w-full bg-[#0B1220] rounded-full h-1.5 overflow-hidden">
            <div className={`h-full ${m.color}`} style={{ width: `${m.value}%` }} />
          </div>
        </div>
      ))}
    </div>
  );
};
"""

    return files

print("frontend_foundation.py loaded")
