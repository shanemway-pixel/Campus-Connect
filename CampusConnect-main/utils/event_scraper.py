
import requests
from bs4 import BeautifulSoup
import sqlite3
from pathlib import Path
from datetime import datetime
import re


class CampusEventScraper:

    def __init__(self, url):
        self.url = url
        self.db_path = (
            Path(__file__).resolve().parent.parent
            / "db"
            / "campusconnect.db"
        )

    # Download the basketball schedule.
    def get_page(self):
        response = requests.get(
            self.url,
            headers={"User-Agent": "Mozilla/5.0"},
            timeout=20
        )
        response.raise_for_status()
        return BeautifulSoup(response.text, "html.parser")

    # Extract basketball games.
    def scrape_events(self):
        soup = self.get_page()
        events = []

        game_rows = soup.select(".sidearm-schedule-game")

        print("Game rows found:", len(game_rows))

        for row in game_rows:
            text = row.get_text(" ", strip=True)

            details = re.search(
                r"Hide/Show Additional Information For (.+?) - "
                r"([A-Za-z]+ \d{1,2}, \d{4})",
                text,
                re.IGNORECASE
            )

            if details:
                opponent = details.group(1).strip()
                date_text = details.group(2)
            else:
                date_match = re.search(
                    r"([A-Z][a-z]{2} \d{1,2}).*?"
                    r"(?:vs\.?|at)\s+(.+?)(?:Box Score|Recap|Watch Live|$)",
                    text,
                    re.IGNORECASE
                )

                if not date_match:
                    continue

                opponent = date_match.group(2).strip()
                date_text = date_match.group(1) + " 2026"

            # Remove extra website text from opponent names.
            opponent = re.sub(
                r"\s+(History|Watch Live Stats|Box Score|Recap).*$",
                "",
                opponent,
                flags=re.IGNORECASE
            ).strip()

            try:
                parsed_date = datetime.strptime(
                    date_text, "%B %d, %Y"
                )
            except ValueError:
                try:
                    parsed_date = datetime.strptime(
                        date_text, "%b %d %Y"
                    )
                except ValueError:
                    continue

            # January through February belong to 2027.
            if parsed_date.month <= 2:
                parsed_date = parsed_date.replace(year=2027)

            event_date = parsed_date.strftime("%Y-%m-%d")

            time_match = re.search(
                r"\d{1,2}(?::\d{2})?\s*p\.m\.",
                text
            )

            game_time = (
                time_match.group(0)
                if time_match else "Time TBD"
            )

            is_away = re.search(
                r"\bat\s+" + re.escape(opponent),
                text,
                re.IGNORECASE
            )

            if is_away:
                location = f"Away - {opponent}"
                matchup = f"at {opponent}"
            else:
                location = "Belmont Abbey College"
                matchup = f"vs. {opponent}"

            events.append({
                "title": f"Men's Basketball {matchup}",
                "date": event_date,
                "location": location,
                "description": (
                    f"Belmont Abbey men's basketball game at {game_time}."
                )
            })

        print("Games extracted:", len(events))
        return events

    # Save games into SQLite.
    def save_events(self, events):
        if not events:
            print("No games found. Existing records were kept.")
            return

        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()

        cursor.execute("DELETE FROM external_events")

        for event in events:
            cursor.execute("""
                INSERT INTO external_events
                (title, date, location, description)
                VALUES (?, ?, ?, ?)
            """, (
                event["title"],
                event["date"],
                event["location"],
                event["description"]
            ))

        connection.commit()
        connection.close()

        print(f"Saved {len(events)} games to the database.")

    # Run the scraper.
    def run(self):
        events = self.scrape_events()
        self.save_events(events)
        return events




