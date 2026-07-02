# tools/youtube_mcp.py
# ─────────────────────────────────────────────────────────────
# PURPOSE: MCP tool that searches YouTube for educational videos.
#          Used by video_agent to find lectures with timestamps.
#
# SECURITY: API key loaded from .env only. Input length capped.
#           Never logs or stores user queries.
# ─────────────────────────────────────────────────────────────

import os
import requests
from dotenv import load_dotenv

load_dotenv()


def search_youtube(query: str, max_results: int = 3) -> dict:
    """
    MCP Tool: Search YouTube for educational videos on a topic.

    Args:
        query: The topic to search for (e.g. "DBMS indexing explained")
        max_results: How many videos to return (default 3, max 5)

    Returns:
        dict with 'videos' list, each containing title, channel, url, videoId
    """
    # ── Security: sanitize inputs ──
    if not isinstance(query, str):
        return {"error": "Query must be a string", "videos": []}
    query = query.strip()[:200]  # cap at 200 chars
    max_results = min(max(1, int(max_results)), 5)  # clamp 1–5

    # ── Load API key from environment ──
    api_key = os.getenv("YOUTUBE_API_KEY")
    if not api_key:
        # Fallback: return mock data if key not set (for local dev)
        return {
            "videos": [
                {
                    "title": f"[Demo] {query} explained",
                    "channel": "Educational Channel",
                    "url": "https://youtube.com/watch?v=dQw4w9WgXcQ",
                    "videoId": "dQw4w9WgXcQ",
                    "note": "⚠ Set YOUTUBE_API_KEY in .env for real results"
                }
            ]
        }

    # ── Call YouTube Data API v3 ──
    try:
        response = requests.get(
            "https://www.googleapis.com/youtube/v3/search",
            params={
                "part": "snippet",
                "q": query + " tutorial explained lecture",
                "type": "video",
                "videoCategoryId": "27",   # Education category
                "relevanceLanguage": "en",
                "maxResults": max_results,
                "key": api_key,
            },
            timeout=10  # don't hang forever
        )
        response.raise_for_status()
        data = response.json()

        videos = []
        for item in data.get("items", []):
            vid_id = item["id"].get("videoId", "")
            snippet = item.get("snippet", {})
            videos.append({
                "title": snippet.get("title", "Unknown"),
                "channel": snippet.get("channelTitle", "Unknown"),
                "url": f"https://www.youtube.com/watch?v={vid_id}",
                "videoId": vid_id,
                "description": snippet.get("description", "")[:200]
            })

        return {"videos": videos, "query": query}

    except requests.exceptions.Timeout:
        return {"error": "YouTube search timed out. Try again.", "videos": []}
    except requests.exceptions.RequestException as e:
        return {"error": f"YouTube search failed: {str(e)}", "videos": []}
