import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv

# LangChain imports
from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits import create_sql_agent
from langchain_google_genai import ChatGoogleGenerativeAI


load_dotenv()

app = FastAPI(title="FMCG AI Assistant API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str

# Database setup
db_path = "sqlite:///fmcg.db"
db = None
agent_executor = None

def get_agent():
    global db, agent_executor
    if agent_executor is None:
        try:
            db = SQLDatabase.from_uri(db_path)
            # Use Gemini API
            llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro-latest", temperature=0)
            
            # Create SQL Agent
            agent_executor = create_sql_agent(
                llm=llm,
                toolkit=None, # Will use db instead of toolkit in newer versions, or directly pass db
                db=db,
                agent_type="zero-shot-react-description",
                verbose=True,
                handle_parsing_errors=True
            )
        except Exception as e:
            print(f"Error initializing agent: {e}")
            return None
    return agent_executor

@app.on_event("startup")
async def startup_event():
    print("Starting up and initializing AI agent...")
    get_agent()

@app.post("/chat")
async def chat(request: ChatRequest):
    agent = get_agent()
    if not agent:
        raise HTTPException(status_code=500, detail="AI Agent not initialized. Please check API keys and Database.")
    
    user_message = request.message
    
    try:
        # Provide a specific prompt to ensure context
        prompt = f"""You are an AI assistant for a Consumer Goods (FMCG) company. 
You are analyzing a database with 4 tables: product_master, store_master, sales_promotions, and inventory.
Answer the following business question based on the data:
{user_message}
"""
        response = agent.invoke({"input": prompt})
        return {"reply": response["output"]}
    except Exception as e:
        print(f"Agent error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
def health_check():
    return {"status": "ok"}
