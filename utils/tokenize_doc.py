import os

from langchain.text_splitter import TokenTextSplitter
from langchain.docstore.document import Document

from transformers import AutoTokenizer

os.environ['PINECONE_API_KEY'] = "your_pinecone_api_key" 
os.environ["HUGGINGFACE_TOKEN"] = "your_huggingface_token" 
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'


pinecone_api_key = os.getenv('PINECONE_API_KEY')
model_id = "mistralai/Mixtral-8x7B-v0.1"

tokenizer = AutoTokenizer.from_pretrained(model_id, token="your_huggingface_token")

def token_len(text):
    tokens = tokenizer.encode(
        text
    )
    return len(tokens)

text_splitter = TokenTextSplitter(
    chunk_size=450, 
    chunk_overlap=20 
)

def tokenize_doc(text):
    documents = []
    chunks = text_splitter.split_text(text)
    total_chunks = len(chunks)
    for chunk_num in range(1,total_chunks+1):
        chunk = chunks[chunk_num-1]
        documents.append(Document(page_content= chunk, metadata={"source": "local"})) 
    return documents