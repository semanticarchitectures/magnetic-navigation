import numpy as np
from typing import List, Tuple
from src.vehicle.aircraft import State
from src.navigation.base import Navigator, NavigationCommand

class WaypointNavigator(Navigator):
    """
    Navigates through a sequence of 3D waypoints.
    """
    def __init__(self, waypoints: List[Tuple[float, float, float]], speed: float = 50.0, acceptance_radius: float = 50.0, loop: bool = False):
        """
        Args:
            waypoints: List of (x, y, z) tuples.
            speed: Desired cruising speed (m/s).
            acceptance_radius: Distance (m) to waypoint to consider it reached.
            loop: If True, restart sequence from beginning when finished.
        """
        self.waypoints = waypoints
        self.speed = speed
        self.acceptance_radius = acceptance_radius
        self.loop = loop
        self.current_waypoint_index = 0
        
    def get_command(self, current_state: State) -> NavigationCommand:
        target_x, target_y, target_z = self.waypoints[min(self.current_waypoint_index, len(self.waypoints)-1)]

        # Check if we have passed all waypoints and are effectively "done" (needing loiter)
        # Note: We check if we are AT the last waypoint inside the reach check below.
        
        dx = target_x - current_state.x
        dy = target_y - current_state.y
        dist = np.sqrt(dx**2 + dy**2)
        
        # Check if reached
        if dist < self.acceptance_radius:
            # We reached the target.
            
            # If we were targeting the last waypoint:
            if self.current_waypoint_index >= len(self.waypoints) - 1:
                if self.loop:
                    self.current_waypoint_index = 0
                else:
                    # Loiter mode: Just circle around the target (or just constant turn)
                    # Simple loiter: turn rate.
                    # Let's just command a heading that changes.
                    # Or simpler: return a command with a specialized "turn rate" if our interface supported it.
                    # Since we only return heading, we simulate a turn by commanding current_heading + small_delta
                    return NavigationCommand(speed=self.speed, heading=current_state.psi + 0.2, altitude=target_z)
            else:
                self.current_waypoint_index += 1
            
            # Update target to new index
            target_x, target_y, target_z = self.waypoints[self.current_waypoint_index]
            dx = target_x - current_state.x
            dy = target_y - current_state.y
            
        target_heading = np.arctan2(dx, dy)
        
        return NavigationCommand(speed=self.speed, heading=target_heading, altitude=target_z)
