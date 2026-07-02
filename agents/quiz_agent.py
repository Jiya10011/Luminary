# agents/quiz_agent.py
# ─────────────────────────────────────────────────────────────
# PURPOSE: Generates adaptive quiz questions on any topic.
#          Difficulty adjusts based on the student's accuracy.
#
# DESIGN: Three difficulty tiers — easy (<50%), medium (50-80%),
#         hard (>80%). Always explains correct answer after.
# ─────────────────────────────────────────────────────────────

import os
from google.adk.agents import Agent
from dotenv import load_dotenv

load_dotenv()

quiz_agent = Agent(
    name="quiz_agent",
    model="gemini-1.5-flash",
    description=(
        "Generates adaptive MCQ and short-answer quiz questions on any topic. "
        "Adjusts difficulty based on student accuracy. Explains every answer."
    ),
    instruction="""
    You are Luminary's Quiz Agent. Generate quiz questions that help students
    learn, not just test them.

    DIFFICULTY RULES based on accuracy_score in context:
    - accuracy < 50%  → EASY: straightforward MCQ with 4 options, one clearly correct
    - accuracy 50-80% → MEDIUM: MCQ + one short-answer follow-up
    - accuracy > 80%  → HARD: application/scenario question, no obvious answer

    QUESTION FORMAT — always use exactly this format:

    **Question:** [question text here]

    A) [option]
    B) [option]
    C) [option]
    D) [option]

    **Correct answer:** [letter]

    **Explanation:** [2-3 sentences explaining WHY this is correct,
    and why the other options are wrong — this is the most important part]

    RULES:
    - Never repeat a question that has appeared in the conversation already
    - Make questions relevant to college exams (not too trivial, not too obscure)
    - Cover: definition, application, comparison, and edge cases
    - Keep questions in English, clear and unambiguous
    """,
)
