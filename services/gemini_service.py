"""
services/gemini_service.py

Gemini API Service
"""

import json
import time
from typing import Any

from google import genai
from google.genai import types

from config import Config
from services.logger import logger


class GeminiService:
    """
    Gemini API wrapper.
    """

    def __init__(self):

        self.client = genai.Client(
            api_key=Config.GEMINI_API_KEY
        )

        self.model = "gemini-2.5-flash"

        self.default_temperature = 0.2

        self.max_retries = 3

    # --------------------------------------------------------
    # Internal API Call
    # --------------------------------------------------------

    def _call_api(
        self,
        prompt: str,
        system_prompt: str | None = None,
        temperature: float | None = None
    ) -> str:

        if temperature is None:
            temperature = self.default_temperature

        config = types.GenerateContentConfig(
            temperature=temperature,
            system_instruction=system_prompt
        )

        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt,
            config=config
        )

        return response.text.strip()

    # --------------------------------------------------------
    # Generate Text
    # --------------------------------------------------------

    async def generate(
        self,
        prompt: str,
        system_prompt: str | None = None,
        temperature: float | None = None
    ) -> str:

        logger.log(
            "gemini_request",
            prompt=prompt
        )

        retries = 0

        while retries < self.max_retries:

            try:

                response = self._call_api(
                    prompt,
                    system_prompt,
                    temperature
                )

                logger.log(
                    "gemini_response",
                    response=response
                )

                return response

            except Exception as e:

                retries += 1

                logger.log(
                    "gemini_retry",
                    retry=retries,
                    error=str(e)
                )

                time.sleep(2)

        raise RuntimeError(
            "Gemini failed after multiple retries."
        )

    # --------------------------------------------------------
    # Generate JSON
    # --------------------------------------------------------

    async def generate_json(
        self,
        prompt: str,
        system_prompt: str | None = None
    ) -> dict[str, Any]:

        response = await self.generate(
            prompt,
            system_prompt
        )

        try:

            return json.loads(response)

        except json.JSONDecodeError:

            logger.log(
                "invalid_json",
                response=response
            )

            raise ValueError(
                "Gemini did not return valid JSON."
            )

    # --------------------------------------------------------
    # Health Check
    # --------------------------------------------------------

    async def health_check(self) -> bool:

        try:

            response = await self.generate(
                "Reply with ONLY the word OK."
            )

            return response.upper() == "OK"

        except Exception:

            return False

    # --------------------------------------------------------
    # Change Model
    # --------------------------------------------------------

    def set_model(self, model_name: str):

        self.model = model_name

    # --------------------------------------------------------
    # Get Current Model
    # --------------------------------------------------------

    def get_model(self):

        return self.model


# Singleton
gemini = GeminiService()
