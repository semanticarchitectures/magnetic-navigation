from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Tuple

from src.vehicle.aircraft import State

@dataclass
class NavigationCommand:
    speed: float
    heading: float
    altitude: float

class Navigator(ABC):
    """
    Abstract base class for navigation algorithms.
    """
    
    @abstractmethod
    def get_command(self, current_state: State) -> NavigationCommand:
        """
        Calculates the next navigation command based on the current state.
        
        Args:
            current_state: The current state of the aircraft.
            
        Returns:
            NavigationCommand: The commanded speed, heading, and altitude.
        """
        pass
