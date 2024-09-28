from groq import Groq
import os

os.environ["GROQ_API_KEY"] = "your_groq_api_key"

groq_api_key = os.getenv('GROQ_API_KEY')
client = Groq(api_key = groq_api_key)

vector_search_model = "mixtral-8x7b-32768"
def run_vector_search(query,relevant_docs):
    """Use the vector search model to answer user query"""
    relevant_excerpts = '\n\n---------------------------------\n\n'.join([doc.page_content for doc in relevant_docs])
    messages = [
        {
            "role": "system",
            "content": "You are a smart assistant. Use the user queries and provide the results from the documents given.",
        },
        {
            "role": "user",
            "content": f"User query: {query}. Relevant Excerpts: {relevant_excerpts}",
        }
    ]
    response = client.chat.completions.create(
        model= vector_search_model,
        messages=messages,
        max_tokens=4096
    )
    response_message = response.choices[0].message

    return response_message.content