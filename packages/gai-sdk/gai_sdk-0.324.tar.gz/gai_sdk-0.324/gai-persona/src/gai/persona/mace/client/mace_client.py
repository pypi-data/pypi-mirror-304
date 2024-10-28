import asyncio
import uuid
import time
import json

from gai.lib.common.logging import getLogger
logger = getLogger(__name__)
from gai.network.gainet_node import GaiNetNode
from gai.lib.dialogue.dialogue_store import DialogueStore
from gai.persona.mace.flow_plan import FlowPlan
from gai.persona.mace.pydantic.FlowMessagePydantic import FlowMessagePydantic


class MaceClient(GaiNetNode):

    def __init__(self, servers, dialogue_id, caller_id, api_host):
        super().__init__(servers,"User")
        self.subscribed={}

        self.rollcall_inbox=self.nc.new_inbox()
        self.rollcall_messages=[]

        self.caller_id=caller_id
        self.dialogue_state={
            "dialogue_id": dialogue_id,
            "round_no":0,
            "turn_no":0,
            "flow_diagram":None
        }
        self.dialogue_store = DialogueStore(
            caller_id=caller_id,
            agent_id=None,
            dialogue_id=dialogue_id,
            api_host=api_host,
            message_count_cap=10,
            message_char_cap=4000
        )

    def _strip_xml(self,message):
        import re
        # This pattern matches the first and last XML tags in the string
        return re.sub(r'^<[^>]+>|<[^>]+>$', '', message)

    @staticmethod
    async def create(servers, 
                    dialogue_id="00000000-0000-0000-0000-000000000000", 
                    caller_id="00000000-0000-0000-0000-000000000000", 
                    api_host="http://localhost:12033"
                    ):
        client = MaceClient(servers=servers, dialogue_id=dialogue_id, caller_id=caller_id,api_host=api_host)
        await client.connect()
        return client
    
    async def subscribe(self, async_chat_handler=None):

        # subscribe to rollcall
        if not self.subscribed.get(self.rollcall_inbox):
            await self.nc.subscribe(self.rollcall_inbox, cb=self.rollcall_handler)
            self.subscribed[self.rollcall_inbox]=True

        # subscribe to dialogue
        if async_chat_handler:
            dialogue_id=self.dialogue_state["dialogue_id"]
            subject=f"dialogue.{dialogue_id}"
            if not self.subscribed.get(subject,None):
                await self.nc.subscribe(subject,cb=async_chat_handler)
                self.subscribed[subject]=True
        
    async def rollcall_handler(self,msg):
        subject = msg.subject
        data=msg.data.decode()
        self.rollcall_messages.append({
            "subject":subject,
            "data":data
        })
        name=json.loads(data)["Name"]
        logger.debug(f"system.rollcall: {name}")

    async def rollcall(self):
        logger.info(f"start rollcall")
        self.rollcall_messages = []
        await self.nc.publish("system.rollcall", self.node_name.encode(), self.rollcall_inbox)
        await asyncio.sleep(5)
        for message in self.rollcall_messages:
            data = json.loads(message["data"])
            logger.info(data["Name"]+":"+data["AgentDescription"])

    # async def broadcast(self, msg, message_id=None):
    #     self.chat_messages = []
    #     if not message_id:
    #         message_id = str(uuid.uuid4())
    #     message = {
    #         "message_id":message_id,
    #         "name":self.node_name,
    #         "content":msg
    #     }
    #     message=json.dumps(message)
    #     await self.nc.publish(f"broadcast.{self.dialogue_id}", message.encode(), self.chat_inbox)
    #     await asyncio.sleep(10)

    async def list_dialogue_messages(self):
        return self.dialogue_store.list_dialogue_messages()

    async def reset_dialogue(self):
        dialogue_id = self.dialogue_state["dialogue_id"]
        self.dialogue_state={
            "dialogue_id": dialogue_id,
            "round_no":0,
            "turn_no":0,
            "flow_diagram":None
        }
        self.dialogue_store.clear()

    """
    This will start a new round of dialogue with the following states:
      - dialogue_id : unchanged.
      - round_no    : increase by 1
      - turn_no     : reset to 0
    """
    async def dialogue(self, msg, flow_diagram):
        
        # Start a new round of dialogue
        dialogue_id = self.dialogue_state["dialogue_id"]
        round_no = self.dialogue_state["round_no"] + 1
        turn_no = 0
        message_id=f"{dialogue_id}:{round_no}:{turn_no}"
        self.chat_messages = []

        # parse flow
        plan = FlowPlan(flow_diagram=flow_diagram)
        turn = plan.get_turn(turn_no=turn_no)
        
        # prepare message
        message = FlowMessagePydantic(
            DialogueId=dialogue_id,
            RoundNo=round_no,
            TurnNo=turn_no,
            FlowDiagram=flow_diagram,
            Sender=self.node_name,
            Recipient=turn.Dest,
            Content=msg
        )
        logger.info(f"\nUser:\n{message.Content}")

        # send message
        subject=f"dialogue.{dialogue_id}"
        message=json.dumps(message.dict())
        await self.send_raw(subject,message)

        # save message
        self.dialogue_store.add_user_message(
            user_id=self.caller_id,
            message_id=message_id,
            content=msg,
            timestamp=int(time.time())
        )

        self.dialogue_state={
            "dialogue_id": dialogue_id,
            "round_no":round_no,
            "turn_no":turn_no,
            "flow_diagram":flow_diagram,
            "user_message":msg
        }
        return message_id

    """
    This will continue the next turn within the same round:
      - dialogue_id : unchanged.
      - round_no    : unchanged.
      - turn_no     : increase by 1
    """
    async def next(self):

        dialogue_id = self.dialogue_state["dialogue_id"]
        round_no = self.dialogue_state["round_no"]
        turn_no = self.dialogue_state["turn_no"] + 1
        flow_diagram=self.dialogue_state["flow_diagram"]
        user_message=self.dialogue_state["user_message"]

        if not flow_diagram:
            raise Exception("Dialogue not started.")

        flow = FlowPlan(flow_diagram=flow_diagram)
        turn = flow.get_turn(turn_no)

        if not turn:
            # ran out of turns
            return None
        
        # prepare message
        message = FlowMessagePydantic(
            DialogueId=dialogue_id,
            RoundNo=round_no,
            TurnNo=turn_no,
            FlowDiagram=flow_diagram,
            Sender=self.node_name,
            Recipient=turn.Dest,
            Content=""
        )
        if turn.Src == "User":
            # polling
            message.Content = user_message
        else:
            # pipelining
            message.Content = f"{turn.Dest}, it is your turn to respond."
        logger.info(f"\nUser:\n{message.Content}")

        subject=f"dialogue.{dialogue_id}"
        message=json.dumps(message.dict())
        await self.send_raw(subject,message)

        self.dialogue_state={
            "dialogue_id": dialogue_id,
            "round_no":round_no,
            "turn_no":turn_no,
            "flow_diagram":flow_diagram,
            "user_message":user_message
        }

        return turn
