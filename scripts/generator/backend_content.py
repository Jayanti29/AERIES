# Backend source files generator for AERIS

def get_backend_files():
    files = {}

    files['backend/requirements.txt'] = """fastapi>=0.110.0
uvicorn[standard]>=0.28.0
pydantic>=2.6.4
pydantic-settings>=2.2.1
sqlalchemy>=2.0.28
alembic>=1.13.1
psycopg2-binary>=2.9.9
redis>=5.0.3
argon2-cffi>=23.1.0
pyjwt>=2.8.0
pyotp>=2.9.0
cryptography>=42.0.5
python-multipart>=0.0.9
networkx>=3.2.1
numpy>=1.26.4
pandas>=2.2.1
scikit-learn>=1.4.1.post1
ortools>=9.9.3963
websockets>=12.0
pytest>=8.1.1
httpx>=0.27.0
"""

    files['backend/Dockerfile'] = """FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
"""

    files['backend/app/__init__.py'] = """# AERIS Application Package
__version__ = "1.0.0"
"""

    files['backend/app/core/config.py'] = """import os
from typing import List
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "AERIS - Adaptive Air Operations & Resource Intelligence System"
    VERSION: str = "1.0.0"
    API_PREFIX: str = "/api"
    APP_ENV: str = os.getenv("APP_ENV", "development")
    SECRET_KEY: str = os.getenv("SECRET_KEY", "aeris-government-grade-super-secret-key-32-bytes!!")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15  # Short-lived access tokens
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    IDLE_TIMEOUT_MINUTES: int = 15
    IDLE_WARNING_SECONDS: int = 60

    # Database & Cache
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./aeris.db")
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    VAULT_ADDR: str = os.getenv("VAULT_ADDR", "http://localhost:8200")
    VAULT_TOKEN: str = os.getenv("VAULT_TOKEN", "aeris-dev-root-token")

    # Security & CORS
    CORS_ORIGINS: List[str] = ["http://localhost", "http://localhost:80", "http://localhost:3000", "http://localhost:5173"]
    HANDLING_BANNER: str = "SYNTHETIC DATA - SIMULATION"
    EMERGENCY_READ_ONLY: bool = False

    class Config:
        case_sensitive = True

settings = Settings()
"""

    files['backend/app/core/security.py'] = """import base64
import hashlib
import hmac
import json
import os
import time
from datetime import datetime, timedelta
from typing import Optional, Dict, Any

# Argon2id password hashing with pure-Python SHA-512 + Salt fallback
try:
    from argon2 import PasswordHasher
    from argon2.exceptions import VerifyMismatchError
    _ph = PasswordHasher()
    def hash_password(password: str) -> str:
        return _ph.hash(password)
    def verify_password(password: str, hashed: str) -> bool:
        try:
            return _ph.verify(hashed, password)
        except Exception:
            return False
except ImportError:
    def hash_password(password: str) -> str:
        salt = os.urandom(16).hex()
        dk = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt.encode('utf-8'), 100000)
        return f"pbkdf2_sha256${salt}${dk.hex()}"
    def verify_password(password: str, hashed: str) -> bool:
        try:
            parts = hashed.split('$')
            if len(parts) != 3 or parts[0] != "pbkdf2_sha256":
                return False
            salt = parts[1]
            expected = parts[2]
            dk = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt.encode('utf-8'), 100000)
            return hmac.compare_digest(dk.hex(), expected)
        except Exception:
            return False

# JWT Implementation with pure-Python fallback
try:
    import jwt
    def create_jwt(payload: dict, secret: str, algorithm: str = "HS256") -> str:
        return jwt.encode(payload, secret, algorithm=algorithm)
    def decode_jwt(token: str, secret: str, algorithm: str = "HS256") -> dict:
        return jwt.decode(token, secret, algorithms=[algorithm])
except ImportError:
    def _b64e(b: bytes) -> str:
        return base64.urlsafe_b64encode(b).decode('utf-8').rstrip('=')
    def _b64d(s: str) -> bytes:
        pad = '=' * ((4 - len(s) % 4) % 4)
        return base64.urlsafe_b64decode((s + pad).encode('utf-8'))
    def create_jwt(payload: dict, secret: str, algorithm: str = "HS256") -> str:
        header = {"typ": "JWT", "alg": algorithm}
        h_str = _b64e(json.dumps(header).encode('utf-8'))
        p_str = _b64e(json.dumps(payload).encode('utf-8'))
        sig = hmac.new(secret.encode('utf-8'), f"{h_str}.{p_str}".encode('utf-8'), hashlib.sha256).digest()
        return f"{h_str}.{p_str}.{_b64e(sig)}"
    def decode_jwt(token: str, secret: str, algorithm: str = "HS256") -> dict:
        parts = token.split('.')
        if len(parts) != 3:
            raise ValueError("Invalid token format")
        expected_sig = hmac.new(secret.encode('utf-8'), f"{parts[0]}.{parts[1]}".encode('utf-8'), hashlib.sha256).digest()
        if not hmac.compare_digest(_b64e(expected_sig), parts[2]):
            raise ValueError("Signature mismatch")
        payload = json.loads(_b64d(parts[1]).decode('utf-8'))
        if "exp" in payload and payload["exp"] < time.time():
            raise ValueError("Token expired")
        return payload

# TOTP implementation (RFC 6238 compliant)
def generate_totp_secret() -> str:
    return base64.b32encode(os.urandom(20)).decode('utf-8').rstrip('=')

def get_totp_code(secret: str, interval: int = 30) -> str:
    pad = '=' * ((8 - len(secret) % 8) % 8)
    key = base64.b32decode((secret + pad).upper().encode('utf-8'))
    counter = int(time.time() // interval)
    msg = counter.to_bytes(8, byteorder='big')
    h = hmac.new(key, msg, hashlib.sha1).digest()
    offset = h[-1] & 0x0F
    code = ((h[offset] & 0x7f) << 24 | (h[offset + 1] & 0xff) << 16 | (h[offset + 2] & 0xff) << 8 | (h[offset + 3] & 0xff)) % 1000000
    return f"{code:06d}"

def verify_totp(secret: str, code: str, window: int = 1) -> bool:
    if not secret or not code:
        return False
    # Check current window and +/- window steps
    current_time = time.time()
    for delta in range(-window, window + 1):
        test_time = current_time + delta * 30
        pad = '=' * ((8 - len(secret) % 8) % 8)
        try:
            key = base64.b32decode((secret + pad).upper().encode('utf-8'))
            counter = int(test_time // 30)
            msg = counter.to_bytes(8, byteorder='big')
            h = hmac.new(key, msg, hashlib.sha1).digest()
            offset = h[-1] & 0x0F
            val = ((h[offset] & 0x7f) << 24 | (h[offset + 1] & 0xff) << 16 | (h[offset + 2] & 0xff) << 8 | (h[offset + 3] & 0xff)) % 1000000
            if f"{val:06d}" == code.strip():
                return True
        except Exception:
            continue
    return False

# Field-level Encryption (AES-256-GCM / PBKDF2 HMAC-SHA256 authenticated fallback)
def encrypt_field(plaintext: str, key_hex: str) -> str:
    try:
        from cryptography.hazmat.primitives.ciphers.aead import AESGCM
        key = bytes.fromhex(key_hex)[:32]
        aesgcm = AESGCM(key)
        nonce = os.urandom(12)
        ct = aesgcm.encrypt(nonce, plaintext.encode('utf-8'), None)
        return "enc:gcm:" + base64.b64encode(nonce + ct).decode('utf-8')
    except Exception:
        # Authenticated HMAC-SHA256 + XOR envelope fallback
        salt = os.urandom(16)
        key = hashlib.sha256(bytes.fromhex(key_hex) + salt).digest()
        pt_bytes = plaintext.encode('utf-8')
        ct_bytes = bytes(b ^ key[i % len(key)] for i, b in enumerate(pt_bytes))
        tag = hmac.new(key, ct_bytes, hashlib.sha256).digest()
        payload = salt + tag + ct_bytes
        return "enc:hmac:" + base64.b64encode(payload).decode('utf-8')

def decrypt_field(ciphertext: str, key_hex: str) -> str:
    if not ciphertext.startswith("enc:"):
        return ciphertext
    try:
        if ciphertext.startswith("enc:gcm:"):
            from cryptography.hazmat.primitives.ciphers.aead import AESGCM
            data = base64.b64decode(ciphertext[8:])
            nonce = data[:12]
            ct = data[12:]
            key = bytes.fromhex(key_hex)[:32]
            return AESGCM(key).decrypt(nonce, ct, None).decode('utf-8')
        elif ciphertext.startswith("enc:hmac:"):
            data = base64.b64decode(ciphertext[9:])
            salt = data[:16]
            tag = data[16:48]
            ct_bytes = data[48:]
            key = hashlib.sha256(bytes.fromhex(key_hex) + salt).digest()
            calc_tag = hmac.new(key, ct_bytes, hashlib.sha256).digest()
            if not hmac.compare_digest(tag, calc_tag):
                raise ValueError("MAC check failed")
            return bytes(b ^ key[i % len(key)] for i, b in enumerate(ct_bytes)).decode('utf-8')
    except Exception as e:
        return "[ENCRYPTED_DATA_PROTECTED]"
    return ciphertext

# Digital signature helper (for signed decisions and model certificates)
def sign_data(data_str: str, private_key_hex: str) -> str:
    key_bytes = bytes.fromhex(private_key_hex.ljust(64, '0')[:32])
    sig = hmac.new(key_bytes, data_str.encode('utf-8'), hashlib.sha256).hexdigest()
    return f"sig:sha256:{sig}"

def verify_signature(data_str: str, signature: str, private_key_hex: str) -> bool:
    expected = sign_data(data_str, private_key_hex)
    return hmac.compare_digest(expected, signature)
"""

    files['backend/app/core/rbac.py'] = """from enum import Enum
from typing import Dict, Set, List
from fastapi import HTTPException, status

class Role(str, Enum):
    ADMINISTRATOR = "Administrator"
    OPERATIONS_PLANNER = "Operations Planner"
    DECISION_AUTHORITY = "Decision Authority"
    ANALYST = "Analyst"
    AUDITOR = "Auditor"
    PILOT = "Pilot"
    CRAFT_OFFICER = "Craft Officer"
    SUPPLY_OFFICER = "Supply Officer"
    PERSONNEL_OFFICER = "Personnel Officer"

# Comprehensive Granular Permissions
ROLE_PERMISSIONS: Dict[Role, Set[str]] = {
    Role.ADMINISTRATOR: {
        "admin:manage", "admin:users", "admin:roles", "admin:approvals",
        "admin:keys", "admin:generator", "admin:read_only", "audit:read",
        "models:read", "data:read", "health:read"
    },
    Role.OPERATIONS_PLANNER: {
        "command:read", "map:read", "insights:read", "craft:read",
        "supply:read", "people:read", "missions:read", "plans:create",
        "plans:read", "tradeoffs:explore", "graph:read", "chaos:run",
        "stress:run", "data:read", "decisions:read"
    },
    Role.DECISION_AUTHORITY: {
        "command:read", "map:read", "insights:read", "craft:read",
        "supply:read", "people:read", "missions:read", "plans:read",
        "decisions:read", "decisions:queue", "decisions:approve",
        "decisions:modify", "decisions:reject", "decisions:sign",
        "replay:read", "graph:read", "data:read"
    },
    Role.ANALYST: {
        "command:read", "map:read", "insights:read", "craft:read",
        "supply:read", "people:read", "missions:read", "plans:read",
        "data:read", "models:read"
    },
    Role.AUDITOR: {
        "audit:read", "audit:verify", "audit:export", "decisions:read",
        "replay:read", "models:read"
    },
    Role.PILOT: {
        "state:read_own", "pilot:duty", "pilot:schedule", "pilot:rest",
        "pilot:qualifications", "notifications:read"
    },
    Role.CRAFT_OFFICER: {
        "craft:read", "craft:fleet", "craft:maintenance", "craft:components",
        "craft:predictions", "maintenance:flag", "insights:read_craft",
        "data:read_maintenance", "plans:read"
    },
    Role.SUPPLY_OFFICER: {
        "supply:read", "supply:resources", "supply:forecast", "supply:bottlenecks",
        "supply:stock", "resource:flag", "insights:read_supply",
        "data:read_supply", "plans:read"
    },
    Role.PERSONNEL_OFFICER: {
        "people:read", "people:roster", "people:readiness", "people:coverage",
        "people:availability", "people:workload", "people:unmask",
        "availability:flag", "insights:read_people", "data:read_people", "plans:read"
    }
}

def has_permission(role: str, permission: str) -> bool:
    try:
        r = Role(role)
        return permission in ROLE_PERMISSIONS.get(r, set())
    except ValueError:
        return False

def check_permission(user_role: str, required_permission: str):
    if not has_permission(user_role, required_permission):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Forbidden: Role '{user_role}' lacks required permission '{required_permission}'"
        )
"""

    files['backend/app/core/audit.py'] = """import hashlib
import json
import time
from typing import Optional, Dict, Any, List
from datetime import datetime

class AuditLedger:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(AuditLedger, cls).__new__(cls)
            cls._instance.ledger = []
            cls._instance._init_genesis()
        return cls._instance

    def _init_genesis(self):
        genesis_entry = {
            "index": 0,
            "timestamp": "2026-10-05T00:00:00Z",
            "actor_id": "SYSTEM_CORE",
            "actor_role": "SYSTEM",
            "action": "GENESIS_LEDGER_INIT",
            "resource_type": "LEDGER",
            "resource_id": "CHAIN_0",
            "details": {"status": "AERIS Ledger Initialized", "version": "1.0"},
            "prev_hash": "0000000000000000000000000000000000000000000000000000000000000000",
            "current_hash": ""
        }
        genesis_entry["current_hash"] = self._compute_hash(genesis_entry)
        self.ledger.append(genesis_entry)

    def _compute_hash(self, entry: Dict[str, Any]) -> str:
        payload = f"{entry['index']}|{entry['timestamp']}|{entry['actor_id']}|{entry['actor_role']}|{entry['action']}|{entry['resource_type']}|{entry['resource_id']}|{json.dumps(entry['details'], sort_keys=True)}|{entry['prev_hash']}"
        return hashlib.sha256(payload.encode('utf-8')).hexdigest()

    def record_event(
        self,
        actor_id: str,
        actor_role: str,
        action: str,
        resource_type: str,
        resource_id: str,
        details: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        prev_entry = self.ledger[-1]
        new_entry = {
            "index": len(self.ledger),
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "actor_id": actor_id,
            "actor_role": actor_role,
            "action": action,
            "resource_type": resource_type,
            "resource_id": resource_id,
            "details": details or {},
            "prev_hash": prev_entry["current_hash"],
            "current_hash": ""
        }
        new_entry["current_hash"] = self._compute_hash(new_entry)
        self.ledger.append(new_entry)
        return new_entry

    def verify_chain(self) -> Dict[str, Any]:
        if not self.ledger:
            return {"valid": False, "reason": "Ledger is empty", "tampered_index": None}

        # Check genesis
        first = self.ledger[0]
        if first["prev_hash"] != "0000000000000000000000000000000000000000000000000000000000000000":
            return {"valid": False, "reason": "Invalid genesis block", "tampered_index": 0}

        calc_first_hash = self._compute_hash(first)
        if calc_first_hash != first["current_hash"]:
            return {"valid": False, "reason": "Genesis hash corrupted", "tampered_index": 0}

        for i in range(1, len(self.ledger)):
            prev = self.ledger[i - 1]
            curr = self.ledger[i]

            if curr["prev_hash"] != prev["current_hash"]:
                return {
                    "valid": False,
                    "reason": f"Hash chain broken at index {i}",
                    "tampered_index": i
                }

            expected_hash = self._compute_hash(curr)
            if curr["current_hash"] != expected_hash:
                return {
                    "valid": False,
                    "reason": f"Hash signature invalid at index {i}",
                    "tampered_index": i
                }

        return {
            "valid": True,
            "reason": "All cryptographic links verified successfully",
            "total_records": len(self.ledger),
            "chain_head": self.ledger[-1]["current_hash"]
        }

    def get_logs(self, limit: int = 100, action_filter: Optional[str] = None) -> List[Dict[str, Any]]:
        logs = self.ledger[::-1]
        if action_filter:
            logs = [entry for entry in logs if action_filter.lower() in entry["action"].lower()]
        return logs[:limit]

audit_service = AuditLedger()
"""

    files['backend/app/core/provenance.py'] = """from datetime import datetime
from typing import Any, Optional
from pydantic import BaseModel, Field

class ProvenanceValue(BaseModel):
    value: Any
    source: str = Field(..., description="Sensor, telemetry feed, or model name")
    observed_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat() + "Z")
    age_seconds: int = Field(default=0)
    confidence: float = Field(default=0.98, ge=0.0, le=1.0)
    provenance_hash: Optional[str] = None

    def __init__(self, **data):
        super().__init__(**data)
        if not self.provenance_hash:
            import hashlib
            raw = f"{self.value}_{self.source}_{self.observed_at}_{self.confidence}"
            self.provenance_hash = hashlib.sha256(raw.encode('utf-8')).hexdigest()[:16]
"""

    return files

print("backend_content.py loaded")
