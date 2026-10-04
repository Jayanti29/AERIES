# Architecture Decision Records (ADRs)

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
