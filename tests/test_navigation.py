import unittest
import numpy as np
from src.vehicle.aircraft import State
from src.navigation.waypoint import WaypointNavigator

class TestWaypointNavigator(unittest.TestCase):
    
    def test_initial_heading(self):
        # Start at (0,0), target (100, 100). Should be 45 deg (pi/4) or something similar depending on convention.
        # Navigator uses atan2(dx, dy) which corresponds to 0=North (Y+), Clockwise+
        # Target (100, 100) -> dx=100, dy=100 -> atan2(100, 100) = pi/4 (45 deg)
        waypoints = [(100.0, 100.0, 50.0)]
        nav = WaypointNavigator(waypoints)
        state = State(x=0.0, y=0.0, z=0.0, psi=0.0)
        
        cmd = nav.get_command(state)
        
        self.assertAlmostEqual(cmd.heading, np.pi/4, places=2)
        self.assertEqual(cmd.altitude, 50.0)

    def test_waypoint_sequencing(self):
        # Waypoints: (0, 100) [North], then (100, 100) [East]
        waypoints = [(0.0, 100.0, 50.0), (100.0, 100.0, 50.0)]
        nav = WaypointNavigator(waypoints, acceptance_radius=10.0)
        
        # 1. Start at origin, should head North (0 deg)
        state = State(x=0.0, y=0.0, z=50.0)
        cmd = nav.get_command(state)
        self.assertAlmostEqual(cmd.heading, 0.0, places=2) # atan2(0, 100) = 0
        
        # 2. Arrive at first waypoint
        state = State(x=0.0, y=100.0, z=50.0)
        cmd = nav.get_command(state)
        
        # Should now target second waypoint (100, 100)
        # From (0, 100) to (100, 100) is East (+X)
        # dx=100, dy=0 -> atan2(100, 0) = pi/2 (90 deg)
        self.assertAlmostEqual(cmd.heading, np.pi/2, places=2)
        
    def test_completion_behavior(self):
        waypoints = [(10.0, 0.0, 10.0)]
        nav = WaypointNavigator(waypoints, acceptance_radius=5.0)
        
        # Arrive
        state = State(x=10.0, y=0.0, z=10.0, psi=1.5)
        cmd = nav.get_command(state)
        
        # Should return maintain current heading (or whatever logic we chose)
        # The logic was: keep last heading if done.
        # Actually logic in code: return NavigationCommand(speed=self.speed, heading=current_state.psi, altitude=current_state.z)
        self.assertEqual(cmd.heading, 1.5)

if __name__ == '__main__':
    unittest.main()
