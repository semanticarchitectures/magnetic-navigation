# Agent Evolution Roadmap: From Rules to Collaborative LLMs

This roadmap outlines the strategic evolution of the `antigravity` agent architecture from its current Python-based logic to a fully realized Collaborative Multi-Agent System (MAS) utilizing LLMs.

## Phase 1: Structured Foundation (Current Status)
**Goal:** Establish the data structures required for "Cognitive" agents.
- [x] **Context Definition**: `AgentContext`, `Situation`, `Mission` data classes defined.
- [x] **Basic Loop**: `Monitor` -> `Estimate` -> `Decide` -> `Act` cycle implemented.
- [x] **Rule-Based TTPs**: Hardcoded logic (e.g., "If GPS variance > 5, switch mode").
- **Why this matters for LLMs**: LLMs require structured, serializable text context to make decisions. Our `Context` object can be directly serialized to JSON for prompting.

## Phase 2: Role Decomposition (The "Crew" Concept)
**Goal:** Break the monolithic `Agent` into specialized roles, mirroring a human flight crew.
- [ ] **Navigator Agent**: Responsible purely for pathfinding and state estimation.
- [ ] **System Operator**: Responsible for sensor health and platform constraints.
- [ ] **Commander Agent**: Responsible for mission goals and risk acceptance.
- [ ] **Architecture Change**: The `Agent` class becomes a container/bus for these sub-agents.

## Phase 3: Hybrid Neuro-Symbolic Minds (LLM Integration)
**Goal:** Introduce LLM reasoning for complex, low-frequency decisions (Strategy), while keeping Python for high-frequency control (Reflexes).
- [ ] **The "Slow" Loop (1Hz - 0.1Hz)**:
    - The `Commander` agent sends the `SituationContext` JSON to an LLM.
    - Prompt: *"You are the Mission Commander. GPS is degrading. Risk tolerance is Low. Recommend course of action."*
    - Output: Structured reconfiguration commands (e.g., "Switch to MagNav", "Abort to Loiter").
- [ ] **The "Fast" Loop (10-100Hz)**:
    - Pure Python control loops (`WaypointNavigator`, PID controllers) execute the current strategy.

## Phase 4: Collaborative Multi-Agent System (MAS)
**Goal:** Enable conversation and negotiation between agents.
- [ ] **Message Bus**: Agents publish messages (e.g., `NavAgent`: "Confidence dropping.", `CommsAgent`: "I have intermittent link.").
- [ ] **LLM Protocol**: Implement a protocol (like AutoGen or CrewAI concepts) where agents "discuss" a problem before acting.
    - *Example*:
        - **Navigator**: "I cannot guarantee position accuracy > 100m."
        - **Mission**: "That violates safety protocols for this sector."
        - **Navigator**: "Request update to 'High Altitude' mode to regain GPS."
        - **Commander**: "Approved."

## Phase 5: Organization-Level Swarms
**Goal:** Multiple platforms (Aircraft A, Aircraft B) collaborating.
- [ ] **Shared Context**: `OrganizationContext` expands to include live status of peers.
- [ ] **Distributed Solving**: "Aircraft A has lost sensors, Aircraft B guides it home."

## Next Immediate Steps
1. Refactor `Agent` core to support a pluggable "Brain" interface (so we can swap `_make_decisions` with an LLM call).
2. Create a conceptual `LLMPlanner` that takes a `MissionContext` and outputs a `Waypoint` list.
