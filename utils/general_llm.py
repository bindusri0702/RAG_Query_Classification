from groq import Groq
import json
import os
import nltk
from nltk.corpus import wordnet

nltk.download('wordnet')
nltk.download('omw-1.4')

os.environ["GROQ_API_KEY"] = "your_groq_api_key"
groq_api_key = os.getenv('GROQ_API_KEY')
client = Groq(api_key = groq_api_key)

ROUTING_MODEL = "llama3-70b-8192"
TOOL_USE_MODEL = "llama3-groq-70b-8192-tool-use-preview"
GENERAL_MODEL = "llama3-70b-8192"

def calculate(expression):
    """Tool to evaluate a mathematical expression"""
    try:
        result = eval(expression)
        return json.dumps({"result": result})
    except:
        return json.dumps({"error": "Invalid expression"})
    
def dictionary(word):
    """Tool to get the meaning of words"""
    synsets = wordnet.synsets(word)

    if not synsets:
        return f"Sorry, no meanings found for '{word}'."

    meanings = []
    for idx, synset in enumerate(synsets, 1):
        meanings.append(f"{idx}. {synset.definition()}")

    return "\n".join(meanings)

def route_query2(query):
    """Routing logic to let LLM decide if tools are needed"""
    routing_prompt = f"""
    Analyze the following user query and decide if a tool is required to provide an accurate answer:
    - If a mathematical calculation is needed, respond with: 'TOOL: CALCULATE'.
    - If the user is asking for the meaning of a word, respond with: 'TOOL: DICTIONARY'.
    - If no tools are necessary to answer the query, respond with: 'NO TOOL'.

    User query: {query}

    Response:
    """

    
    response = client.chat.completions.create(
        model=ROUTING_MODEL,
        messages=[
            {"role": "system", "content": "You are a routing assistant. Determine if tools are needed based on the user query."},
            {"role": "user", "content": routing_prompt}
        ],
        max_tokens=20  
    )
    
    routing_decision = response.choices[0].message.content.strip()
    
    if "TOOL: CALCULATE" in routing_decision:
        return "with calculator tool"
    elif "TOOL: DICTIONARY" in routing_decision:
        return "with dictionary tool"
    else:
        return "with no tool"

def run_with_calculator(query):
    """Use the tool use model to perform the calculation"""
    messages = [
        {
            "role": "system",
            "content": "You are a calculator assistant. Use the calculate function to perform mathematical operations and provide the results.",
        },
        {
            "role": "user",
            "content": query,
        }
    ]
    tools = [
        {
            "type": "function",
            "function": {
                "name": "calculate",
                "description": "Evaluate a mathematical expression",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "expression": {
                            "type": "string",
                            "description": "The mathematical expression to evaluate",
                        }
                    },
                    "required": ["expression"],
                },
            },
        }
    ]
    response = client.chat.completions.create(
        model=TOOL_USE_MODEL,
        messages=messages,
        tools=tools,
        tool_choice="auto",
        max_tokens=4096
    )
    response_message = response.choices[0].message
    tool_calls = response_message.tool_calls
    if tool_calls:
        messages.append(response_message)
        for tool_call in tool_calls:
            function_args = json.loads(tool_call.function.arguments)
            function_response = calculate(function_args.get("expression"))
            messages.append(
                {
                    "tool_call_id": tool_call.id,
                    "role": "tool",
                    "name": "calculate",
                    "content": function_response,
                }
            )
        second_response = client.chat.completions.create(
            model=TOOL_USE_MODEL,
            messages=messages
        )
        return second_response.choices[0].message.content
    return response_message.content

def run_with_dictionary(query):
    """Use the tool use model to search the dictionary"""
    messages = [
        {
            "role": "system",
            "content": "You are a dictionary seraching assistant. Use the dictionary function to search for meaning and provide the results.",
        },
        {
            "role": "user",
            "content": query,
        }
    ]
    tools = [
        {
            "type": "function",
            "function": {
                "name": "dictionary",
                "description": "Serach for meaning",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "meaning": {
                            "type": "string",
                            "description": "The word to search in dictionary",
                        }
                    },
                    "required": ["meaning"],
                },
            },
        }
    ]
    response = client.chat.completions.create(
        model=TOOL_USE_MODEL,
        messages=messages,
        tools=tools,
        tool_choice="auto",
        max_tokens=4096
    )
    response_message = response.choices[0].message
    tool_calls = response_message.tool_calls
    if tool_calls:
        messages.append(response_message)
        for tool_call in tool_calls:
            function_args = json.loads(tool_call.function.arguments)
            function_response = dictionary(function_args.get("meaning"))
            messages.append(
                {
                    "tool_call_id": tool_call.id,
                    "role": "tool",
                    "name": "dictionary",
                    "content": function_response,
                }
            )
        second_response = client.chat.completions.create(
            model=TOOL_USE_MODEL,
            messages=messages
        )
        return second_response.choices[0].message.content
    return response_message.content

def run_general2(query):
    """Use the general model to answer the query since no tool is needed"""
    response = client.chat.completions.create(
        model=GENERAL_MODEL,
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": query}
        ]
    )
    return response.choices[0].message.content

def process_query(query):
    """Process the query and route it to the appropriate model"""
    route = route_query2(query)
    if "calculate" in route.lower():
        response = run_with_calculator(query)
    elif "dictionary" in route.lower():
        response = run_with_dictionary(query)       
    else:
        response = run_general2(query)
    
    return f"{route} - {response}"