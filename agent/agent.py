"""
Main AI Agent.
"""

from agent.prompts import SYSTEM_PROMPT
from agent.planner import planner
from agent.executor import executor
from services.gemini_service import gemini
from services.logger import logger


class DataAnalystAgent:

    async def solve(self, question: str):

        logger.log(
            "planning_started",
            question=question
        )

        plan = planner.create_plan(question)

        logger.log(
            "plan_created",
            plan=plan
        )

        answer = await executor.execute(
            question,
            plan,
        )


        logger.log(
            "agent_finished",
            answer=answer
        )

        return answer


agent = DataAnalystAgent()
