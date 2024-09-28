from groq import Groq
import os

os.environ["GROQ_API_KEY"] = "your_groq_api_key" # set this to your own GROQ API key

groq_api_key = os.getenv('GROQ_API_KEY')
client = Groq(api_key = groq_api_key)

doubts_model = "mixtral-8x7b-32768"

def clarify_doubts(doubt, relevant_docs, chat_history=None):
    """Use the doubts_model to clarify the user doubts"""
    if chat_history is None:
        chat_history = []

    relevant_excerpts = '\n\n---------------------------------\n\n'.join([doc.page_content for doc in relevant_docs])

    messages = chat_history + [
        {"role": "system", "content": "You are a teacher. Help the students in clarifying their doubts."},
        {"role": "user", "content": f"User doubt: {doubt}. Relevant Excerpts: {relevant_excerpts}"}
    ]

    response = client.chat.completions.create(
        model=doubts_model,
        messages=messages
    )

    assistant_response = response.choices[0].message.content

    chat_history.append({"role": "user", "content": f"User doubt: {doubt}. Relevant Excerpts: {relevant_excerpts}"})
    chat_history.append({"role": "assistant", "content": assistant_response})

    return assistant_response, chat_history