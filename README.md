# Rag_College_Data

A Retrieval-Augmented Generation (RAG) system designed to answer questions about college data using a vector database and Large Language Models.

## Project Structure

- `backend/`: FastAPI server that handles document retrieval and LLM response generation.
- `frontend/`: React-based user interface for interacting with the chatbot.
- `data/`: PDF documents used for context.
- `scripts/`: Utility scripts for data ingestion and testing.

## Features

- **RAG Pipeline**: Retrieves context from PDF documents using FAISS vector database.
- **Persistent Chat History**: Stores user sessions in MongoDB for multi-turn conversations.
- **Modern UI**: Clean and responsive chat interface built with Vite and React.
- **Support for multiple LLMs**: Configurable to use various LLM providers.

## Getting Started

### Backend Setup
1. Navigate to `backend/`.
2. Install dependencies: `pip install -r requirements.txt`.
3. Configure `.env` with your API keys.
4. Run the server: `python main.py`.

### Frontend Setup
1. Navigate to `frontend/`.
2. Install dependencies: `npm install`.
3. Run the development server: `npm run dev`.

## Technologies Used
- FastAPI
- React
- LangChain
- FAISS
- MongoDB
- Google Gemini / Other LLMs
