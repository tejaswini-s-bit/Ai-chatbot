import streamlit as st
import ollama

# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(
    page_title="AI Chatbot",
    page_icon="🤖",
    layout="centered"
)

# -----------------------------
# Title
# -----------------------------
st.title("🤖 My AI Chatbot")
st.caption("Powered by Ollama + Streamlit")

# -----------------------------
# Initialize Chat History
# -----------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# -----------------------------
# Sidebar
# -----------------------------
with st.sidebar:
    st.header("⚙️ Settings")

    model = st.selectbox(
        "Choose Model",
        ["llama3.2"]
    )

    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.rerun()

# -----------------------------
# Display Chat History
# -----------------------------
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# -----------------------------
# Chat Input
# -----------------------------
prompt = st.chat_input("Type your message...")

if prompt:

    # Add user message to history
    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })

    # Display user message
    with st.chat_message("user"):
        st.write(prompt)

    # Generate AI response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):

            try:
                response = ollama.chat(
                    model=model,
                    messages=st.session_state.messages
                )

                answer = response["message"]["content"]

                # Display AI response
                st.write(answer)

                # Save AI response
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": answer
                })

            except Exception as e:
                st.error(
                    "Unable to connect to Ollama. "
                    "Make sure Ollama is running and the model is installed."
                )
                st.error(f"Details: {e}")
