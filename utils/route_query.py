from groq import Groq
import os

os.environ["GROQ_API_KEY"] = "your_groq_api_key" # set this to your own GROQ API key

groq_api_key = os.getenv('GROQ_API_KEY')
client = Groq(api_key = groq_api_key)

ROUTING_MODEL = "llama3-70b-8192"
def route_query(query, summary):
    response = client.chat.completions.create(
        model=ROUTING_MODEL,
        messages=[
            {"role": "system", "content": """
            You are an intelligent assistant. Your task is to determine whether a user query is related to the summary of the documents provided.

            Here are some examples:
            - User Query: "What is training loss?", Summary: "The document discusses machine learning techniques." -> Response: "related"
            - User Query: "What is the weather like today?", Summary: "The document discusses machine learning techniques." -> Response: "No relation"
            - User Query: "hi/hello/thank you", Summary: "The document discusses machine learning techniques." -> Response: "No relation"
            
            If the user query is related to the documents, respond with "related".
            If the user query is not related to the documents, respond with "No relation".
            Do not provide any additional information or return summary.
            """},
            {"role": "user", "content": f"User Query: {query}, Summary: {summary}"}
        ],
        max_tokens=20  
    )

    routing_decision = response.choices[0].message.content.strip()

    if 'doubt' in query.lower():
        return "Doubts"
    elif 'relation' in routing_decision.lower():
        return "Not Required"
    else:
        return "Vector Search Required"