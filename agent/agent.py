"""
Main AI Agent.
"""

from agent.prompts import SYSTEM_PROMPT
from agent.planner import planner

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

        answer = await gemini.generate(
            prompt=question,
            system_prompt=SYSTEM_PROMPT
        )

        logger.log(
            "agent_finished",
            answer=answer
        )

        return answer


agent = DataAnalystAgent()
