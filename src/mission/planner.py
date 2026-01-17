import numpy as np
from dataclasses import dataclass
from typing import List, Tuple

@dataclass
class Waypoint:
    x: float
    y: float
    z: float

class LawnmowerPattern:
    """
    Generates a lawnmower survey pattern.
    """
    def __init__(self, bounds: Tuple[float, float, float, float], spacing: float, altitude: float):
        """
        Args:
            bounds: (min_x, max_x, min_y, max_y)
            spacing: Distance between parallel tracks (meters).
            altitude: Flight altitude (meters).
        """
        self.min_x, self.max_x, self.min_y, self.max_y = bounds
        self.spacing = spacing
        self.altitude = altitude

    def generate(self) -> List[Waypoint]:
        """
        Generates the list of waypoints.
        """
        waypoints = []
        
        # Calculate number of passes
        width = self.max_x - self.min_x
        num_passes = int(np.ceil(width / self.spacing))
        
        # We sweep along Y (North-South) and step along X (East-West)
        for i in range(num_passes):
            x = self.min_x + i * self.spacing
            
            # Ensure we stay within bounds
            if x > self.max_x:
                x = self.max_x
            
            # Alternate direction
            if i % 2 == 0:
                # Go North (min_y -> max_y)
                waypoints.append(Waypoint(x, self.min_y, self.altitude))
                waypoints.append(Waypoint(x, self.max_y, self.altitude))
            else:
                # Go South (max_y -> min_y)
                waypoints.append(Waypoint(x, self.max_y, self.altitude))
                waypoints.append(Waypoint(x, self.min_y, self.altitude))
                
        return waypoints
