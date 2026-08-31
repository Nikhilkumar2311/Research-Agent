from state import AgentState

def should_continue(state: AgentState) -> str:
  if "APPROVED" in state.get("critique", "").upper():
      print("--- DECISION: DRAFT APPROVED! GOING TO END ---")
      return "end"
        
    # Safety valve: If the agent has looped 3 times, force it to stop
  if state.get("revision_count", 0) >= 3:
      print("--- DECISION: MAX REVISIONS REACHED. FORCING END ---")
      return "end"
        
    # If it's not approved and we haven't hit the limit, loop back to research
  print(f"--- DECISION: REVISION REQUIRED (Attempt {state.get('revision_count', 0)}/3) ---")
  return "continue"