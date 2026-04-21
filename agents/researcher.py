# agents/researcher.py
import os
import time
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.tools.tavily_search import (
    TavilySearchResults
)

load_dotenv()


def get_llm():
    return ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        google_api_key=os.getenv("GOOGLE_API_KEY"),
        temperature=0,
        convert_system_message_to_human=True
    )


def researcher_agent(state):
    topic = state["topic"]
    print(f"\n[Researcher] Searching for: {topic}")

    search_tool = TavilySearchResults(
        max_results=5,
        search_depth="advanced"
    )
    search_results = search_tool.invoke(topic)

    sources = []
    search_content = ""
    for result in search_results:
        search_content += f"\n{result['content']}\n"
        sources.append(result['url'])

    llm = get_llm()

    prompt = f"""
    You are a research specialist. Based on the
    following search results about "{topic}", create
    a comprehensive research summary.

    Include:
    - Key facts and statistics
    - Recent developments
    - Different perspectives
    - Important trends

    Search Results:
    {search_content}

    Provide a detailed research summary:
    """

    response = llm.invoke(prompt)
    time.sleep(4)

    print(f"[Researcher] Done. Found {len(sources)} sources.")

    return {
        "research_data": response.content,
        "sources": sources,
        "current_agent": "researcher"
    }