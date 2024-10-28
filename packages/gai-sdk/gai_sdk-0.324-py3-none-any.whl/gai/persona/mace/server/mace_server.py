import json
import os
import base64
import time
from nats.aio.msg import Msg

from gai.lib.common.logging import getLogger
logger = getLogger(__name__)
from gai.network.gainet_node import GaiNetNode
from gai.persona.mace.flow_plan import FlowPlan
from gai.persona.mace.pydantic.FlowMessagePydantic import FlowMessagePydantic
from gai.persona.persona_builder import PersonaBuilder

class MaceServer(GaiNetNode):

    def __init__(self, servers, persona):
        super().__init__(servers,persona.agent_profile.Name)
        self.persona = persona
        self.other_content=""

    def _strip_xml(self,message):
        import re
        # This pattern matches the first and last XML tags in the string
        return re.sub(r'^<[^>]+>|<[^>]+>$', '', message)

    @staticmethod
    async def create(servers,persona):
        node = MaceServer(servers=servers, persona=persona)
        await node.connect()
        return node

    async def rollcall_handler(self,msg):
        logger.debug("rollcall received")
        subject=msg.subject
        data=msg.data.decode()
        reply = msg.reply
        self.messages.append({
            "subject":subject,
            "data":data
        })

        # reply with name and portrait
        # here = os.path.dirname(__file__)
        # image_path=os.path.join(here,"persona","data",self.node_name,"img","128x128.png")
        # with open(image_path,"rb") as f:
        #     image_bin = f.read()
        image_bin=self.persona.agent_image.Image128
        image_base64 = base64.b64encode(image_bin).decode('utf-8')
        response = {
            "Name": self.persona.agent_profile.Name,
            "ClassName": self.persona.agent_profile.ClassType.ClassName,
            "AgentDescription": self.persona.agent_profile.AgentDescription,
            "AgentShortDesc": self.persona.agent_profile.AgentShortDesc,
            "Image64": image_base64,
            "Image128": image_base64
        }        
        await self.send_raw(reply,json.dumps(response))

    # async def broadcast_handler(self,msg):
    #     subject=msg.subject
    #     data=msg.data.decode()
    #     reply=msg.reply
    #     self.messages.append({
    #         "subject":subject,
    #         "data":data
    #     })

    #     # generate llm response
    #     data=json.loads(data)
    #     message  = data["content"]
    #     message_id = data["message_id"]
    #     response = self.persona.act(message)

    #     # stream chunk
    #     chunk_id = 0
    #     for chunk in response:
    #         payload = {
    #             "name":self.node_name,
    #             "message_id":message_id,
    #             "chunk_id":chunk_id,
    #             "content":chunk
    #         }
    #         await self.send_raw(reply, json.dumps(payload))
    #         await self.flush()
    #         chunk_id+=1


    async def _send_reply(self,
            dialogue_id,
            round_no,
            turn_no,
            content,
            flow_diagram):
        
        # Check Plan for routing info
        plan=FlowPlan(flow_diagram=flow_diagram)
        turn=plan.get_turn(turn_no)

        # stream chunk
        response = self.persona.act(content)
        chunk_no = 0
        combined_chunks = ""

        # send message start
        message_start=f"<{self.node_name}>"
        message = FlowMessagePydantic(
            DialogueId=dialogue_id,
            RoundNo=round_no,
            TurnNo=turn.TurnNo,
            FlowDiagram=flow_diagram,
            Sender=self.node_name,
            Recipient="User",
            ChunkNo=chunk_no,
            Chunk=message_start
        )
        message = json.dumps(message.dict())
        subject=f"dialogue.{dialogue_id}"
        await self.send_raw(subject, message)
        await self.flush()

        # stream message
        for chunk in response:
            print(chunk,end="",flush=True)
            chunk_no += 1
            message = FlowMessagePydantic(
                DialogueId=dialogue_id,
                RoundNo=round_no,
                TurnNo=turn.TurnNo,
                FlowDiagram=flow_diagram,
                Sender=self.node_name,
                Recipient="User",
                ChunkNo=chunk_no,
                Chunk=chunk
            )
            message = json.dumps(message.dict())
            await self.send_raw(subject, message)
            await self.flush()
            combined_chunks += chunk
        
        # send message end
        message_end=f"</{self.node_name}>"
        message = FlowMessagePydantic(
            DialogueId=dialogue_id,
            RoundNo=round_no,
            TurnNo=turn.TurnNo,
            FlowDiagram=flow_diagram,
            Sender=self.node_name,
            Recipient="User",
            ChunkNo="<eom>",
            Chunk=message_end
        )
        message = json.dumps(message.dict())
        await self.send_raw(subject, message)
        await self.flush()

        return combined_chunks        


    async def dialogue_handler(self,msg: Msg):

        # Unwrap message
        subject=msg.subject
        data=msg.data.decode()
        dialogue_id=subject.split(".")[1]
        self.messages.append({
            "subject":subject,
            "data":data
        })

        # parse FlowMessage
        data=json.loads(data)
        pydantic = FlowMessagePydantic(**data)

        # Exception Case: Message from self to user or others
        if pydantic.Sender == self.node_name:
            # ignore message from self
            return

        # Exception Case: Message from anyone to anyone
        if pydantic.Sender == pydantic.Recipient:
            return

        # Case 2: Message from user
        if pydantic.Sender == "User" and pydantic.Recipient != self.node_name:

            # If step came from user, save user message
            message_id=f"{dialogue_id}:{pydantic.RoundNo}:{pydantic.TurnNo}"
            self.persona.add_user_message(
                user_id=self.persona.caller_id,
                user_message_id=message_id,
                content=pydantic.Content + f" {pydantic.Recipient}, let's begin with you.",
                timestamp=int(time.time())
                )

        # Case A: Message to this node
        if pydantic.Recipient == self.node_name:

            # Reply to user
            assistant_message = await self._send_reply(
                dialogue_id=dialogue_id,
                round_no=pydantic.RoundNo,
                turn_no=pydantic.TurnNo,
                content=pydantic.Content,
                flow_diagram=pydantic.FlowDiagram)

            # Save this node's reply
            assistant_message = self._strip_xml(assistant_message)
            self.persona.add_assistant_message(
                name=self.node_name,
                content=assistant_message
            )
        else:
        # Case B: Message to others
            
            if pydantic.Chunk:
                self.other_content+=pydantic.Chunk


            if pydantic.ChunkNo=="<eom>":
                self.other_content = self._strip_xml(self.other_content)
                self.persona.add_assistant_message(name=pydantic.Sender,content=self.other_content)
                self.other_content=""



    async def serve(self):
        logger.info("Server is starting to serve.")
        await self.nc.subscribe("system.rollcall", cb=self.rollcall_handler)
        #await self.nc.subscribe("broadcast.>", cb=self.broadcast_handler)
        await self.nc.subscribe("dialogue.>", cb=self.dialogue_handler)
        await self.listen()