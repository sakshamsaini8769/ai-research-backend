from groq import Groq
from app.core.config import settings


class GroqAgent:
    """
    Handles all AI interactions using Groq.
    """

    def __init__(self):
        self.client = Groq(
            api_key=settings.GROQ_API_KEY
        )

        self.model = "llama-3.3-70b-versatile"

    # -------------------------------------------------
    # Generic Chat
    # -------------------------------------------------

    def chat(
        self,
        prompt: str,
        temperature: float = 0.4,
        max_tokens: int = 4096,
    ) -> str:

        response = self.client.chat.completions.create(
            model=self.model,
            temperature=temperature,
            max_tokens=max_tokens,
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
        )

        return response.choices[0].message.content.strip()

    # -------------------------------------------------
    # Research Report
    # -------------------------------------------------

    def generate_report(
        self,
        topic: str,
        content: str,
    ) -> str:

        prompt = f"""
You are an expert AI Research Assistant.

Write a professional research report.

Topic:
{topic}

Reference Material:
{content}

Requirements:

- Professional English
- Markdown Formatting
- Clear Headings
- Detailed Explanation
- Bullet Points
- Conclusion

Report Structure:

# Introduction

# Background

# Key Concepts

# Applications

# Advantages

# Challenges

# Future Scope

# Conclusion

Return ONLY the report.
"""

        return self.chat(
            prompt=prompt,
            temperature=0.3,
            max_tokens=3500,
        )


groq_agent = GroqAgent()