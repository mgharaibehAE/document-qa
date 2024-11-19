import streamlit as st
import openai
import time

# Title of the app
st.title("Regulatory Assistant")

# User input for credentials
api_key = st.text_input("Enter your OpenAI API Key:", type="password")
username = st.text_input("Enter your username:")
password = st.text_input("Enter your password:", type="password")

# Check credentials
if username == "ClecoDC" and password == "Regulatory" and api_key:
    # Set the OpenAI API key
    openai.api_key = api_key

    # Initialize chat history in session state
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Function to wait for OpenAI run completion
    def wait_on_run(run_id, thread_id):
        """Wait for the OpenAI run to complete."""
        status = "queued"
        while status in ["queued", "in_progress"]:
            run = openai.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run_id)
            status = run.status
            time.sleep(1)
        return run

    # Function to get the assistant's response
    def get_assistant_response(content):
        """Get the assistant response from OpenAI API."""
        try:
            thread = openai.beta.threads.create()
            message = openai.beta.threads.messages.create(thread_id=thread.id, role="user", content=content)
            assistant_id = "asst_PJzdjZtWBpZYtgA7JtF5Pynp"  # Fixed assistant ID
            run = openai.beta.threads.runs.create(thread_id=thread.id, assistant_id=assistant_id)
            run = wait_on_run(run.id, thread.id)
            messages = openai.beta.threads.messages.list(thread.id)
            return messages
        except Exception as e:
            st.error(f"An error occurred: {e}")
            return None

    # Display chat messages from history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"], unsafe_allow_html=True)

    # User input for the assistant
    if user_input := st.chat_input("Ask a question to the Regulatory Assistant..."):
        with st.chat_message("user"):
            st.markdown(user_input)
        st.session_state.messages.append({"role": "user", "content": user_input})
        messages = get_assistant_response(user_input)
        if messages:
            for msg in messages.data:
                if msg.role == "assistant":
                    response_text = msg.content[0].text.value
                    with st.chat_message("assistant"):
                        st.markdown(response_text, unsafe_allow_html=True)  # Render text with hyperlinks
                    st.session_state.messages.append({"role": "assistant", "content": response_text})

else:
    st.warning("Please enter valid credentials to access the Regulatory Assistant.")
