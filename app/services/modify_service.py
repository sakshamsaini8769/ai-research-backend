from app.agents.groq_agent import groq_agent


class ModifyService:
    """
    AI Report Editing Service
    """

    def modify_report(
        self,
        report: str,
        instruction: str,
    ) -> str:

        prompt = f"""
You are an expert AI Research Editor.

Modify the research report according to the user's instruction.

Rules:

- Preserve factual accuracy.
- Keep markdown formatting.
- Improve readability.
- Return ONLY the updated report.

--------------------------------------------------

USER INSTRUCTION

{instruction}

--------------------------------------------------

CURRENT REPORT

{report}

--------------------------------------------------

UPDATED REPORT
"""

        return groq_agent.chat(
            prompt=prompt,
            temperature=0.4,
            max_tokens=3500,
        )


modify_service = ModifyService()