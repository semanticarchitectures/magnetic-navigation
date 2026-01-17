import numpy as np
from src.world.environment import World

class Magnetometer:
    """
    Simulates a scalar magnetometer.
    """
    def __init__(self, noise_std: float = 0.1, bias: float = 0.0):
        self.noise_std = noise_std
        self.bias = bias
        self.rng = np.random.default_rng()

    def read(self, world: World, x: float, y: float, z: float) -> float:
        """
        Takes a reading from the world at the given position.
        
        Args:
            world: The World object containing the magnetic map.
            x, y, z: Position.
            
        Returns:
            Measured magnetic field intensity (nT).
        """
        true_value = world.get_magnetic_field(x, y, z)
        
        noise = self.rng.normal(0, self.noise_std)
        reading = true_value + self.bias + noise
        
        return reading
