# state.py
from typing import TypedDict, List, Optional

class AgentState(TypedDict):
    topic: str

    research_data: Optional[str]
    sources: Optional[List[str]]

    analysis: Optional[str]
    key_points: Optional[List[str]]

    report: Optional[str]

    review_feedback: Optional[str]
    is_approved: Optional[bool]

    revision_count: int
    current_agent: str