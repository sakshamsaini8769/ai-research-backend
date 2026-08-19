import os
from firecrawl import FirecrawlApp


class FirecrawlAgent:
    def __init__(self):
        api_key = os.getenv("FIRECRAWL_API_KEY")

        if not api_key:
            raise ValueError("FIRECRAWL_API_KEY environment variable is not set")

        self.client = FirecrawlApp(api_key=api_key)

    def scrape_url(self, url: str) -> str:
        """
        Scrape a webpage and return its main text content.
        """

        if not url:
            return ""

        try:
            result = self.client.scrape_url(
                url,
                params={
                    "formats": ["markdown"]
                }
            )

            if not result:
                return ""

            # Firecrawl response can contain markdown
            if isinstance(result, dict):
                markdown = result.get("markdown")

                if markdown:
                    return markdown

                # Fallback for older response formats
                data = result.get("data")

                if isinstance(data, dict):
                    return data.get("markdown", "") or data.get("content", "")

                if isinstance(data, str):
                    return data

            return str(result)

        except Exception as e:
            print(f"Firecrawl scraping error: {e}")
            return ""


# Global agent instance
firecrawl_agent = FirecrawlAgent()
