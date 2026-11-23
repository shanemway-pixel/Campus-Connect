
import os
import sqlite3
import requests
from flask import Blueprint, render_template
from utils.event_scraper import CampusEventScraper

event_bp = Blueprint('event', __name__)

DB_PATH = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        '..',
        'db',
        'campusconnect.db'
    )
)

# Belmont Abbey men's basketball schedule
EVENTS_URL = "https://abbeyathletics.com/sports/mens-basketball/schedule"


@event_bp.route("/events")
def events():

    # Scrape the basketball schedule and save games.
    try:
        scraper = CampusEventScraper(EVENTS_URL)
        scraped_events = scraper.run()
        print(f"Scraped {len(scraped_events)} basketball games.")

    except requests.RequestException as error:
        print(f"Schedule scraping error: {error}")

    except Exception as error:
        print(f"Unexpected error: {error}")

    # Get internal campus events.
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(
        "SELECT title, location, date FROM events"
    )
    internal_events = cursor.fetchall()

    # Get scraped basketball games.
    cursor.execute("""
        SELECT title, location, date, description
        FROM external_events
    """)
    external_events = cursor.fetchall()

    conn.close()

    return render_template(
        "events.html",
        internal_events=internal_events,
        external_events=external_events
    )

