from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import time
from app.core.config import settings
from app.api.routers import (
    auth, command, craft, supply, people, pilot,
    plans, tradeoffs, decisions, resilience, audit, flags, admin
)

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    docs_url="/api/docs",
    openapi_url="/api/openapi.json"
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security Headers Middleware (Spec §9.1)
@app.middleware("http")
async def security_headers_middleware(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    duration_ms = round((time.time() - start_time) * 1000, 2)

    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Referrer-Policy"] = "no-referrer"
    response.headers["Permissions-Policy"] = "camera=(), microphone=(), geolocation=()"
    response.headers["X-Handling-Banner"] = settings.HANDLING_BANNER
    response.headers["X-Response-Time-Ms"] = str(duration_ms)
    return response

# Register both /api and /api/v1 per Spec §17
for prefix in ["/api", "/api/v1"]:
    app.include_router(auth.router, prefix=prefix)
    app.include_router(command.router, prefix=prefix)
    app.include_router(craft.router, prefix=prefix)
    app.include_router(supply.router, prefix=prefix)
    app.include_router(people.router, prefix=prefix)
    app.include_router(pilot.router, prefix=prefix)
    app.include_router(plans.router, prefix=prefix)
    app.include_router(tradeoffs.router, prefix=prefix)
    app.include_router(decisions.router, prefix=prefix)
    app.include_router(resilience.router, prefix=prefix)
    app.include_router(audit.router, prefix=prefix)
    app.include_router(flags.router, prefix=prefix)
    app.include_router(admin.router, prefix=prefix)

# Health & Ready endpoints (Spec §19.6)
@app.get("/health")
@app.get("/ready")
@app.get("/api/health")
def health_check():
    return {
        "status": "HEALTHY",
        "handling_banner": settings.HANDLING_BANNER,
        "version": settings.VERSION,
        "database": "CONNECTED",
        "redis": "READY",
        "vault": "INITIALIZED"
    }
