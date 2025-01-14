import streamlit as st
from groq import Groq
import time

# Initialize Groq client
client = Groq(
    api_key="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"
)

# Set page configuration
st.set_page_config(page_title="Chat with LLaMA", page_icon="🦙", layout="wide")

# Initialize session state for chat history and system message if they don't exist
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "system",
            "content": "You are a helpful assistant."
        }
    ]

# Simplified CSS for better readability
st.markdown("""
<style>
    .user-message {
        background-color: #F0F2F6;
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
    }
    .assistant-message {
        background-color: #E8EAF6;
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
    }
    .stMarkdown {
        color: black !important;
    }
</style>
""", unsafe_allow_html=True)

# Display chat title
st.title("💬 Chat with LLaMA")

# Simplified sidebar with essential controls
with st.sidebar:
    st.markdown("### Model Settings")
    temperature = st.slider("Temperature", 0.0, 1.0, 0.5, 0.1)
    max_tokens = st.slider("Max Tokens", 256, 4096, 1024, 256)

# Display chat messages
for message in st.session_state.messages[1:]:  # Skip system message
    if message["role"] == "user":
        st.markdown(f"""<div class="user-message">👤 <b>You:</b> {message["content"]}</div>""", unsafe_allow_html=True)
    else:
        st.markdown(f"""<div class="assistant-message">🤖 <b>Assistant:</b> {message["content"]}</div>""", unsafe_allow_html=True)

# Chat input
if prompt := st.chat_input("What would you like to know?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Create the chat completion
    with st.spinner("Thinking..."):
        try:
            chat_completion = client.chat.completions.create(
                messages=st.session_state.messages,
                model="llama-3.3-70b-versatile",
                temperature=temperature,
                max_tokens=max_tokens,
                stream=True
            )
            
            # Initialize placeholder for streaming response
            response_placeholder = st.empty()
            full_response = ""
            
            # Stream the response
            for chunk in chat_completion:
                if chunk.choices[0].delta.content is not None:
                    full_response += chunk.choices[0].delta.content
                    response_placeholder.markdown(
                        f"""<div class="assistant-message">🤖 <b>Assistant:</b> {full_response}</div>""",
                        unsafe_allow_html=True
                    )
            
            # Add assistant response to chat history
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")