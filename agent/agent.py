"""
Agent entry point.
"""

from agent.executor import Executor


class Agent:

    def __init__(self):

        self.executor = Executor()

    async def handle(self, question: str):

        return await self.executor.execute(question)
