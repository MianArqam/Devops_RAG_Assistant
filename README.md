# DevOps RAG Assistant

DevOps RAG Assistant is a Retrieval-Augmented Generation application designed to behave like a junior DevOps engineer. Instead of manually searching AWS, Docker, Kubernetes, or troubleshooting documentation, a user can paste an error message or log output and receive a context-aware explanation, likely cause, suggested fix, and source citations.

The system combines a React frontend, a FastAPI backend, a local knowledge base, embedding-based retrieval, and an LLM provider such as Gemini or OpenAI.

## Purpose

Modern DevOps troubleshooting often requires searching through documentation, logs, cloud provider references, and previous incidents. This project automates the first stage of that workflow.

Example input:

```text
Error: AccessDenied: User is not authorized to perform s3:PutObject
```

Example output:

```text
Possible cause:
The IAM user or role is missing s3:PutObject permission for the target S3 bucket object ARN.

Suggested fix:
Attach a policy that allows s3:PutObject on arn:aws:s3:::my-bucket/*

Source:
aws/iam.txt
```

## Key Features

- Chat with local DevOps documentation
- Analyze raw infrastructure and application logs
- Upload PDF, TXT, and Markdown documents
- Retrieve relevant documentation chunks from a vector index
- Generate final answers using Gemini or OpenAI
- Show source citations for transparency
- Maintain frontend session history
- Run locally with simple PowerShell scripts
- Work without a paid LLM by returning retrieved documentation snippets

## Architecture

```text
User
  |
  v
React Frontend
  |
  v
FastAPI Backend
  |
  v
Document Loader
  |
  v
Text Splitter
  |
  v
Embedding Model
  |
  v
Vector Store / FAISS-compatible Search
  |
  v
Relevant Documentation Chunks
  |
  v
LLM Provider
  |
  v
Answer + Source Citations
```

## How the RAG Pipeline Works

RAG means Retrieval-Augmented Generation. The application does not send only the user question to the LLM. It first retrieves relevant documentation from the local knowledge base and then sends both the user query and retrieved context to the model.

### 1. Document Ingestion

Documents are stored in:

```text
knowledge_base/
```

The backend reads supported files:

- `.txt`
- `.md`
- `.pdf`

Uploaded files are saved under:

```text
knowledge_base/uploads/
```

### 2. Text Splitting

Large documents are split into smaller chunks so the retriever can search specific sections instead of entire files.

Current chunking strategy:

```python
chunks = split_text(document, chunk_size=500, overlap=80)
```

### 3. Embedding Generation

Each text chunk is converted into a vector embedding. Embeddings are numerical representations of text meaning.

Default behavior:

- Uses a lightweight built-in hash embedding fallback so the project runs easily on limited machines.

Optional ML stack:

- `sentence-transformers/all-MiniLM-L6-v2`
- FAISS

### 4. Vector Search

When the user asks a question, the backend embeds the query and compares it with stored document vectors.

The top matching chunks are returned as context.

Example:

```text
Query: AccessDenied s3:PutObject
Top source: knowledge_base/aws/iam.txt
```

### 5. LLM Answer Generation

The retrieved context and user question are sent to the selected LLM provider.

Supported providers:

- Gemini
- OpenAI
- Local fallback response when no LLM is configured

The LLM produces:

- Possible cause
- Suggested fix
- Relevant commands or policy examples
- Source citations

## Technology Stack

### Frontend

- React
- Vite
- Tailwind CSS
- Lucide React icons

Frontend pages:

- Chat
- Error Analysis
- Upload Documents
- History

### Backend

- Python
- FastAPI
- Uvicorn
- Pydantic Settings
- PyPDF
- OpenAI SDK
- Gemini REST API through `httpx`

### Retrieval and Embeddings

- Built-in lightweight embedding fallback
- Optional `sentence-transformers/all-MiniLM-L6-v2`
- Optional FAISS vector index

### Knowledge Base

Current starter knowledge base includes:

```text
knowledge_base/
  aws/
    iam.txt
    s3.txt
    ec2.txt
    lambda.txt
    vpc.txt
    cloudwatch.txt
  docker/
    build_errors.txt
    networking.txt
  kubernetes/
    pods.txt
    deployments.txt
  logs/
    nginx_errors.txt
    lambda_errors.txt
```

## Project Structure

```text
devops-rag-assistant/
  backend/
    app/
      api/
        routes.py
      core/
        config.py
      models/
        schemas.py
      rag/
        document_loader.py
        embeddings.py
        llm.py
        text_splitter.py
        vector_store.py
      main.py
    storage/
    requirements.txt
    requirements-ml.txt
    .env.example

  frontend/
    src/
      components/
      lib/
      pages/
      App.jsx
      main.jsx
      styles.css
    package.json

  knowledge_base/
    aws/
    docker/
    kubernetes/
    logs/

  scripts/
    run_backend.ps1
    run_frontend.ps1
```

## API Endpoints

### Health Check

```http
GET /health
```

Example response:

```json
{
  "status": "ok",
  "indexed_chunks": 12,
  "llm_provider": "gemini"
}
```

### Upload Documentation

```http
POST /upload
```

Uploads and indexes a PDF, TXT, or Markdown file.

Example response:

```json
{
  "filename": "iam-guide.pdf",
  "chunks_added": 18,
  "message": "Document uploaded and indexed."
}
```

### Chat

```http
POST /chat
```

Request:

```json
{
  "query": "Why am I getting AccessDenied for s3:PutObject?"
}
```

Response:

```json
{
  "answer": "Possible cause...",
  "sources": [
    {
      "source": "aws/iam.txt",
      "score": 0.397,
      "text": "IAM access denied errors usually mean..."
    }
  ]
}
```

### Analyze Logs

```http
POST /analyze-log
```

Request:

```json
{
  "log": "CrashLoopBackOff: back-off restarting failed container"
}
```

Response:

```json
{
  "answer": "Possible cause...",
  "sources": []
}
```

## Environment Configuration

Create:

```text
backend/.env
```

You can copy from:

```text
backend/.env.example
```

### Gemini Configuration

Recommended for the current free-plan setup:

```env
LLM_PROVIDER=gemini
GEMINI_API_KEY=your_gemini_api_key_here
GEMINI_MODEL=gemini-3.5-flash
```

Gemini free-plan limits are low, so rate-limit or quota errors may happen after repeated requests.

### OpenAI Configuration

```env
LLM_PROVIDER=openai
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-4o-mini
```

### No LLM Mode

```env
LLM_PROVIDER=none
```

In this mode, the app still retrieves relevant source documents and returns them as context.

## Running the Project

Open two PowerShell windows.

### 1. Start Backend

```powershell
cd C:\Users\muham\OneDrive\Desktop\devops-rag-assistant
.\scripts\run_backend.ps1
```

Backend URL:

```text
http://127.0.0.1:8000
```

API docs:

```text
http://127.0.0.1:8000/docs
```

### 2. Start Frontend

```powershell
cd C:\Users\muham\OneDrive\Desktop\devops-rag-assistant
.\scripts\run_frontend.ps1
```

Frontend URL:

```text
http://127.0.0.1:5173
```

## Optional Full ML Setup

The default setup is lightweight so it can run on a normal Windows machine without downloading large ML packages.

For a stronger local retrieval setup, install the optional ML requirements:

```powershell
cd C:\Users\muham\OneDrive\Desktop\devops-rag-assistant\backend
.\.venv\Scripts\pip install -r requirements-ml.txt
```

This enables:

- `sentence-transformers/all-MiniLM-L6-v2`
- FAISS CPU index
- Higher-quality semantic retrieval

## Security Notes

- Do not commit `backend/.env`.
- API keys should stay only in `.env`.
- If an API key is exposed in logs, screenshots, terminal output, or Git history, rotate it immediately.
- The `.env.example` file should contain placeholders only.
- Uploaded documents are stored locally under `knowledge_base/uploads/`.

## Current Limitations

- The default embedding fallback is lightweight and less accurate than a real transformer embedding model.
- The history page stores only browser-session history, not database-backed history.
- There is no user authentication.
- Uploaded documents are indexed locally only.
- Gemini free-plan usage is limited by Google rate limits and daily quotas.
- The app is built for local development, not production deployment.

## Future Improvements

- Add persistent chat history with SQLite or PostgreSQL
- Add user accounts and authentication
- Add ChromaDB or Pinecone as a managed vector database
- Add Docker Compose for easier deployment
- Add streaming LLM responses
- Add better document chunking with metadata
- Add source highlighting in the UI
- Add evaluation tests for retrieval quality
- Add support for Ollama local models
- Add CI/CD pipeline with GitHub Actions
- Add cloud deployment on AWS, Azure, or Render

## CV Description

Built a DevOps-focused RAG assistant using FastAPI, React, Tailwind, local document ingestion, embedding-based retrieval, and Gemini/OpenAI integration. The system retrieves relevant AWS, Docker, Kubernetes, and log documentation from a local knowledge base and generates troubleshooting guidance with source citations.

## Example Troubleshooting Flow

Input:

```text
Error: AccessDenied: User is not authorized to perform s3:PutObject
```

Retrieval:

```text
aws/iam.txt
aws/s3.txt
```

Generated answer:

```text
Possible cause:
The IAM role or user does not have s3:PutObject permission for the object ARN.

Suggested fix:
Add an IAM policy allowing s3:PutObject on arn:aws:s3:::my-bucket/*

Source:
aws/iam.txt
```
#   D e v o p s _ R A G _ A s s i s t a n t  
 