import numpy as np
import matplotlib.pyplot as plt
from src.world.environment import World, MapConfig
from src.vehicle.aircraft import Aircraft, State
from src.agent.context import AgentContext, OrganizationContext, PlatformContext, MissionContext, SituationContext
from src.agent.core import Agent

def run_agent_simulation():
    # 1. Setup World
    config = MapConfig(width=5000, height=5000, resolution=10.0, seed=42)
    world = World(config)
    
    # 2. Setup Aircraft
    initial_state = State(x=100.0, y=100.0, z=100.0, psi=0.0, v=50.0)
    aircraft = Aircraft(initial_state)
    
    # 3. Setup Agent Context
    org = OrganizationContext("Red Tails", "Red-1", 123.45)
    platform = PlatformContext(max_speed=100.0, max_altitude=1000.0, sensors_list=["GPS", "Magnetometer"])
    
    waypoints = [
        (100.0, 4000.0, 100.0),   
        (4000.0, 4000.0, 100.0), 
        (4000.0, 100.0, 100.0),  
        (100.0, 100.0, 100.0)    
    ]
    mission = MissionContext(objectives=["Patrol"], waypoints=waypoints, risk_tolerance=0.5)
    situation = SituationContext(estimated_state=initial_state)
    
    context = AgentContext(org, platform, mission, situation)
    
    # 4. Initialize Agent
    agent = Agent(context, aircraft)
    
    # 5. Run Loop
    dt = 0.5
    duration = 600.0 
    steps = int(duration / dt)
    
    trajectory_x = []
    trajectory_y = []
    trajectory_z = []
    modes = []
    
    print("Starting Agent Simulation...")
    
    for i in range(steps):
        # Simulate environment conditions
        # Inject GPS "Jamming" (Variance spike) between t=200 and t=400
        current_time = i * dt
        gps_variance = 0.1
        if 200.0 < current_time < 400.0:
            gps_variance = 10.0 # High noise!
            
        # Update Agent
        agent.update(dt, external_gps_variance=gps_variance)
        
        # Log
        pos = aircraft.get_position()
        trajectory_x.append(pos[0])
        trajectory_y.append(pos[1])
        trajectory_z.append(pos[2])
        modes.append(agent.context.situation.current_nav_mode.value)
        
    return world, trajectory_x, trajectory_y, trajectory_z, waypoints, modes

def plot_results(world, traj_x, traj_y, traj_z, waypoints, modes):
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
    
    # Plot Map and Trajectory
    extent = world.get_map_bounds()
    im = ax1.imshow(world.magnetic_map, origin='lower', extent=extent, cmap='viridis')
    
    # Color code trajectory by mode
    # Simple trick: plot segment by segment or just overlay?
    # Let's plot main line black, and overlay dots?
    ax1.plot(traj_x, traj_y, 'k-', linewidth=1, label='Path', alpha=0.5)
    
    # Create mask for MagNav
    mag_indices = [i for i, m in enumerate(modes) if m == "MAG_NAV"]
    gps_indices = [i for i, m in enumerate(modes) if m == "GPS"]
    
    if mag_indices:
        ax1.scatter([traj_x[i] for i in mag_indices], [traj_y[i] for i in mag_indices], c='orange', s=2, label='MagNav Mode')
    if gps_indices:
        ax1.scatter([traj_x[i] for i in gps_indices], [traj_y[i] for i in gps_indices], c='blue', s=2, label='GPS Mode')

    # Waypoints
    wx, wy = zip(*[(p[0], p[1]) for p in waypoints])
    ax1.scatter(wx, wy, c='white', marker='x', s=100, label='Waypoints')
    
    ax1.set_title("Agent Trajectory with Mode Switching")
    ax1.set_xlabel("Easting (m)")
    ax1.set_ylabel("Northing (m)")
    ax1.legend()
    
    # Plot Altitude to show behavioral change
    ax2.plot(traj_z)
    ax2.set_title("Altitude Profile")
    ax2.set_xlabel("Time Step")
    ax2.set_ylabel("Altitude (m)")
    ax2.grid(True)
    # Highlight regions
    ax2.text(100, 110, "Standard GPS Cruise", color='blue')
    ax2.text(500, 60, "MagNav Low-Fly", color='orange')
    
    plt.tight_layout()
    plt.savefig('agent_simulation.png')
    print("Simulation result saved to agent_simulation.png")

if __name__ == "__main__":
    world, tx, ty, tz, wps, modes = run_agent_simulation()
    plot_results(world, tx, ty, tz, wps, modes)
