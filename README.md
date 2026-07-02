# ✦ Luminary — AI Study Companion

> *An intelligent, adaptive study companion for college students — powered by Google ADK multi-agent orchestration and Gemini 2.5 Flash.*

[![Python 3.11+](https://img.shields.io/badge/Python-3.11+-blue)](https://python.org)
[![Google ADK](https://img.shields.io/badge/Google-ADK-4285F4)](https://google.github.io/adk-docs/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.111-009688)](https://fastapi.tiangolo.com)
[![Gemini](https://img.shields.io/badge/Gemini-2.5%20Flash-8A2BE2)](https://aistudio.google.com)

---

## The Problem

College students waste hours studying the wrong things. Static study apps give you fixed content — they can't see that you've answered 5 indexing questions wrong, can't decide to give you 2 extra days on transactions, and can't find you the exact YouTube video that explains your weak spot at the right timestamp.

**Agents can.** Luminary observes how you're actually doing, reasons about what you need, and takes action — just like a human tutor would.

---

## Solution

Luminary is a multi-agent AI study OS that:
- Generates personalized study plans based on your exam date and weak topics
- Quizzes you with **interactive MCQ** — click to answer, instant feedback, score summary
- Teaches any college subject with structured explanations and resources
- Finds the best YouTube lectures with exact timestamps
- Tracks your accuracy across topics using spaced repetition
- Gives you a DSA roadmap and placement prep for any company
- Lets you keep notes, a study diary, a to-do list, and a 90-day streak heatmap
- **Daily Challenge** with topic picker — one question every day to build your streak
- Socratic Mode, Formula Sheet Generator, Past Paper Analyzer, and more

---

## Architecture

```
User Message
     │
     ▼
┌─────────────────────────────────┐
│     Luminary Orchestrator        │
│   (Intent classifier + router)   │
└──┬──┬──┬──┬──┬──┬──┬────────────┘
   │  │  │  │  │  │  │
   ▼  ▼  ▼  ▼  ▼  ▼  ▼
Planner Quiz Tracker Revision Teaching Video Coding
Agent  Agent Agent   Agent    Agent   Agent Agent
   │              │              │       │
   └──────────────┴──────────────┴───────┘
                  │
          ┌───────┴───────┐
          │   MCP Tools   │
          ├───────────────┤
          │ YouTube API   │
          │ Web Search    │
          └───────────────┘
                  │
          ┌───────┴───────┐
          │ Session Memory│
          │ (per-user JSON)│
          └───────────────┘
```

### Agents

| Agent | Purpose |
|-------|---------|
| Orchestrator | Classifies intent, routes to correct sub-agent |
| Planner | Day-by-day study schedules from subject + exam date |
| Quiz | Adaptive MCQ with interactive answer selection and explanations |
| Tracker | Weak topic detection, spaced repetition scheduling |
| Revision | Flashcards, summaries, mnemonics, mock tests |
| Teaching | Explains any college concept with analogy + resources |
| Video | Finds YouTube lectures with timestamps |
| Coding | DSA roadmaps, placement kits, CS fundamentals Q&A |

---

## Key Concepts Demonstrated

| Concept | Where |
|---------|-------|
| Multi-agent system (ADK) | `agents/orchestrator.py` — orchestrator + 7 sub-agents |
| MCP Server | `tools/youtube_mcp.py`, `tools/websearch_mcp.py` |
| Antigravity | Demo video — CLI reads BDD specs in `specs/` folder |
| Security features | `.env` only, input sanitization, session isolation |
| Deployability | Render.com — Docker-based deployment, public URL |
| Agent skills / CLI | ADK agents CLI used to run and test agent chains |

---

## Setup Instructions

### 1. Clone the repository
```bash
git clone https://github.com/YOUR_USERNAME/luminary.git
cd luminary
```

### 2. Create virtual environment
```bash
python -m venv luminary-env
luminary-env\Scripts\activate      # Windows
source luminary-env/bin/activate   # Mac/Linux
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Set up API keys
```bash
cp .env.example .env
# Open .env and fill in your keys
```

| Key | Where to get it | Required? |
|-----|----------------|-----------|
| `GOOGLE_API_KEY` | [aistudio.google.com](https://aistudio.google.com) → Get API key | ✅ Yes |
| `YOUTUBE_API_KEY` | Google Cloud Console → Enable YouTube Data API v3 | Optional |
| `GOOGLE_SEARCH_API_KEY` | Google Cloud Console → Enable Custom Search API | Optional |
| `GOOGLE_SEARCH_CX` | [cse.google.com](https://cse.google.com) → Create engine → Copy CX | Optional |

### 5. Run locally
```bash
uvicorn backend.server:app --reload --port 8000
```
Open `http://localhost:8000` in your browser.

### 6. Run tests
```bash
pytest tests/ -v
```

---

## Deployment — Render (Free)

Luminary is deployed on [Render.com](https://render.com) using Docker.

1. Push this repo to GitHub (public)
2. Go to render.com → New Web Service → connect your GitHub repo
3. Runtime: **Docker** (auto-detected from Dockerfile)
4. Add environment variable: `GOOGLE_API_KEY` = your key
5. Click Deploy — live URL provided in ~5 minutes

**Live app:** https://luminary.onrender.com

---

## Security

- All API keys stored in `.env` — never in code
- `.env` in `.gitignore` — never committed to GitHub
- Input sanitized on all tool calls (length cap, type check, path traversal prevention)
- Session isolation — each user's data in separate JSON file
- No user PII stored beyond session scope
- Dockerfile has no hardcoded secrets — injected at runtime via environment variables

---

## Project Structure

```
luminary/
├── agents/          # ADK agent definitions (orchestrator + 7 sub-agents)
├── tools/           # MCP tool wrappers (YouTube, web search)
├── memory/          # Session store (per-user progress JSON)
├── eval/            # Evaluation loop agents
├── backend/         # FastAPI server (server.py)
├── frontend/        # Single-file HTML/CSS/JS frontend (index.html)
├── specs/           # BDD spec files (Antigravity input)
├── tests/           # Pytest test suite
├── .env.example     # Template — fill and rename to .env
├── requirements.txt
├── Dockerfile
└── README.md
```

---

## Frontend Features

| Page | Feature |
|------|---------|
| Chat | Multi-agent conversational AI with Gemini 2.5 Flash |
| Quiz Me | Interactive MCQ — click to answer, instant correct/wrong feedback, score summary |
| Study Plan | Personalized day-by-day schedule from exam date |
| Flashcards | 3D flip cards with spaced repetition |
| Videos | YouTube lecture finder with timestamps |
| Teach Me | Socratic Mode, structured concept explanations |
| Daily Challenge | Topic picker, streak tracking, answer history |
| Formula Sheet | AI-generated concept reference sheets |
| Past Paper Analyzer | Upload past papers → topic weights + predictions |
| Streak | 90-day study heatmap, best streak counter |
| Focus Timer | Pomodoro timer with ambient music player |
| Badges | 12 achievement badges to unlock |

---

*Built for the Kaggle × Google AI Agents Vibe Coding Capstone 2026*
