# AERIS System Architecture

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
