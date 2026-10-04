# AERIS REST and WebSocket API Specification

## 1. Authentication & Session (`/api/auth`)
- `POST /api/auth/login`: Authenticate with username and password. Returns challenge or session.
- `POST /api/auth/mfa/verify`: Verify 6-digit TOTP code.
- `POST /api/auth/refresh`: Refresh JWT access token.
- `POST /api/auth/logout`: Invalidate session and clear cookies.
- `POST /api/auth/step-up`: Re-authenticate for sensitive operations.
- `GET /api/auth/me`: Get current user profile and permitted scopes.
- `POST /api/auth/switch-role`: Quick role switch for evaluation/demo.

## 2. Command & Operational State (`/api/command`)
- `GET /api/command/summary`: High-level system KPIs (System health %, missions at risk, data health).
- `GET /api/command/health`: 8 domain health scores with primary constraint.
- `GET /api/command/map-layers`: GeoJSON features for bases, aircraft, and airspace zones.
- `GET /api/command/insights`: Automated insights (hidden constraints, bottlenecks, SPOFs).
- `GET /api/command/timeline`: Projected operational state scrubber (+15, +30, +60, +120 mins).

## 3. Domain Dashboards
- `GET /api/craft/summary`: Fleet readiness and subsystem health.
- `GET /api/craft/fleet`: Virtualized fleet table.
- `GET /api/supply/summary`: Resource pressure and projected shortfalls.
- `GET /api/supply/resources`: Stock levels, demand, and bottlenecks.
- `GET /api/people/summary`: Personnel availability and workload.
- `GET /api/people/roster`: Masked personnel records.
- `POST /api/people/unmask`: Unmask identity (audited, step-up required).
- `GET /api/pilot/me`: Current pilot duty, schedule, and rest status.

## 4. Planning & Optimization
- `GET /api/missions`: Active missions and requirements.
- `POST /api/plans/generate`: Generate Plan A/B/C using CP-SAT optimizer.
- `POST /api/plans/tradeoffs`: Dynamic recalculation with custom slider weights.
- `POST /api/decisions/submit`: Submit plan to Decision Authority.
- `POST /api/decisions/review`: Accept, modify, or reject plan with cryptographic signature.

## 5. Resilience & Simulation
- `GET /api/resilience/graph`: Dependency network nodes and edges.
- `POST /api/resilience/cascade`: Run failure impact simulation along dependency edges.
- `POST /api/resilience/chaos`: Inject disruptions in Chaos Lab.
- `POST /api/resilience/stress`: Execute 1,000-scenario Monte Carlo resilience test.

## 6. Audit & Governance
- `GET /api/audit/logs`: Query tamper-evident audit records.
- `POST /api/audit/verify`: Verify SHA-256 hash chain integrity.
- `GET /api/models/registry`: Inspect machine learning models and SHAP explanations.
