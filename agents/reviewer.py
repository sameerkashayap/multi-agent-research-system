# agents/reviewer.py
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


def reviewer_agent(state):
    report = state["report"]
    topic = state["topic"]
    revision_count = state.get("revision_count", 0)

    print(f"\n[Reviewer] Reviewing report (revision {revision_count})")

    llm = get_llm()

    prompt = f"""
    You are a strict quality reviewer. Review this
    report about "{topic}".

    REPORT:
    {report}

    Evaluate (score 1-10 each):
    1. Completeness - covers all aspects
    2. Accuracy - facts are correct
    3. Structure - well organized
    4. Clarity - easy to understand
    5. Professionalism - appropriate tone

    If AVERAGE score >= 7: APPROVE
    If AVERAGE score < 7: REJECT with specific feedback

    Respond in this EXACT format:
    SCORES: [completeness, accuracy, structure,
             clarity, professionalism]
    AVERAGE: [number]
    DECISION: APPROVE or REJECT
    FEEDBACK: [specific suggestions if rejected,
               or "Looks good." if approved]
    """

    response = llm.invoke(prompt)
    time.sleep(4)

    review_text = response.content
    is_approved = "APPROVE" in review_text.upper()

    if revision_count >= 2:
        is_approved = True
        print("[Reviewer] Max revisions reached. Auto-approving.")

    if is_approved:
        print("[Reviewer] Report APPROVED.")
    else:
        print("[Reviewer] Report REJECTED. Sending back to writer.")

    return {
        "review_feedback": review_text,
        "is_approved": is_approved,
        "revision_count": revision_count + 1,
        "current_agent": "reviewer"
    }