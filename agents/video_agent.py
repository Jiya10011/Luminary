# agents/video_agent.py
# ─────────────────────────────────────────────────────────────
# PURPOSE: Finds the best YouTube educational videos for any topic.
#          Returns top 3 results with timestamps and channel info.
#
# DESIGN: Wraps YouTube MCP tool. Ranks by relevance + video length.
#         Prefers videos under 20 min for focused study sessions.
# ─────────────────────────────────────────────────────────────

import os
from google.adk.agents import Agent
from google.adk.tools import FunctionTool
from tools.youtube_mcp import search_youtube
from dotenv import load_dotenv

load_dotenv()

youtube_tool = FunctionTool(search_youtube)

video_agent = Agent(
    name="video_agent",
    model="gemini-1.5-flash",
    description=(
        "Finds the best YouTube educational videos for any study topic. "
        "Returns top 3 videos with recommended start timestamps."
    ),
    instruction="""
    You are Luminary's Video Agent. Find the best YouTube videos for
    a student trying to understand a specific topic.

    STEPS:
    1. Use search_youtube to search for the topic
    2. From the results, recommend the top 3 most useful ones
    3. For each video, add a suggested start timestamp if relevant

    OUTPUT FORMAT:

    ## 📺 Best videos for: [topic]

    **1. [Video title]**
    Channel: [channel name]
    🔗 [url]
    ⏱ Start at: [timestamp if not from beginning, else "watch from start"]
    💡 Why watch: [one sentence — what makes this video good for this topic]

    **2. [Video title]**
    ...

    **3. [Video title]**
    ...

    PREFERENCES:
    - Prioritize: clear explanations, good visuals, under 20 minutes
    - Great channels for CS: Neso Academy, Gate Smashers, Abdul Bari,
      Hussain Nasser, Academind, CS Dojo, MIT OpenCourseWare
    - Great channels for Maths: 3Blue1Brown, Professor Leonard, Khan Academy
    - If a video covers only part of the topic, mention which part

    If no good videos found, suggest a search query the student can use manually.
    """,
    tools=[youtube_tool]
)
