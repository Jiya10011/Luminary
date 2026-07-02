# tests/test_agents.py
# ─────────────────────────────────────────────────────────────
# PURPOSE: Basic tests for all agents and tools.
#          Run with: pytest tests/ -v
# ─────────────────────────────────────────────────────────────

import pytest
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from memory.session_store import (
    get_session, save_session, update_topic_score,
    get_weak_topics, add_diary_entry, add_todo
)
from tools.youtube_mcp import search_youtube
from tools.websearch_mcp import web_search

TEST_SESSION = "test_session_luminary_001"


# ── Memory store tests ──

def test_session_starts_empty():
    """New session should have empty topics and todos."""
    session = get_session("brand_new_session_xyz123")
    assert session["topics"] == {}
    assert session["todos"] == []
    assert session["diary"] == []


def test_update_topic_score_correct():
    """Correct answer should increase accuracy."""
    update_topic_score(TEST_SESSION, "Indexing", correct=True)
    update_topic_score(TEST_SESSION, "Indexing", correct=True)
    session = get_session(TEST_SESSION)
    assert session["topics"]["Indexing"]["correct"] == 2
    assert session["topics"]["Indexing"]["total"] == 2


def test_update_topic_score_wrong():
    """Wrong answer should decrease accuracy."""
    update_topic_score(TEST_SESSION, "Transactions", correct=False)
    update_topic_score(TEST_SESSION, "Transactions", correct=False)
    session = get_session(TEST_SESSION)
    assert session["topics"]["Transactions"]["total"] == 2
    assert session["topics"]["Transactions"]["correct"] == 0


def test_weak_topics_detection():
    """Topics with <65% accuracy should be flagged as weak."""
    weak = get_weak_topics(TEST_SESSION)
    weak_names = [t["topic"] for t in weak]
    assert "Transactions" in weak_names


def test_add_diary_entry():
    """Diary entries should be saved correctly."""
    add_diary_entry(TEST_SESSION, "Good study session today!", mood="😊 great")
    session = get_session(TEST_SESSION)
    assert len(session["diary"]) > 0
    assert session["diary"][-1]["text"] == "Good study session today!"


def test_add_todo():
    """Todos should be saved with correct priority."""
    add_todo(TEST_SESSION, "Revise indexing", priority="high")
    session = get_session(TEST_SESSION)
    todos = session["todos"]
    assert any(t["text"] == "Revise indexing" for t in todos)


# ── Security tests ──

def test_session_id_sanitization():
    """Malicious session IDs should be sanitized."""
    # Path traversal attempt
    malicious_id = "../../etc/passwd"
    session = get_session(malicious_id)
    # Should return empty session, not crash
    assert isinstance(session, dict)


def test_youtube_input_sanitization():
    """YouTube search should handle long/invalid inputs."""
    long_query = "x" * 1000
    result = search_youtube(long_query)
    # Should not crash — returns videos or error dict
    assert isinstance(result, dict)


def test_websearch_input_sanitization():
    """Web search should handle invalid input types."""
    result = web_search(12345)  # wrong type
    assert "error" in result or "results" in result


# ── Tool tests ──

def test_youtube_returns_dict():
    """YouTube search should always return a dict."""
    result = search_youtube("DBMS indexing explained")
    assert isinstance(result, dict)
    assert "videos" in result or "error" in result


def test_websearch_returns_dict():
    """Web search should always return a dict."""
    result = web_search("Operating system CPU scheduling")
    assert isinstance(result, dict)
    assert "results" in result or "error" in result
