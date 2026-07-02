# backend/server.py
import os, sys, uuid
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

from memory.session_store import (
    get_session, save_session, update_topic_score,
    get_weak_topics, add_diary_entry, add_todo, add_history
)

app = FastAPI(title="Luminary API")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

class ChatRequest(BaseModel):
    session_id: str
    message: str

class DiaryRequest(BaseModel):
    session_id: str
    text: str
    mood: str = "okay"

class TodoRequest(BaseModel):
    session_id: str
    text: str
    priority: str = "medium"

class ScoreRequest(BaseModel):
    session_id: str
    topic: str
    correct: bool

class NoteRequest(BaseModel):
    session_id: str
    title: str
    body: str
    tags: list[str] = []


async def run_agent(message: str, session_id: str) -> str:
    """
    Run Luminary orchestrator agent.
    Uses google-generativeai directly as fallback if ADK runner fails.
    This ensures compatibility across ADK versions.
    """
    import google.generativeai as genai

    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        return "⚠️ GOOGLE_API_KEY not set in .env file. Please add it and restart the server."

    # Build context with weak topics
    weak = get_weak_topics(session_id[:64])
    context = message
    if weak:
        weak_names = ", ".join([t["topic"] for t in weak[:3]])
        context = f"[Student weak topics: {weak_names}]\n\n{message}"

    # Try ADK runner first, fall back to direct Gemini if it fails
    try:
        from google.adk.runners import Runner
        from google.adk.sessions import InMemorySessionService
        from google.genai import types as genai_types
        from agents.orchestrator import root_agent

        session_service = InMemorySessionService()
        # InMemorySessionService.create_session may be sync in some versions
        try:
            session = await session_service.create_session(
                app_name="luminary", user_id=session_id, session_id=session_id
            )
        except TypeError:
            session = session_service.create_session(
                app_name="luminary", user_id=session_id, session_id=session_id
            )

        runner = Runner(agent=root_agent, app_name="luminary", session_service=session_service)
        content = genai_types.Content(role="user", parts=[genai_types.Part(text=context)])

        response_text = ""
        async for event in runner.run_async(
            user_id=session_id, session_id=session_id, new_message=content
        ):
            if hasattr(event, "content") and event.content:
                for part in event.content.parts:
                    if hasattr(part, "text") and part.text:
                        response_text += part.text

        if response_text.strip():
            add_history(session_id, "user", message)
            add_history(session_id, "assistant", response_text[:500])
            return response_text

    except Exception as adk_error:
        print(f"ADK runner failed: {adk_error}. Falling back to direct Gemini.")

    # ── Fallback: direct Gemini API with full agent instructions ──
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel(
            model_name="gemini-2.5-flash",
            system_instruction="""You are Luminary ✦ — a calm, intelligent AI study companion for college students.

You help with:
- Study plans: generate day-by-day schedules for any subject and exam date
- Quizzes: adaptive MCQ questions with explanations on any topic
- Teaching: explain any college concept (DBMS, OS, CN, OOP, DSA, Maths) clearly with analogies and examples
- YouTube videos: suggest the best YouTube channels and search queries for any topic
- DSA roadmaps: ordered topic-by-topic coding preparation with LeetCode problem lists
- Placement prep: company-specific interview preparation kits
- CS fundamentals: interview Q&A for OS, DBMS, CN, OOP

Always be encouraging, clear, and structured. Use markdown formatting with headers and bullet points.
When explaining concepts always include: definition, analogy, example, exam tip, and resources.
When suggesting YouTube videos mention channels like: Neso Academy, Gate Smashers, Abdul Bari, 
Hussain Nasser, 3Blue1Brown, MIT OpenCourseWare."""
        )

        # Include recent history for context
        session_data = get_session(session_id[:64])
        history = session_data.get("history", [])[-6:]  # last 3 exchanges

        chat_history = []
        for h in history:
            chat_history.append({
                "role": h["role"] if h["role"] == "user" else "model",
                "parts": [h["content"]]
            })

        chat = model.start_chat(history=chat_history)
        response = chat.send_message(context)
        response_text = response.text

        add_history(session_id, "user", message)
        add_history(session_id, "assistant", response_text[:500])
        return response_text

    except Exception as e:
        return f"⚠️ Error: {str(e)}\n\nMake sure GOOGLE_API_KEY is correctly set in your .env file."


# ── API Endpoints ──

@app.post("/api/chat")
async def chat(req: ChatRequest):
    response = await run_agent(req.message[:2000], req.session_id[:64])
    return {"response": response, "session_id": req.session_id}

@app.get("/api/session/{session_id}")
async def get_session_data(session_id: str):
    data = get_session(session_id[:64])
    weak = get_weak_topics(session_id[:64])
    return {"session": data, "weak_topics": weak}

@app.post("/api/score")
async def score_topic(req: ScoreRequest):
    update_topic_score(req.session_id[:64], req.topic[:100], req.correct)
    return {"ok": True}

@app.post("/api/diary")
async def save_diary(req: DiaryRequest):
    add_diary_entry(req.session_id[:64], req.text[:1000], req.mood)
    return {"ok": True}

@app.post("/api/todo")
async def save_todo(req: TodoRequest):
    add_todo(req.session_id[:64], req.text[:200], req.priority)
    return {"ok": True}

@app.post("/api/note")
async def save_note(req: NoteRequest):
    from datetime import datetime
    data = get_session(req.session_id[:64])
    data["notes"].append({
        "title": req.title[:100],
        "body": req.body[:2000],
        "tags": req.tags[:10],
        "created": datetime.now().strftime("%b %d, %H:%M")
    })
    save_session(req.session_id[:64], data)
    return {"ok": True}

@app.put("/api/todo/{session_id}/{idx}/done")
async def mark_done(session_id: str, idx: int):
    data = get_session(session_id[:64])
    if 0 <= idx < len(data["todos"]):
        data["todos"][idx]["done"] = True
        save_session(session_id[:64], data)
    return {"ok": True}

@app.get("/api/new-session")
async def new_session():
    return {"session_id": str(uuid.uuid4())}

@app.get("/health")
async def health():
    return {"status": "ok", "api_key_set": bool(os.getenv("GOOGLE_API_KEY"))}

# ── Serve frontend ──
app.mount("/static", StaticFiles(directory="frontend/static"), name="static")

@app.get("/")
async def serve_frontend():
    return FileResponse("frontend/index.html")