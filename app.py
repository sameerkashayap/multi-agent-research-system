# app.py
import streamlit as st
from graph import build_agent_graph

st.set_page_config(
    page_title="Multi-Agent Research System",
    layout="wide"
)

st.title("Multi-Agent Research System")
st.write(
    "4 AI agents collaborate to research, analyze, "
    "write, and review reports on any topic."
)

# Sidebar
with st.sidebar:
    st.header("How It Works")
    st.text("""
    1. Researcher
       Searches the web, summarizes findings

    2. Analyst
       Extracts insights and key points

    3. Writer
       Writes a structured report

    4. Reviewer
       Scores the report (1-10)
       Approves or sends back for revision
    """)

    st.divider()
    st.text("Tech Stack:")
    st.text("- Google Gemini 2.5 Flash")
    st.text("- LangGraph")
    st.text("- Tavily Search")
    st.text("- Streamlit")

# Main input
topic = st.text_input(
    "Enter a research topic",
    placeholder="Example: AI trends 2025, "
                "Electric vehicle market..."
)

start = st.button("Start Research")

if start and topic:

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

    # Status indicators
    st.divider()
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        s1 = st.empty()
        s1.info("Researcher: Waiting")
    with c2:
        s2 = st.empty()
        s2.info("Analyst: Waiting")
    with c3:
        s3 = st.empty()
        s3.info("Writer: Waiting")
    with c4:
        s4 = st.empty()
        s4.info("Reviewer: Waiting")

    progress = st.progress(0)
    status = st.empty()

    try:
        status.warning("Agents are working. Please wait...")
        final_result = dict(initial_state)

        for step in app.stream(initial_state):
            node_name = list(step.keys())[0]
            node_output = step[node_name]
            final_result.update(node_output)

            if node_name == "researcher":
                s1.success("Researcher: Done")
                progress.progress(25)

            elif node_name == "analyst":
                s2.success("Analyst: Done")
                progress.progress(50)

            elif node_name == "writer":
                s3.success("Writer: Done")
                progress.progress(75)

            elif node_name == "reviewer":
                if node_output.get("is_approved"):
                    s4.success("Reviewer: Approved")
                    progress.progress(100)
                else:
                    s4.warning("Reviewer: Revising")
                    s3.warning("Writer: Revising")

        progress.progress(100)
        status.success("Research complete.")

    except Exception as e:
        st.error(f"Error: {str(e)}")
        st.stop()

    # Results
    st.divider()

    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "Final Report",
        "Analysis",
        "Research Data",
        "Sources",
        "Review Feedback"
    ])

    with tab1:
        st.markdown(
            final_result.get("report", "No report generated")
        )

    with tab2:
        st.markdown(
            final_result.get("analysis", "No analysis available")
        )
        st.subheader("Key Takeaways")
        for i, point in enumerate(
            final_result.get("key_points", []), 1
        ):
            st.write(f"{i}. {point}")

    with tab3:
        st.markdown(
            final_result.get("research_data", "No data")
        )

    with tab4:
        for source in final_result.get("sources", []):
            st.markdown(f"- [{source}]({source})")

    with tab5:
        st.markdown(
            final_result.get("review_feedback", "No review")
        )

    # Stats
    st.divider()
    m1, m2, m3 = st.columns(3)
    m1.metric("Revisions", final_result.get("revision_count", 0))
    m2.metric("Sources", len(final_result.get("sources", [])))
    m3.metric(
        "Status",
        "Approved" if final_result.get("is_approved")
        else "Rejected"
    )

    # Download
    st.download_button(
        label="Download Report",
        data=final_result.get("report", ""),
        file_name=f"report_{topic.replace(' ', '_')}.md",
        mime="text/markdown"
    )

elif start and not topic:
    st.warning("Please enter a topic first.")