# FMCG AI Assistant

This is an end-to-end conversational AI assistant for FMCG beverage analytics. It allows business users to query sales, inventory, and promotional data using natural language.

## Modules Included
This repository satisfies M6 (Code & Build) and M7 (Deployment/System).

## Tech Stack
- **Backend**: Python 3.10+, FastAPI, LangChain, SQLite
- **Frontend**: React (Vite), Vanilla CSS

## Setup & Running Locally

### 1. Backend Setup
1. Navigate to the `backend` directory.
2. Create a virtual environment: `python -m venv venv`
3. Activate it:
   - Windows: `.\venv\Scripts\activate`
   - Mac/Linux: `source venv/bin/activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Generate the synthetic database (this will create `fmcg.db` and CSV files in `data/`):
   ```bash
   python generate_data.py
   ```
6. Copy `.env.example` to `.env` and add your LLM API key (e.g., `GEMINI_API_KEY`).
7. Run the FastAPI server:
   ```bash
   uvicorn main:app --reload --port 8000
   ```

### 2. Frontend Setup
1. Navigate to the `frontend` directory.
2. Install dependencies: `npm install`
3. Run the development server:
   ```bash
   npm run dev
   ```
4. Open the provided localhost URL (usually http://localhost:5173) in your browser.

## Features
- **Conversational Analytics**: Ask questions like "What was the revenue for Spark Lemon in the North region?"
- **Premium UI**: Dark mode, glassmorphism, and responsive design.
- **Agentic SQL**: The backend LLM agent automatically inspects the SQLite schema, writes the SQL query, executes it, and formats the result.

## Biggest Technical Issue (M6 Requirement)
**Issue**: LLM hallucinating column names or SQL syntax for SQLite.
**Resolution**: Instead of a naive text-to-SQL prompt, we implemented LangChain's SQL Agent (`create_sql_agent`). This uses a ReAct pattern where the LLM first requests the schema (`sql_db_schema`), then writes the query, and if the query fails, it reads the error and rewrites the query before returning the final answer.
