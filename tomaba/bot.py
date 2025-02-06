import os
import discord
import logging
import asyncio
import httpx
from datetime import datetime, timedelta

from discord.ext import commands
from dotenv import load_dotenv

from models.recipe import Recipe, RecipeSummary

# Load environment variables
load_dotenv()

PREFIX = "!"
SERVER_URL = "http://localhost:8080/chat"

# Setup logging
logger = logging.getLogger("discord")

# Setup bot intents
intents = discord.Intents.all()
intents.messages = True
intents.guilds = True


class DiscordBot(commands.Bot):
    """
    A lightweight Discord bot that listens for messages and forwards them to a FastAPI server.
    """

    def __init__(self, token: str):
        super().__init__(command_prefix=PREFIX, intents=intents)
        self.token = token

    async def on_ready(self):
        """Triggered when the bot successfully connects to Discord."""
        logger.info(f"{self.user} has connected to Discord!")

    async def on_message(self, message):
        """Handle incoming messages."""
        if message.author == self.user:
            return

        try:
            # Fetch message history from the channel
            message_history = []
            async for msg in message.channel.history(limit=3):  # Adjust limit as needed
                # Skip messages older than the current conversation
                if msg.created_at < message.created_at - timedelta(minutes=5):  # Adjust timeframe as needed
                    break
                # Add to history if it's from the bot or the current conversation
                if msg.author == self.user or msg.author == message.author:
                    message_history.insert(0, {
                        "author": str(msg.author),
                        "content": msg.content
                    })

            # Get response from server
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    SERVER_URL,
                    json={
                        "author": str(message.author),
                        "content": message.content,
                        "message_history": message_history
                    },
                    timeout=120,
                )

            response_data = response.json()

            # Check response type and handle accordingly
            if response_data["type"] == "recipe" and isinstance(response_data["response"], dict):
                max_message_length = 2000
                recipe = Recipe.from_json(response_data["response"])
                recipe_summary = RecipeSummary(recipe)
                
                # Send summary in parts 
                # TODO: should put this entire splitting in parts in a separate function
                summary_parts = [recipe_summary.summary[i:i+max_message_length] 
                               for i in range(0, len(recipe_summary.summary), max_message_length)]
                for part in summary_parts:
                    await message.reply(part)

                # Send ingredients in parts
                ingredients_parts = [recipe_summary.ingredients[i:i+max_message_length] 
                                  for i in range(0, len(recipe_summary.ingredients), max_message_length)]
                for part in ingredients_parts:
                    await message.reply(part)

                # Split steps into parts that don't exceed max message length
                current_part = ""
                steps_parts = []
                
                for step in recipe_summary.steps.split('\n'):
                    # If adding this step would exceed max length, start new part
                    if len(current_part + step + '\n') > max_message_length:
                        steps_parts.append(current_part)
                        current_part = step + '\n'
                    else:
                        current_part += step + '\n'
                
                # Add final part if not empty
                if current_part:
                    steps_parts.append(current_part)
                    
                # Send each part of the steps
                for part in steps_parts:
                    await message.reply(part)
            else:
                # If it's just a text response, send it
                await message.channel.send(response_data["response"])

        except Exception as e:
            logger.error(f"Error processing message: {e}")
            if response_data and "response" in response_data:
                logger.error(f"Response data content: {response_data['response']}")
            await message.channel.send("Sorry, I encountered an error processing your request.")

    def run_bot(self):
        """Runs the bot asynchronously."""
        asyncio.set_event_loop(asyncio.new_event_loop())
        self.run(self.token)
