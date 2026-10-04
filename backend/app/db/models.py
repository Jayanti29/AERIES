from sqlalchemy import Column, Integer, String, Boolean, Float, DateTime, ForeignKey, Text, JSON
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
