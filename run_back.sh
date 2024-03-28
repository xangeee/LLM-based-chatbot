#!/bin/bash

# Pre-processing tasks
echo "Storing the papers dataset in vector database ChromaDB..."

# Run the embedding script
python backend/src/langchain/create_retriever.py

echo "Starting the API application..."
uvicorn backend.src.main:app --host 0.0.0.0 --port 8000

