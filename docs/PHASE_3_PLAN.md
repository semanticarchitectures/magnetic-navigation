# Phase 3 Software Development Plan: Hybrid Neuro-Symbolic Minds

## 1. Overview
Phase 3 introduces **Large Language Models (LLMs)** into the agent architecture. We move from hard-coded "Rule-Based" TTPs to "Neuro-Symbolic" agents where an LLM provides strategic reasoning based on context, while Python handles high-frequency control.

## 2. Objectives
1.  **Abstract the Brain**: Create a pluggable `Brain` interface for agents.
2.  **LLM Integration**: Implement an `LLMClient` that can send `AgentContext` (as JSON) and receive structured commands.
3.  **Strategic Commander**: Upgrade the `CommanderAgent` to use the LLM for decision making during critical events (e.g., "GPS Jamming detected").
4.  **Mocking for deterministic testing**: Ensure we can mock the LLM for reliable unit tests.

## 3. Work Breakdown Structure

### 3.1 Core Infrastructure
- **Task 3.1.1**: Define `LLMInterface` abstract base class.
    - Method: `generate_response(system_prompt, user_context) -> str`.
- **Task 3.1.2**: Implement `MockLLMClient` for testing.
    - Returns predefined responses based on keywords in the prompt.
- **Task 3.1.3**: Define `CognitiveService`.
    - Wrapper that handles prompt engineering: building the "Persona" (Commander) and formatting the JSON context.

### 3.2 Agent Upgrades
- **Task 3.2.1**: Refactor `CommanderAgent` to hold a `CognitiveService`.
- **Task 3.2.2**: Replace hardcoded `receive_message` logic with:
    1. Parse incoming message.
    2. Update internal `SituationContext`.
    3. Trigger `CognitiveService.decide(context)`.
    4. Parse LLM output (e.g., JSON command `{"action": "ORDER_SWITCH_MAGNAV"}`).
    5. Publish result to Bus.

### 3.3 Simulation
- **Task 3.3.1**: Update `run_crew_sim.py` to inject the `MockLLMClient` (or real one if available) into the Crew.
- **Task 3.3.2**: Verify that the "LLM" (or mock) correctly identifies the jamming scenario and issues the correct order.

## 4. Technical Specifications

### Prompt Strategy
The system will use a **System Prompt** defining the Persona and TTPs, and a **User Prompt** containing the dynamic JSON context.

**System Prompt Example:**
```text
You are the Commander of an autonomous aircraft. 
Your goal is to complete the mission while minimizing risk.
Current TTPs:
- If GPS variance > 5.0, GPS is unreliable.
- If GPS is unreliable, switch to Magnetic Navigation (MagNav).
Response Format: JSON {"order": "..."}
```

**User Context (JSON):**
```json
{
  "gps_variance": 10.5,
  "current_mode": "GPS",
  "incoming_message": "Navigator reports GPS Variance High"
}
```

## 5. Timeline
- **Week 1**: Infrastructure (LLM Interface, Mock Client).
- **Week 2**: Cognitive Service & Prompt Engineering.
- **Week 3**: Commander Agent Integration.
- **Week 4**: Verification & Tuning.

## 6. Security & Safety (Neuro-Symbolic Guardrails)
- **Rate Limiting**: The LLM is only called on *significant events* (e.g., status change messages), not every tick.
- **Output Validation**: The Python layer validates that the LLM's returned "Order" is a valid command before executing it.
