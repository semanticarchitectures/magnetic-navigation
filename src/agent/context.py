from dataclasses import dataclass, field
from typing import List, Tuple, Dict, Optional
from enum import Enum
from src.vehicle.aircraft import State

class SensorStatus(Enum):
    OPERATIONAL = "OPERATIONAL"
    DEGRADED = "DEGRADED"
    FAILED = "FAILED"
    UNKNOWN = "UNKNOWN"

class NavigationMode(Enum):
    GPS = "GPS"
    MAG_NAV = "MAG_NAV"
    DEAD_RECKONING = "DEAD_RECKONING"

@dataclass
class OrganizationContext:
    squadron_name: str
    callsign: str
    command_frequency: float

@dataclass
class PlatformContext:
    max_speed: float
    max_altitude: float
    sensors_list: List[str]

@dataclass
class MissionContext:
    objectives: List[str]
    waypoints: List[Tuple[float, float, float]] # x, y, z
    risk_tolerance: float # 0.0 to 1.0

@dataclass
class SituationContext:
    estimated_state: State
    sensor_health: Dict[str, SensorStatus] = field(default_factory=dict)
    active_threats: List[str] = field(default_factory=list)
    current_nav_mode: NavigationMode = NavigationMode.GPS
    gps_variance: float = 0.0 # Simulated metric for jamming detection

@dataclass
class AgentContext:
    organization: OrganizationContext
    platform: PlatformContext
    mission: MissionContext
    situation: SituationContext
