import os
os.environ["LOG_LEVEL"] = "DEBUG"
import argparse
from fastapi import FastAPI
from fastapi.responses import StreamingResponse,JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
import json
import asyncio
import time
from nats.aio.msg import Msg
from typing import Dict
from io import BytesIO
import base64

from rich.console import Console
console=Console()
from gai.lib.common.logging import getLogger
logger = getLogger(__name__)
from gai.persona.mace.client.mace_client import MaceClient
from gai.persona.mace.pydantic.FlowMessagePydantic import FlowMessagePydantic
from gai.persona.docs.api.document_router import document_router

# Set up argparse to handle command-line arguments
parser = argparse.ArgumentParser(description="Start Gai Agent service.")
parser.add_argument('--nats', type=str, default="nats://localhost:4222", help='Specify the persona (e.g., sara)')
parser.add_argument("--all", action="store_true", help="Load all routers")
args = parser.parse_args()
nats = args.nats

console.print(f"[yellow]connection={nats}[/]")

# Setup APIs
app = FastAPI()
app.include_router(document_router)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5123"],  # Specify the origins (use ["*"] for all origins)
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods or specify specific ones ["POST", "GET"]
    allow_headers=["*"],  # Allow all headers or specify specific ones
)

response_q = asyncio.Queue()
mace_client=None
image_storage: Dict[str, bytes] = {}
thumbnail_storage: Dict[str, bytes] = {}

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
        await response_q.put(pydantic)
        # if pydantic.Chunk:
        #     await response_q.put(pydantic.Chunk)
        # if pydantic.ChunkNo=="<eom>":
        #     await response_q.put(None)

# Dequeue and stream chunk
async def streamer(mace_client):
    global response_q
    start_time = time.time()
    timeout = 60
    elapsed = 0
    content=""
    try:
        while elapsed <= timeout:
            try:
                # Get message from queue with a small timeout to avoid blocking indefinitely
                pydantic = await asyncio.wait_for(response_q.get(), timeout=0.5)
                if pydantic.ChunkNo=="<eom>":
                    # If end of message, save assistant message to store
                    content=mace_client._strip_xml(content)
                    mace_client.dialogue_store.add_assistant_message(name=pydantic.Sender, content=content)

                    # Log details
                    print(pydantic.Chunk,end="",flush=True)
                    print()
                    logger.info("List dialogue messages:")
                    messages = await mace_client.list_dialogue_messages()
                    for message in messages:
                        print()
                        print(message)
                        print()

                    # Yield final chunk
                    yield pydantic.Chunk
                    return
                
                print(pydantic.Chunk,end="",flush=True)
                content+=pydantic.Chunk
                yield pydantic.Chunk
            except asyncio.TimeoutError:
                # continue looping and do not terminate
                pass
            finally:
                elapsed = time.time() - start_time
    except Exception as e:
        logger.error("mace_router.stream: error="+e)
        raise Exception("mace_router.stream: error="+e)
    finally:
        pass
        #await mace_client.close()

    if elapsed > timeout:
        raise Exception("mace_router.streamer: timeout")

@app.on_event("startup")
async def startup_event():
    global mace_client
    mace_client = await MaceClient.create(
        servers="nats://localhost:4222"
    )
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
@app.post("/api/v1/user/dialogue")
async def post_user_dialogue(req: PersonaChatRequest):
    global mace_client
    await mace_client.dialogue(msg=req.user_message,flow_diagram=req.seq_diagram)
    return StreamingResponse(streamer(mace_client))

# GET "/api/v1/user/dialogue"
@app.get("/api/v1/user/dialogue")
async def get_user_dialogue_next():
    global mace_client
    response = await mace_client.next()
    if not response:
        return JSONResponse(status_code=404,content="")
    return StreamingResponse(streamer(mace_client))

# GET "/api/v1/user/dialogue/messages"
@app.get("/api/v1/user/dialogue/messages")
async def get_user_dialogue_messages():
    global mace_client
    return await mace_client.list_dialogue_messages()

# DELETE "/api/v1/user/dialogue/messages"
@app.delete("/api/v1/user/dialogue/messages")
async def delete_user_dialogue_messages():
    global mace_client
    return await mace_client.reset_dialogue()

# GET "/api/v1/user/personas"
@app.get("/api/v1/user/personas")
async def get_dialogue_participants():
    global mace_client
    await mace_client.rollcall()
    personas=[]
    for msg in mace_client.rollcall_messages:
        data=json.loads(msg["data"])
        name = data["Name"]
        class_name = data["ClassName"]
        short_desc = data["AgentShortDesc"]
        desc=data["AgentDescription"]
        image_url = f"http://localhost:12033/api/v1/persona/{name}/image"
        thumbnail_url = f"http://localhost:12033/api/v1/persona/{name}/thumbnail"
        if not image_storage.get(name,None):
            # 128x128
            image_storage[name] = base64.b64decode(data["Image128"])
        if not thumbnail_storage.get(name,None):
            # 64x64
            thumbnail_storage[name] = base64.b64decode(data["Image64"])

        data = {
            "Name":name,
            "ClassName":class_name,
            "AgentShortDesc":short_desc,
            "AgentDescription":desc,
            "ImageUrl": image_url,
            "ThumbnailUrl": thumbnail_url
        }

        personas.append(data)
    return personas

# GET "/api/v1/user/persona/{persona_name}/image"
@app.get("/api/v1/persona/{persona_name}/image")
async def get_persona_image(persona_name:str):
    response = StreamingResponse(BytesIO(image_storage[persona_name]), media_type="image/png")
    response.headers["Cache-Control"] = "public, max-age=86400"  # Example: cache for 1 day
    return response

# GET "/api/v1/user/persona/{persona_name}/thumbnail"
@app.get("/api/v1/persona/{persona_name}/thumbnail")
async def get_persona_thumbnail(persona_name:str):
    response = StreamingResponse(BytesIO(thumbnail_storage[persona_name]), media_type="image/png")
    response.headers["Cache-Control"] = "public, max-age=86400"  # Example: cache for 1 day
    return response

if __name__ == "__main__":
    logger.info("Gai Local App Server version 0.0.1")
    uvicorn.run(app, host="0.0.0.0", 
                port=12033,
                ws_ping_interval=20,    # Server will ping every 20 seconds
                ws_ping_timeout=300     # Server will wait 5 min for pings before closing
                )