# Smart_RAG

## Overview
*Smart_RAG* is a Retrieval Augmented Generation (RAG) application that optimizes vector search by performing query classification. This approach helps determine when vector search is necessary, ensuring efficient and accurate responses to user queries. It also use tools to route the queries that require special modules.

## Features
- **Query Classification**: Determines the necessity of vector search.
- **PDF Reading**: Extracts text from uploaded PDF files.
- **Smart Actions** -
    - **Vector Search**: Performs similarity search on documents.
    - **Clarify Doubts**: Handles user queries by clarifying doubts based on document content with knowledge of chat history.
    - **General Query Handling**: Processes general user queries.
    - **Calculator**: Evaluates mathematical expression.
    - **Dictionary**: Get the meaning of words.
- **Text-to-Speech Integration**: Converts responses to audio using Sarvam.ai Text-to-Speech API.
- **Gradio Interface**: Provides a user-friendly interface for interaction.

## Installation
1. Clone the repository:
    ```bash
    git clone https://github.com/bindusri0702/sarvamai_RAG.git
    cd sarvamai_RAG
    ```

2. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3. Run the application:
    ```bash
    uvicorn rag_app:app --reload
    ```

## API Endpoints
- **`GET /`**: Welcome message.
- **`GET /read_pdf`**: Reads and extracts text from an uploaded PDF file.
- **`GET /route_query`**: Routes the query to the appropriate endpoint based on classification.
- **`POST /vector_search`**: Performs vector search on the documents.
- **`POST /clarify_doubts`**: Clarifies doubts based on document content.
- **`POST /general_query`**: Handles general user queries.
    - *`Calculate`* and *`Dictionary`* are included inside general query enpoints.

## Gradio Interface
The application includes a Gradio interface for easy interaction:
- **Query Input**: Textbox for user queries.
- **File Upload**: Upload field for PDF files.
- **Response Output**: Textbox for displaying responses.
- **Audio Output**: Audio player for playing the generated speech.

## Usage
1. Access the Gradio interface at `/gradio`.
2. Enter your query and upload a PDF file.
3. Receive the response in text and audio formats.

