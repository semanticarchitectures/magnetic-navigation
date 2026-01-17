import numpy as np
from typing import List, Tuple
from src.vehicle.aircraft import State
from src.navigation.base import Navigator, NavigationCommand

class WaypointNavigator(Navigator):
    """
    Navigates through a sequence of 3D waypoints.
    """
    def __init__(self, waypoints: List[Tuple[float, float, float]], speed: float = 50.0, acceptance_radius: float = 50.0):
        """
        Args:
            waypoints: List of (x, y, z) tuples.
            speed: Desired cruising speed (m/s).
            acceptance_radius: Distance (m) to waypoint to consider it reached.
        """
        self.waypoints = waypoints
        self.speed = speed
        self.acceptance_radius = acceptance_radius
        self.current_waypoint_index = 0
        
    def get_command(self, current_state: State) -> NavigationCommand:
        if self.current_waypoint_index >= len(self.waypoints):
            # Mission complete, encircle last point or just hold last heading? 
            # For now, let's just hold position/circle or fly straight. 
            # Let's fly straight at current heading and altitude.
            return NavigationCommand(speed=self.speed, heading=current_state.psi, altitude=current_state.z)
            
        target_x, target_y, target_z = self.waypoints[self.current_waypoint_index]
        
        dx = target_x - current_state.x
        dy = target_y - current_state.y
        dist = np.sqrt(dx**2 + dy**2)
        
        # Check if reached
        if dist < self.acceptance_radius:
            self.current_waypoint_index += 1
            if self.current_waypoint_index >= len(self.waypoints):
                 return NavigationCommand(speed=self.speed, heading=current_state.psi, altitude=target_z)
            # Recalculate for next waypoint immediately
            target_x, target_y, target_z = self.waypoints[self.current_waypoint_index]
            dx = target_x - current_state.x
            dy = target_y - current_state.y
            
        # Calculate desired heading
        # Angle from North (Y axis) clockwise positive?
        # Standard math atan2(y, x) gives angle from East (0) counter-clockwise.
        # Aircraft model uses: 0=North, clockwise+.
        # Let's be careful.
        # Vector is (dx, dy).
        # We want angle PSI such that:
        # dx_norm = sin(PSI)
        # dy_norm = cos(PSI)
        # -> PSI = atan2(dx, dy)
        
        target_heading = np.arctan2(dx, dy)
        
        return NavigationCommand(speed=self.speed, heading=target_heading, altitude=target_z)
