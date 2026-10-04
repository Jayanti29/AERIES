# AERIS User & Evaluator Guide

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
