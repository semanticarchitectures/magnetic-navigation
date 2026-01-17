import numpy as np
from src.vehicle.aircraft import Aircraft, State
from src.navigation.waypoint import WaypointNavigator

def debug_simulation():
    # Setup Aircraft
    # Start at (100, 100)
    initial_state = State(x=100.0, y=100.0, z=100.0, psi=0.0, v=50.0)
    aircraft = Aircraft(initial_state)
    
    # Setup Navigator
    waypoints = [
        (100.0, 4000.0, 100.0),   # North
        (4000.0, 4000.0, 100.0),  # East
        (4000.0, 100.0, 100.0),   # South
        (100.0, 100.0, 100.0)     # West (back to start)
    ]
    navigator = WaypointNavigator(waypoints, speed=60.0, acceptance_radius=100.0)
    
    dt = 0.5
    duration = 500.0
    steps = int(duration / dt)
    
    print(f"Starting simulation. Steps: {steps}")
    
    for i in range(steps):
        # State before update
        s = aircraft.state
        dist_to_wp = np.linalg.norm([
            waypoints[navigator.current_waypoint_index][0] - s.x,
            waypoints[navigator.current_waypoint_index][1] - s.y
        ]) if navigator.current_waypoint_index < len(waypoints) else 0.0
        
        if i % 100 == 0 or dist_to_wp < 200:
            print(f"Step {i}: Pos=({s.x:.1f}, {s.y:.1f}), Psi={s.psi:.2f}, WP_Idx={navigator.current_waypoint_index}, Dist={dist_to_wp:.1f}")

        # Gets command
        cmd = navigator.get_command(aircraft.state)
        
        # Update
        aircraft.update(dt, commanded_speed=cmd.speed, commanded_heading=cmd.heading, commanded_altitude=cmd.altitude)

        if s.x > 10000:
            print(f"Step {i}: OVERSHOOT! Pos=({s.x:.1f}, {s.y:.1f})")
            break

if __name__ == "__main__":
    debug_simulation()
