import streamlit as st
from groq import Groq
import json
import os
from dotenv import load_dotenv


load_dotenv()
api_key = os.getenv("GROQ_API_KEY")


client = Groq(api_key=api_key)


if 'messages' not in st.session_state:
    st.session_state.messages = []


st.sidebar.header("⚙️ Settings")
model_options = [
    "gemma2-9b-it", "deepseek-r1-distill-llama-70b", "llama-3.1-8b-instant",
    "llama-3.2-11b-vision-preview", "llama-3.2-1b-preview", "llama-3.2-3b-preview",
    "llama-3.2-90b-vision-preview", "llama-3.3-70b-specdec", "llama-3.3-70b-versatile",
    "llama-guard-3-8b"
]  
selected_model = st.sidebar.selectbox("🤖 Select Model", model_options)

temperature = st.sidebar.slider("🌡 Temperature", min_value=0.1, max_value=2.0, value=1.0, step=0.1)
max_tokens = st.sidebar.slider("📝 Max Tokens", min_value=100, max_value=4096, value=1024, step=100)


st.title("Your Buddy 😎")


for message in st.session_state.messages:
    with st.chat_message("user" if message["role"] == "user" else "assistant"):
        st.markdown(message["content"])


user_input = st.chat_input("© 2025 Sundram Sharma. All rights reserved....")


if user_input:
    
    st.session_state.messages.append({"role": "user", "content": user_input})

    
    with st.chat_message("user"):
        st.markdown(user_input)

  
    try:
        response = client.chat.completions.create(
            model=selected_model,
            messages=st.session_state.messages,
            temperature=temperature,
            max_tokens=max_tokens,
            top_p=1,
        )

        
        response_text = response.choices[0].message.content.strip()

      
        st.session_state.messages.append({"role": "assistant", "content": response_text})

        
        with st.chat_message("assistant"):
            st.markdown(response_text)

    except Exception as e:
        st.error(f"❌ Error: {str(e)}")




