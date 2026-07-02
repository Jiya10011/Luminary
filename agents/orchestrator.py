# agents/orchestrator.py
# ─────────────────────────────────────────────────────────────
# PURPOSE: Root orchestrator agent that receives every user message,
#          classifies the intent, and delegates to the right sub-agent.
#
# DESIGN: Intent-based routing using ADK's sub_agents system.
#         Maintains session context for personalized responses.
# ─────────────────────────────────────────────────────────────

import os
from google.adk.agents import Agent
from dotenv import load_dotenv

from agents.planner_agent import planner_agent
from agents.quiz_agent import quiz_agent
from agents.tracker_agent import tracker_agent
from agents.revision_agent import revision_agent
from agents.teaching_agent import teaching_agent
from agents.video_agent import video_agent
from agents.coding_agent import coding_agent

load_dotenv()  # loads API keys from .env file — never hardcoded

# ─────────────────────────────────────────────────────────────
# ROOT AGENT — this is the entry point for every user message
# ─────────────────────────────────────────────────────────────
root_agent = Agent(
    name="luminary_orchestrator",
    model="gemini-1.5-flash",
    description="Luminary AI Study Companion — orchestrates all study agents.",
    instruction="""
    You are Luminary ✦ — a calm, intelligent AI study companion for college students.
    Your personality: encouraging, patient, clear, never condescending.

    Your job is to understand what the student needs and route to the right agent.

    ROUTING RULES — always follow these:

    → Study plan / schedule / timetable → transfer_to_agent: planner_agent
    → Quiz / test me / practice questions → transfer_to_agent: quiz_agent
    → Explain / teach / what is / how does → transfer_to_agent: teaching_agent
    → YouTube / video / watch / lecture → transfer_to_agent: video_agent
    → DSA / roadmap / LeetCode / placement / company prep → transfer_to_agent: coding_agent
    → Progress / weak topics / how am I doing → transfer_to_agent: tracker_agent
    → Flashcards / revision / mock test / summary → transfer_to_agent: revision_agent

    For GREETINGS or UNCLEAR messages:
    Respond warmly yourself. Ask what subject they are studying and what they need.
    Example: "Hi! I'm Luminary ✦ — what are you studying today?"

    CONTEXT AWARENESS:
    - If the student mentions an exam date, remember it and factor it into all responses
    - If they mention weak topics, pass those to the relevant agent
    - Always use their name if you know it

    Keep your own responses short (1-2 sentences) before transferring.
    The sub-agents will do the detailed work.
    """,
    sub_agents=[
        planner_agent,
        quiz_agent,
        tracker_agent,
        revision_agent,
        teaching_agent,
        video_agent,
        coding_agent,
    ]
)
