# frontend/app.py — Luminary UI v2 (full aesthetic redesign)

import streamlit as st
import asyncio
import uuid
import os
import sys
from datetime import datetime, date

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from dotenv import load_dotenv
load_dotenv()

from memory.session_store import (
    get_session, save_session, update_topic_score,
    get_weak_topics, add_diary_entry, add_todo, add_history
)

# ─── PAGE CONFIG ───
st.set_page_config(
    page_title="Luminary ✦",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── FULL CSS OVERHAUL ───
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&family=DM+Serif+Display&display=swap');

/* ── Reset & base ── */
*, *::before, *::after { box-sizing: border-box; }
html, body, [data-testid="stAppViewContainer"] {
    background: #f7f5f0 !important;
    font-family: 'Inter', system-ui, sans-serif;
}

/* ── Hide Streamlit chrome ── */
#MainMenu, footer, header, [data-testid="stToolbar"],
[data-testid="stDecoration"], [data-testid="stStatusWidget"] { display: none !important; }

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: #f0ece4 !important;
    border-right: 1px solid #e0d8cc !important;
    padding-top: 0 !important;
}
[data-testid="stSidebar"] > div:first-child { padding: 0 !important; }

/* ── Sidebar buttons ── */
[data-testid="stSidebar"] .stButton > button {
    width: 100%;
    text-align: left !important;
    background: transparent !important;
    border: none !important;
    border-radius: 8px !important;
    color: #4a5568 !important;
    font-size: 13px !important;
    font-weight: 400 !important;
    padding: 8px 14px !important;
    margin: 1px 0 !important;
    transition: all 0.15s !important;
    box-shadow: none !important;
}
[data-testid="stSidebar"] .stButton > button:hover {
    background: #e8e2d8 !important;
    color: #1a1f2e !important;
}

/* ── Main content area ── */
[data-testid="stMain"] {
    background: #f7f5f0 !important;
}
.block-container {
    padding: 0 !important;
    max-width: 100% !important;
}

/* ── All main buttons ── */
.main-btn > button, [data-testid="stMain"] .stButton > button {
    border-radius: 10px !important;
    background: #7fb5c8 !important;
    color: white !important;
    border: none !important;
    font-size: 13px !important;
    font-weight: 500 !important;
    padding: 8px 20px !important;
    transition: all 0.2s !important;
    box-shadow: 0 1px 3px rgba(0,0,0,0.08) !important;
}
[data-testid="stMain"] .stButton > button:hover {
    background: #6aa5b8 !important;
    box-shadow: 0 3px 8px rgba(127,181,200,0.3) !important;
    transform: translateY(-1px) !important;
}

/* ── Chat input ── */
[data-testid="stChatInput"] {
    border-radius: 24px !important;
    background: white !important;
    border: 1px solid #e0d8cc !important;
    box-shadow: 0 2px 12px rgba(0,0,0,0.06) !important;
    margin: 0 24px 20px !important;
}
[data-testid="stChatInput"] textarea {
    font-family: 'Inter', sans-serif !important;
    font-size: 14px !important;
    color: #1a1f2e !important;
}

/* ── Chat messages ── */
[data-testid="stChatMessage"] {
    background: white !important;
    border: 1px solid #e8e2d8 !important;
    border-radius: 14px !important;
    padding: 14px 18px !important;
    margin: 6px 0 !important;
    box-shadow: 0 1px 4px rgba(0,0,0,0.04) !important;
}

/* ── Text inputs ── */
.stTextInput input, .stTextArea textarea, .stSelectbox select,
[data-testid="stDateInput"] input {
    border: 1px solid #e0d8cc !important;
    border-radius: 10px !important;
    background: white !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 13px !important;
    color: #1a1f2e !important;
    padding: 10px 14px !important;
}
.stTextInput input:focus, .stTextArea textarea:focus {
    border-color: #7fb5c8 !important;
    box-shadow: 0 0 0 3px rgba(127,181,200,0.15) !important;
}

/* ── Select slider ── */
.stSlider > div > div > div { background: #7fb5c8 !important; }

/* ── Progress bar ── */
.stProgress > div > div > div { background: #7fb5c8 !important; border-radius: 4px !important; }
.stProgress > div > div { background: #e8e2d8 !important; border-radius: 4px !important; }

/* ── Expander ── */
.streamlit-expanderHeader {
    background: white !important;
    border: 1px solid #e0d8cc !important;
    border-radius: 10px !important;
    font-size: 13px !important;
    color: #1a1f2e !important;
}

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {
    background: transparent !important;
    gap: 4px !important;
    border-bottom: 1px solid #e0d8cc !important;
}
.stTabs [data-baseweb="tab"] {
    background: transparent !important;
    border-radius: 8px 8px 0 0 !important;
    color: #8896a8 !important;
    font-size: 13px !important;
    font-weight: 500 !important;
    padding: 8px 16px !important;
}
.stTabs [aria-selected="true"] {
    background: white !important;
    color: #1a1f2e !important;
    border-bottom: 2px solid #7fb5c8 !important;
}

/* ── Divider ── */
hr { border: none !important; border-top: 1px solid #e0d8cc !important; margin: 16px 0 !important; }

/* ── Info / warning / success boxes ── */
.stInfo { background: #eef5f9 !important; border-color: #7fb5c8 !important; border-radius: 10px !important; }
.stSuccess { background: #edf5ed !important; border-color: #a8c8a0 !important; border-radius: 10px !important; }
.stWarning { background: #fdf6e8 !important; border-color: #e8b86a !important; border-radius: 10px !important; }

/* ── Metrics ── */
[data-testid="stMetric"] {
    background: white !important;
    border: 1px solid #e0d8cc !important;
    border-radius: 12px !important;
    padding: 16px !important;
}
[data-testid="stMetricLabel"] { font-size: 11px !important; color: #8896a8 !important; text-transform: uppercase; letter-spacing: 0.05em; }
[data-testid="stMetricValue"] { font-size: 24px !important; font-weight: 600 !important; color: #1a1f2e !important; }

/* ── Custom card ── */
.lum-card {
    background: white;
    border: 1px solid #e8e2d8;
    border-radius: 14px;
    padding: 20px 22px;
    margin-bottom: 12px;
    box-shadow: 0 1px 4px rgba(0,0,0,0.04);
}
.lum-card h3 { font-size: 14px; font-weight: 600; color: #1a1f2e; margin: 0 0 12px; }

/* ── Quick action chips ── */
.qa-chip {
    display: inline-block;
    background: white;
    border: 1px solid #e0d8cc;
    border-radius: 20px;
    padding: 7px 16px;
    font-size: 12.5px;
    color: #4a5568;
    cursor: pointer;
    margin: 4px;
    transition: all 0.15s;
}
.qa-chip:hover { background: #eef5f9; border-color: #7fb5c8; color: #1a4060; }

/* ── Section headers ── */
.section-label {
    font-size: 10px;
    font-weight: 600;
    color: #a0a8b8;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    padding: 12px 16px 4px;
}

/* ── Topbar ── */
.lum-topbar {
    background: #f0ece4;
    border-bottom: 1px solid #e0d8cc;
    padding: 14px 28px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 0;
}

/* ── Weak topic pill ── */
.weak-pill {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: #fdf6e8;
    border: 1px solid #e8b86a;
    border-radius: 20px;
    padding: 4px 10px;
    font-size: 11px;
    color: #7a5800;
    margin: 3px 0;
}

/* ── Note card ── */
.note-card {
    background: white;
    border: 1px solid #e8e2d8;
    border-left: 3px solid #7fb5c8;
    border-radius: 0 10px 10px 0;
    padding: 12px 14px;
    margin-bottom: 8px;
}
.note-card.green { border-left-color: #a8c8a0; }
.note-card.lav { border-left-color: #b5a8d8; }
.note-card.amber { border-left-color: #e8b86a; }

/* ── Diary card ── */
.diary-card {
    background: #f8fbf8;
    border-left: 3px solid #a8c8a0;
    border-radius: 0 10px 10px 0;
    padding: 11px 14px;
    margin-bottom: 8px;
}
.diary-card.lav { background: #f8f6fc; border-left-color: #b5a8d8; }
.diary-card.amber { background: #fdf9f2; border-left-color: #e8b86a; }

/* ── Todo item ── */
.todo-row {
    background: white;
    border: 1px solid #e8e2d8;
    border-radius: 10px;
    padding: 10px 14px;
    margin-bottom: 6px;
    display: flex;
    align-items: center;
    gap: 10px;
}

/* ── Stat mini card ── */
.stat-mini {
    background: white;
    border: 1px solid #e8e2d8;
    border-radius: 12px;
    padding: 16px;
    text-align: center;
}
.stat-mini .val { font-size: 26px; font-weight: 600; color: #1a1f2e; letter-spacing: -0.5px; }
.stat-mini .lbl { font-size: 10px; color: #8896a8; text-transform: uppercase; letter-spacing: 0.06em; margin-top: 2px; }
.stat-mini .sub { font-size: 11px; color: #aaa; margin-top: 3px; }

/* ── Chat welcome ── */
.welcome-text {
    text-align: center;
    padding: 60px 20px 30px;
    color: #8896a8;
}
.welcome-text h1 {
    font-size: 32px;
    font-weight: 600;
    color: #1a1f2e;
    letter-spacing: -0.5px;
    margin-bottom: 8px;
}
.welcome-text p { font-size: 15px; color: #8896a8; }
</style>
""", unsafe_allow_html=True)

# ─── SESSION STATE ───
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())
if "messages" not in st.session_state:
    st.session_state.messages = []
if "page" not in st.session_state:
    st.session_state.page = "chat"

sid = st.session_state.session_id
session_data = get_session(sid)

# ─── RUN AGENT ───
def run_agent(prompt: str) -> str:
    try:
        from agents.orchestrator import root_agent
        weak = get_weak_topics(sid)
        context = prompt
        if weak:
            weak_names = ", ".join([t["topic"] for t in weak[:3]])
            context = f"[Student weak topics: {weak_names}]\n\n{prompt}"
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        result = loop.run_until_complete(root_agent.run_async(context))
        loop.close()
        add_history(sid, "user", prompt)
        add_history(sid, "assistant", str(result)[:500])
        return str(result)
    except Exception as e:
        return f"⚠️ {str(e)}\n\nMake sure your `GOOGLE_API_KEY` is set in `.env`"

# ─────────────────────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='padding: 20px 16px 14px; border-bottom: 1px solid #e0d8cc;'>
        <div style='display:flex; align-items:center; gap:10px;'>
            <div style='width:32px;height:32px;border-radius:50%;background:linear-gradient(135deg,#a8c8a0,#7fb5c8);
                        display:flex;align-items:center;justify-content:center;font-size:14px;font-weight:700;color:white;'>✦</div>
            <div>
                <div style='font-size:15px;font-weight:600;color:#1a1f2e;letter-spacing:-0.3px;'>Luminary</div>
                <div style='font-size:11px;color:#8896a8;'>your AI study companion</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="section-label">Study</div>', unsafe_allow_html=True)
    if st.button("💬  Chat", key="nav_chat"):
        st.session_state.page = "chat"
        st.rerun()
    if st.button("📅  Study Plan", key="nav_plan"):
        st.session_state.page = "planner"
        st.rerun()
    if st.button("❓  Quiz Me", key="nav_quiz"):
        st.session_state.page = "quiz"
        st.rerun()
    if st.button("📺  Videos", key="nav_vid"):
        st.session_state.page = "videos"
        st.rerun()

    st.markdown('<div class="section-label">My Space</div>', unsafe_allow_html=True)
    if st.button("📝  Notes & Diary", key="nav_notes"):
        st.session_state.page = "notes"
        st.rerun()
    if st.button("✅  To-do List", key="nav_todo"):
        st.session_state.page = "todos"
        st.rerun()

    st.markdown('<div class="section-label">Placement</div>', unsafe_allow_html=True)
    if st.button("💻  DSA Roadmap", key="nav_dsa"):
        st.session_state.page = "dsa"
        st.rerun()
    if st.button("📊  My Progress", key="nav_prog"):
        st.session_state.page = "progress"
        st.rerun()

    st.markdown("---")

    # Weak topics
    weak = get_weak_topics(sid)
    if weak:
        st.markdown('<div class="section-label">⚠ Weak topics</div>', unsafe_allow_html=True)
        for t in weak[:4]:
            pct = t["accuracy"] / 100
            st.progress(pct, text=f"{t['topic']}  {t['accuracy']}%")
    else:
        st.markdown("""
        <div style='padding:12px 16px;font-size:12px;color:#a0a8b8;font-style:italic;'>
            Take a quiz to track your progress
        </div>""", unsafe_allow_html=True)

    st.markdown("---")

    # Exam date
    st.markdown('<div style="padding:0 16px 4px;font-size:12px;font-weight:500;color:#4a5568;">📅 Exam date</div>', unsafe_allow_html=True)
    exam_date = st.date_input("", value=None, key="exam_input", label_visibility="collapsed")
    if exam_date:
        days_left = (exam_date - date.today()).days
        if days_left > 0:
            st.markdown(f"""
            <div style='margin:6px 16px;padding:8px 12px;background:#fdf6e8;border:1px solid #e8b86a;
                        border-radius:8px;font-size:12px;color:#7a5800;font-weight:500;'>
                ⏰ {days_left} days to exam
            </div>""", unsafe_allow_html=True)
        elif days_left == 0:
            st.warning("📝 Exam is today!")
        else:
            st.success("✅ Exam passed!")

    # Footer
    st.markdown("""
    <div style='padding:14px 16px;margin-top:16px;border-top:1px solid #e0d8cc;
                font-size:11px;color:#a0a8b8;'>
        Luminary ✦ · Kaggle × Google 2026
    </div>""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────
# MAIN AREA WRAPPER
# ─────────────────────────────────────────────────────────────
def page_header(icon, title, subtitle=""):
    st.markdown(f"""
    <div style='background:#f0ece4;border-bottom:1px solid #e0d8cc;
                padding:18px 28px 14px;margin-bottom:0;'>
        <div style='font-size:20px;font-weight:600;color:#1a1f2e;letter-spacing:-0.3px;'>
            {icon} {title}
        </div>
        {'<div style="font-size:12px;color:#8896a8;margin-top:3px;">'+subtitle+'</div>' if subtitle else ''}
    </div>
    """, unsafe_allow_html=True)

def card(content_fn, padding="20px 24px"):
    st.markdown(f'<div class="lum-card">', unsafe_allow_html=True)
    content_fn()
    st.markdown('</div>', unsafe_allow_html=True)

pad = st.container()
with pad:
    main = st.container()

# ─────────────────────────────────────────────────────────────
# PAGE: CHAT
# ─────────────────────────────────────────────────────────────
if st.session_state.page == "chat":
    page_header("✦", "Luminary", "Ask me anything — I'll teach, quiz, plan, and find resources for you")

    with st.container():
        st.markdown("<div style='padding: 0 24px;'>", unsafe_allow_html=True)

        if not st.session_state.messages:
            st.markdown("""
            <div class="welcome-text">
                <div style="font-size:40px;margin-bottom:12px;">✦</div>
                <h1>Good day! I'm Luminary</h1>
                <p>Your intelligent AI study companion.<br>
                What are you studying today?</p>
            </div>
            """, unsafe_allow_html=True)

            # Quick actions
            st.markdown("""
            <div style='display:flex;flex-wrap:wrap;justify-content:center;gap:8px;
                        padding:0 40px 32px;'>
            """, unsafe_allow_html=True)

            cols = st.columns(4)
            quick_actions = [
                ("📅", "Make a study plan", "Create a study plan for me"),
                ("❓", "Quiz me", "Quiz me on my weakest topic"),
                ("📺", "Find videos", "Find YouTube videos for my current topic"),
                ("💻", "DSA roadmap", "Give me a complete DSA roadmap for placement"),
            ]
            for i, (icon, label, prompt) in enumerate(quick_actions):
                with cols[i]:
                    st.markdown(f"""
                    <div style='background:white;border:1px solid #e0d8cc;border-radius:12px;
                                padding:16px;text-align:center;cursor:pointer;
                                box-shadow:0 1px 4px rgba(0,0,0,0.04);'>
                        <div style='font-size:22px;margin-bottom:6px;'>{icon}</div>
                        <div style='font-size:12.5px;font-weight:500;color:#1a1f2e;'>{label}</div>
                    </div>
                    """, unsafe_allow_html=True)
                    if st.button(f"→ {label}", key=f"qa_{i}", use_container_width=True):
                        st.session_state.messages.append({"role": "user", "content": prompt})
                        st.rerun()

        else:
            st.markdown("<div style='padding:16px 0;'>", unsafe_allow_html=True)
            for msg in st.session_state.messages:
                icon = "✦" if msg["role"] == "assistant" else "👤"
                with st.chat_message(msg["role"], avatar=icon):
                    st.markdown(msg["content"])
            st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

    if prompt := st.chat_input("Ask Luminary anything — explain, quiz, plan, find videos..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user", avatar="👤"):
            st.markdown(prompt)
        with st.chat_message("assistant", avatar="✦"):
            with st.spinner(""):
                response = run_agent(prompt)
                st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.rerun()


# ─────────────────────────────────────────────────────────────
# PAGE: STUDY PLANNER
# ─────────────────────────────────────────────────────────────
elif st.session_state.page == "planner":
    page_header("📅", "Study Planner", "Generate a personalized day-by-day study schedule")

    st.markdown("<div style='padding:24px;'>", unsafe_allow_html=True)

    st.markdown('<div class="lum-card">', unsafe_allow_html=True)
    st.markdown("<h3 style='font-size:14px;font-weight:600;color:#1a1f2e;margin:0 0 16px;'>Set up your plan</h3>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        subject = st.text_input("Subject", placeholder="e.g. DBMS, Operating Systems, Calculus")
        level = st.selectbox("Your level", ["Beginner", "Intermediate", "Advanced"])
    with col2:
        exam_date_p = st.date_input("Exam date", key="planner_exam")
        weak_topics = st.text_input("Weak topics (optional)", placeholder="e.g. Transactions, Indexing")

    if st.button("✦ Generate my study plan", key="gen_plan"):
        if subject:
            days_left = (exam_date_p - date.today()).days
            prompt = f"""Create a detailed study plan for:
Subject: {subject}
Exam date: {exam_date_p} ({days_left} days from today)
Level: {level}
Weak topics: {weak_topics if weak_topics else 'None specified yet'}
Generate a complete day-by-day schedule."""
            with st.spinner("Creating your personalized study plan..."):
                response = run_agent(prompt)
            st.markdown("---")
            st.markdown(response)
        else:
            st.warning("Please enter a subject name first.")

    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────
# PAGE: QUIZ
# ─────────────────────────────────────────────────────────────
elif st.session_state.page == "quiz":
    page_header("❓", "Quiz Me", "Adaptive quizzes that adjust to your accuracy level")

    st.markdown("<div style='padding:24px;'>", unsafe_allow_html=True)
    st.markdown('<div class="lum-card">', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        topic = st.text_input("Topic", placeholder="e.g. SQL Joins, CPU Scheduling, Binary Trees")
    with col2:
        difficulty = st.selectbox("Difficulty", ["Auto (based on my progress)", "Easy", "Medium", "Hard"])

    if st.button("✦ Start quiz", key="start_quiz"):
        if topic:
            with st.spinner("Generating quiz..."):
                response = run_agent(f"Quiz me on: {topic}. Difficulty: {difficulty}. Generate 5 questions.")
            st.markdown("---")
            st.markdown(response)
            st.markdown("---")
            st.markdown("**How did you do on this topic?**")
            c1, c2, c3 = st.columns(3)
            with c1:
                if st.button("😊 Got most right", key="q_good"):
                    update_topic_score(sid, topic, correct=True)
                    st.success("Marked as improving ✓")
            with c2:
                if st.button("😐 Mixed", key="q_mid"):
                    update_topic_score(sid, topic, correct=True)
                    st.info("Keep going!")
            with c3:
                if st.button("😔 Struggled", key="q_bad"):
                    update_topic_score(sid, topic, correct=False)
                    st.warning("Added to weak topics for extra revision")
        else:
            st.warning("Please enter a topic first.")

    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────
# PAGE: VIDEOS
# ─────────────────────────────────────────────────────────────
elif st.session_state.page == "videos":
    page_header("📺", "Video Lessons", "Find the best YouTube lectures for any topic")

    st.markdown("<div style='padding:24px;'>", unsafe_allow_html=True)
    st.markdown('<div class="lum-card">', unsafe_allow_html=True)

    topic_v = st.text_input("Search for videos on...", placeholder="e.g. B+ trees, deadlock, recursion")
    if st.button("✦ Find videos", key="find_vids"):
        if topic_v:
            with st.spinner("Searching YouTube..."):
                response = run_agent(f"Find the best YouTube videos for: {topic_v}")
            st.markdown("---")
            st.markdown(response)
        else:
            st.warning("Enter a topic to search.")

    st.markdown("</div>", unsafe_allow_html=True)

    # Suggested searches
    st.markdown("""
    <div style='margin-top:8px;'>
        <div style='font-size:11px;color:#a0a8b8;margin-bottom:8px;
                    text-transform:uppercase;letter-spacing:0.07em;font-weight:600;'>
            Popular searches
        </div>
    </div>
    """, unsafe_allow_html=True)

    suggestions = ["DBMS Indexing", "OS CPU Scheduling", "TCP/IP Model", "Binary Search Trees", "Dynamic Programming", "OOP Polymorphism"]
    cols = st.columns(3)
    for i, s in enumerate(suggestions):
        with cols[i % 3]:
            if st.button(f"🔍 {s}", key=f"sug_{i}", use_container_width=True):
                with st.spinner(f"Finding videos for {s}..."):
                    response = run_agent(f"Find YouTube videos for: {s}")
                st.markdown(response)

    st.markdown("</div>", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────
# PAGE: NOTES & DIARY
# ─────────────────────────────────────────────────────────────
elif st.session_state.page == "notes":
    page_header("📝", "Notes & Study Diary", "Your personal study space")

    st.markdown("<div style='padding:24px;'>", unsafe_allow_html=True)
    tab1, tab2 = st.tabs(["📝  Notes", "📖  Study Diary"])

    with tab1:
        notes = session_data.get("notes", [])

        with st.expander("✦ Add new note", expanded=len(notes) == 0):
            nt = st.text_input("Title", placeholder="e.g. B+ Tree key insights", key="n_title")
            nb = st.text_area("Notes", height=130, placeholder="Write your notes here...", key="n_body")
            ng = st.text_input("Tags", placeholder="DBMS, indexing, exam", key="n_tags")
            if st.button("Save note ✦", key="save_note"):
                if nt:
                    session_data["notes"].append({
                        "title": nt, "body": nb,
                        "tags": [t.strip() for t in ng.split(",") if t.strip()],
                        "created": datetime.now().strftime("%b %d, %H:%M")
                    })
                    save_session(sid, session_data)
                    st.success("Note saved!")
                    st.rerun()

        colors = ["", "green", "lav", "amber"]
        for i, note in enumerate(reversed(notes)):
            c = colors[i % 4]
            tags_html = "".join([f'<span style="background:#f0f4f0;color:#4a7a5a;font-size:10px;padding:2px 7px;border-radius:8px;margin-right:4px;">{t}</span>' for t in note.get("tags", [])])
            st.markdown(f"""
            <div class="note-card {c}">
                <div style='font-size:13px;font-weight:600;color:#1a1f2e;margin-bottom:5px;'>{note['title']}</div>
                <div style='font-size:11.5px;color:#5a6578;line-height:1.6;margin-bottom:8px;'>{note['body'][:200]}{'...' if len(note['body'])>200 else ''}</div>
                <div style='display:flex;align-items:center;justify-content:space-between;'>
                    <div>{tags_html}</div>
                    <div style='font-size:10px;color:#a0a8b8;'>{note['created']}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

    with tab2:
        diary = session_data.get("diary", [])

        st.markdown('<div class="lum-card">', unsafe_allow_html=True)
        st.markdown("<div style='font-size:13px;font-weight:600;color:#1a1f2e;margin-bottom:10px;'>Today's entry</div>", unsafe_allow_html=True)
        mood = st.select_slider("Mood", options=["😔 tough", "😐 okay", "😊 great"], key="diary_mood")
        entry_text = st.text_area("How did today go?", height=100,
            placeholder="What did you study? What clicked? What was confusing?", key="diary_text")
        if st.button("Save entry ✦", key="save_diary"):
            if entry_text:
                add_diary_entry(sid, entry_text, mood)
                st.success("Entry saved!")
                st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<div style='margin-top:16px;'>", unsafe_allow_html=True)
        mood_colors = {"😊 great": "", "😐 okay": "lav", "😔 tough": "amber"}
        mood_icons = {"😊 great": "🟢", "😐 okay": "🟡", "😔 tough": "🔴"}
        for entry in reversed(diary[-8:]):
            c = mood_colors.get(entry["mood"], "")
            ic = mood_icons.get(entry["mood"], "⚪")
            st.markdown(f"""
            <div class="diary-card {c}">
                <div style='font-size:10px;color:#8896a8;font-weight:500;margin-bottom:4px;'>
                    {ic} {entry['date']} · {entry['mood']}
                </div>
                <div style='font-size:12px;color:#1a1f2e;line-height:1.6;'>{entry['text']}</div>
            </div>
            """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────
# PAGE: TO-DO LIST
# ─────────────────────────────────────────────────────────────
elif st.session_state.page == "todos":
    page_header("✅", "To-do List", "Track tasks, deadlines, and study goals")

    st.markdown("<div style='padding:24px;'>", unsafe_allow_html=True)
    st.markdown('<div class="lum-card">', unsafe_allow_html=True)

    c1, c2, c3 = st.columns([4, 1, 1])
    with c1:
        new_task = st.text_input("New task", placeholder="e.g. Revise indexing chapter", key="todo_input", label_visibility="collapsed")
    with c2:
        pri = st.selectbox("", ["🔴 high", "🟡 medium", "🟢 low"], key="todo_pri", label_visibility="collapsed")
    with c3:
        if st.button("Add ✦", key="add_todo"):
            if new_task:
                add_todo(sid, new_task, pri.split(" ")[1])
                st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)

    todos = session_data.get("todos", [])
    pending = [t for t in todos if not t.get("done")]
    done_list = [t for t in todos if t.get("done")]

    pri_icons = {"high": "🔴", "medium": "🟡", "low": "🟢"}
    pri_order = {"high": 0, "medium": 1, "low": 2}
    pending_sorted = sorted(pending, key=lambda x: pri_order.get(x.get("priority", "medium"), 1))

    if pending_sorted:
        st.markdown("<div style='font-size:11px;font-weight:600;color:#a0a8b8;text-transform:uppercase;letter-spacing:0.07em;margin:8px 0 6px;'>Pending</div>", unsafe_allow_html=True)
        for i, todo in enumerate(pending_sorted):
            col1, col2 = st.columns([9, 1])
            with col1:
                ic = pri_icons.get(todo.get("priority", "medium"), "⚪")
                st.markdown(f"""
                <div class="todo-row">
                    <span style='font-size:14px;'>{ic}</span>
                    <span style='font-size:13px;color:#1a1f2e;'>{todo['text']}</span>
                </div>
                """, unsafe_allow_html=True)
            with col2:
                if st.button("✓", key=f"td_{i}"):
                    idx = todos.index(todo)
                    session_data["todos"][idx]["done"] = True
                    save_session(sid, session_data)
                    st.rerun()

    if done_list:
        st.markdown("<div style='font-size:11px;font-weight:600;color:#a0a8b8;text-transform:uppercase;letter-spacing:0.07em;margin:16px 0 6px;'>Done ✅</div>", unsafe_allow_html=True)
        for todo in done_list:
            st.markdown(f"""
            <div style='padding:8px 14px;border-radius:10px;background:#f5f3ee;
                        font-size:12.5px;color:#a0a8b8;text-decoration:line-through;margin-bottom:5px;'>
                {todo['text']}
            </div>
            """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────
# PAGE: PROGRESS
# ─────────────────────────────────────────────────────────────
elif st.session_state.page == "progress":
    page_header("📊", "My Progress", "Track your accuracy across all topics")

    st.markdown("<div style='padding:24px;'>", unsafe_allow_html=True)
    topics = session_data.get("topics", {})
    weak = get_weak_topics(sid)

    if not topics:
        st.markdown("""
        <div style='text-align:center;padding:60px 20px;'>
            <div style='font-size:40px;margin-bottom:12px;'>📊</div>
            <div style='font-size:16px;font-weight:500;color:#1a1f2e;margin-bottom:8px;'>No data yet</div>
            <div style='font-size:13px;color:#8896a8;'>Start quizzing to track your topic accuracy here</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        total = len(topics)
        strong = len([t for t, s in topics.items() if s["total"] > 0 and s["correct"]/s["total"] > 0.75])
        weak_count = len(weak)

        c1, c2, c3, c4 = st.columns(4)
        with c1:
            st.metric("Topics tracked", total)
        with c2:
            st.metric("Strong ✅", strong)
        with c3:
            st.metric("Needs work ⚠️", weak_count)
        with c4:
            avg = sum(s["correct"]/s["total"] for s in topics.values() if s["total"]>0) / max(len(topics),1)
            st.metric("Overall accuracy", f"{avg*100:.0f}%")

        st.markdown("---")
        st.markdown('<div class="lum-card">', unsafe_allow_html=True)
        st.markdown("<div style='font-size:13px;font-weight:600;color:#1a1f2e;margin-bottom:14px;'>Topic breakdown</div>", unsafe_allow_html=True)

        for topic, scores in sorted(topics.items(), key=lambda x: x[1]["correct"]/max(x[1]["total"],1)):
            if scores["total"] > 0:
                acc = scores["correct"] / scores["total"]
                bar_color = "#a8c8a0" if acc > 0.75 else ("#e8b86a" if acc > 0.5 else "#e8a090")
                icon = "✅" if acc > 0.75 else ("⚠️" if acc > 0.5 else "🔴")
                st.markdown(f"""
                <div style='display:flex;align-items:center;gap:10px;margin-bottom:10px;'>
                    <span style='font-size:14px;'>{icon}</span>
                    <span style='font-size:12.5px;color:#1a1f2e;flex:1;'>{topic}</span>
                    <span style='font-size:11px;color:#8896a8;'>{scores['correct']}/{scores['total']}</span>
                    <span style='font-size:12px;font-weight:600;color:#1a1f2e;min-width:38px;text-align:right;'>{acc*100:.0f}%</span>
                </div>
                """, unsafe_allow_html=True)
                st.progress(acc)

        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────
# PAGE: DSA ROADMAP
# ─────────────────────────────────────────────────────────────
elif st.session_state.page == "dsa":
    page_header("💻", "DSA & Placement Prep", "Roadmaps, company kits, and CS fundamentals")

    st.markdown("<div style='padding:24px;'>", unsafe_allow_html=True)

    option = st.radio("", ["📍 Full DSA Roadmap", "🏢 Company prep", "🎯 CS Fundamentals Q&A"],
                      horizontal=True, key="dsa_radio", label_visibility="collapsed")

    st.markdown('<div class="lum-card" style="margin-top:12px;">', unsafe_allow_html=True)

    if option == "📍 Full DSA Roadmap":
        weeks = st.slider("Weeks available", 4, 16, 8)
        if st.button("✦ Generate roadmap", key="gen_road"):
            with st.spinner("Building your DSA roadmap..."):
                response = run_agent(f"Give me a complete DSA roadmap for placement prep. I have {weeks} weeks. Cover arrays to DP with LeetCode problems.")
            st.markdown("---")
            st.markdown(response)

    elif option == "🏢 Company prep":
        company = st.text_input("Company name", placeholder="e.g. TCS, Infosys, Amazon, Google")
        if st.button("✦ Generate prep kit", key="gen_comp") and company:
            with st.spinner(f"Building {company} placement kit..."):
                response = run_agent(f"Give me a complete placement prep kit for {company}.")
            st.markdown("---")
            st.markdown(response)

    elif option == "🎯 CS Fundamentals Q&A":
        subj = st.selectbox("Subject", ["Operating Systems", "DBMS", "Computer Networks", "OOP", "System Design"])
        if st.button("✦ Get interview Q&As", key="gen_cs"):
            with st.spinner("Fetching most-asked questions..."):
                response = run_agent(f"Give me top 10 most-asked interview questions on {subj} with detailed answers.")
            st.markdown("---")
            st.markdown(response)

    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)