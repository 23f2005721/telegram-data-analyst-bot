"""
agent/executor.py

Executes the plan created by the planner.
"""

from __future__ import annotations

import re
from pathlib import Path

from services.gemini_service import gemini
from services.logger import logger

from tools.downloader import downloader
from tools.csv_tool import csv_tool

from agent.prompts import SYSTEM_PROMPT


class Executor:

    URL_PATTERN = r"https?://[^\s]+"

    # ---------------------------------------------------------
    # Execute
    # ---------------------------------------------------------

    async def execute(
        self,
        question: str,
        plan: dict,
    ) -> str:

        logger.log(
            "executor_started",
            question=question
        )

        url = self.extract_url(question)

        # ------------------------------
        # Pure reasoning
        # ------------------------------

        if url is None:

            logger.log(
                "reasoning_only"
            )

            return await gemini.generate(
                prompt=question,
                system_prompt=SYSTEM_PROMPT,
            )

        # ------------------------------
        # Download
        # ------------------------------

        path = downloader.download(url)

        file_type = downloader.file_type(path)

        logger.log(
            "file_detected",
            file_type=file_type,
            path=str(path)
        )

        # ------------------------------
        # CSV
        # ------------------------------

        if file_type == "csv":

            df = csv_tool.read(path)

            summary = csv_tool.info(df)

            prompt = f"""
Dataset Information

{summary}

User Question

{question}

Answer the user's question using the dataset information.
"""

            return await gemini.generate(
                prompt=prompt,
                system_prompt=SYSTEM_PROMPT,
            )

        # ------------------------------
        # Unsupported
        # ------------------------------

        return (
            f"Unsupported file type: {file_type}"
        )

    # ---------------------------------------------------------
    # Extract URL
    # ---------------------------------------------------------

    def extract_url(
        self,
        text: str,
    ) -> str | None:

        match = re.search(
            self.URL_PATTERN,
            text,
        )

        if match:
            return match.group()

        return None


executor = Executor()
