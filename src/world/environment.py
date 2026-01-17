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
        Generates a synthetic magnetic map using multi-scale filtered noise
        to mimic geological features (less periodic, more random/fractal).
        Values are in nanoTesla (nT).
        """
        from scipy.ndimage import gaussian_filter
        
        width_px = int(self.config.width / self.config.resolution)
        height_px = int(self.config.height / self.config.resolution)
        
        # Base field (Earth's background field, e.g., ~50,000 nT)
        self.background_field = 50000.0
        self.magnetic_map = np.full((height_px, width_px), self.background_field)
        
        # Multi-scale noise parameters (Scale in pixels, Amplitude in nT)
        # Assuming 10m resolution, 5000m width -> 500px
        scales = [
            (100.0, 500.0), # Large geological structures (1km)
            (25.0, 150.0),  # Mid-size features (250m)
            (5.0, 40.0),    # Finer details (50m)
            (1.0, 5.0)      # High freq noise
        ]
        
        for sigma, amplitude in scales:
            # Generate random white noise
            noise = self.rng.standard_normal((height_px, width_px))
            # Smooth it
            filtered = gaussian_filter(noise, sigma=sigma)
            # Normalize and scale
            if filtered.max() > filtered.min():
                filtered = (filtered - filtered.mean()) / (filtered.std() + 1e-6)
            
            self.magnetic_map += filtered * amplitude

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
