import os
import json
from typing import List, Dict
from utils.constants import DATABASE_PATH

def save_to_json(question, answer):
    # Initialize the database if it does not exist
    if not os.path.exists(DATABASE_PATH):
        with open(DATABASE_PATH, 'w') as file:
            json.dump([], file)
    
    try:
        # Read the existing data
        with open(DATABASE_PATH, 'r') as file:
            data = json.load(file)
    except json.JSONDecodeError:
        data = []
    
    # Append the new question and answer
    data.append({"user": question, "assistant": answer})
    
    # Write the updated data back to the file
    with open(DATABASE_PATH, 'w') as file:
        json.dump(data, file, indent=4)
    
    return "success"

#############################################################################################################################################
    
async def read_chat_history(limit: int = 999999) -> List[Dict[str, str]]:
    try:
        with open(DATABASE_PATH, 'r') as file:
            data = json.load(file)
            filtered_data = [entry for entry in data if not (entry.get('role') == 'system')]
            return filtered_data[-limit:]
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        return []

#############################################################################################################################################

async def format_chat_history(chat_history: List[Dict[str, str]]) -> List:
    formatted_history = []
    
    for entry in chat_history:
        if "user" in entry:
            formatted_history.append({
                "role":"user",
                "content":entry["user"]
            })
        if "assistant" in entry:
            formatted_history.append({
                "role":"assistant",
                "content":entry["assistant"]
            })
    
    return formatted_history

#############################################################################################################################################

def update_system_prompt(system_prompt):
    # Load existing data
    if os.path.exists(DATABASE_PATH):
        with open(DATABASE_PATH, 'r') as file:
            data = json.load(file)
    else:
        data = []

    # Check if a system prompt exists and replace or add new one
    updated = False
    new_data = []
    for item in data:
        if 'role' in item and item['role'] == 'system':
            # Replace existing system prompt
            new_data.append({'role': 'system', 'content': system_prompt})
            updated = True
        else:
            new_data.append(item)

    # If no existing system prompt was found, add the new one at the top
    if not updated:
        new_data.insert(0, {'role': 'system', 'content': system_prompt})

    # Save updated data back to file
    with open(DATABASE_PATH, 'w') as file:
        json.dump(new_data, file, indent=4)

    return new_data

#############################################################################################################################################

def read_system_prompt() -> List[Dict[str, str]]:
    try:
        with open(DATABASE_PATH, 'r') as file:
            data = json.load(file)
            # Find the system prompt entry
            for entry in data:
                if entry.get('role') == 'system':
                    return [{'role': 'system', 'content': entry['content']}]
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        return []

    # Return an empty list if no system prompt is found
    return []

#############################################################################################################################################

def clear_chat_history():
    # Check if the file exists
    if not os.path.exists(DATABASE_PATH):
        print(f"The file {DATABASE_PATH} does not exist.")
        return

    # Clear the chat history by writing an empty list to the file
    with open(DATABASE_PATH, 'w') as file:
        json.dump([], file, indent=4)

    return 'success'