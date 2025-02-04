import json
import os
from typing import Dict
from mistralai import Any, Mistral, ChatCompletionResponse

from tomaba.models.recipe import Recipe
from tomaba.prompt import CREATE_RECIPE_SYSTEM_PROMPT

import logging

logger = logging.getLogger("agent")

MISTRAL_MODEL = "mistral-large-latest"


class MistralAgent:
    def __init__(self):
        MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")

        self.client = Mistral(api_key=MISTRAL_API_KEY)

    def response_to_json(self, response: ChatCompletionResponse) -> Dict[str, Any]:
        try:
            content = response.choices[0].message.content
            json_str = content.split("```json")[1].split("```")[0].strip()
            return json.loads(json_str)
        except (json.JSONDecodeError, IndexError, AttributeError):
            raise ValueError("Failed to parse response as JSON")

    async def create_recipe(self, message: str) -> Dict[str, Any]:

        messages = [
            {"role": "system", "content": CREATE_RECIPE_SYSTEM_PROMPT},
            {"role": "user", "content": message},
        ]

        response = await self.client.chat.complete_async(
            model=MISTRAL_MODEL,
            messages=messages,
        )

        logger.info(f"Response: {response.choices[0].message.content}")

        return self.response_to_json(response)
