import os
os.environ["LOG_LEVEL"] = "DEBUG"
import argparse
from fastapi import FastAPI
from fastapi import APIRouter, Body, HTTPException, Header, Depends, Request
from pydantic import BaseModel
from fastapi.responses import StreamingResponse
import uvicorn
import json
import asyncio
import time
from nats.aio.msg import Msg

from rich.console import Console
console=Console()
from gai.lib.common.logging import getLogger
logger = getLogger(__name__)
from gai.persona.mace.client.mace_client import MaceClient
from gai.persona.mace.pydantic.FlowMessagePydantic import FlowMessagePydantic

# Set up argparse to handle command-line arguments
parser = argparse.ArgumentParser(description="Start Gai Agent service.")
parser.add_argument('--nats', type=str, default="nats://localhost:4222", help='Specify the persona (e.g., sara)')
parser.add_argument("--all", action="store_true", help="Load all routers")
args = parser.parse_args()
nats = args.nats

console.print(f"[yellow]connection={nats}[/]")

# Setup APIs
app = FastAPI()
mace_router = APIRouter()
app.include_router(mace_router)
response_q = asyncio.Queue()

# Enqueue incoming messages
async def on_chat(msg: Msg):
    global response_q

    data=msg.data.decode()
    if not data:
        return
    
    data=json.loads(data)
    pydantic = FlowMessagePydantic(**data)

    # Case 1: from "User" to Persona
    if pydantic.Sender == "User":
        # Ignore
        return
    
    # Case 2: from "Persona" to User
    if pydantic.Recipient == "User":
        if pydantic.Chunk:
            await response_q.put(pydantic.Chunk)
        if pydantic.ChunkNo=="<eom>":
            await response_q.put(None)

# Dequeue and stream chunk
async def streamer(mace_client):
    global response_q
    start_time = time.time()
    timeout = 60
    elapsed = 0
    try:
        chunk = True
        while elapsed <= timeout or chunk==None:
            try:
                # Get message from queue with a small timeout to avoid blocking indefinitely
                chunk = await asyncio.wait_for(response_q.get(), timeout=0.5)
                if not chunk:
                    print()
                    logger.info("End of message.")
                    return
                print(chunk,end="",flush=True)
                yield chunk
                elapsed = time.time() - start_time
            except asyncio.TimeoutError:
                # continue looping and do not terminate
                pass
            finally:
                elapsed = time.time() - start_time
    except Exception as e:
        logger.error("mace_router.stream: error="+e)
        raise Exception("mace_router.stream: error="+e)
    finally:
        await mace_client.close()

    if elapsed > timeout:
        raise Exception("mace_router.streamer: timeout")

@app.on_event("startup")
async def startup_event():
    mace_client = await MaceClient.create(
        servers="nats://localhost:4222"
    )
    app.state.mace_client = mace_client
    await mace_client.subscribe(async_chat_handler=on_chat)

"""
The endpoint will take in a message and send it to a server with the response handled via on_chat() callback.
on_chat() will queue the request to be picked up and stream as response.
The stream ends by either timeout or receiving the terminating tag, ie. </{src}>
"""
# POST "/api/v1/user/dialogue"
class PersonaChatRequest(BaseModel):
    round_no:int=0
    user_message:str
    seq_diagram:str
@mace_router.post("/api/v1/user/dialogue")
async def post_user_dialogue(req: PersonaChatRequest, request: Request):
    mace_client = request.app.state.mace_client
    await mace_client.dialogue(msg=req.user_message,flow_diagram=req.seq_diagram)
    return StreamingResponse(streamer(mace_client))

# GET "/api/v1/user/dialogue"
@mace_router.get("/api/v1/user/dialogue/next")
async def get_user_dialogue_next(req: PersonaChatRequest, request: Request):
    mace_client = request.app.state.mace_client
    await mace_client.next()
    return StreamingResponse(streamer(mace_client))

if __name__ == "__main__":
    logger.info("Gai Local App Server version 0.0.1")
    uvicorn.run(app, host="0.0.0.0", 
                port=12033,
                ws_ping_interval=20,    # Server will ping every 20 seconds
                ws_ping_timeout=300     # Server will wait 5 min for pings before closing
                )