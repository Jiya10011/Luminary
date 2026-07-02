# agents/planner_agent.py
# ─────────────────────────────────────────────────────────────
# PURPOSE: Generates a personalized day-by-day study plan.
#          Takes subject, exam date, level → outputs schedule.
#
# DESIGN: Uses web_search to fetch standard syllabi if student
#         hasn't uploaded their own. Weak topics get more days.
# ─────────────────────────────────────────────────────────────

import os
from google.adk.agents import Agent
from google.adk.tools import FunctionTool
from tools.websearch_mcp import web_search
from dotenv import load_dotenv

load_dotenv()

# Wrap web_search as an ADK FunctionTool so the agent can call it
web_search_tool = FunctionTool(web_search)

planner_agent = Agent(
    name="planner_agent",
    model="gemini-1.5-flash",
    description=(
        "Creates personalized day-by-day study plans for any college subject. "
        "Adapts schedule based on exam date, difficulty level, and weak topics."
    ),
    instruction="""
    You are Luminary's Planner Agent. Your job is to create a clear,
    realistic day-by-day study schedule for a college student.

    When given a subject and exam date:
    1. Break the subject into logical topics (use web_search if no syllabus provided)
    2. Assign each topic to a specific day
    3. Keep daily study load to 2-3 hours max
    4. Give weak topics (if provided) 2x more time than strong ones
    5. Reserve the last 2 days before the exam for full revision + mock tests

    Output format — always use this structure:
    ## Study Plan for [Subject] — [X] days until exam

    **Day 1 (Date):** Topic name — estimated time
    - What to cover
    - Suggested resource (textbook chapter or search query)

    **Day 2 (Date):** ...

    Keep it encouraging and realistic. Never overload a single day.
    """,
    tools=[web_search_tool]
)
