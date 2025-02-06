import os
import sys
from mistralai import Mistral
from dotenv import load_dotenv
import discord
import asyncio

from agent import MistralAgent
from server import Recipe

# Load environment variables from .env
load_dotenv()

# Get API keys and settings
MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
DISCORD_CHANNEL_ID = int(os.getenv("DISCORD_CHANNEL_ID"))

# Initialize Mistral API client
api_key = os.environ["MISTRAL_API_KEY"]
model = "mistral-large-latest"
mistral_client = Mistral(api_key=api_key)


# Function to get chat response from Mistral
def get_chat_response(user: str):
    chat_response = mistral_client.chat.complete(
        model=model,
        messages=[
            {
                "role": "user",
                "content": f"Write a short message that {user} is testing the code in the theme of a pirate",
            },
        ],
    )
    return chat_response.choices[0].message.content


# Set up Discord intents
intents = discord.Intents.default()
intents.messages = True

# Create a Discord client
discord_client = discord.Client(intents=intents)


async def run_tests():
    # First test Discord
    channel = discord_client.get_channel(DISCORD_CHANNEL_ID)
    if channel is not None:
        username = os.getenv("USER")
        await channel.send(get_chat_response(username))
    else:
        print("Channel not found or invalid channel ID.")

    # Then test recipe creation
    mistral_agent = MistralAgent()
    test_message = "Create a simple pasta recipe with tomato sauce and basil."
    recipe = await mistral_agent.create_recipe(test_message)

    print(recipe)
    recipe_object = Recipe.from_json(recipe)
    print(recipe_object)
    recipe_summary = RecipeSummary(recipe_object)
    print(recipe_summary.summary)
    print(recipe_summary.ingredients)
    print(recipe_summary.steps)

    # Close the Discord client
    await discord_client.close()


@discord_client.event
async def on_ready():
    print(f"Logged in as {discord_client.user}")
    await run_tests()


if __name__ == "__main__":
    discord_client.run(DISCORD_TOKEN)
