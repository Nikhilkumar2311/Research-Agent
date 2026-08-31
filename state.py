from typing import TypedDict, List

'''
We define a custom TypeDict. This tells LangGraph exactly what variables
our "shared notebook" will keep track of throughout the life of the agent loop.
'''
class AgentState(TypedDict):
  topic: str # The user's input topic (e.g., "AI Trends in 2026")
  search_queries: List[str] # List of sub-queries generated to search the web
  research_notes: str # The combined raw research facts found by the searcher
  draft: str # The current version of the newsletter newsletter draft
  critique: str # The feedback/review from the Editor node
  revision_count: int # A counter to stop infinite loops (max 3 tries)