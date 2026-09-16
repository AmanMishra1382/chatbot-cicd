import streamlit as st
import uuid

from backend import get_response


# Page configuration
st.set_page_config(
    page_title="LangGraph Chatbot",
    page_icon="🤖"
)


# Title
st.title("🤖 LangGraph Chatbot")
st.caption("Powered by LangGraph + Mistral")


# Create a unique thread ID for this user session
if "thread_id" not in st.session_state:
    st.session_state.thread_id = str(uuid.uuid4())


# Store messages for displaying in Streamlit
if "messages" not in st.session_state:
    st.session_state.messages = []


# Display previous messages
for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# Chat input
user_input = st.chat_input("Type your message...")


# When user sends a message
if user_input:

    # Display user message
    with st.chat_message("user"):
        st.markdown(user_input)

    # Save user message
    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_input
        }
    )

    # Get response from LangGraph backend
    with st.chat_message("assistant"):

        with st.spinner("Thinking..."):

            response = get_response(
                user_input,
                st.session_state.thread_id
            )

        st.markdown(response)

    # Save AI response
    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": response
        }
    )