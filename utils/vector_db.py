from langchain_huggingface import HuggingFaceEmbeddings
from pinecone.grpc import PineconeGRPC as Pinecone
from langchain_pinecone import PineconeVectorStore
from utils.tokenize_doc import tokenize_doc
from pinecone import ServerlessSpec

pinecone_index_name = "ncert-rag" 

pc = Pinecone(api_key = "your_pinecone_api_key")

indices_list = pc.list_indexes()
chk_indices = [indices_list[i]['name'] for i in range(len(indices_list))]

if pinecone_index_name not in chk_indices:
    pc.create_index(
        name=pinecone_index_name,
        dimension=384,
        metric="cosine",
        spec=ServerlessSpec(
            cloud='aws', 
            region='us-east-1'
        ) 
    ) 

def clear_vectorstore(index_name):
    index = pc.Index(index_name)
    index.delete(delete_all=True)

def vector_db(text):
    clear_vectorstore(pinecone_index_name)
    documents = tokenize_doc(text)
    embedding_function = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    docsearch = PineconeVectorStore.from_documents(documents, embedding_function, index_name=pinecone_index_name)
    return docsearch

