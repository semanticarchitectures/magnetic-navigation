import numpy as np
import matplotlib.pyplot as plt
from src.world.environment import World, MapConfig
from src.vehicle.aircraft import Aircraft, State
from src.sensors.magnetometer import Magnetometer
from src.navigation.waypoint import WaypointNavigator

def run_simulation():
    # 1. Setup World
    config = MapConfig(width=5000, height=5000, resolution=10.0, seed=42)
    world = World(config)
    
    # 2. Setup Aircraft
    # Start at (100, 100)
    initial_state = State(x=100.0, y=100.0, z=100.0, psi=0.0, v=50.0)
    aircraft = Aircraft(initial_state)
    
    # 3. Setup Navigator
    # Define a simple square pattern
    waypoints = [
        (100.0, 4000.0, 100.0),   # North
        (4000.0, 4000.0, 100.0),  # East
        (4000.0, 100.0, 100.0),   # South
        (100.0, 100.0, 100.0)     # West (back to start)
    ]
    navigator = WaypointNavigator(waypoints, speed=60.0, acceptance_radius=100.0)
    
    # 4. Setup Sensor
    mag = Magnetometer(noise_std=2.0)
    
    # 5. Run Loop
    dt = 0.5
    duration = 500.0 # Enough time to fly the square
    steps = int(duration / dt)
    
    trajectory_x = []
    trajectory_y = []
    trajectory_z = []
    measurements = []
    
    for _ in range(steps):
        # 1. Get Navigation Command
        cmd = navigator.get_command(aircraft.state)
        
        # 2. Update Physics
        aircraft.update(dt, commanded_speed=cmd.speed, commanded_heading=cmd.heading, commanded_altitude=cmd.altitude)
        
        # 3. Read Sensor
        pos = aircraft.get_position()
        val = mag.read(world, *pos)
        
        # 4. Log
        trajectory_x.append(pos[0])
        trajectory_y.append(pos[1])
        trajectory_z.append(pos[2])
        measurements.append(val)
        
    return world, trajectory_x, trajectory_y, measurements, waypoints

def plot_results(world, traj_x, traj_y, measurements, waypoints):
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
    
    # Plot Map and Trajectory
    extent = world.get_map_bounds()
    im = ax1.imshow(world.magnetic_map, origin='lower', extent=extent, cmap='viridis')
    
    # Plot Waypoints
    wx, wy = zip(*[(p[0], p[1]) for p in waypoints])
    ax1.scatter(wx, wy, c='white', marker='x', s=100, label='Waypoints')
    
    ax1.plot(traj_x, traj_y, 'r-', linewidth=2, label='Flight Path')
    ax1.set_title("Navigation Test: Square Pattern")
    ax1.set_xlabel("Easting (m)")
    ax1.set_ylabel("Northing (m)")
    ax1.legend()
    plt.colorbar(im, ax=ax1, label='Magnetic Intensity (nT)')
    
    # Plot Measurements
    ax2.plot(measurements)
    ax2.set_title("Magnetometer Readings")
    ax2.set_xlabel("Time Step")
    ax2.set_ylabel("Intensity (nT)")
    ax2.grid(True)
    
    plt.tight_layout()
    plt.savefig('nav_simulation_result.png')
    print("Simulation result saved to nav_simulation_result.png")

if __name__ == "__main__":
    world, tx, ty, meas, wps = run_simulation()
    plot_results(world, tx, ty, meas, wps)
