from tavily import TavilyClient
from app.core.config import settings


class TavilyAgent:
    """
    Tavily Search Agent
    """

    def __init__(self):
        self.client = TavilyClient(
            api_key=settings.TAVILY_API_KEY
        )

    def search(self, topic: str):

        response = self.client.search(
            query=topic,
            search_depth="advanced",
            max_results=5,
            include_answer=True,
            include_images=False,
            include_raw_content=False,
        )

        return response


tavily_agent = TavilyAgent()