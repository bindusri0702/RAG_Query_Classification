from fastapi import FastAPI, HTTPException, UploadFile
from pydantic import BaseModel
import gradio as gr
import asyncio
import io
import fitz
import os
import requests
import base64

from utils.vector_search import run_vector_search
from utils.doubts import clarify_doubts
from utils.vector_db import vector_db
from utils.route_query import route_query
from utils.general_llm import process_query
from utils.summarize_doc import summarize_doc

app = FastAPI(
    title="RAG_APP",
    description="""
        Retrieval Augmented Generation (RAG) application that optimizes vector search 
        by performing query classification. This approach helps determine when vector search is necessary, 
        ensuring efficient and accurate responses to user queries. """
)

class QueryModel(BaseModel):
    query: str
    documents: str

@app.get("/")
def read_root():
    return {"message": "Welcome to the RAG_APP"}

@app.get("/read_pdf")
async def read_pdf(file):
    if file is None or os.path.getsize(file.name) == 0:
        text = "Uploaded file is empty or not accessible."
        flag = 0
    try:
        with fitz.open(file.name) as pdf:
            text = ""
            for page in pdf:
                text += page.get_text()
        flag = 1
    except Exception as e:
        text =  f"Error reading PDF: {str(e)}"
        flag = 0
    return text, flag

@app.get("/route_query")
async def route_query_endpoint(input: QueryModel):
    vector_db_summary = summarize_doc(input.documents)
    route = route_query(input.query,vector_db_summary)
    if "Vector Search" in route:
        return await vector_search_endpoint(input)
    elif "Doubts" in route:
        return await clarify_doubts_endpoint(input)
    else:
        return await general_query_endpoint(input)

@app.post("/vector_search")
async def vector_search_endpoint(input: QueryModel):
    docsearch = vector_db(input.documents)
    if not input.query:
        raise HTTPException(status_code=400, detail="Query cannot be empty.")
    
    relevant_docs = docsearch.similarity_search(input.query)
    response = run_vector_search(input.query, relevant_docs)
    
    return "Vector Search - " + response
    

chat_history = None

@app.post("/clarify_doubts")
async def clarify_doubts_endpoint(input: QueryModel):
    docsearch = vector_db(input.documents)
    global chat_history  
    
    if not input.query:
        raise HTTPException(status_code=400, detail="Query cannot be empty.")
    
    relevant_docs = docsearch.similarity_search(input.query)
    response, updated_chat_history = clarify_doubts(input.query, relevant_docs, chat_history)
    chat_history = updated_chat_history  
    
    return "Doubts - " + response

@app.post("/general_query")
async def general_query_endpoint(input: QueryModel):
    if not input.query:
        raise HTTPException(status_code=400, detail="Query cannot be empty.")
    
    response = process_query(input.query)
    
    return "General Query " + response

url = "https://api.sarvam.ai/text-to-speech"
headers = {
    "api-subscription-key": "7abba42f-b286-4dd4-98f3-9ec078a70f0d",
    "Content-Type": "application/json"
}

def gradio_get_generated_answer(query: str, file: UploadFile):
    text, flag = asyncio.run(read_pdf(file))
    if flag:
        input_data = QueryModel(query=query, documents=text)
        result = asyncio.run(route_query_endpoint(input_data))
    else:
        result = text

    payload = {
        "inputs": [result],
        "speaker": "meera",
        "target_language_code": "en-IN"
    }
    response = requests.post(url, json=payload, headers=headers)
    if response.status_code == 200:
        audio_data = base64.b64decode(response.json()['audios'][0])
        with open("output.wav", "wb") as audio_file:
            audio_file.write(audio_data)
        audio_otpt =  "output.wav"
    else:
        audio_otpt = None
    return result, audio_otpt

io = gr.Interface(
    fn=gradio_get_generated_answer,
    inputs=[
        gr.components.Textbox(label="Query"),
        gr.components.File(label="Upload File")
    ],
    outputs=[
        gr.components.Textbox(label="Response"),
        gr.Audio(type="filepath")
    ]
)

app = gr.mount_gradio_app(app, io, path="/gradio")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
