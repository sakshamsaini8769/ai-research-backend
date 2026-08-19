import os
from firecrawl import Firecrawl


class FirecrawlAgent:
    def __init__(self):
        api_key = os.getenv("FIRECRAWL_API_KEY")

        if not api_key:
            raise ValueError(
                "FIRECRAWL_API_KEY environment variable is not set"
            )

        self.client = Firecrawl(api_key=api_key)

    def scrape_url(self, url: str) -> str:
        if not url:
            return ""

        try:
            result = self.client.scrape(
                url,
                formats=["markdown"]
            )

            if result is None:
                return ""

            # Current Firecrawl SDK returns a document object
            markdown = getattr(result, "markdown", None)

            if markdown:
                return markdown

            # Fallback if response is dictionary-like
            if isinstance(result, dict):
                return (
                    result.get("markdown")
                    or result.get("content")
                    or ""
                )

            return str(result)

        except Exception as e:
            print(f"Firecrawl scraping error: {e}")
            return ""


firecrawl_agent = FirecrawlAgent()
