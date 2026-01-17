import numpy as np
from dataclasses import dataclass

@dataclass
class State:
    x: float = 0.0 # Easting
    y: float = 0.0 # Northing
    z: float = 0.0 # Altitude (ASL)
    psi: float = 0.0 # Heading (yaw) in radians, 0 = North? Standard math: 0=East. 
                     # Let's standardize: 0 = North, clockwise positive.
    v: float = 0.0 # Speed m/s

class Aircraft:
    """
    Simulates a fixed-wing aircraft with simple 2D kinematics + altitude.
    """
    def __init__(self, initial_state: State = State()):
        self.state = initial_state
        self.dt = 0.1 # Time step

    def update(self, dt: float, commanded_speed: float, commanded_heading: float, commanded_altitude: float):
        """
        Updates the aircraft state based on commands.
        
        Args:
            dt: Time delta.
            commanded_speed: Target speed (m/s).
            commanded_heading: Target heading (radians).
            commanded_altitude: Target altitude (m).
        """
        self.dt = dt
        
        # Simple proportional control / physics
        # Assume instant response for now for simplicity, or add simple lag
        self.state.v = commanded_speed
        self.state.psi = commanded_heading # Turn rate limit could be added here
        
        # Kinematics
        # If 0 heading is North (Y axis) and clockwise is positive:
        # Vx = V * sin(psi)
        # Vy = V * cos(psi)
        
        # Standard navigation frame:
        # X: East, Y: North
        # Heading 0 -> North -> vy = v, vx = 0
        # Heading 90 -> East -> vy = 0, vx = v
        # vx = v * sin(psi)
        # vy = v * cos(psi)
        
        vx = self.state.v * np.sin(self.state.psi)
        vy = self.state.v * np.cos(self.state.psi)
        
        self.state.x += vx * dt
        self.state.y += vy * dt
        
        # Altitude change
        vz = (commanded_altitude - self.state.z) * 0.1 # Simple P controller for climb
        self.state.z += vz * dt

    def get_position(self):
        return self.state.x, self.state.y, self.state.z
