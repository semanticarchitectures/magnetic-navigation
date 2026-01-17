import numpy as np
from scipy.interpolate import griddata
from typing import Tuple

class MapReconstructor:
    """
    Reconstructs a grid map from scattered data points.
    """
    @staticmethod
    def reconstruct(x_points: np.ndarray, y_points: np.ndarray, values: np.ndarray, 
                   grid_bounds: Tuple[float, float, float, float], resolution: float) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """
        Args:
            x_points: 1D array of x coordinates.
            y_points: 1D array of y coordinates.
            values: 1D array of measured values.
            grid_bounds: (min_x, max_x, min_y, max_y)
            resolution: Grid resolution.
            
        Returns:
            (grid_x, grid_y, grid_z) where grid_z is the interpolated map.
        """
        min_x, max_x, min_y, max_y = grid_bounds
        
        # Create target grid
        xi = np.linspace(min_x, max_x, int((max_x - min_x) / resolution))
        yi = np.linspace(min_y, max_y, int((max_y - min_y) / resolution))
        grid_x, grid_y = np.meshgrid(xi, yi)
        
        # Interpolate
        # 'cubic' is good for smooth fields, but 'linear' is more robust to sparsity.
        # Let's use 'linear' generally, or 'nearest' if very sparse.
        grid_z = griddata((x_points, y_points), values, (grid_x, grid_y), method='linear')
        
        return grid_x, grid_y, grid_z
