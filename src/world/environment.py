import numpy as np
from dataclasses import dataclass
from typing import Tuple, Optional

@dataclass
class MapConfig:
    width: float  # meters
    height: float # meters
    resolution: float # meters per pixel
    seed: Optional[int] = None

class World:
    """
    Represents the physical world and the magnetic environment.
    """
    def __init__(self, config: MapConfig):
        self.config = config
        self.rng = np.random.default_rng(config.seed)
        self._generate_magnetic_map()

    def _generate_magnetic_map(self):
        """
        Generates a synthetic magnetic map.
        Currently uses a simple combination of sine waves to simulate anomalies.
        Values are in nanoTesla (nT).
        """
        x = np.linspace(0, self.config.width, int(self.config.width / self.config.resolution))
        y = np.linspace(0, self.config.height, int(self.config.height / self.config.resolution))
        self.xx, self.yy = np.meshgrid(x, y)
        
        # Base field (Earth's background field, e.g., ~50,000 nT)
        self.background_field = 50000.0
        
        # Synthetic anomalies
        # Multiple frequencies to mimic geological features
        f1 = np.sin(2 * np.pi * self.xx / 2000) * np.cos(2 * np.pi * self.yy / 2000) * 500
        f2 = np.sin(2 * np.pi * self.xx / 500) * np.sin(2 * np.pi * self.yy / 500) * 100
        f3 = self.rng.normal(0, 5, self.xx.shape) # Sensor noise / small variations
        
        self.magnetic_map = self.background_field + f1 + f2 + f3

    def get_magnetic_field(self, x: float, y: float, z: float) -> float:
        """
        Returns the scalar magnetic intensity at the given position.
        
        Args:
            x: Easting (meters)
            y: Northing (meters)
            z: Altitude (meters) - Currently ignored for 2D map, but interface ready.
            
        Returns:
            Magnetic intensity in nT.
        """
        # Simple nearest neighbor or bilinear interpolation could be used here.
        # For now, let's just map to grid indices.
        
        idx_x = int(x / self.config.resolution)
        idx_y = int(y / self.config.resolution)
        
        # Boundary checks
        if 0 <= idx_x < self.magnetic_map.shape[1] and 0 <= idx_y < self.magnetic_map.shape[0]:
            return self.magnetic_map[idx_y, idx_x]
        else:
            return self.background_field # Return background if out of bounds

    def get_map_bounds(self) -> Tuple[float, float, float, float]:
        """Returns (min_x, max_x, min_y, max_y)"""
        return (0.0, self.config.width, 0.0, self.config.height)
