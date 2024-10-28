import uuid
import base64
from io import BytesIO

# fastapi
from fastapi import APIRouter, Body, HTTPException, Header, Depends, Request
from gai.lib.common.errors import InternalException
from gai.lib.common.logging import getLogger
logger = getLogger(__name__)
from gai.persona.images.pydantic.GenerateImagePydantic import GenerateImagePydantic
from gai.tti.client.tti_client import TTIClient
from gai.persona.images.system_images_mgr import SystemImagesMgr

# Implementations Below
image_router = APIRouter()

def convert_image_to_base64(image_bytes):
    # Ensure you have a bytes-like object. If you have a file path, you would need to read it in binary mode first.
    buffered = BytesIO(image_bytes)
    encoded_string = base64.b64encode(buffered.getvalue())
    return encoded_string.decode('utf-8')  # Convert bytes to string if necessary

### POST /api/v1/persona/image
@image_router.post("/api/v1/persona/image")
async def post_persona_image(req: GenerateImagePydantic=Body(...)):
    try:
        mgr = SystemImagesMgr(
            tti_client=TTIClient(config={
                "type":"tti",
                "url":"http://localhost:12035/sdapi/v1/txt2img"
            })
        )
        if not req.AgentId:
            req.AgentId = "00000000-0000-0000-0000-000000000000"
        agent_image = mgr.generate_image(
            agent_id=req.AgentId,
            agent_name=req.Name,
            agent_traits=req.AgentTraits,
            image_styles=req.AgentImageStyles,
            description=req.AgentDescription
        )
        mgr.export_image(agent_image)
        image_bytes = mgr.get_agent_image(agent_id=req.AgentId,size="256x256")
        image_base64 = convert_image_to_base64(image_bytes=image_bytes)
        imageType = 'image/png'
        dataUrl = f'data:{imageType};base64,{image_base64}'
        return {"data_url":dataUrl}

    except Exception as e:
        id = str(uuid.uuid4())
        logger.error(str(e)+" "+id)
        raise InternalException(id)
    

### GET /api/v1/persona/profile
@image_router.get("/api/v1/persona/image/{size}/{persona_id}")
async def get_persona_image(size:str,persona_id:str):
    mgr = SystemImagesMgr(
        tti_client=TTIClient(config={
            "type":"tti",
            "url":"http://localhost:12035/sdapi/v1/txt2img"
        })
    )
    image_bytes = mgr.get_agent_image(agent_id=persona_id,size=size)
    image_base64 = convert_image_to_base64(image_bytes=image_bytes)
    imageType = 'image/png'
    dataUrl = f'data:{imageType};base64,{image_base64}'
    return {"data_url":dataUrl}
