# Phase 2 Software Development Plan: Role Decomposition & The "Crew" Concept

## 1. Overview
Building on the "Context-Aware Agent" foundation established in Phase 1, Phase 2 focuses on **Role Decomposition**. We will transition from a single monolithic `Agent` class to a modular **Multi-Agent System (MAS)** where distinct sub-agents (Navigator, Commander, Operator) collaborate to operate the vehicle.

This architecture mimics a human flight crew and prepares the system for Phase 3, where these sub-agents will be powered by LLMs.

## 2. Objectives
1.  **Decompose the Monolith**: Refactor `src/agent/core.py` into a container that manages multiple specialized sub-agents.
2.  **Define Agent Interfaces**: Establish a standard protocol (input/output/state) for sub-agents to communicate.
3.  **Implement Specialized Roles**:
    - **Commander**: High-level goal setting and risk management.
    - **Navigator**: Pathfinding, state estimation (EKF/Particle Filter), and obstacle avoidance.
    - **Operator**: Systems monitoring, sensor health, and platform constraints.
4.  **Verification**: Demonstrate a complex scenario where agents must negotiate (e.g., Navigator requests a course change due to uncertainty, Commander approves based on mission priority).

## 3. Work Breakdown Structure (WBS)

### 3.1 Architecture Refactoring
- **Task 2.1.1**: Define `SubAgent` abstract base class.
    - Inputs: `SharedContext` subset.
    - Outputs: `Messages` or `StateUpdates`.
- **Task 2.1.2**: Create `AgentBus` or `Blackboard` for inter-agent communication.
    - Agents publish observations (e.g., "GPS signal lost").
    - Agents subscribe to relevant topics.

### 3.2 Role Implementation
- **Task 2.2.1**: Implement `NavigatorAgent`.
    - Responsibilities: Wraps the `WaypointNavigator`. Monitors `SituationContext`.
    - Logic: "If GPS variance is high, I cannot guarantee accuracy < 10m."
- **Task 2.2.2**: Implement `OperatorAgent`.
    - Responsibilities: Monitors platform battery/fuel, sensor health.
    - Logic: "Battery low, advising Return-to-Base (RTB)."
- **Task 2.2.3**: Implement `CommanderAgent`.
    - Responsibilities: Holds the `MissionContext`.
    - Logic: Arbitrates conflicts. "Mission priority is CRITICAL. Override safety warning. Continuue."

### 3.3 Simulation Integration
- **Task 2.3.1**: Create `run_crew_sim.py`.
- **Task 2.3.2**: Design a "Conflict Scenario".
    - Scenario: Low battery (Operator warning) + High Value Target (Commander priority) + Storm/Jamming (Navigator warning).
    - Goal: Observe the agents resolving the conflict.

## 4. Technical Specifications
### Directory Structure
```
src/
└── agent/
    ├── bus.py          # Message Bus
    ├── base.py         # SubAgent Interface
    ├── commander.py    # Commander Logic
    ├── navigator.py    # Navigator Logic
    ├── operator.py     # Operator Logic
    └── crew.py         # The container (formerly Agent)
```

### Protocol
**Aviation Voice Protocol**: Communication between agents will emulate standard human aviation voice traffic (e.g., BREVITY codes, standard phraseology).
- format: `[Callsign] [Recipient], [Message]`.
- example: `"Navigator, Commander. GPS Unreliable. Switch MagNav."`
- This ensures seamless integration with human operators who might listen in or participate on the same channel.

## 5. Timeline & Milestones
- **Week 1**: Architecture Refactoring (Bus & Base Classes).
- **Week 2**: Implementation of Navigator and Operator agents.
- **Week 3**: Commander Agent & Conflict Resolution Logic.
- **Week 4**: Simulation & Verification (The "Crew" Demo).

## 6. Success Criteria
- **Modular Code**: Each agent is in its own file and can be unit tested independently.
- **Communication**: Agents interact via the Bus/Blackboard, not direct hard-coded calls.
- **Behavior**: The simulation log shows a clear "dialogue" of decision making (e.g., "Operator reported Error", "Commander acknowledged").
