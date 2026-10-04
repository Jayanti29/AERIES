from datetime import datetime
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
