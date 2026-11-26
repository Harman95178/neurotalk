import streamlit as st
import google.generativeai as genai
import webbrowser

if "chat_data" not in st.session_state:
    st.session_state.chat_data = []

genai.configure(api_key="YOUR_API_KEY")
model = genai.GenerativeModel("gemini-2.5-flash")

st.header("🤖 My Personal AI Bot")
st.subheader("Ask anything in your mind❓")

user_input = st.chat_input("Write your query...")

if user_input:
    st.session_state.chat_data.append(("👩‍🦰Me", user_input))

    if any(phrase in user_input.lower() for phrase in ["who build you", "who make you", "who developed you"]):
        bot_reply = "I am an AI Model. Designed and developed by Harmandeep Kaur in 2025."
    elif "open youtube" in user_input.lower():
        webbrowser.open("https://www.youtube.com/")
        bot_reply = "✅ Opening YouTube for you..."
    else:
        response = model.generate_content(user_input)
        bot_reply = response.text

    st.session_state.chat_data.append(("🤖Bot", bot_reply))

for role, msg in st.session_state.chat_data:
    with st.chat_message(role):
        if role == "👩‍🦰Me":
            st.warning(msg)
        else:
            st.success(msg)
    