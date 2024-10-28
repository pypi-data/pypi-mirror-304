import queue
import time
import asyncio
import json

# fastapi
from fastapi import APIRouter, Body, HTTPException, Header, Depends, Request
from pydantic import BaseModel
from fastapi.responses import StreamingResponse
from gai.lib.common.logging import getLogger
logger = getLogger(__name__)
from nats.aio.msg import Msg
from gai.persona.mace.client.mace_client import MaceClient
from gai.persona.mace.pydantic.FlowMessagePydantic import FlowMessagePydantic

# Implementations Below
mace_router = APIRouter()



@mace_router.post("/api/v1/user/dialogue/{dialogue_id}/{round_no}")
async def persona_chat(dialogue_id:str, round_no:str, request: Request):
    pass

@mace_router.post("/api/v1/user/dialogue/{dialogue_id}/clear")
async def clear_dialogue(dialogue_id:str):
    pass

@mace_router.get("/api/v1/dialogue/{dialogue_id}/participants")
async def get_dialogue_participants(dialogue_id:str):

    pass