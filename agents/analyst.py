# agents/analyst.py
import os
import time
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

load_dotenv()


def get_llm():
    return ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        google_api_key=os.getenv("GOOGLE_API_KEY"),
        temperature=0,
        convert_system_message_to_human=True
    )


def analyst_agent(state):
    research_data = state["research_data"]
    topic = state["topic"]

    print(f"\n[Analyst] Analyzing research on: {topic}")

    llm = get_llm()

    analysis_prompt = f"""
    You are a senior analyst. Analyze the following
    research about "{topic}".

    Research Data:
    {research_data}

    Provide:
    1. Executive Summary (2-3 sentences)
    2. Key Insights (5 bullet points)
    3. Trends and Patterns identified
    4. Risks and Challenges
    5. Opportunities
    6. Data Points and Statistics (if available)

    Be specific, analytical, and data-driven.
    """

    response = llm.invoke(analysis_prompt)
    time.sleep(4)

    key_points_prompt = f"""
    From this analysis, extract exactly 5 key
    takeaways as a Python list of strings.
    Return ONLY the Python list, nothing else.
    Example: ["point 1", "point 2", "point 3",
              "point 4", "point 5"]

    Analysis:
    {response.content}
    """

    key_points_response = llm.invoke(key_points_prompt)
    time.sleep(4)

    try:
        key_points = eval(key_points_response.content)
        if not isinstance(key_points, list):
            key_points = ["See full analysis for details"]
    except Exception:
        key_points = ["See full analysis for details"]

    print(f"[Analyst] Done. Extracted {len(key_points)} insights.")

    return {
        "analysis": response.content,
        "key_points": key_points,
        "current_agent": "analyst"
    }