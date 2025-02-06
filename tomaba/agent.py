import json
import os
from typing import Dict, Union
from mistralai import Any, Mistral, ChatCompletionResponse
from dotenv import load_dotenv

from prompt import CREATE_RECIPE_SYSTEM_PROMPT, ANALYZE_CONVERSATION_SYSTEM_PROMPT

import logging

logger = logging.getLogger("agent")

MISTRAL_MODEL = "mistral-large-latest"


class MistralAgent:
    def __init__(self):
        """Initialize the Mistral client."""
        load_dotenv()  # Add this if not already present
        api_key = os.getenv("MISTRAL_API_KEY")
        if not api_key:
            raise ValueError("MISTRAL_API_KEY environment variable not set")
        self.client = Mistral(api_key=api_key)

    def response_to_json(self, content: str):
        """Convert a response string to JSON, handling both recipe and text formats."""
        try:
            # First try to extract JSON from code blocks
            if "```json" in content:
                json_str = content.split("```json")[1].split("```")[0].strip()
                return json.loads(json_str)
            elif "```" in content:
                # Try to extract from any code block
                json_str = content.split("```")[1].split("```")[0].strip()
                try:
                    return json.loads(json_str)
                except json.JSONDecodeError:
                    # If it's not valid JSON, return the text content
                    return content
            else:
                # If no code blocks, return the raw content
                return content
        except Exception as e:
            logger.warning(f"Failed to parse response as JSON: {e}")
            # Return the original content if parsing fails
            return content

    async def create_recipe(self, prompt: str) -> Union[dict, str]:
        """Generate a recipe based on the prompt."""
        try:
            messages = [
                {"role": "system", "content": CREATE_RECIPE_SYSTEM_PROMPT},
                {"role": "user", "content": prompt}
            ]

            response = await self.client.chat.complete_async(
                model=MISTRAL_MODEL,
                messages=messages,
            )
            
            content = response.choices[0].message.content
            return self.response_to_json(content)
        except Exception as e:
            logger.error(f"Error generating recipe: {e}")
            return f"Sorry, I encountered an error: {str(e)}"

    async def analyze_conversation(self, conversation: str) -> Union[dict, str]:
        """Analyze the conversation and generate an appropriate response."""
        try:
            # Log the conversation for debugging
            logger.info(f"Analysis response: {conversation}")
            
            messages = [
                {"role": "system", "content": ANALYZE_CONVERSATION_SYSTEM_PROMPT},
                {"role": "user", "content": conversation}
            ]

            response = await self.client.chat.complete_async(
                model=MISTRAL_MODEL,
                messages=messages,
            )
            
            content = response.choices[0].message.content
            return {"message": content}
        except Exception as e:
            logger.error(f"Error analyzing conversation: {e}")
            return f"Sorry, I encountered an error: {str(e)}"
    
    
    