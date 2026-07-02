# tools/websearch_mcp.py
# ─────────────────────────────────────────────────────────────
# PURPOSE: MCP tool that searches the web for educational content.
#          Used by teaching_agent and planner_agent.
#
# SECURITY: API key from .env only. Input sanitized.
# ─────────────────────────────────────────────────────────────

import os
import requests
from dotenv import load_dotenv

load_dotenv()


def web_search(query: str, num_results: int = 5) -> dict:
    """
    MCP Tool: Search the web for educational content on a topic.

    Args:
        query: Topic or question to search for
        num_results: Number of results (default 5, max 10)

    Returns:
        dict with 'results' list, each containing title, snippet, url
    """
    # ── Security: sanitize input ──
    if not isinstance(query, str):
        return {"error": "Query must be a string", "results": []}
    query = query.strip()[:300]
    num_results = min(max(1, int(num_results)), 10)

    # ── Load API keys from environment ──
    api_key = os.getenv("GOOGLE_SEARCH_API_KEY")
    cx = os.getenv("GOOGLE_SEARCH_CX")

    if not api_key or not cx:
        # Fallback mock response for local dev without keys
        return {
            "results": [
                {
                    "title": f"[Demo] Search result for: {query}",
                    "snippet": "Set GOOGLE_SEARCH_API_KEY and GOOGLE_SEARCH_CX in .env for real results.",
                    "url": "https://google.com"
                }
            ]
        }

    # ── Call Google Custom Search API ──
    try:
        response = requests.get(
            "https://www.googleapis.com/customsearch/v1",
            params={
                "key": api_key,
                "cx": cx,
                "q": query,
                "num": num_results,
            },
            timeout=10
        )
        response.raise_for_status()
        items = response.json().get("items", [])

        results = []
        for item in items:
            results.append({
                "title": item.get("title", ""),
                "snippet": item.get("snippet", ""),
                "url": item.get("link", ""),
            })

        return {"results": results, "query": query}

    except requests.exceptions.Timeout:
        return {"error": "Search timed out. Try again.", "results": []}
    except requests.exceptions.RequestException as e:
        return {"error": f"Search failed: {str(e)}", "results": []}
