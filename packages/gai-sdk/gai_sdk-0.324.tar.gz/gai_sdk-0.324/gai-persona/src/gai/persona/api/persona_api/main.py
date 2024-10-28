import os
os.environ["LOG_LEVEL"] = "DEBUG"
import argparse
from fastapi import FastAPI
import uvicorn
from rich.console import Console
console=Console()
from gai.lib.common.logging import getLogger
logger = getLogger(__name__)
from gai.persona.profile.api.profile_router import profile_router
from gai.persona.images.api.image_router import image_router
from gai.persona.prompts.api.prompt_router import prompt_router
from gai.persona.tools.api.tool_router import tool_router
from gai.persona.docs.api.document_router import document_router
from fastapi.middleware.cors import CORSMiddleware

# Set up argparse to handle command-line arguments
parser = argparse.ArgumentParser(description="Start Gai Agent service.")
parser.add_argument('--nats', type=str, default="nats://localhost:4222", help='Specify nats address')
parser.add_argument("--all", action="store_true", help="Load all routers")
args = parser.parse_args()
nats = args.nats

console.print(f"[yellow]connection={nats}[/]")

# Setup APIs
app = FastAPI()
app.include_router(profile_router)
app.include_router(image_router)
app.include_router(prompt_router)
app.include_router(tool_router)
app.include_router(document_router)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5123"],  # Specify the origins (use ["*"] for all origins)
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods or specify specific ones ["POST", "GET"]
    allow_headers=["*"],  # Allow all headers or specify specific ones
)

if __name__ == "__main__":
    logger.info("Gai Local App Server version 0.0.1")
    uvicorn.run(app, host="0.0.0.0", 
                port=12033,
                ws_ping_interval=20,    # Server will ping every 20 seconds
                ws_ping_timeout=300     # Server will wait 5 min for pings before closing
                )