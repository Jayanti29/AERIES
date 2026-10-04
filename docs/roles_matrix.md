# AERIS Role-Based Access Control (RBAC) Matrix

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
