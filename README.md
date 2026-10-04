# AERIS — Adaptive Air Operations & Resource Intelligence System

> **HANDLING NOTICE**: `SYNTHETIC DATA - SIMULATION`  
> All airframes, personnel names, callsigns, coordinate bases, and resource parameters are purely synthetic and generated for operational research and simulation testing. No classified or real-world operational data is utilized.

AERIS is a secure, role-based operational decision-support and simulation web platform engineered for high-consequence operational air command and resource logistics.

---

## 1. System Overview & Technology Stack

- **Frontend**: React 18, TypeScript (strict), Vite, Tailwind CSS, Radix UI, TanStack Table & Query, Zustand, MapLibre GL, Apache ECharts, Cytoscape.js.
- **Backend**: Python 3.11/3.13, FastAPI, Pydantic v2, SQLAlchemy 2, Alembic, Redis 7, Celery.
- **Optimization & ML**: Google OR-Tools CP-SAT multi-objective solver, NetworkX dependency graphs, scikit-learn, XGBoost, SHAP.
- **Security & Privacy**: Argon2id password hashing, RFC 6238 TOTP MFA, AES-256-GCM field-level encryption, SHA-256 hash-chained tamper-evident audit ledger, 15-minute idle timeout with 60s warning.
- **Platform & Topology**: Docker Compose multi-network boundary (`edge`, `app`, `data`), Nginx reverse proxy with TLS, strict CSP, and rate limiting.

---

## 2. Default Test Accounts for Evaluation

All accounts share the standard evaluation password: `AERIS_Pass_2026!`  
For MFA evaluation, the standard Base32 seed is `JBSWY3DPEHPK3PXP`. An interactive **Demo Role Switcher** is also provided in the top navigation bar to seamlessly inspect views across all 9 roles!

| Username | Role | Assigned Callsign | Default Landing Screen | Permitted Menu Groups |
|---|---|---|---|---|
| `planner` | **Operations Planner** | `STRATEGIST` | Command Center | Command, Domains (read), Planning, Resilience, Data |
| `authority` | **Decision Authority** | `COMMANDANT` | Decision Queue | Command, Domains (read), Planning (read), Decisions, Data |
| `craft_officer` | **Craft Officer** | `CHIEF-AIR` | Craft Dashboard | Craft, Insights, Data Health, Plans (read) |
| `supply_officer` | **Supply Officer** | `QUARTERMASTER` | Supply Dashboard | Supply, Insights, Data Health, Plans (read) |
| `personnel_officer` | **Personnel Officer** | `ADJUTANT` | People Dashboard | People, Insights, Data Health, Plans (read) |
| `pilot_01` | **Pilot** | `MAVERICK` | My Duty | Pilot Menu (My Duty, Schedule, Rest, Quals) |
| `auditor` | **Auditor** | `INSPECTOR` | Audit Log | Governance (Audit Log, Model Registry), Decisions, Replay |
| `admin` | **Administrator** | `OVERLORD` | Administration | Administration, Governance, Data, System Health |
| `analyst` | **Analyst** | `SENTINEL` | Command Center | Command, Domains (read), Planning (read), Data |

---

## 3. Architecture & Network Boundary

```
[ Internet / Evaluator Browser ]
               │
               ▼ (Port 80 / 443)
┌────────────────────────────────────────────────────────┐
│ Edge Network (Nginx Reverse Proxy)                     │
│ - TLS Termination & Strict CSP                         │
│ - Rate Limiting (30r/s general, 5r/m auth)             │
└──────────────┬──────────────────────────┬──────────────┘
               │                          │
               ▼                          ▼
┌────────────────────────┐      ┌────────────────────────┐
│ App Network (Frontend) │      │ App Network (Backend)  │
│ - React 18 / Vite SPA  │      │ - FastAPI ASGI Server  │
│ - Radix UI / Tailwind  │      │ - CP-SAT Solver        │
│ - ECharts / Cytoscape  │      │ - Hash Chain Ledger    │
└────────────────────────┘      └──────────┬─────────────┘
                                           │
                        ┌──────────────────┴──────────────────┐
                        ▼                                     ▼
       ┌─────────────────────────────────┐   ┌────────────────────────────────┐
       │ Data Network (Postgres PostGIS) │   │ Data Network (Redis 7 Cache)   │
       │ - Encrypted PII Fields          │   │ - Live State Cache & Pub/Sub   │
       └─────────────────────────────────┘   └────────────────────────────────┘
```

---

## 4. Quickstart Execution

### Running via Docker Compose
```bash
# Start edge proxy, backend, frontend, postgres, redis, and vault
docker compose up -d --build

# Access web application
open http://localhost:3000
# or access through edge reverse proxy
open http://localhost
```

### Running Backend Locally
```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

### Running Verification & Tests
```bash
python3 -m unittest discover -s tests -p "test_*.py"
```

---

## 5. Security & Cryptographic Verifications

1. **Deny-by-Default RBAC**: Every endpoint enforces explicit permissions. Separation of duties prevents Planners from approving plans, and Decision Authority cannot generate plans.
2. **Audit Hash Chain Integrity**: Navigate to **Governance -> Audit Log** and click **Verify Hash Chain Integrity**. The SHA-256 links are validated cryptographically against tampering.
3. **Field-Level Envelope Encryption**: Personnel real names are encrypted in the database using AES-256-GCM. Unmasking requires `people:unmask`, justification reason, and step-up authentication.
