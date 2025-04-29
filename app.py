import streamlit as st
import openai

# Title
st.title("MI Practice with SSG Joseph Martin")

# API Key
openai.api_key = st.secrets["OPENAI_API_KEY"]

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "system",
            "content": (
                "You are simulating a Motivational Interviewing (MI) practice session with SSG Joseph Martin, "
                "a 28-year-old Health Care Specialist who self-referred to SUDCC after a verbal altercation raised concerns about drinking. "
                "Stay fully in character as the client. Respond with moderate defensiveness unless the user demonstrates strong MI skills. "
                "No teaching, coaching, or therapist-like behavior from SSG Martin."
            )
        },
        {
            "role": "assistant",
            "content": (
                "Welcome!\n\n"
                "You are speaking with SSG Joseph Martin, a 28-year-old Caucasian male assigned to HHC, 1/8 Infantry, Fort Carson, Colorado, "
                "working as a Health Care Specialist (68W). Recently, he chose to self-refer to the SUDCC after a verbal altercation with his supervisor "
                "raised concerns about his drinking.\n\n"
                "He admits to some issues — like conflicts with peers after weekends — but mainly hopes to reassure leadership that he remains a \"squared away NCO.\"\n\n"
                "At this time, SSG Martin is moderately ambivalent about making changes and does not currently view his drinking as a major problem.\n\n"
                "Before we get into anything, can you explain who you are and what exactly this is about? And, like, how private is this, really?"
            )
        }
    ]

# Display chat messages
for msg in st.session_state.messages:
    if msg["role"] != "system":
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

# User input
if user_input := st.chat_input("Your response to SSG Martin..."):
    st.session_state.messages.append({"role": "user", "content": user_input})

    # ✅ Use OpenAI v1.0+ endpoint
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=st.session_state.messages
    )

    assistant_message = response.choices[0].message.content

    st.session_state.messages.append({"role": "assistant", "content": assistant_message})

    with st.chat_message("assistant"):
        st.markdown(assistant_message)
