 Multi-Agent Research System

A research automation tool where 4 specialized AI agents
collaborate to produce comprehensive reports on any topic.

## Architecture
User enters topic
|
Researcher --> searches web, summarizes findings
|
Analyst --> extracts insights, identifies patterns
|
Writer --> writes structured report
|
Reviewer --> scores quality (1-10)
|
Approved? --> YES --> Final report
--> NO --> Back to Writer (max 2 revisions)


## Tech Stack

- Agent Framework: LangGraph
- LLM: Google Gemini 1.5 Flash
- Web Search: Tavily AI
- Orchestration: LangChain
- Frontend: Streamlit
- Language: Python

## Features

- 4 specialized agents with defined roles
- Automatic quality review and revision loop
- Real-time web research using Tavily
- Source citations for all claims
- Downloadable markdown reports
- Runs on Gemini free tier (no cost)

## How to Run

```bash
git clone <repo-url>
cd multi-agent-system
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt