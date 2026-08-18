import json
from pathlib import Path
from datetime import datetime

from app.agents.tavily_agent import tavily_agent
from app.agents.firecrawl_agent import firecrawl_agent
from app.agents.groq_agent import groq_agent


HISTORY_FILE = Path(__file__).resolve().parents[2] / "history.json"


class ResearchService:

    # ---------------------------------------
    # Load History
    # ---------------------------------------

    def load_history(self):

        if not HISTORY_FILE.exists():
            return []

        try:
            with open(
                HISTORY_FILE,
                "r",
                encoding="utf-8",
            ) as file:
                return json.load(file)

        except Exception as e:
            print(f"History load error: {e}")
            return []

    # ---------------------------------------
    # Save History
    # ---------------------------------------

    def save_history(
        self,
        topic: str,
        report: str,
    ):

        try:
            history = self.load_history()

            history.insert(
                0,
                {
                    "topic": topic,
                    "report": report,
                    "date": datetime.now().strftime(
                        "%d-%m-%Y %I:%M %p"
                    ),
                },
            )

            with open(
                HISTORY_FILE,
                "w",
                encoding="utf-8",
            ) as file:

                json.dump(
                    history,
                    file,
                    indent=4,
                    ensure_ascii=False,
                )

        except Exception as e:
            print(f"History save error: {e}")

    # ---------------------------------------
    # Delete History
    # ---------------------------------------

    def delete_history(
        self,
        index: int,
    ):

        history = self.load_history()

        if index < 0 or index >= len(history):
            return False

        history.pop(index)

        try:

            with open(
                HISTORY_FILE,
                "w",
                encoding="utf-8",
            ) as file:

                json.dump(
                    history,
                    file,
                    indent=4,
                    ensure_ascii=False,
                )

            return True

        except Exception as e:

            print(f"History delete error: {e}")
            return False

    # ---------------------------------------
    # Generate Research
    # ---------------------------------------

    def generate_report(
        self,
        topic: str,
    ):

        print(f"Starting research for: {topic}")

        # -----------------------------------
        # Step 1: Tavily Search
        # -----------------------------------

        try:

            search = tavily_agent.search(topic)

            print("Tavily search completed.")

        except Exception as e:

            print(f"Tavily error: {e}")

            raise Exception(
                f"Tavily search failed: {str(e)}"
            )

        if (
            not search
            or "results" not in search
            or not search["results"]
        ):

            raise Exception(
                "No search results found."
            )

        # -----------------------------------
        # Step 2: Firecrawl Scraping
        # -----------------------------------

        contents = []

        for item in search["results"][:5]:

            url = item.get("url")

            if not url:
                continue

            try:

                print(f"Scraping: {url}")

                markdown = firecrawl_agent.scrape(url)

                if markdown:

                    contents.append(
                        markdown[:3000]
                    )

                    print(
                        "Firecrawl scrape successful."
                    )

            except Exception as e:

                print(
                    f"Firecrawl failed for {url}: {e}"
                )

                continue

        # -----------------------------------
        # Fallback to Tavily content
        # -----------------------------------

        if not contents:

            print(
                "Firecrawl returned no content. "
                "Using Tavily results as fallback."
            )

            for item in search["results"][:5]:

                content = item.get(
                    "content",
                    ""
                )

                if content:

                    contents.append(
                        content[:3000]
                    )

        if not contents:

            raise Exception(
                "Unable to collect research content "
                "from Tavily or Firecrawl."
            )

        # -----------------------------------
        # Step 3: Combine Research
        # -----------------------------------

        combined = "\n\n".join(contents)

        print(
            f"Collected research content: "
            f"{len(combined)} characters"
        )

        # -----------------------------------
        # Step 4: Groq Report Generation
        # -----------------------------------

        try:

            print("Generating report with Groq...")

            report = groq_agent.generate_report(
                topic,
                combined,
            )

            print("Groq report generated.")

        except Exception as e:

            print(f"Groq error: {e}")

            raise Exception(
                f"Groq report generation failed: {str(e)}"
            )

        if not report:

            raise Exception(
                "Groq returned an empty report."
            )

        # -----------------------------------
        # Step 5: Save History
        # -----------------------------------

        self.save_history(
            topic,
            report,
        )

        print("Research completed successfully.")

        return report


research_service = ResearchService()
        
