# graph.py
from langgraph.graph import StateGraph, START, END
from state import AgentState
from agents.researcher import researcher_agent
from agents.analyst import analyst_agent
from agents.writer import writer_agent
from agents.reviewer import reviewer_agent


def should_revise(state):
    if state.get("is_approved", False):
        return "end"
    else:
        return "revise"


def build_agent_graph():
    workflow = StateGraph(AgentState)

    workflow.add_node("researcher", researcher_agent)
    workflow.add_node("analyst", analyst_agent)
    workflow.add_node("writer", writer_agent)
    workflow.add_node("reviewer", reviewer_agent)

    workflow.add_edge(START, "researcher")
    workflow.add_edge("researcher", "analyst")
    workflow.add_edge("analyst", "writer")
    workflow.add_edge("writer", "reviewer")

    workflow.add_conditional_edges(
        "reviewer",
        should_revise,
        {
            "end": END,
            "revise": "writer"
        }
    )

    app = workflow.compile()
    print("[Graph] Agent workflow built successfully.")
    return app


def run_agents(topic):
    app = build_agent_graph()

    initial_state = {
        "topic": topic,
        "research_data": None,
        "sources": None,
        "analysis": None,
        "key_points": None,
        "report": None,
        "review_feedback": None,
        "is_approved": False,
        "revision_count": 0,
        "current_agent": ""
    }

    print(f"\nStarting multi-agent research on: {topic}")
    print("-" * 50)

    final_state = app.invoke(initial_state)
    return final_state