import numpy as np
import matplotlib.pyplot as plt
from src.world.environment import World, MapConfig
from src.vehicle.aircraft import Aircraft, State
from src.sensors.magnetometer import Magnetometer

def run_simulation():
    # 1. Setup World
    config = MapConfig(width=5000, height=5000, resolution=10.0, seed=42)
    world = World(config)
    
    # 2. Setup Aircraft
    # Start at bottom-left, heading East (90 deg)
    initial_state = State(x=100.0, y=2500.0, z=100.0, psi=np.pi/2, v=50.0)
    aircraft = Aircraft(initial_state)
    
    # 3. Setup Sensor
    mag = Magnetometer(noise_std=2.0)
    
    # 4. Run Loop
    dt = 0.5
    duration = 60.0 # seconds
    steps = int(duration / dt)
    
    trajectory_x = []
    trajectory_y = []
    measurements = []
    
    for _ in range(steps):
        # Update Physics
        # Simple straight line flight
        aircraft.update(dt, commanded_speed=50.0, commanded_heading=np.pi/2, commanded_altitude=100.0)
        
        # Read Sensor
        pos = aircraft.get_position()
        val = mag.read(world, *pos)
        
        # Log
        trajectory_x.append(pos[0])
        trajectory_y.append(pos[1])
        measurements.append(val)
        
    return world, trajectory_x, trajectory_y, measurements

def plot_results(world, traj_x, traj_y, measurements):
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    
    # Plot Map and Trajectory
    extent = world.get_map_bounds()
    im = ax1.imshow(world.magnetic_map, origin='lower', extent=extent, cmap='viridis')
    ax1.plot(traj_x, traj_y, 'r-', linewidth=2, label='Flight Path')
    ax1.set_title("Flight Path over Magnetic Map")
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
    plt.savefig('simulation_result.png')
    print("Simulation result saved to simulation_result.png")

if __name__ == "__main__":
    world, tx, ty, meas = run_simulation()
    plot_results(world, tx, ty, meas)
