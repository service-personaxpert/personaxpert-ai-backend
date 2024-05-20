# server.py
from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from app.utils.logger import get_logger
from gemini_functions_agent import agent_executor as gemini_functions_agent_chain
from rag_supabase.chain import chain as rag_supabase_chain
from app.modules.agents.api import (
    create_blog_suggestion_chain,
    create_blog_section_chain,
    create_blog_content_chain,
    router as agents_router  # Import the router for database operations
)
from langserve import add_routes
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

# Set all CORS enabled origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

@app.get("/")
async def redirect_root_to_docs():
    return RedirectResponse("/docs")

add_routes(app, gemini_functions_agent_chain, path="/gemini-functions-agent")
add_routes(app, rag_supabase_chain, path="/rag-supabase")

# Add the blog-related routes with unique paths
add_routes(app, create_blog_suggestion_chain, path="/blogs/suggestions/create")
add_routes(app, create_blog_section_chain, path="/blogs/sections/create")
add_routes(app, create_blog_content_chain, path="/blogs/content/create")
# Include the router for database operations
app.include_router(agents_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
