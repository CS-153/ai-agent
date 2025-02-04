import threading
import uvicorn
import logging
import signal
import sys
import os

from tomaba.bot import DiscordBot
from tomaba.server import app

logging.basicConfig(level=logging.INFO)

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

bot = DiscordBot(DISCORD_TOKEN)
bot_thread = None


def start_bot():
    """Starts the Discord bot in a separate thread."""
    global bot_thread
    bot_thread = threading.Thread(target=bot.run_bot, daemon=True)
    bot_thread.start()


def shutdown_handler(signal_received, frame):
    """Handles graceful shutdown of bot and server."""
    logging.info("Shutting down gracefully...")
    if bot_thread and bot_thread.is_alive():
        bot.close()  # Ensures bot disconnects cleanly
    sys.exit(0)


# Register signal handlers
signal.signal(signal.SIGINT, shutdown_handler)
signal.signal(signal.SIGTERM, shutdown_handler)

if __name__ == "__main__":
    start_bot()
    uvicorn.run(app, host="0.0.0.0", port=8080)
