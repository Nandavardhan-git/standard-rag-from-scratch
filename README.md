
# Standard RAG From Scratch

A production-oriented Retrieval-Augmented Generation (RAG) project built from first principles to understand how each component works before combining them into a complete pipeline.

The project takes a raw PDF, processes and chunks its content, converts the chunks into embeddings, stores them in ChromaDB, retrieves relevant information for a user query, and uses Gemini to generate a grounded answer.

---

## Tech Stack

- **Python** — Core implementation
- **PyMuPDF** — PDF text extraction
- **LangChain** — Recursive text splitting
- **Sentence Transformers** — Embedding generation
- **BAAI/bge-small-en-v1.5** — Embedding model
- **NumPy** — Numerical operations
- **ChromaDB** — Persistent vector database
- **HNSW** — Approximate nearest-neighbor search
- **Google GenAI SDK** — Gemini integration
- **Gemini** — LLM generation
- **python-dotenv** — Environment variables
- **Git & GitHub** — Version control

---

## RAG Pipeline

Retrieval-Augmented Generation retrieves relevant information from an external knowledge source and provides it to an LLM before generating an answer.

```text
                    RAG SYSTEM
                        │
            ┌───────────┴───────────┐
            │                       │
            ▼                       ▼
      INGESTION PATH           QUERY PATH
            │                       │
            ▼                       ▼
        Load PDF                User Query
            │                       │
            ▼                       ▼
        Clean Text             Query Embedding
            │                       │
            ▼                       ▼
         Chunk Text              Retrieval
            │                       │
            ▼                       ▼
        Embeddings             Relevant Chunks
            │                       │
            ▼                       │
         ChromaDB                   │
            │                       │
            └───────────┬───────────┘
                        ▼
                 Prompt Builder
                        │
                        ▼
                     Gemini
                        │
                        ▼
                   Final Answer
````

---

# Modules

## Module 1 — PDF Processing

The first stage converts the source PDF into clean, machine-processable text.

### Pipeline

```text
PDF
 ↓
PyMuPDF
 ↓
Raw Text
 ↓
Text Cleaning
 ↓
Clean Text
```

### Implementation

* PDF loading with PyMuPDF
* Exception handling
* Text extraction
* Text cleaning

Cleaning removes unnecessary whitespace, line breaks, and extraction artifacts before the text reaches the chunking stage.

---

## Module 2 — Intelligent Text Chunking

Large documents are divided into smaller pieces so retrieval can return focused sections instead of an entire document.

```text
Clean Document
      │
      ▼
   Chunker
      │
      ├── Chunk 1
      ├── Chunk 2
      ├── Chunk 3
      ├── Chunk 4
      └── Chunk N
```

### Implementation

* Custom character-based chunker
* Chunk overlap
* Recursive chunking
* LangChain `RecursiveCharacterTextSplitter`

### Why Overlap?

```text
Without overlap:

Chunk 1: A B C D E
Chunk 2: F G H I J


With overlap:

Chunk 1: A B C D E
Chunk 2: D E F G H
Chunk 3: G H I J K
```

Overlap helps preserve context around chunk boundaries.

---

## Module 3 — Embeddings

Embeddings convert text into numerical vectors so semantic similarity can be measured.

```text
Text
 ↓
Embedding Model
 ↓
[0.21, -0.43, 0.17, 0.82, ...]
```

The project uses:

```text
BAAI/bge-small-en-v1.5
```

The model generates **384-dimensional embeddings**.

For the current document:

```text
39 chunks
    ↓
BGE Model
    ↓
39 × 384 Embedding Matrix
```

Result:

```text
Embedding Shape: (39, 384)
```

Document chunks and user queries are embedded using the same model so they exist in the same vector space.

---

## Module 4 — Vector Database & Retrieval

After embeddings are generated, they need to be stored and searched efficiently.

The project uses **ChromaDB** as the persistent vector database.

```text
┌─────────────────────────────────┐
│             ChromaDB            │
│                                 │
│  Document Chunks                │
│        +                        │
│  Embeddings                     │
│        +                        │
│  Metadata                       │
│        +                        │
│  HNSW Index                     │
└─────────────────────────────────┘
```

### Persistent Storage

The vector store is persisted locally so embeddings do not need to be regenerated every time the application starts.

```text
Python
   │
   ▼
Persistent ChromaDB
   │
   ▼
Disk
   │
   ▼
Available in future runs
```

### Semantic Retrieval

```text
User Question
     │
     ▼
Query Embedding
     │
     ▼
384-D Query Vector
     │
     ▼
ChromaDB
     │
     ▼
HNSW Search
     │
     ▼
Top-K Relevant Chunks
```

### HNSW

HNSW stands for:

**Hierarchical Navigable Small World**

It provides approximate nearest-neighbor search by navigating a graph of vectors instead of exhaustively comparing the query against every stored vector.

---

## Module 5 — Prompt Engineering & Gemini

The retrieved chunks are provided to Gemini as context.

```text
Retrieved Context
       +
User Question
       +
Instructions
       ↓
Prompt Builder
       ↓
Final Prompt
       ↓
Gemini
       ↓
Final Answer
```

Gemini was first tested independently before integrating it with the retrieval pipeline.

The API key is stored in `.env` and loaded using `python-dotenv`.

```text
.env
 ↓
Environment Variable
 ↓
Google GenAI Client
 ↓
Gemini
```

The API key is never hardcoded into the source code.

---

# Complete Architecture

```text
                         ┌─────────────────┐
                         │    SOURCE PDF   │
                         └────────┬────────┘
                                  │
                                  ▼
                         ┌─────────────────┐
                         │  PDF PROCESSING │
                         │                 │
                         │ Extract + Clean │
                         └────────┬────────┘
                                  │
                                  ▼
                         ┌─────────────────┐
                         │     CHUNKING    │
                         │                 │
                         │ Recursive Split │
                         └────────┬────────┘
                                  │
                                  ▼
                         ┌─────────────────┐
                         │    EMBEDDINGS   │
                         │                 │
                         │ BGE-small-en-v1 │
                         └────────┬────────┘
                                  │
                                  ▼
                  ┌─────────────────────────────┐
                  │          CHROMADB           │
                  │                             │
                  │ Chunks + Embeddings + HNSW │
                  └──────────────┬──────────────┘
                                 │
                                 │
                            QUERY TIME
                                 │
                                 ▼
                       ┌──────────────────┐
                       │    USER QUERY    │
                       └────────┬─────────┘
                                │
                                ▼
                       ┌──────────────────┐
                       │ QUERY EMBEDDING  │
                       │    BGE Model     │
                       └────────┬─────────┘
                                │
                                ▼
                       ┌──────────────────┐
                       │ HNSW RETRIEVAL   │
                       │    ChromaDB      │
                       └────────┬─────────┘
                                │
                                ▼
                          Top-K Chunks
                                │
                                ▼
                       ┌──────────────────┐
                       │  PROMPT BUILDER  │
                       │ Context + Query  │
                       └────────┬─────────┘
                                │
                                ▼
                         ┌──────────────┐
                         │    GEMINI    │
                         │     LLM      │
                         └──────┬───────┘
                                │
                                ▼
                          FINAL ANSWER
```

---

# Ingestion vs Query

A key architectural decision was separating document ingestion from querying.

## Ingestion

Implemented in:

```text
src/ingest.py
```

```text
PDF
 ↓
Extract
 ↓
Clean
 ↓
Chunk
 ↓
Embed
 ↓
ChromaDB
```

This is performed when a document is added or modified.

## Query

Implemented in:

```text
src/query.py
```

```text
User Question
 ↓
Query Embedding
 ↓
ChromaDB
 ↓
HNSW Retrieval
 ↓
Top-K Chunks
 ↓
Prompt Builder
 ↓
Gemini
 ↓
Final Answer
```

The document is **not** reprocessed for every question.

This changes the inefficient design:

```text
Question
 ↓
Load PDF
 ↓
Clean
 ↓
Chunk
 ↓
Embed Everything
 ↓
Retrieve
 ↓
Gemini
```

into:

```text
          ONE-TIME INGESTION

PDF
 ↓
Processing
 ↓
Chunking
 ↓
Embeddings
 ↓
ChromaDB
      │
      ├── Query 1 → Retrieve → Gemini
      ├── Query 2 → Retrieve → Gemini
      └── Query N → Retrieve → Gemini
```

---

# Project Structure

```text
rag-engine/
│
├── data/
│   └── raw/
│       └── pdf/
│
├── database/
│   └── chroma.sqlite3
│
├── src/
│   ├── loaders/
│   │   └── pdf_loader.py
│   │
│   ├── preprocessors/
│   │   └── text_cleaner.py
│   │
│   ├── chunkers/
│   │   └── text_chunker.py
│   │
│   ├── embeddings/
│   │   └── embeddings_generator.py
│   │
│   ├── vector_store/
│   │   └── chroma_store.py
│   │
│   ├── llm/
│   │   ├── gemini_client.py
│   │   └── prompt_builder.py
│   │
│   ├── ingest.py
│   └── query.py
│
├── .env
├── .gitignore
├── README.md
└── requirements.txt
```

---

# Component Responsibilities

| File                      | Responsibility                         |
| ------------------------- | -------------------------------------- |
| `pdf_loader.py`           | Extract text from PDFs                 |
| `text_cleaner.py`         | Clean extracted text                   |
| `text_chunker.py`         | Split documents into chunks            |
| `embeddings_generator.py` | Generate document and query embeddings |
| `chroma_store.py`         | Store and retrieve vectors             |
| `gemini_client.py`        | Communicate with Gemini                |
| `prompt_builder.py`       | Build context-aware prompts            |
| `ingest.py`               | Run document ingestion                 |
| `query.py`                | Run retrieval and generation           |

---

# Setup

## 1. Clone the Repository

```bash
git clone <repository-url>
cd rag-engine
```

## 2. Create Virtual Environment

```bash
python -m venv .venv
```

Windows:

```bash
.venv\Scripts\activate
```

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

## 4. Configure Gemini

Create a `.env` file in the project root:

```env
GEMINI_API_KEY=your_api_key_here
```

The `.env` file is excluded from Git.

---

# Running the Project

## 1. Add a PDF

Place the document inside:

```text
data/raw/pdf/
```

## 2. Ingest

```bash
python src/ingest.py
```

This performs:

```text
PDF
 ↓
Extraction
 ↓
Cleaning
 ↓
Chunking
 ↓
Embedding
 ↓
ChromaDB
```

## 3. Query

```bash
python src/query.py
```

Example:

```text
Ask a question: What is this book about?
```

The query is embedded, relevant chunks are retrieved, the prompt is constructed, and Gemini generates the final response.

Type:

```text
exit
```

to stop the query loop.

---

# Current Dataset & Results

The current implementation uses:

```text
Skill with People, 10th ed.
Les Giblin
```

Current results:

```text
Total Chunks    : 39
Embedding Model : BAAI/bge-small-en-v1.5
Embedding Size  : 384
Matrix Shape    : (39, 384)
Vector Store    : ChromaDB
Index           : HNSW
LLM             : Gemini
```

---

# Project Status

| Module                      | Status     |
| --------------------------- | ---------- |
| PDF Processing              | ✅ Complete |
| Intelligent Chunking        | ✅ Complete |
| Embeddings                  | ✅ Complete |
| Vector Database & Retrieval | ✅ Complete |
| Prompt Engineering & Gemini | ✅ Complete |
| End-to-End RAG              | ✅ Complete |

### Complete Pipeline

```text
PDF
 ↓
PyMuPDF
 ↓
Text Cleaning
 ↓
Recursive Chunking
 ↓
BGE Embeddings
 ↓
ChromaDB
 ↓
HNSW Retrieval
 ↓
Relevant Context
 ↓
Prompt Builder
 ↓
Gemini
 ↓
Grounded Answer
```

---

# Key Design Decisions

### Chunk-Based Retrieval

Documents are divided into smaller chunks so retrieval can return focused information.

### Semantic Retrieval

Embeddings allow retrieval based on meaning rather than exact keyword matching.

### BGE Embeddings

`BAAI/bge-small-en-v1.5` provides 384-dimensional embeddings for the current implementation.

### Persistent ChromaDB

The vector database persists locally, allowing repeated queries without regenerating document embeddings.

### HNSW Retrieval

HNSW provides efficient approximate nearest-neighbor search.

### Separate Ingestion and Query Pipelines

Document processing happens independently from repeated querying.

### Retrieval Before Generation

Gemini receives retrieved document context before generating an answer.

### Environment-Based Secrets

API credentials are stored in `.env` rather than source code.

---

# Limitations

The current implementation focuses on the core RAG pipeline.

Not yet implemented:

* Retrieval evaluation
* Reranking
* Hybrid search
* Metadata filtering
* Query rewriting
* Conversation memory
* Streaming responses
* Web interface
* Production API deployment
* Observability
* Automated evaluation datasets

---

# Future Improvements

* Retrieval quality evaluation
* Precision and recall analysis
* Reranking
* Hybrid keyword + semantic search
* Metadata filtering
* Query transformation
* Improved chunking strategies
* Conversation memory
* Streaming responses
* FastAPI backend
* Web interface
* Logging and observability
* Automated evaluation
* Production deployment

---

# Final Result

The project now implements a complete basic RAG system:

```text
Document
   ↓
Processing
   ↓
Chunking
   ↓
Embeddings
   ↓
Vector Database
   ↓
Semantic Retrieval
   ↓
Context
   ↓
Prompt
   ↓
Gemini
   ↓
Grounded Response
```

The core RAG pipeline is complete and ready for the next stage of development: improving retrieval quality and moving toward a production-oriented implementation.


