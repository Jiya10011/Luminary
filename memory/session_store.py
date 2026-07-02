# memory/session_store.py
# ─────────────────────────────────────────────────────────────
# PURPOSE: Stores each student's quiz scores, weak topics,
#          diary entries, notes, and todos across sessions.
#
# SECURITY: Session IDs are sanitized to prevent path traversal.
#           No PII stored. Each user's data is fully isolated.
# ─────────────────────────────────────────────────────────────

import json
import os
from datetime import datetime

# Local folder where session JSON files are saved
DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
os.makedirs(DATA_DIR, exist_ok=True)


def _safe_path(session_id: str) -> str:
    """
    Sanitize session_id and return safe file path.
    Prevents path traversal attacks (e.g. ../../etc/passwd).
    """
    safe_id = "".join(c for c in session_id if c.isalnum() or c in "-_")
    safe_id = safe_id[:64]  # cap length
    return os.path.join(DATA_DIR, f"{safe_id}.json")


def _default_session() -> dict:
    """Returns a blank session object for new users."""
    return {
        "topics": {},       # { topic_name: { correct: int, total: int } }
        "diary": [],        # [ { date, mood, text } ]
        "todos": [],        # [ { text, done, priority } ]
        "notes": [],        # [ { title, body, tags, created } ]
        "history": [],      # last 20 messages for context
        "study_plan": None, # current active study plan
        "created": datetime.now().isoformat()
    }


def get_session(session_id: str) -> dict:
    """Load session data. Returns blank session if none exists yet."""
    path = _safe_path(session_id)
    if not os.path.exists(path):
        return _default_session()
    with open(path, "r") as f:
        return json.load(f)


def save_session(session_id: str, data: dict):
    """Save session data to disk."""
    with open(_safe_path(session_id), "w") as f:
        json.dump(data, f, indent=2)


def update_topic_score(session_id: str, topic: str, correct: bool):
    """
    Update quiz accuracy for a topic.
    Called by tracker_agent after every quiz answer.
    """
    data = get_session(session_id)
    topic = topic.strip()[:100]  # sanitize input
    if topic not in data["topics"]:
        data["topics"][topic] = {"correct": 0, "total": 0}
    data["topics"][topic]["total"] += 1
    if correct:
        data["topics"][topic]["correct"] += 1
    save_session(session_id, data)


def get_weak_topics(session_id: str, threshold: float = 0.65) -> list:
    """
    Returns topics where accuracy is below threshold (default 65%).
    Sorted by worst accuracy first.
    """
    data = get_session(session_id)
    weak = []
    for topic, scores in data["topics"].items():
        if scores["total"] >= 2:  # need at least 2 attempts
            accuracy = scores["correct"] / scores["total"]
            if accuracy < threshold:
                weak.append({
                    "topic": topic,
                    "accuracy": round(accuracy * 100, 1),
                    "attempts": scores["total"]
                })
    return sorted(weak, key=lambda x: x["accuracy"])


def add_diary_entry(session_id: str, text: str, mood: str = "okay"):
    """Add a diary entry for today."""
    data = get_session(session_id)
    data["diary"].append({
        "date": datetime.now().strftime("%Y-%m-%d"),
        "time": datetime.now().strftime("%H:%M"),
        "mood": mood,
        "text": text[:1000]  # cap diary entry length
    })
    save_session(session_id, data)


def add_todo(session_id: str, text: str, priority: str = "medium"):
    """Add a to-do item."""
    data = get_session(session_id)
    data["todos"].append({
        "text": text[:200],
        "done": False,
        "priority": priority,
        "created": datetime.now().isoformat()
    })
    save_session(session_id, data)


def add_history(session_id: str, role: str, content: str):
    """
    Store conversation history for context passing to agents.
    Keeps last 20 messages only to avoid token overflow.
    """
    data = get_session(session_id)
    data["history"].append({"role": role, "content": content[:500]})
    data["history"] = data["history"][-20:]  # keep last 20 only
    save_session(session_id, data)
