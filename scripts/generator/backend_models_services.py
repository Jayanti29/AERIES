# Backend Models and Core Services for AERIS

def get_backend_models_services():
    files = {}

    files['backend/app/db/session.py'] = """from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import settings

# Engine configuration with SQLite fallback for rapid testing
if settings.DATABASE_URL.startswith("sqlite"):
    engine = create_engine(
        settings.DATABASE_URL,
        connect_args={"check_same_thread": False}
    )
else:
    engine = create_engine(
        settings.DATABASE_URL,
        pool_pre_ping=True,
        pool_size=10,
        max_overflow=20
    )

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
"""

    files['backend/app/db/models.py'] = """from sqlalchemy import Column, Integer, String, Boolean, Float, DateTime, ForeignKey, Text, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.session import Base

class User(Base):
    __tablename__ = "users"
    id = Column(String(64), primary_key=True, index=True)
    username = Column(String(64), unique=True, index=True, nullable=False)
    callsign = Column(String(64), nullable=True)
    hashed_password = Column(String(256), nullable=False)
    role = Column(String(64), nullable=False, index=True)
    is_active = Column(Boolean, default=True)
    mfa_enabled = Column(Boolean, default=True)
    mfa_secret = Column(String(64), nullable=True)
    force_password_change = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

class BaseStation(Base):
    __tablename__ = "base_stations"
    code = Column(String(16), primary_key=True)  # e.g., B-Alpha
    name = Column(String(64), nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    capacity_platforms = Column(Integer, default=20)
    current_readiness = Column(Float, default=0.92)
    status = Column(String(32), default="OPERATIONAL")

class AircraftPlatform(Base):
    __tablename__ = "aircraft_platforms"
    code = Column(String(16), primary_key=True)  # A01 to A60
    base_code = Column(String(16), ForeignKey("base_stations.code"), nullable=False)
    platform_type = Column(String(32), nullable=False)  # Fighter, Tanker, Transport, Recon, AEW&C
    status = Column(String(32), default="READY")  # READY, IN_FLIGHT, MAINTENANCE, TURNAROUND
    readiness_score = Column(Float, default=0.95)
    flight_hours = Column(Float, default=1240.5)
    hours_to_inspection = Column(Float, default=32.0)
    current_mission = Column(String(32), nullable=True)
    predicted_constraint_prob = Column(Float, default=0.08)

class ComponentSubsystem(Base):
    __tablename__ = "component_subsystems"
    id = Column(String(64), primary_key=True)
    aircraft_code = Column(String(16), ForeignKey("aircraft_platforms.code"), nullable=False)
    name = Column(String(64), nullable=False)  # Engine-1, Radar APG-81, Avionics Bus, Hydraulics
    health_index = Column(Float, default=0.94)
    trend = Column(String(16), default="STABLE")  # STABLE, DEGRADING, CRITICAL
    last_inspected = Column(DateTime, default=datetime.utcnow)

class PersonnelRecord(Base):
    __tablename__ = "personnel"
    code = Column(String(16), primary_key=True)  # P-0001 to P-0400
    callsign = Column(String(32), nullable=False)
    masked_name = Column(String(64), default="[CLASSIFIED PERSONNEL]")
    encrypted_real_name = Column(Text, nullable=False)
    team = Column(String(32), nullable=False)
    role = Column(String(32), nullable=False)
    status = Column(String(32), default="AVAILABLE")
    workload_pct = Column(Float, default=62.0)
    duty_hours_today = Column(Float, default=4.5)
    rest_remaining_hrs = Column(Float, default=0.0)
    qualifications = Column(JSON, default=list)

class ResourceStock(Base):
    __tablename__ = "resource_stocks"
    id = Column(String(64), primary_key=True)
    code = Column(String(16), nullable=False)  # R01 to R12
    name = Column(String(64), nullable=False)
    base_code = Column(String(16), ForeignKey("base_stations.code"), nullable=False)
    unit = Column(String(32), nullable=False)
    available_qty = Column(Float, default=5000.0)
    demand_qty = Column(Float, default=4200.0)
    projected_shortfall = Column(Float, default=0.0)
    reserve_threshold = Column(Float, default=1000.0)
    pressure_level = Column(String(16), default="NOMINAL")  # NOMINAL, ELEVATED, CRITICAL

class Mission(Base):
    __tablename__ = "missions"
    code = Column(String(16), primary_key=True)  # M001 to M024
    name = Column(String(64), nullable=False)
    priority = Column(String(16), default="HIGH")  # CRITICAL, HIGH, MEDIUM, LOW
    status = Column(String(32), default="ACTIVE")  # SCHEDULED, ACTIVE, COMPLETED, AT_RISK
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    required_platforms = Column(JSON, default=list)
    assigned_platforms = Column(JSON, default=list)
    required_personnel = Column(JSON, default=list)
    assigned_personnel = Column(JSON, default=list)
    resource_demands = Column(JSON, default=dict)
    constraint_state = Column(String(32), default="CLEAR")
"""

    files['backend/app/data/seed_generator.py'] = """import random
from datetime import datetime, timedelta
from app.core.security import hash_password, encrypt_field, generate_totp_secret

# Deterministic Seed Configuration
SEED_VALUE = 42

def generate_seed_data():
    random.seed(SEED_VALUE)
    key_hex = "0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef"

    # 1. Six Fictional Bases
    bases = [
        {"code": "B-Alpha", "name": "Alpha Station Forward", "latitude": 34.05, "longitude": -118.24, "capacity": 20, "readiness": 0.94, "status": "OPERATIONAL"},
        {"code": "B-Bravo", "name": "Bravo Ridge Airfield", "latitude": 36.16, "longitude": -115.13, "capacity": 15, "readiness": 0.91, "status": "OPERATIONAL"},
        {"code": "B-Charlie", "name": "Charlie Coastal Hub", "latitude": 32.71, "longitude": -117.16, "capacity": 25, "readiness": 0.88, "status": "OPERATIONAL"},
        {"code": "B-Delta", "name": "Delta Desert Logistics", "latitude": 33.44, "longitude": -112.07, "capacity": 18, "readiness": 0.96, "status": "OPERATIONAL"},
        {"code": "B-Echo", "name": "Echo Highlands Depot", "latitude": 39.73, "longitude": -104.99, "capacity": 12, "readiness": 0.85, "status": "ELEVATED_OPS"},
        {"code": "B-Foxtrot", "name": "Foxtrot Northern Outpost", "latitude": 47.60, "longitude": -122.33, "capacity": 10, "readiness": 0.92, "status": "OPERATIONAL"},
    ]

    # 2. 60 Aircraft (A01 - A60)
    platform_types = ["Fighter Interceptor", "Strategic Tanker", "Tactical Transport", "Reconnaissance Drone", "AEW&C Sentinel"]
    aircraft = []
    for i in range(1, 61):
        code = f"A{i:02d}"
        base = bases[(i - 1) % len(bases)]["code"]
        ptype = platform_types[(i - 1) % len(platform_types)]
        readiness = round(random.uniform(0.78, 0.99), 2)
        status = "READY" if readiness > 0.82 else "MAINTENANCE"
        flight_hrs = round(random.uniform(800.0, 3200.0), 1)
        hrs_to_insp = round(random.uniform(5.0, 75.0), 1)
        aircraft.append({
            "code": code,
            "base_code": base,
            "platform_type": ptype,
            "status": status,
            "readiness_score": readiness,
            "flight_hours": flight_hrs,
            "hours_to_inspection": hrs_to_insp,
            "current_mission": f"M{random.randint(1, 24):03d}" if status == "READY" and random.random() > 0.4 else None,
            "predicted_constraint_prob": round(random.uniform(0.02, 0.35), 2)
        })

    # 3. 400 Personnel (P-0001 - P-0400)
    teams = ["Viper Flight", "Ghost Recon", "Falcon Logistics", "Titan Support", "Raven Maintenance", "Skyguard Ops"]
    roles = ["Mission Commander", "Lead Pilot", "Co-Pilot", "Avionics Specialist", "Weapons Tech", "Flight Engineer"]
    personnel = []
    for i in range(1, 401):
        code = f"P-{i:04d}"
        callsign = f"CALLSIGN-{code[2:]}"
        real_name = f"Synthetic Operator {i}"
        team = teams[(i - 1) % len(teams)]
        role = roles[(i - 1) % len(roles)]
        workload = round(random.uniform(45.0, 96.0), 1)
        status = "AVAILABLE" if workload < 88.0 else "OVERLOADED"
        personnel.append({
            "code": code,
            "callsign": callsign,
            "masked_name": f"OPERATOR {code[-4:]} [MASKED]",
            "encrypted_real_name": encrypt_field(real_name, key_hex),
            "team": team,
            "role": role,
            "status": status,
            "workload_pct": workload,
            "duty_hours_today": round(random.uniform(2.0, 9.5), 1),
            "rest_remaining_hrs": round(random.uniform(0.0, 8.0), 1) if workload > 85 else 0.0,
            "qualifications": ["Night Ops", "High-G Combat", "Electronic Warfare"]
        })

    # 4. 12 Resource Types (R01 - R12)
    resource_defs = [
        ("R01", "Jet Fuel JP-8", "Gallons"),
        ("R02", "AvGas 100LL", "Gallons"),
        ("R03", "Liquid Oxygen Aviator", "Liters"),
        ("R04", "Hydraulic Fluid MIL-PRF", "Liters"),
        ("R05", "Precision Avionics Line", "Units"),
        ("R06", "Turbine Replacement Core", "Kits"),
        ("R07", "Composite Airframe Repair", "Kits"),
        ("R08", "Abstract Payload Alpha", "Containers"),
        ("R09", "Abstract Payload Beta", "Containers"),
        ("R10", "Abstract Sensor Pod", "Units"),
        ("R11", "Field Operations Rations", "Boxes"),
        ("R12", "Ground Power Generator Unit", "Units")
    ]
    resources = []
    for b in bases:
        for rcode, rname, runit in resource_defs:
            avail = round(random.uniform(1200.0, 9500.0), 1)
            # Demand tuned to ~90% capacity to induce real trade-offs
            demand = round(avail * random.uniform(0.82, 0.96), 1)
            shortfall = max(0.0, demand - avail)
            pressure = "CRITICAL" if shortfall > 0 else ("ELEVATED" if demand / avail > 0.88 else "NOMINAL")
            resources.append({
                "id": f"{b['code']}_{rcode}",
                "code": rcode,
                "name": rname,
                "base_code": b["code"],
                "unit": runit,
                "available_qty": avail,
                "demand_qty": demand,
                "projected_shortfall": shortfall,
                "reserve_threshold": round(avail * 0.15, 1),
                "pressure_level": pressure
            })

    # 5. 24 Active Missions (M001 - M024)
    now = datetime.utcnow()
    missions = []
    for i in range(1, 25):
        mcode = f"M{i:03d}"
        priority = "CRITICAL" if i <= 4 else ("HIGH" if i <= 14 else "MEDIUM")
        assigned_p = [f"A{((i * 2 + j) % 60) + 1:02d}" for j in range(2)]
        assigned_pers = [f"P-{((i * 15 + j) % 400) + 1:04d}" for j in range(4)]
        missions.append({
            "code": mcode,
            "name": f"Operation Sentinel Watch {i}",
            "priority": priority,
            "status": "ACTIVE" if i <= 18 else "SCHEDULED",
            "start_time": (now - timedelta(hours=i % 4)).isoformat() + "Z",
            "end_time": (now + timedelta(hours=4 + i % 6)).isoformat() + "Z",
            "required_platforms": assigned_p,
            "assigned_platforms": assigned_p,
            "required_personnel": assigned_pers,
            "assigned_personnel": assigned_pers,
            "resource_demands": {"R01": 2500, "R03": 50, "R08": 2},
            "constraint_state": "AT_RISK" if i in [3, 7, 12] else "CLEAR"
        })

    # 6. Default User Accounts (One for each of the 9 roles)
    users = [
        {"id": "usr-admin", "username": "admin", "role": "Administrator", "callsign": "OVERLORD"},
        {"id": "usr-planner", "username": "planner", "role": "Operations Planner", "callsign": "STRATEGIST"},
        {"id": "usr-authority", "username": "authority", "role": "Decision Authority", "callsign": "COMMANDANT"},
        {"id": "usr-analyst", "username": "analyst", "role": "Analyst", "callsign": "SENTINEL"},
        {"id": "usr-auditor", "username": "auditor", "role": "Auditor", "callsign": "INSPECTOR"},
        {"id": "usr-pilot", "username": "pilot_01", "role": "Pilot", "callsign": "MAVERICK"},
        {"id": "usr-craft", "username": "craft_officer", "role": "Craft Officer", "callsign": "CHIEF-AIR"},
        {"id": "usr-supply", "username": "supply_officer", "role": "Supply Officer", "callsign": "QUARTERMASTER"},
        {"id": "usr-personnel", "username": "personnel_officer", "role": "Personnel Officer", "callsign": "ADJUTANT"},
    ]
    # Standard evaluator password for hackathon
    std_pass_hash = hash_password("AERIS_Pass_2026!")
    for u in users:
        u["hashed_password"] = std_pass_hash
        u["mfa_secret"] = "JBSWY3DPEHPK3PXP" # Base32 test secret
        u["mfa_enabled"] = True
        u["force_password_change"] = False

    return {
        "bases": bases,
        "aircraft": aircraft,
        "personnel": personnel,
        "resources": resources,
        "missions": missions,
        "users": users
    }
"""

    return files

print("backend_models_services.py loaded")
