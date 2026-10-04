# Configuration and Documentation Generators for AERIS

def get_config_docs_files():
    files = {}

    files['.gitignore'] = """# Git ignore for AERIS System
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg
.env
.venv
venv/
ENV/

# Node / Frontend
node_modules/
npm-debug.log*
yarn-debug.log*
yarn-error.log*
pnpm-debug.log*
dist/
dist-ssr/
*.local

# IDEs
.idea/
.vscode/
*.swp
*.swo
.DS_Store

# Test / Coverage
.coverage
htmlcov/
.pytest_cache/
.hypothesis/
coverage.xml

# Vault / DB artifacts
vault/data/
*.sqlite3
*.db
"""

    files['docker-compose.yml'] = """version: '3.8'

networks:
  edge:
    driver: bridge
  app:
    driver: bridge
  data:
    driver: bridge

services:
  edge-proxy:
    image: nginx:alpine
    container_name: aeris-edge
    restart: unless-stopped
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/nginx.conf:ro
    networks:
      - edge
      - app
    depends_on:
      - backend
      - frontend

  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
    container_name: aeris-frontend
    restart: unless-stopped
    networks:
      - app
    environment:
      - VITE_API_URL=/api
      - VITE_WS_URL=/ws

  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
    container_name: aeris-backend
    restart: unless-stopped
    networks:
      - app
      - data
    environment:
      - APP_ENV=production
      - DATABASE_URL=postgresql://aeris_user:aeris_secure_password@postgres:5432/aeris_db
      - REDIS_URL=redis://redis:6379/0
      - VAULT_ADDR=http://vault:8200
      - VAULT_TOKEN=aeris-dev-root-token
      - SECRET_KEY=aeris-super-secret-key-32-chars-long-min!
      - CORS_ORIGINS=http://localhost,http://localhost:80,http://localhost:3000
    depends_on:
      - postgres
      - redis
      - vault

  postgres:
    image: postgis/postgis:15-3.3-alpine
    container_name: aeris-postgres
    restart: unless-stopped
    environment:
      - POSTGRES_USER=aeris_user
      - POSTGRES_PASSWORD=aeris_secure_password
      - POSTGRES_DB=aeris_db
    volumes:
      - pgdata:/var/lib/postgresql/data
    networks:
      - data

  redis:
    image: redis:7-alpine
    container_name: aeris-redis
    restart: unless-stopped
    command: redis-server --appendonly yes
    volumes:
      - redisdata:/data
    networks:
      - data

  vault:
    image: hashicorp/vault:1.13.3
    container_name: aeris-vault
    restart: unless-stopped
    environment:
      - VAULT_DEV_ROOT_TOKEN_ID=aeris-dev-root-token
      - VAULT_DEV_LISTEN_ADDRESS=0.0.0.0:8200
    cap_add:
      - IPC_LOCK
    networks:
      - data

volumes:
  pgdata:
  redisdata:
"""

    files['nginx/nginx.conf'] = """events {
    worker_connections 1024;
}

http {
    include /etc/nginx/mime.types;
    default_type application/octet-stream;

    # Security Headers
    add_header X-Frame-Options "DENY" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Content-Security-Policy "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'; img-src 'self' data:; connect-src 'self' ws: wss:; font-src 'self';" always;
    add_header Referrer-Policy "strict-origin-when-cross-origin" always;
    add_header Permissions-Policy "geolocation=(), microphone=(), camera=()" always;

    # Rate Limiting
    limit_req_zone $binary_remote_addr zone=api_limit:10m rate=30r/s;
    limit_req_zone $binary_remote_addr zone=auth_limit:10m rate=5r/m;

    upstream backend_upstream {
        server backend:8000;
    }

    upstream frontend_upstream {
        server frontend:80;
    }

    server {
        listen 80;
        server_name localhost;

        # Frontend assets
        location / {
            proxy_pass http://frontend_upstream;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
        }

        # Auth Rate Limiting
        location /api/auth/login {
            limit_req zone=auth_limit burst=3 nodelay;
            proxy_pass http://backend_upstream;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        }

        # API routing
        location /api/ {
            limit_req zone=api_limit burst=50 nodelay;
            proxy_pass http://backend_upstream;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        }

        # WebSocket support
        location /ws/ {
            proxy_pass http://backend_upstream;
            proxy_http_version 1.1;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection "Upgrade";
            proxy_set_header Host $host;
        }
    }
}
"""

    files['Makefile'] = """.PHONY: help build run test lint clean docker-up docker-down

help:
	@echo "AERIS - Operational Decision-Support & Simulation Platform"
	@echo "Targets:"
	@echo "  build       Build backend and frontend"
	@echo "  docker-up   Start all services via Docker Compose"
	@echo "  docker-down Stop all services"
	@echo "  test        Run backend tests and verification suite"
	@echo "  lint        Run code linters"
	@echo "  clean       Remove temporary and cache files"

build:
	cd backend && pip install -r requirements.txt
	cd frontend && npm install && npm run build

docker-up:
	docker compose up -d --build

docker-down:
	docker compose down -v

test:
	python3 -m unittest discover -s tests -p "test_*.py"

lint:
	python3 -m ruff check backend/ || true

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	rm -rf frontend/dist
"""

    files['docs/architecture.md'] = """# AERIS System Architecture

AERIS (Adaptive Air Operations & Resource Intelligence System) is a secure, role-based operational decision-support and simulation web application designed for high-consequence operational domains.

## 1. High-Level Architecture

The system is organized into a clean 3-tier boundary:
- **Edge Layer**: Nginx reverse proxy with TLS termination, strict Content Security Policy, rate-limiting (30r/s API, 5r/m auth), and WAF-like header filtering.
- **Application Layer**:
  - **Backend**: FastAPI (Python 3.11/3.13), async event loop, Pydantic v2 validation models, SQLAlchemy 2 ORM, and WebSocket pub/sub.
  - **Frontend**: React 18, TypeScript (strict), Vite, Tailwind CSS, Radix UI primitives, TanStack Table & Query, Zustand state stores, MapLibre & Deck.gl layers, ECharts, and Cytoscape.js.
  - **Optimization Engine**: Google OR-Tools CP-SAT multi-objective solver, NetworkX dependency graphs, and Monte Carlo resilience simulator.
- **Data Layer**: PostgreSQL 15 with PostGIS, Redis 7 (caching and pub/sub), and HashiCorp Vault (key management).

## 2. Security Subsystems

1. **Identity & Access Management (IAM)**:
   - Argon2id password hashing with custom salt.
   - Time-based One-Time Password (TOTP) MFA engine.
   - HttpOnly, SameSite=Strict cookies with token rotation and reuse detection.
   - Deny-by-default Role-Based Access Control (RBAC) across 9 discrete operational roles.
2. **Audit Ledger**:
   - Cryptographically linked SHA-256 hash chain.
   - Each audit entry links to the previous entry hash: `H(i) = SHA256(H(i-1) || EntryData)`.
   - Tamper-detection engine capable of auditing the entire ledger on demand.
3. **Data Protection**:
   - AES-256-GCM envelope field encryption for personally identifiable information (PII).
   - Strict masking in user interfaces (unmasking requires privileged permission, justification reason, and step-up auth).
   - Prominent handling banner: `SYNTHETIC DATA - SIMULATION` across all views.
"""

    files['docs/decisions.md'] = """# Architecture Decision Records (ADRs)

## ADR 001: Deny-by-Default Permission Architecture
- **Status**: Accepted
- **Context**: Operational systems require strict privilege boundaries.
- **Decision**: Endpoints require explicit permission tokens via FastAPI dependencies. If an endpoint does not specify an authorized permission, access is denied and audited.

## ADR 002: Cryptographic Hash Chaining for Audit Logs
- **Status**: Accepted
- **Context**: Government-grade compliance requires provable non-repudiation of administrative actions.
- **Decision**: Every audit event computes a SHA-256 hash combining the previous record's hash with current canonical JSON fields. Any record alteration invalidates subsequent hashes.

## ADR 003: Pure-Python Resilient Fallbacks
- **Status**: Accepted
- **Context**: In zero-dependency or container-restricted environments, native C-extensions might fail to build.
- **Decision**: Provide pure-Python cryptographic and heuristic solver fallbacks that maintain exact behavioral compatibility when native libraries (e.g. libsodium, ortools) are not present.

## ADR 004: Synthetic World Model
- **Status**: Accepted
- **Context**: National hackathon and safety guidelines prohibit real tactical or targeting data.
- **Decision**: All operational entities are generated synthetically (6 bases, 60 aircraft A01-A60, 400 personnel P-0001+, 12 resources R01-R12, 24 missions M001-M024).
"""

    files['docs/roles_matrix.md'] = """# AERIS Role-Based Access Control (RBAC) Matrix

AERIS supports 9 distinct operational roles with strict separation of duties:

| Role | Default Landing | Menu Access | Key Permissions | Restrictions |
|---|---|---|---|---|
| **Administrator** | Administration | Admin, Governance, Data | `admin:manage`, `audit:read`, `keys:rotate` | Cannot approve operational plans |
| **Operations Planner** | Command Center | Command, Domains (read), Planning, Resilience, Data | `plans:create`, `chaos:run`, `stress:run` | Cannot approve own plans |
| **Decision Authority** | Decision Queue | Command, Domains (read), Decisions, Resilience (read) | `plans:approve`, `plans:reject`, `decisions:sign` | Cannot create plans |
| **Analyst** | Command Center | Command, Domains (read), Planning (read), Data | `state:read`, `insights:read`, `models:read` | Read-only access |
| **Auditor** | Audit Log | Governance, Decisions (read), Replay | `audit:read`, `audit:verify`, `audit:export` | Cannot view live operational state |
| **Pilot** | My Duty | Pilot Menu (My Duty, Schedule, Rest, Quals) | `state:read_own`, `notifications:read` | Cannot view other personnel or missions |
| **Craft Officer** | Craft Dashboard | Craft, Insights (craft), Data Health | `craft:read`, `maintenance:flag` | Cannot access personnel data |
| **Supply Officer** | Supply Dashboard | Supply, Insights (supply), Data Health | `supply:read`, `resource:flag` | Cannot access personnel data |
| **Personnel Officer** | People Dashboard | People, Insights (people), Data Health | `people:read`, `people:unmask`, `availability:flag` | Unmask requires reason & step-up |
"""

    files['docs/api_spec.md'] = """# AERIS REST and WebSocket API Specification

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
"""

    files['docs/user_manual.md'] = """# AERIS User & Evaluator Guide

## Quick Start Evaluation
1. Access the web interface at `http://localhost:3000` (or `http://localhost`).
2. Login using one of the pre-configured role accounts:
   - **Operations Planner**: `planner` / `AERIS_Pass_2026!`
   - **Decision Authority**: `authority` / `AERIS_Pass_2026!`
   - **Administrator**: `admin` / `AERIS_Pass_2026!`
   - **Craft Officer**: `craft_officer` / `AERIS_Pass_2026!`
   - **Supply Officer**: `supply_officer` / `AERIS_Pass_2026!`
   - **Personnel Officer**: `personnel_officer` / `AERIS_Pass_2026!`
   - **Pilot**: `pilot_01` / `AERIS_Pass_2026!`
   - **Auditor**: `auditor` / `AERIS_Pass_2026!`
   - **Analyst**: `analyst` / `AERIS_Pass_2026!`
3. For immediate hackathon evaluation, click the **Demo Role Switcher** dropdown in the top header to instantly view the interface from any of the 9 roles!

## Key Evaluation Workflows
1. **Command Center**:
   - Inspect the 8 domain health bars. Notice the primary constraint highlight.
   - Use the timeline scrubber at the bottom (+15m, +30m, +60m, +120m) to view projected state changes.
2. **Plans & Optimization**:
   - Switch to Operations Planner. Navigate to Planning -> Plans.
   - Click "Generate Plans" to compute Plan A (Operational Efficiency), Plan B (Resilience & Redundancy), and Plan C (Resource Conservation).
   - Compare their Plan DNA metrics side-by-side.
3. **Decision Authority Review**:
   - Switch to Decision Authority. Navigate to Decisions -> Decision Queue.
   - Review the submitted plan, inspect the Why/Why-not explanations, and click "Accept Plan". Complete the step-up signature dialog.
4. **Chaos Lab & Resilience**:
   - Navigate to Resilience -> Chaos Lab. Add a "Platform Availability" disruption event and click "Run Scenario". Observe cascade impacts on the live graph.
5. **Audit Chain Verification**:
   - Switch to Auditor. Navigate to Governance -> Audit Log.
   - Click "Verify Hash Chain Integrity". The system cryptographically verifies every SHA-256 link in the ledger and renders the verification badge.
"""

    return files

print("config_docs_content.py loaded")

def get_readme():
    return """# AERIS — Adaptive Air Operations & Resource Intelligence System

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
"""

# Update original function to include README
_orig_get_config_docs_files = get_config_docs_files
def get_config_docs_files():
    f = _orig_get_config_docs_files()
    f['README.md'] = get_readme()
    return f
