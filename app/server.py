from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from langserve import add_routes
from app.utils.logger import get_logger
from gemini_functions_agent import agent_executor as gemini_functions_agent_chain
from rag_supabase.chain import chain as rag_supabase_chain
import os
from google.cloud import secretmanager
from dotenv import load_dotenv

# Initialize logger
logger = get_logger(__name__)


# Load environment variables from .env file if present
load_dotenv()
# Fetch and set environment variables from GCP Secret Manager
env = os.getenv("ENV")
print(f"ENV: {env}")

logger.info(f"Launching PersonaXpert AI Backend in {env} environment 🚀")

app = FastAPI()

@app.get("/")
async def redirect_root_to_docs():
    return RedirectResponse("/docs")

add_routes(app, gemini_functions_agent_chain, path="/gemini-functions-agent")
add_routes(app, rag_supabase_chain, path="/rag-supabase")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
