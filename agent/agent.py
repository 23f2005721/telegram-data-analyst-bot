"""
agent.py

Thin orchestrator between the Telegram handler
and the executor.
"""

from agent.executor import Executor


class Agent:

    def __init__(self):
        self.executor = Executor()

    async def solve(
        self,
        chat_id: int,
        question: str
    ):
        """
        Execute a user question.
        """

        return await self.executor.execute(
            chat_id=chat_id,
            question=question
        )


# Singleton
agent = Agent()
