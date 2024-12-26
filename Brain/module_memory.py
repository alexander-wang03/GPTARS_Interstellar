"""
module_memory.py

Memory Management Module for GPTARS.

Handles long-term and short-term memory storage, memory injections, character data management, 
and token count calculations. Ensures contextual and historical knowledge during interactions.
"""
# === Standard Libraries ===
import os
import sys
import re
import json
import requests
from typing import List
from datetime import datetime
from transformers import pipeline
from hyperdb import HyperDB

# === Custom Modules ===
from module_config import load_config
from memory.hyperdb import *

# === Constants and Globals ===
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
os.chdir(BASE_DIR)
sys.path.insert(0, BASE_DIR)
sys.path.append(os.getcwd())

CONFIG = load_config()
MEMORY_DB_PATH = os.path.abspath(f"memory/{CONFIG['CHAR']['char_name']}.pickle.gz")

# Memory configuration
longMEM_Use = True

# UNUSED
def get_shortterm_memories_recent(max_entries: int) -> List[str]:
    """
    Retrieve the most recent short-term memories.

    Parameters:
    - max_entries (int): Number of recent memories to retrieve.

    Returns:
    - List[str]: List of recent memory documents.
    """
    # Get the memory dictionary
    memory_dict = hyper_db.dict()
    return [entry['document'] for entry in memory_dict[-max_entries:]] # Retrieve the most recent entries

def get_shortterm_memories_tokenlimit(short_term_tokens: int) -> str:
    """
    Retrieve recent short-term memories constrained by token limits.

    Parameters:
    - short_term_tokens (int): Maximum number of tokens.

    Returns:
        str: Concatenated memories formatted for output.
    """
    memory_dict = hyper_db.dict()
    accumulated_documents = []  # Accumulate (user_input, bot_response) tuples
    accumulated_length = 0

    # Process entries in reverse to start with the most recent
    for entry in reversed(memory_dict):
        user_input = entry['document'].get('user_input', "")
        bot_response = entry['document'].get('bot_response', "")

        # Skip if user_input or bot_response is empty
        if not user_input or not bot_response:
            continue
        
        # Prepare text for token counting
        text_str = f"user_input: {user_input}\nbot_response: {bot_response}"
        text_length = token_count(text_str)['length']

        # Check if adding this entry would exceed the token limit
        if accumulated_length + text_length > short_term_tokens:
            # If so, since we are iterating in reverse, stop adding newer entries
            continue
        
        # Accumulate entry if it doesn't exceed the token limit
        accumulated_documents.append((user_input, bot_response))
        accumulated_length += text_length

    # Since we processed entries in reverse, reverse the accumulated list to maintain the original order in output
    #formatted_output = '\n'.join([f"user_input: {ui}\nbot_response: {br}" for ui, br in reversed(accumulated_documents)])
    formatted_output = '\n'.join([f"{{user}}: {ui}\n{{char}}: {br}" for ui, br in reversed(accumulated_documents)])

    return formatted_output

def get_related_memories(query: str) -> str:
    """
    Retrieve memories related to a given query from the HyperDB.

    Parameters:
    - query (str): The input query.

    Returns:
    - str: Relevant memories or a fallback message.
    """
    # Get a dictionary representation of the memories
    lst = hyper_db.dict()

    # Get the highest likelihood memory
    results = hyper_db.query(query, top_k=1, return_similarities=False)

    if results:
        # Get the highest likelihood memory
        memory = results[0]

        # Find the index of the highest likelihood memory in the list
        start_index = next((i for i, d in enumerate(lst) if d['document'] == memory), None)

        if start_index is not None:
            prev_count = 1
            post_count = 1

            # Calculate the start and end indices for retrieving context memories
            start = max(start_index - prev_count, 0)
            end = min(start_index + post_count + 1, len(lst))

            # Retrieve the context memories
            result = [lst[i]['document'] for i in range(start, end)]

            return result
        else:
            return f"Error: Could not locate memory in the database. Memory: {memory}"
    else:
        return "No memories found for the query."
    
def get_longterm_memory(user_input: str) -> str:
    """
    Retrieve long-term memory relevant to a user input.

    Parameters:
    - user_input (str): The user input.

    Returns:
    - str: Relevant memory.
    """
    try:
        if longMEM_Use:
            past = f'{get_related_memories(user_input)}'
        else:
            past = "None"
        return past
    except Exception as e:
        print(f'Error: {e}')
        return "Error retrieving long-term memory."

def write_longterm_memory(userinput: str, bot_response: str):
    """
    Store a user input and bot response as a long-term memory.

    Parameters:
    - userinput (str): The user's input.
    - bot_response (str): The bot's response.
    """
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    document = {
        "timestamp": current_time,
        "user_input": userinput,
        "bot_response": bot_response
    }
    hyper_db.add_document(document)
    hyper_db.save(MEMORY_DB_PATH)

# UNUSED
def write_tool_used(toolused: str):
    """
    Record the use of a tool in long-term memory.

    Parameters:
    - toolused (str): Description of the tool used.
    """
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    document = {
        "timestamp": current_time,
        "bot_response": toolused
    }
    hyper_db.add_document(document)
    hyper_db.save(MEMORY_DB_PATH)

def load_initial_memory(json_file_path: str):
    """
    Load memories from a JSON file and inject them into the memory database.

    Parameters:
    - json_file_path (str): Path to the JSON file.
    """
    # Check if json_file_path exists or it breaks
    if os.path.exists(json_file_path):
        print("Injecting Memories.")

        # Load memories from the JSON file
        with open(json_file_path, 'r') as file:
            memories = json.load(file)

        # Inject memories into the database
        for memory in memories:
            time = memory.get("time", "")
            userinput = memory.get("userinput", "")
            botresponse = memory.get("botresponse", "")

            # Check if "time" is not provided in the JSON and generate the current time
            if not time:
                time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # Check if "botresponse" is not provided in the JSON
            if not botresponse:
                botresponse = ""  # Or provide a default value if needed

            # Call the function to add the memory to the database
            write_longterm_memory(userinput, botresponse)

        # Rename the JSON file with the ".loaded" extension
        new_file_path = os.path.splitext(json_file_path)[0] + ".loaded"
        os.rename(json_file_path, new_file_path)
        #print(f"Memory Loaded: {new_file_path}")

def init_dynamic_memory():
    """
    Initialize and load long-term memory from a file.

    Parameters:
    - memory_db_path (str): Path to the memory database file.
    """
    global hyper_db, char_name
    hyper_db = HyperDB()
    
    # print('Initializing memory...')
    
    if os.path.exists(MEMORY_DB_PATH):

        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] LOAD: Found existing memory db: {MEMORY_DB_PATH}")
        loaded_successfully = hyper_db.load(MEMORY_DB_PATH)

        if loaded_successfully and hyper_db.vectors is not None:
            #print('Memory loaded successfully')
            print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] LOAD: Memory loaded successfully")
            #print(f'Documents: {hyper_db.documents}')
            #print(f'Vectors shape: {hyper_db.vectors.shape}')
        else:
            print("Error: Memory loading failed or is empty.")
            hyper_db.vectors = np.empty((0, 0), dtype=np.float32)  # Initialize vectors to an empty array
    else:
        print(f'No existing memory DB found. Creating new one: {MEMORY_DB_PATH}')
        hyper_db.add_document({"text": f'{char_name}: {char_greeting}'})  # Use add_document instead of memorize
        hyper_db.save(MEMORY_DB_PATH)

def summarize_text(article, max_len=250, min_len=0, do_sample=False):
    """
    Summarize a given text using a summarization model.

    Parameters:
    - article (str): Text to summarize.
    - max_len (int): Maximum length of the summary.
    - min_len (int): Minimum length of the summary.
    - do_sample (bool): Sampling behavior.

    Returns:
    - str: Summarized text.
    """
    summarizer = pipeline("summarization", model="Falconsai/text_summarization")
    summary = summarizer(article, max_length=max_len, min_length=min_len, do_sample=do_sample)
    return summary
    # prompt = shortMEM + "\n" + "\n" + str(last_six_lines) + str(new_line) + f'\n{{"role": "TARS.", "date": "{date}", "time": "{time}", "content": "'
    # prompt = str(prompt)

def load_character_attributes():
    """
    Load character attributes from the character card file.
    """
    global char_name, char_persona, personality, world_scenario, char_greeting, example_dialogue

    charactercard = CONFIG['CHAR']['charactercard']
    try:
        # Read the character card file content
        with open(charactercard, "r") as file:
            content = file.read()

        # Define a helper function to extract matched groups
        def extract_match(pattern, content, group=2, default=""):
            match = re.search(pattern, content)
            return match.group(group) if match else default
            
        # Extract character attributes using regex patterns
        char_name = extract_match(r'("char_name"|"name"):\s*"([^"]*)"', content)
        char_persona = extract_match(r'("char_persona"|"description"):\s*"([^"]*)"', content)
        personality = extract_match(r'"personality":\s*"([^"]*)"', content, group=1)
        world_scenario = extract_match(r'("world_scenario"|"scenario"):\s*"([^"]*)"', content)
        char_greeting = extract_match(r'("char_greeting"|"first_mes"):\s*"([^"]*)"', content)
        example_dialogue = extract_match(r'("example_dialogue"|"mes_example"):\s*"([^"]*)"', content)

        # Populate and format greeting with dynamic placeholders
        char_greeting = char_greeting.replace("{{user}}", CONFIG['CHAR']['user_name'])
        char_greeting = char_greeting.replace("{{char}}", char_name)
        char_greeting = char_greeting.replace("{{time}}", datetime.now().strftime("%Y-%m-%d %H:%M"))

        #print("Character Variables:")
        #print(f"Loading the character {char_name} ... DONE!!!")
        
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] LOAD: Injecting {char_name} character file...")
        #print(f"char_persona: {char_persona}")
        #print(f"personality: {personality}")
        #print(f"world_scenario: {world_scenario}")
        #print(f"char_greeting: {char_greeting}")
        #print(f"example_dialogue: {example_dialogue}")

    except FileNotFoundError:
        print(f"Error: Character file '{charactercard}' not found.")
    except Exception as e:
        print(f"Error: An unexpected issue occurred while reading the character file. Details: {e}")

def token_count(text):
    """
    Calculate the number of tokens in a given text.

    Parameters:
    - text (str): Input text.

    Returns:
    - dict: Dictionary with token count.
    """
    # Check the LLM backend and set the URL accordingly
    if CONFIG['LLM']['backend'] == "openai":
        # OpenAI doesn’t have a direct token count endpoint; you must estimate using tiktoken or similar tools.
        # This implementation assumes you calculate the token count locally.
        from tiktoken import encoding_for_model
        enc = encoding_for_model(CONFIG['LLM']['openai_model'])
        length = {"length": len(enc.encode(text))}
        return length
    elif CONFIG['LLM']['backend'] == "ooba":
        url = f"{CONFIG['LLM']['base_url']}/v1/internal/token-count"
    elif CONFIG['LLM']['backend'] == "tabby":
        url = f"{CONFIG['LLM']['base_url']}/v1/token/encode"

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {CONFIG['LLM']['api_key']}"
    }
    data = {
        "text": text
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        return response.json()
    else:
        print("Error:", response.status_code, response.text)
        return None

# === Initialization ===
load_character_attributes() # HOW IS THIS USED IN APP and MODULE MAIN??
init_dynamic_memory()

# Load memories from a JSON file
initial_memory_path = os.path.abspath("memory/initial_memory.json")
load_initial_memory(initial_memory_path)