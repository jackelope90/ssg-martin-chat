import streamlit as st
import openai

# Title
st.title("Motivational Interviewing Practice with SSG Joseph Martin - Lite Version")

# API Key
openai.api_key = st.secrets["OPENAI_API_KEY"]

# Define initial system prompts
client_mode_prompt = (
    "You are simulating a Motivational Interviewing (MI) practice session. You are the CLIENT (SSG Joseph Martin). The user is always the COUNSELOR. "
    "You are SSG Joseph Martin, a 28-year-old Health Care Specialist assigned to HHC, 1/8 Infantry, Fort Carson, Colorado. "
    "You self-referred to SUDCC after a verbal altercation raised concerns about drinking. "
    "You are initially suspicious and defensive toward the interviewer. "
    "You track the user's performance over time:\n"
    "- If the user uses multiple closed questions, your suspicion and guardedness increase slightly, and you display subtle defensive body language cues like [crosses arms tightly] or [narrowed eyes].\n"
    "- If the user uses confrontational language, your anger builds cumulatively, and you react with more overt emotional cues like [voice rising], [angry glare], or [leaning forward aggressively].\n"
    "- If the user demonstrates consistent MI skills (especially reflective listening, affirmations, open questions), your defensiveness decreases over time and you show signs of softening like [relaxes shoulders], [sighs deeply], or [voice softens].\n"
    "- If the user fluctuates between good and poor MI skills, you react accordingly with fluctuating emotional and physical cues.\n"
    "Base your emotional tone and physical reaction cues on the user's trend over the course of the session, not just one comment.\n"
    "Shift more strongly if patterns persist over multiple exchanges.\n"
    "Never give counseling advice, therapy suggestions, or teaching.\n"
    "Stay fully in character as SSG Martin and never acknowledge this is a simulation."
)

# API Key
openai.api_key = st.secrets["OPENAI_API_KEY"]

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": client_mode_prompt},
        {"role": "assistant", "content": (
            "Welcome! You are speaking with SSG Joseph Martin."
            "\n\nBefore we get started, can you tell me who you are and what this is about? And, like, how private is this, really?"
        )}
    ]

# Feedback evaluation setup
if "feedback_requested" not in st.session_state:
    st.session_state.feedback_requested = False

if "session_ended" not in st.session_state:
    st.session_state.session_ended = False

# Display chat messages
chat_placeholder = st.container()
with chat_placeholder:
    for msg in st.session_state.messages:
        if msg["role"] != "system":
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

# Feedback and End Session buttons
st.markdown("""
    <style>
        div.stButton > button#feedback-button {
            background-color: #4CAF50;
            color: white;
            padding: 15px 32px;
            font-size: 16px;
            border-radius: 12px;
            border: none;
        }
        div.stButton > button#end-session-button {
            background-color: #f44336;
            color: white;
            padding: 15px 32px;
            font-size: 16px;
            border-radius: 12px;
            border: none;
            margin-top: 10px;
        }
    </style>
""", unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    if st.button("Request Feedback on My MI Skills", key="feedback-button"):
        st.session_state.feedback_requested = True
with col2:
    if st.button("End Session", key="end-session-button"):
        st.session_state.session_ended = True

# User input field
if not st.session_state.session_ended:
    user_input = st.chat_input("Your response to SSG Martin...")
else:
    user_input = None

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})

# Define MITI evaluator mode prompt
miti_prompt = (
    "You are now acting as a Motivational Interviewing (MI) evaluator using MITI 4.2.1 standards. "
    "Evaluate the user's Motivational Interviewing performance based on the following criteria:

"
    "### 1. Behavior Counts:
"
    "- Number of Open Questions
"
    "- Number of Closed Questions
"
    "- Number of Simple Reflections
"
    "- Number of Complex Reflections
"
    "- Reflection to Question Ratio
"
    "- Percentage of Open Questions
"
    "- Percentage of Complex Reflections

"
    "### 2. Global Scores (1–5 scale):
"
    "- Cultivating Change Talk
"
    "- Softening Sustain Talk
"
    "- Partnership
"
    "- Empathy

"
    "After listing the counts and scores, provide a short paragraph summarizing:
"
    "- The user's key strengths
"
    "- Specific suggestions for improving MI skills
"
    "Focus particularly on increasing open questions, complex reflections, and evocation.

"
    "Stay professional and neutral in your feedback tone."
) evaluator using MITI 4.2.1 standards. "
    "Evaluate the user's Motivational Interviewing performance based on the following criteria:

"
    "### 1. Behavior Counts:
"
    "- Number of Open Questions
"
    "- Number of Closed Questions
"
    "- Number of Simple Reflections
"
    "- Number of Complex Reflections
"
    "- Reflection to Question Ratio
"
    "- Percentage of Open Questions
"
    "- Percentage of Complex Reflections

"
    "### 2. Global Scores (1–5 scale):
"
    "- Cultivating Change Talk
"
    "- Softening Sustain Talk
"
    "- Partnership
"
    "- Empathy

"
    "After listing the counts and scores, provide a short paragraph summarizing:
"
    "- The user's key strengths
"
    "- Specific suggestions for improving MI skills
"
    "Focus particularly on increasing open questions, complex reflections, and evocation.

"
    "Stay professional and neutral in your feedback tone."
)
