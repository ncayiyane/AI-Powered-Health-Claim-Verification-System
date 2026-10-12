# AI-Powered Health Claim Verification System

An evidence-grounded AI application that verifies health-related claims by retrieving relevant information from a trusted knowledge base and using a local Large Language Model (LLM) to classify the claim.

The system combines **Retrieval-Augmented Generation (RAG)** with **Llama 3.1**, allowing the model to make verification decisions based on retrieved evidence rather than relying solely on its pretrained knowledge.

> **Important:** This project is an informational/technical demonstration and is not a substitute for professional medical advice, diagnosis, or treatment.

---

## Overview

Health information on the internet can contain misleading, exaggerated, or unsupported claims.

This project explores how AI and RAG can be used to provide an evidence-based verification workflow.

A user submits a health claim such as:

> "Drinking lemon water cures diabetes."

The system:

1. Receives the claim through the React frontend.
2. Sends the claim to the FastAPI backend.
3. Converts the claim into an embedding.
4. Searches the ChromaDB vector store for relevant evidence.
5. Retrieves the most relevant documents.
6. Sends the claim and retrieved evidence to Llama 3.1 through Ollama.
7. Classifies the claim.
8. Returns a structured result containing:

   * Verdict
   * Confidence score
   * Explanation
   * Supporting evidence
9. Displays the result in the frontend.
10. Stores the most recent verification results in the browser history.

---

## Key Features

* Evidence-grounded health claim verification
* Retrieval-Augmented Generation (RAG)
* Semantic similarity search
* ChromaDB vector database
* Sentence Transformer embeddings
* Configurable LLM providers: local Ollama or hosted Groq
* FastAPI REST API
* React frontend
* Structured JSON verification responses
* Confidence scoring
* Evidence/source display
* Recent verification history
* Input validation
* API error handling
* Environment-based configuration
* Protected `.env` secrets
* Automated verification test suite

---

## Verification Categories

The system supports four verdict categories:

| Verdict          | Meaning                                                                         |
| ---------------- | ------------------------------------------------------------------------------- |
| `TRUE`           | The retrieved evidence supports the claim.                                      |
| `FALSE`          | The retrieved evidence contradicts the claim.                                   |
| `PARTIALLY_TRUE` | The claim contains both supported and unsupported or contradictory components.  |
| `UNVERIFIED`     | The available evidence does not provide enough information to verify the claim. |

---

## System Architecture

```text
                    ┌─────────────────────────┐
                    │      React Frontend     │
                    │                         │
                    │  Claim Input / Results  │
                    │  Evidence / History     │
                    └────────────┬────────────┘
                                 │
                                 │ HTTP POST
                                 ▼
                    ┌─────────────────────────┐
                    │       FastAPI API       │
                    │                         │
                    │  Claim Verification     │
                    │       Endpoint          │
                    └────────────┬────────────┘
                                 │
                                 ▼
                    ┌─────────────────────────┐
                    │      RAG Pipeline       │
                    │                         │
                    │  Embeddings + Retrieval │
                    └────────────┬────────────┘
                                 │
                                 ▼
                    ┌─────────────────────────┐
                    │        ChromaDB         │
                    │                         │
                    │   Vector Knowledge Base │
                    └────────────┬────────────┘
                                 │
                         Retrieved Evidence
                                 │
                                 ▼
                    ┌─────────────────────────┐
                    │      Ollama + Llama     │
                    │          3.1             │
                    │                         │
                    │   Evidence-based LLM    │
                    │       Verification      │
                    └────────────┬────────────┘
                                 │
                                 ▼
                    ┌─────────────────────────┐
                    │   Structured Response   │
                    │                         │
                    │ Verdict                 │
                    │ Confidence              │
                    │ Explanation             │
                    │ Evidence                │
                    └─────────────────────────┘
```

---

## Technology Stack

### Frontend

* React
* Vite
* JavaScript
* CSS

### Backend

* Python
* FastAPI
* Pydantic
* Uvicorn

### AI / Machine Learning

* Llama 3.1 8B (Ollama or Groq)
* Ollama and Groq
* Sentence Transformers
* Hugging Face

### Retrieval

* ChromaDB
* LangChain Chroma
* LangChain Hugging Face embeddings
* Semantic similarity search

### Development

* Git
* GitHub
* Python virtual environment
* npm

---

## RAG Pipeline

The project uses Retrieval-Augmented Generation to provide the LLM with relevant evidence before asking it to verify a claim.

### 1. Document Loading

Health reference documents are loaded into the backend.

### 2. Document Chunking

Large documents are divided into smaller sections so that relevant passages can be retrieved more effectively.

### 3. Embedding Generation

The document chunks are converted into numerical vector representations using a Sentence Transformer embedding model.

### 4. Vector Storage

The embeddings are stored in ChromaDB.

### 5. Query Embedding

When a user submits a claim, the claim is converted into an embedding using the same embedding model.

### 6. Similarity Search

ChromaDB compares the claim embedding with stored document embeddings and retrieves the most relevant evidence.

### 7. LLM Verification

The retrieved evidence and the original claim are passed to Llama 3.1 through Ollama.

The model is instructed to return a structured verification result.

### 8. Response Validation

The backend validates:

* Verdict
* Confidence score
* Explanation
* Evidence references

Invalid or malformed LLM responses are handled safely rather than being returned directly to the user.

---

## Example Verification

### Claim

```text
Regular physical activity provides health benefits.
```

### Result

```text
Verdict: TRUE
Confidence: 0.90
```

The system retrieved evidence from the World Health Organization supporting the health benefits of regular physical activity.

---

### Claim

```text
Exercise improves cardiovascular fitness and cures every disease.
```

### Result

```text
Verdict: PARTIALLY_TRUE
Confidence: 0.80
```

The retrieved evidence supports the cardiovascular-fitness component but does not support the claim that exercise cures every disease.

---

### Claim

```text
Drinking lemon water cures diabetes.
```

### Result

```text
Verdict: UNVERIFIED
Confidence: 0.20
```

The retrieved evidence discusses diabetes management and hydration but does not directly establish that drinking lemon water cures diabetes.

---

## API

### Health Check

```http
GET /
```

Returns the API status.

### Health Endpoint

```http
GET /health
```

Returns the backend health status.

### Verify Claim

```http
POST /api/v1/claims/verify
```

Example request:

```json
{
  "claim": "Regular physical activity provides health benefits."
}
```

Example response:

```json
{
  "claim": "Regular physical activity provides health benefits.",
  "verdict": "TRUE",
  "confidence": 0.9,
  "explanation": "The retrieved evidence supports the claim.",
  "evidence": []
}
```

The evidence array contains the retrieved source information used during verification.

---

## Project Structure

```text
Health/
│
├── backend/
│   │
│   ├── app/
│   │   ├── api/
│   │   │   └── routes.py
│   │   │
│   │   ├── llm/
│   │   │   ├── client.py
│   │   │   ├── prompts.py
│   │   │   ├── verifier.py
│   │   │   └── test_verifier.py
│   │   │
│   │   ├── models/
│   │   │   └── schemas.py
│   │   │
│   │   └── rag/
│   │       ├── chunker.py
│   │       ├── document_loader.py
│   │       ├── embeddings.py
│   │       ├── ingestion.py
│   │       ├── retriever.py
│   │       └── vector_store.py
│   │
│   ├── data/
│   ├── requirements.txt
│   ├── .env
│   └── .gitignore
│
├── frontend/
│   │
│   ├── src/
│   │   ├── App.jsx
│   │   ├── App.css
│   │   └── main.jsx
│   │
│   ├── package.json
│   └── .gitignore
│
└── README.md
```

---

## Local Setup

### Prerequisites

Install:

* Python 3.14+
* Node.js
* npm
* Git
* Ollama

The project uses a local Llama 3.1 model through Ollama.

---

## Backend Setup

Navigate to the backend:

```bash
cd backend
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate it on Windows:

```powershell
.\venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Environment Variables

Copy the template to create:

```text
backend/.env
```

Choose a provider with `LLM_PROVIDER`.

For local Ollama:

```env
LLM_PROVIDER=ollama
OLLAMA_URL=http://localhost:11434/api/generate
OLLAMA_MODEL=llama3.1:8b
OLLAMA_CONNECT_TIMEOUT=10
OLLAMA_READ_TIMEOUT=300
```

For Groq:

```env
LLM_PROVIDER=groq
GROQ_API_KEY=your_groq_api_key
GROQ_URL=https://api.groq.com/openai/v1/chat/completions
GROQ_MODEL=llama-3.1-8b-instant
GROQ_CONNECT_TIMEOUT=10
GROQ_READ_TIMEOUT=120
```

Never commit `.env` to GitHub.

---

## Start Ollama

Make sure Ollama is installed and running.

Check the installed model:

```bash
ollama list
```

If necessary:

```bash
ollama pull llama3.1:8b
```

The application communicates with Ollama through:

```text
http://localhost:11434/api/generate
```

---

## Start the Backend

From the `backend` directory:

```bash
uvicorn app.main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

FastAPI documentation is available at:

```text
http://127.0.0.1:8000/docs
```

---

## Start the Frontend

Open another terminal:

```bash
cd frontend
```

Install dependencies:

```bash
npm install
```

Start the development server:

```bash
npm run dev
```

The frontend will normally be available at:

```text
http://localhost:5173
```

---

## Testing

### Backend Verification Tests

Run:

```bash
python -m app.llm.test_verifier
```

The current test suite verifies:

1. A supported health claim.
2. A clearly false universal health claim.
3. A partially true claim containing both supported and unsupported components.
4. A claim for which the available evidence is insufficient.

All four scenarios currently pass.

### Frontend Lint

From `frontend`:

```bash
npm run lint
```

### Production Build

```bash
npm run build
```

---

## Security

Environment variables are stored locally in `.env` files and excluded from Git using `.gitignore`.

Sensitive credentials should never be committed to the repository.

If an API credential is accidentally exposed, it should be revoked and replaced immediately.

---

## Limitations

This project is a research and engineering demonstration.

The system is limited by:

* The quality and coverage of its knowledge base.
* The quality of retrieved evidence.
* Embedding similarity.
* LLM reasoning accuracy.
* The limitations of the local Llama model.
* The absence of unrestricted real-time medical literature retrieval.
* The current local Ollama dependency.

An `UNVERIFIED` result does not necessarily mean that a claim is false. It means that the available retrieved evidence was insufficient to verify the claim.

---

## Future Improvements

Potential improvements include:

* Expand the trusted medical knowledge base.
* Add more authoritative sources.
* Introduce source freshness tracking.
* Add document metadata and publication dates.
* Improve retrieval ranking.
* Add hybrid keyword + semantic retrieval.
* Add reranking models.
* Add automated evaluation datasets.
* Add retrieval precision/recall metrics.
* Add authentication and rate limiting.
* Add persistent verification history.
* Add asynchronous processing for long-running LLM requests.
* Add production monitoring and logging.
* Deploy the backend with a hosted inference solution.
* Add a human-review workflow for uncertain claims.
* Improve multilingual health claim verification.

---

## Engineering Focus

This project demonstrates practical experience with:

* Generative AI
* Large Language Models
* Retrieval-Augmented Generation
* Vector databases
* Semantic search
* Embeddings
* Prompt engineering
* Structured LLM outputs
* AI response validation
* REST API development
* FastAPI
* React
* Python
* Git/GitHub
* Local AI inference
* Full-stack application development

---

## Disclaimer

HealthVerify AI is an educational and engineering project.

The results generated by this system are informational and should not be used as a substitute for advice, diagnosis, treatment, or recommendations from a qualified healthcare professional.

---

## Author

**Aphiwe Ncayiyane**

Software Developer / AI Engineer

GitHub: `https://github.com/ncayiyane`

LinkedIn: `https://www.linkedin.com/in/aphiwe-ncayiyane-4149b31a8`
