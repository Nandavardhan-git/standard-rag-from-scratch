# Standard RAG From Scratch

A production-oriented Retrieval-Augmented Generation (RAG) project built by understanding every component from first principles before using production libraries.

## Project Goals

- Learn every stage of a modern RAG pipeline
- Understand why each component exists
- Build simple implementations first
- Replace them with production-ready solutions
- Document the reasoning behind every design decision

## Tech Stack

- Python
- PyMuPDF
- LangChain
- (Upcoming) Hugging Face
- (Upcoming) ChromaDB
- (Upcoming) Google Gemini

## Progress

### ✅ Module 1 – PDF Processing
- PDF loading using PyMuPDF
- Exception handling
- Text extraction
- Text cleaning

### ✅ Module 2 – Intelligent Text Chunking
- Built a custom character chunker
- Learned chunk overlap
- Identified limitations of naive chunking
- Understood the Recursive Chunking algorithm
- Integrated LangChain's RecursiveCharacterTextSplitter

## Module 3 – Embeddings

### Objectives
- Understand dense embeddings
- Compare embedding models
- Choose a production embedding model
- Generate embeddings for document chunks

### Implementation
- Integrated `sentence-transformers`
- Selected `BAAI/bge-small-en-v1.5`
- Implemented reusable embedding generator
- Generated embeddings for all document chunks

### Output
- 39 document chunks
- Embedding matrix shape: `(39, 384)`

### Key Learnings
- Dense vs Sparse embeddings
- Sentence embeddings
- NumPy output
- Batching
- Deterministic embeddings

## Upcoming Modules


- ⏳ Vector Database
- ⏳ Similarity Search
- ⏳ Retriever
- ⏳ Prompt Engineering
- ⏳ Complete RAG Pipeline
- ⏳ Evaluation & Improvements