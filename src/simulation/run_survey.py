import numpy as np
import matplotlib.pyplot as plt
from src.world.environment import World, MapConfig
from src.vehicle.aircraft import Aircraft, State
from src.sensors.magnetometer import Magnetometer
from src.mission.planner import LawnmowerPattern
from src.world.reconstruction import MapReconstructor

def run_survey(num_passes):
    # 1. Setup World
    width = 5000.0
    height = 5000.0
    config = MapConfig(width=width, height=height, resolution=10.0, seed=123)
    world = World(config)
    
    # 2. Setup Pattern
    spacing = width / num_passes
    print(f"Running survey with {num_passes} passes (spacing={spacing:.1f}m)...")
    
    planner = LawnmowerPattern(bounds=(0, width, 0, height), spacing=spacing, altitude=100.0)
    waypoints = planner.generate()
    
    # 3. Setup Aircraft & Sensor
    start_wp = waypoints[0]
    initial_state = State(x=start_wp.x, y=start_wp.y, z=start_wp.z, psi=0, v=50.0)
    aircraft = Aircraft(initial_state)
    mag = Magnetometer(noise_std=5.0)
    
    # 4. Run Loop
    dt = 0.5
    collected_x = []
    collected_y = []
    collected_vals = []
    
    # Simple waypoint following logic
    current_wp_idx = 0
    flight_speed = 50.0
    max_steps = 200000 
    
    for step in range(max_steps):
        if current_wp_idx >= len(waypoints):
            break
            
        target = waypoints[current_wp_idx]
        
        dx = target.x - aircraft.state.x
        dy = target.y - aircraft.state.y
        dist = np.sqrt(dx*dx + dy*dy)
        
        if dist < 10.0:
            current_wp_idx += 1
            continue
            
        heading = np.arctan2(dx, dy)
        aircraft.update(dt, commanded_speed=flight_speed, commanded_heading=heading, commanded_altitude=target.z)
        
        if step % 2 == 0:
            val = mag.read(world, *aircraft.get_position())
            collected_x.append(aircraft.state.x)
            collected_y.append(aircraft.state.y)
            collected_vals.append(val)
            
    return world, np.array(collected_x), np.array(collected_y), np.array(collected_vals)

def compare_maps(world, obs_x, obs_y, obs_vals, num_passes):
    print(f"Reconstructing map for {num_passes} passes...")
    bounds = world.get_map_bounds()
    # Use larger resolution for faster reconstruction if needed, but 20.0 is fine
    grid_x, grid_y, grid_z = MapReconstructor.reconstruct(obs_x, obs_y, obs_vals, bounds, resolution=20.0)
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 7))
    
    # Ground Truth with Path Overlay
    im1 = ax1.imshow(world.magnetic_map, origin='lower', extent=bounds, cmap='viridis')
    # Downsample path for plotting
    ax1.plot(obs_x, obs_y, 'k-', linewidth=1.0, alpha=0.8, label='Flight Path') # Black line might be more visible on bright viridis
    ax1.set_title(f"Ground Truth & Path ({num_passes} passes, {len(obs_x)} samples)")
    ax1.legend()
    plt.colorbar(im1, ax=ax1, label='nT')
    
    # Reconstructed
    im2 = ax2.imshow(grid_z, origin='lower', extent=bounds, cmap='viridis', vmin=np.nanmin(world.magnetic_map), vmax=np.nanmax(world.magnetic_map))
    ax2.set_title(f"Reconstructed Map ({num_passes} passes)")
    plt.colorbar(im2, ax=ax2, label='nT')
    
    filename = f'survey_comparison_{num_passes}passes.png'
    plt.tight_layout()
    plt.savefig(filename)
    print(f"Saved {filename}")
    plt.close(fig) # Close to free memory

if __name__ == "__main__":
    for passes in [100, 50, 25, 12, 6]:
        world, ox, oy, ov = run_survey(passes)
        compare_maps(world, ox, oy, ov, passes)
