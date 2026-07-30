"""
executor.py

Main execution pipeline.

Responsibilities:
- Parse question
- Restore memory
- Search/download dataset
- Load dataset
- Execute dataframe operations
- Use Gemini only when required
- Format final JSON response
"""

from pathlib import Path

from agent.parser import Parser
from agent.formatter import Formatter
from agent.memory import Memory

from services.search_service import SearchService
from services.gemini_service import GeminiService

from tools.downloader import Downloader
from tools.loader_factory import LoaderFactory
from tools.dataframe import DataFrameTool


class Executor:

    def __init__(self):

        self.parser = Parser()
        self.memory = Memory()

        self.search = SearchService()

        self.downloader = Downloader()
        self.loader = LoaderFactory()

        self.dataframe = DataFrameTool()

        self.gemini = GeminiService()

        self.formatter = Formatter()

    async def execute(self, question: str):

        try:

            # -----------------------------
            # Parse Question
            # -----------------------------

            task = self.parser.parse(question)

            # -----------------------------
            # Recover previous dataset
            # -----------------------------

            dataframe = self.memory.get_dataframe()

            # -----------------------------
            # Download dataset if URL exists
            # -----------------------------

            if task.url:

                filepath = await self.downloader.download(task.url)

                dataframe = self.loader.load(filepath)

                self.memory.save_dataframe(dataframe)

            # -----------------------------
            # Search dataset if needed
            # -----------------------------

            elif dataframe is None:

                result = self.search.search(question)

                if result["url"]:

                    filepath = await self.downloader.download(
                        result["url"]
                    )

                    dataframe = self.loader.load(filepath)

                    self.memory.save_dataframe(dataframe)

            # -----------------------------
            # Still no dataframe
            # -----------------------------

            if dataframe is None:

                if task.requires_llm:

                    answer = await self.gemini.generate(question)

                    return self.formatter.success(
                        {
                            "answer": answer
                        }
                    )

                return self.formatter.error(
                    "No dataset available."
                )

            # -----------------------------
            # Execute dataframe operation
            # -----------------------------

            result = self.run_dataframe_operation(
                dataframe,
                task
            )

            return self.formatter.success(result)

        except Exception as e:

            return self.formatter.error(str(e))

    def run_dataframe_operation(self, df, task):

        operation = task.operation

        if operation == "mean":
            return self.dataframe.mean(df, task.column)

        if operation == "median":
            return self.dataframe.median(df, task.column)

        if operation == "sum":
            return self.dataframe.sum(df, task.column)

        if operation == "count":
            return self.dataframe.count(df)

        if operation == "max":
            return self.dataframe.maximum(df, task.column)

        if operation == "min":
            return self.dataframe.minimum(df, task.column)

        raise ValueError(
            f"Unsupported operation: {operation}"
        )
