import logging
from fastapi import FastAPI
from pydantic import BaseModel

from tomaba.agent import MistralAgent

# Setup logging
logger = logging.getLogger("server")

# Initialize FastAPI app
app = FastAPI()

# Load AI agent
agent = MistralAgent()


class MessageRequest(BaseModel):
    author: str
    content: str


@app.get("/")
def root():
    """Health check endpoint."""
    return {"status": "ok", "message": "Tomaba Discord bot server is running!"}


@app.get("/healthz")
def healthz():
    """Health check endpoint."""
    return {"status": "ok", "message": "Tomaba Discord bot server is running!"}


@app.post("/chat")
async def chat(request: MessageRequest):
    """Processes incoming messages from the bot and returns a response."""
    logging.info(f"Server processing message: {request}")

    # TODO: This is where we will do handling to determine what kind of message
    # is being sent and then call the appropriate agent function

    response = await agent.create_recipe(request.content)

    logger.info(f"Response: {response}")

    # TODO: Eventually, the response will be a recipe with a lot of information
    # in JSON structure. We'll need to parse the message for what to send back
    # to the Discord channel, as well as what to store in the database.

    return {"response": response}
