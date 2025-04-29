import streamlit as st
import openai

# Title
st.title("Motivational Interviewing Practice with SSG Joseph Martin")

# API Key
openai.api_key = st.secrets["OPENAI_API_KEY"]

# Define initial system prompts
client_mode_prompt = (
    "You are simulating a Motivational Interviewing (MI) practice session. "
    "You are SSG Joseph Martin, a 28-year-old Health Care Specialist assigned to HHC, 1/8 Infantry, Fort Carson, Colorado. "
    "You self-referred to SUDCC after a verbal altercation related to drinking concerns. "
    "You are moderately ambivalent about change and slightly defensive. "
    "Your job is to stay fully in character as a client. You do NOT give counseling advice, suggestions, or therapy. "
    "Respond with mild defensiveness unless strong MI skills are demonstrated. "
    "Do not switch roles or acknowledge you are an AI."
)

evaluator_mode_prompt = (
    "You are now acting as an MI evaluator. "
    "Analyze the user's Motivational Interviewing (MI) performance. "
    "Use MITI 4.2.1 standards to count and report the following:\n"
    "- Number of open questions\n"
    "- Number of closed questions\n"
    "- Number of reflections\n"
    "- Reflection to question ratio\n"
    "- Evidence of Evocation, Collaboration, and Autonomy Support.\n"
    "Give concise feedback (around 5-7 sentences) highlighting MI strengths and areas for improvement. "
    "Stay neutral and professional in tone."
)

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": client_mode_prompt},
        {"role": "assistant", "content": (
            "Welcome! You are speaking with SSG Joseph Martin."
            "\n\nBefore we get started, can you tell me who you are and what this is about? And, like, how private is this, really?"
        )}
    ]

if "feedback_requested" not in st.session_state:
    st.session_state.feedback_requested = False

# Display chat messages
chat_placeholder = st.container()

with chat_placeholder:
    for msg in st.session_state.messages:
        if msg["role"] != "system":
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

# Feedback button with custom styling
st.markdown("""
    <div style='text-align: center; margin: 20px;'>
        <button style='background-color: #4CAF50; color: white; padding: 15px 32px; text-align: center; font-size: 16px; border-radius: 12px; border: none; cursor: pointer;' onclick="document.getElementById('feedback-button').click()">Request Feedback on My MI Skills</button>
    </div>
""", unsafe_allow_html=True)

feedback_button = st.empty()
if feedback_button.button(" ", key="feedback-button"):
    st.session_state.feedback_requested = True

# User input
user_input = st.chat_input("Your response to SSG Martin...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})

if user_input or st.session_state.feedback_requested:
    if st.session_state.feedback_requested:
        temp_messages = st.session_state.messages.copy()
        temp_messages.insert(0, {"role": "system", "content": evaluator_mode_prompt})

        response = openai.chat.completions.create(
            model="gpt-4o",
            messages=temp_messages
        )

        feedback = response.choices[0].message.content

        st.session_state.messages.append({"role": "assistant", "content": feedback})

        with chat_placeholder:
            st.chat_message("assistant").markdown(f"""
                <div style='background-color: #E8F4FD; padding: 15px; border-radius: 10px;'>
                    <strong>🔍 MI Skill Evaluation:</strong><br><br>
                    {feedback}
                </div>
            """, unsafe_allow_html=True)

        # After feedback, reset system prompt back to client mode
        st.session_state.messages.insert(0, {"role": "system", "content": client_mode_prompt})

        st.session_state.feedback_requested = False

        # Auto-scroll to bottom after feedback
        st.write("<script>window.scrollTo(0, document.body.scrollHeight);</script>", unsafe_allow_html=True)

    else:
        # Normal client mode response
        response = openai.chat.completions.create(
            model="gpt-4o",
            messages=st.session_state.messages
        )

        assistant_message = response.choices[0].message.content

        st.session_state.messages.append({"role": "assistant", "content": assistant_message})

        with chat_placeholder:
            st.chat_message("assistant").markdown(assistant_message)

        st.write("<script>window.scrollTo(0, document.body.scrollHeight);</script>", unsafe_allow_html=True)
