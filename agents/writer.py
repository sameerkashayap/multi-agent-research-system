# agents/writer.py
import os
import time
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

load_dotenv()


def get_llm():
    return ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        google_api_key=os.getenv("GOOGLE_API_KEY"),
        temperature=0.3,
        convert_system_message_to_human=True
    )


def writer_agent(state):
    topic = state["topic"]
    research = state["research_data"]
    analysis = state["analysis"]
    sources = state.get("sources", [])
    feedback = state.get("review_feedback", None)

    print(f"\n[Writer] Writing report on: {topic}")

    llm = get_llm()

    if feedback and state.get("report"):
        prompt = f"""
        You are a professional report writer.
        Revise this report based on reviewer feedback.

        ORIGINAL REPORT:
        {state['report']}

        REVIEWER FEEDBACK:
        {feedback}

        RESEARCH DATA:
        {research}

        ANALYSIS:
        {analysis}

        Write an improved report. Address ALL feedback.
        Use markdown formatting.
        """
    else:
        source_text = ""
        if sources:
            for i, s in enumerate(sources, 1):
                source_text += f"{i}. {s}\n"

        prompt = f"""
        You are a professional report writer.
        Write a comprehensive report on "{topic}".

        RESEARCH DATA:
        {research}

        ANALYSIS:
        {analysis}

        SOURCES:
        {source_text if source_text else 'N/A'}

        Report Structure:
        # [Title]
        ## Executive Summary
        ## Key Findings
        ## Detailed Analysis
        ## Trends and Outlook
        ## Risks and Challenges
        ## Conclusion
        ## Sources

        Make it professional, data-driven, and
        well-organized with markdown formatting.
        """

    response = llm.invoke(prompt)
    time.sleep(4)

    revision = state.get("revision_count", 0)
    print(f"[Writer] Done. Draft {revision + 1} complete.")

    return {
        "report": response.content,
        "current_agent": "writer"
    }