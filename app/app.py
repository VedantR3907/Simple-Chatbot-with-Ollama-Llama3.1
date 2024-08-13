import asyncio
import streamlit as st
from streamlit_extras.bottom_container import bottom
from api.ollama import ollama_api
from utils.helper.ChatHistory import clear_chat_history, update_system_prompt, read_system_prompt, save_to_json, read_chat_history


def display_chat_history(chat_history):
    for entry in chat_history:
        if "user" in entry:
            with st.chat_message("HUMAN", avatar='./assets/static/images/user.png'):
                st.markdown(entry["user"])
        if "assistant" in entry:
            with st.chat_message("AI", avatar='./assets/static/images/ollama.png'):
                st.markdown(entry["assistant"])

def bottom_container():
    with bottom():      
        user_prompt = st.chat_input("Write a question")
        if user_prompt:
            return user_prompt

async def main():
    # Sidebar for system prompt
    st.sidebar.header("System Prompt")
    system_prompt = st.sidebar.text_area("Enter System Prompt", "", placeholder="You are a helpful assistant.")
    submit_button = st.sidebar.button("Submit System Prompt")

    clear_history_button = st.sidebar.button("Clear Chat History")

    if submit_button:
        update_system_prompt(system_prompt)
    
    if clear_history_button:
        clear_chat_history()

    # Check if system prompt is submitted and not empty
    if read_system_prompt() == []:
        st.sidebar.warning("System prompt cannot be empty. Please enter a system prompt and save it.")
        return  # Exit the function if system prompt is empty
    
    # Proceed with the main content if system prompt is valid
    st.header("OLLAMA CHATBOT LLAMA-3.1")


    user_prompt = bottom_container()
    if user_prompt is not None and user_prompt != '':
        response = await ollama_api(user_prompt)
        with st.container(border=False, height=500):
            chat_history = await read_chat_history()
            display_chat_history(chat_history)
            
            with st.chat_message("HUMAN", avatar='./assets/static/images/user.png'):
                st.markdown(user_prompt)
                
            with st.chat_message("AI", avatar='./assets/static/images/ollama.png'):
                streamed_response = st.write_stream(response)
            
            save_to_json(user_prompt, streamed_response)

if __name__ == "__main__":
    asyncio.run(main())