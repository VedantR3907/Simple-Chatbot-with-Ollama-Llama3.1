from openai import OpenAI
from utils.constants import OLLAMA_API
from utils.helper.ChatHistory import read_chat_history, format_chat_history, read_system_prompt

client = OpenAI(
    base_url = OLLAMA_API,
    api_key='ollama',
)

async def ollama_api(user_prompt):
    chat_history = await read_chat_history(limit=5)
    formatted_history = await format_chat_history(chat_history)
    
    chat_completion = client.chat.completions.create(
        messages=read_system_prompt() +
                 formatted_history +
                 [{'role': 'user', 'content': user_prompt}],
        model='llama3.1',
        stream=True
    )
    
    return chat_completion