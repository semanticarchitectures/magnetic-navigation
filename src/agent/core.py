import numpy as np
from typing import List, Tuple
from src.agent.context import AgentContext, SituationContext, SensorStatus, NavigationMode
from src.vehicle.aircraft import Aircraft, State
from src.navigation.base import NavigationCommand
from src.navigation.waypoint import WaypointNavigator

class Agent:
    def __init__(self, context: AgentContext, aircraft: Aircraft):
        self.context = context
        self.aircraft = aircraft
        
        # Initialize sub-components
        # For now, we reuse the WaypointNavigator. 
        # In a full system, we might have multiple navigators and switch between them.
        self.navigator = WaypointNavigator(
            context.mission.waypoints, 
            speed=context.platform.max_speed * 0.8, # Cruising speed
            acceptance_radius=100.0,
            loop=True 
        )
        
        # Initialize sensor health
        for sensor in self.context.platform.sensors_list:
            self.context.situation.sensor_health[sensor] = SensorStatus.OPERATIONAL

    def update(self, dt: float, external_gps_variance: float = 0.0):
        """
        Main Agent Cycle: Monitor -> Estimate -> Decide -> Act
        
        Args:
            dt: Time step
            external_gps_variance: Injected simulation variance to test logic.
        """
        
        # 1. Monitor (Senses)
        self._monitor_sensors(external_gps_variance)
        
        # 2. Estimate (Fusion)
        self._update_estimation()
        
        # 3. Decide (Command)
        command = self._make_decisions()
        
        # 4. Act (Control)
        self.aircraft.update(dt, command.speed, command.heading, command.altitude)

    def _monitor_sensors(self, gps_variance: float):
        """
        Simulates monitoring sensor health.
        """
        self.context.situation.gps_variance = gps_variance
        
        # TTP: Detect GPS Jamming
        if gps_variance > 5.0:
            self.context.situation.sensor_health["GPS"] = SensorStatus.DEGRADED
            print(f"AGENT ALERT: GPS Variance High ({gps_variance:.1f}). Marking GPS DEGRADED.")
        else:
            self.context.situation.sensor_health["GPS"] = SensorStatus.OPERATIONAL

    def _update_estimation(self):
        """
        Updates the estimated state.
        Realistically this would be a Kalman Filter.
        For now, we just pass through the aircraft Truth state, 
        potentially degrading it if we wanted to simulate error.
        """
        self.context.situation.estimated_state = self.aircraft.state

    def _make_decisions(self) -> NavigationCommand:
        """
        Applies TTPs to generate commands.
        """
        
        # TTP: Select Navigation Mode based on Sensor Health
        if self.context.situation.sensor_health.get("GPS") == SensorStatus.DEGRADED:
            if self.context.situation.current_nav_mode != NavigationMode.MAG_NAV:
                print("AGENT DECISION: Switching to MAG_NAV due to GPS degradation.")
                self.context.situation.current_nav_mode = NavigationMode.MAG_NAV
        else:
            if self.context.situation.current_nav_mode != NavigationMode.GPS:
                print("AGENT DECISION: GPS Healthy. Switching back to GPS.")
                self.context.situation.current_nav_mode = NavigationMode.GPS
                
        # Execute Navigation Strategy based on Mode
        if self.context.situation.current_nav_mode == NavigationMode.MAG_NAV:
            # TTP: In MagNav mode, maybe we fly slower or do a specific maneuver?
            # For this simple demo, we just use the same waypoint navigator 
            # but we could swap the navigator instance here.
            cmd = self.navigator.get_command(self.context.situation.estimated_state)
            # Maybe fly lower for better signal?
            cmd.altitude = 50.0 
        else:
            # Standard Ops
            cmd = self.navigator.get_command(self.context.situation.estimated_state)
            
        return cmd
