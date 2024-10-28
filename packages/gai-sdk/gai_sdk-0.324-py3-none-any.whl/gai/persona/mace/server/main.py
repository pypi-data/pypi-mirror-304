import os
os.environ["LOG_LEVEL"] = "DEBUG"
import json
import argparse
from rich.console import Console
console=Console()
from gai.lib.common.logging import getLogger
logger = getLogger(__name__)

# Set up argparse to handle command-line arguments
parser = argparse.ArgumentParser(description="Start Gai Agent service.")
parser.add_argument('--persona', type=str, required=True, help='Specify the persona (e.g., sara)')
parser.add_argument('--nats', type=str, default="nats://localhost:4222", help='NATS servers address')
parser.add_argument('--ttt', type=str, default="http://localhost:12031", help='TTT host and port')
parser.add_argument("--all", action="store_true", help="Load all routers")
args = parser.parse_args()
if args.persona or args.all:
    persona_name = args.persona
nats=args.nats
ttt=args.ttt

# MaceServer Class
from gai.persona.mace.server.mace_server import MaceServer      

# Start Mace service
async def main():

    console.print(f"[yellow]Building persona: {args.persona}[/]")

    # Load provisioning details and build persona
    from gai.persona.persona_builder import PersonaBuilder
    from gai.persona.profile.pydantic.ProvisionAgentPydantic import ProvisionAgentPydantic
    persona_builder = PersonaBuilder()

    # import persona
    import_dir=os.path.abspath(os.path.join(os.path.dirname(__file__),"persona","data",args.persona))
    await persona_builder.import_async(import_dir=import_dir)

    # Assign LLM engine
    from gai.ttt.client.ttt_client import TTTClient
    persona_builder.set_ttt(ttt_client=TTTClient({
        "type": "ttt",
        "url": f"{ttt}/gen/v1/chat/completions",
        "timeout": 60.0,
        "temperature": 0.7,
        "top_p":0.9,
        "top_k": 50,
        "stop_conditions": ["\n\n","</s>","user:","<br><br>"]
    }))

    persona = persona_builder.build()    

    node = await MaceServer.create(
        servers=nats,
        persona=persona)
    await node.serve()

if __name__ == "__main__":
    logger.info("Gai Persona version 0.0.1")
    logger.info(f"Starting persona: {args.persona}")
    import asyncio
    asyncio.run(main())