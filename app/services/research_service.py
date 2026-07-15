import json
from pathlib import Path
from datetime import datetime

from app.agents.tavily_agent import tavily_agent

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

        except Exception:

            return []

    # ---------------------------------------
    # Save History
    # ---------------------------------------

    def save_history(
        self,
        topic: str,
        report: str,
    ):

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

    # ---------------------------------------
    # Generate Research
    # ---------------------------------------

    def generate_report(
        self,
        topic: str,
    ):

        search = tavily_agent.search(topic)

        if (
            not search
            or "results" not in search
            or len(search["results"]) == 0
        ):
            raise Exception("No search results found.")

        contents = []

        for item in search["results"][:5]:

            try:

                markdown = firecrawl_agent.scrape(
                    item["url"]
                )

                if markdown:
                    contents.append(
                        markdown[:3000]
                    )

            except Exception:
                continue

        combined = "\n\n".join(contents)

        report = groq_agent.generate_report(
            topic,
            combined,
        )

        self.save_history(
            topic,
            report,
        )

        return report


research_service = ResearchService()