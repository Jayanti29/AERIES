export type Role =
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
