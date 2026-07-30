"""
executor.py

Main execution pipeline.
"""

import agent.memory as memory

from agent.parser import Parser
from agent.formatter import Formatter

from services.search_service import SearchService
from services.gemini_service import gemini

from tools.downloader import downloader
from tools.loader_factory import LoaderFactory
from tools.dataframe import DataFrameTool


class Executor:

    def __init__(self):

        self.parser = Parser()

        self.search = SearchService()

        self.loader = LoaderFactory()

        self.dataframe = DataFrameTool()

        self.formatter = Formatter()

        self.operations = {
            "mean": self.dataframe.mean,
            "median": self.dataframe.median,
            "sum": self.dataframe.sum,
            "count": self.dataframe.count,
            "max": self.dataframe.maximum,
            "min": self.dataframe.minimum,
        }

    async def execute(
        self,
        chat_id: int,
        question: str
    ):

        try:

            # -------------------------------------
            # Save conversation
            # -------------------------------------

            memory.add_message(
                chat_id,
                "user",
                question
            )

            # -------------------------------------
            # Parse question
            # -------------------------------------

            task = self.parser.parse(question)

            memory.save_task(chat_id, task)

            # -------------------------------------
            # Load dataframe from memory
            # -------------------------------------

            dataframe = memory.get_dataframe(chat_id)

            # -------------------------------------
            # Download dataset from URL
            # -------------------------------------

            if task.url:

                filepath = downloader.download(task.url)

                memory.save_file(
                    chat_id,
                    str(filepath)
                )

                dataframe = self.loader.load(filepath)

                memory.save_dataframe(
                    chat_id,
                    dataframe
                )

            # -------------------------------------
            # Search dataset if no dataframe exists
            # -------------------------------------

            elif dataframe is None:

                result = self.search.search(question)

                if result["url"]:

                    filepath = downloader.download(
                        result["url"]
                    )

                    memory.save_file(
                        chat_id,
                        str(filepath)
                    )

                    dataframe = self.loader.load(filepath)

                    memory.save_dataframe(
                        chat_id,
                        dataframe
                    )

            # -------------------------------------
            # No dataframe available
            # -------------------------------------

            if dataframe is None:

                if task.requires_llm:

                    answer = await gemini.generate(
                        question
                    )

                    memory.add_message(
                        chat_id,
                        "assistant",
                        answer
                    )

                    return self.formatter.success(
                        {
                            "answer": answer
                        }
                    )

                return self.formatter.error(
                    "No dataset available."
                )

            # -------------------------------------
            # Execute dataframe operation
            # -------------------------------------

            if task.operation is None:

                return self.formatter.error(
                    "No operation detected."
                )

            func = self.operations.get(
                task.operation
            )

            if func is None:

                return self.formatter.error(
                    f"Unsupported operation: {task.operation}"
                )

            # count() has different signature
            if task.operation == "count":

                result = func(dataframe)

            else:

                if task.column is None:

                    return self.formatter.error(
                        "No target column detected."
                    )

                result = func(
                    dataframe,
                    task.column
                )

            memory.add_message(
                chat_id,
                "assistant",
                str(result)
            )

            return self.formatter.success(result)

        except Exception as e:

            return self.formatter.error(
                str(e)
            )
