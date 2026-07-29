"""
Simple planner.
"""


class Planner:

    def create_plan(self, question: str):

        plan = {
            "question": question,
            "requires_download": "http" in question,
            "tool": None
        }

        return plan


planner = Planner()
