
import os
import sqlite3
import requests
from datetime import datetime
from flask import Blueprint, render_template

api_bp = Blueprint('api', __name__)

DB_PATH = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        '..',
        'db',
        'campusconnect.db'
    )
)

# Belmont Abbey College area weather coordinates.
WEATHER_URL = (
    "https://api.open-meteo.com/v1/forecast"
    "?latitude=35.25&longitude=-81.04"
    "&current=temperature_2m,wind_speed_10m,weather_code"
    "&temperature_unit=fahrenheit&wind_speed_unit=mph"
)


def get_weather():
    # Request current weather from Open-Meteo.
    response = requests.get(WEATHER_URL, timeout=20)
    response.raise_for_status()
    data = response.json()

    current = data["current"]

    temperature = current["temperature_2m"]
    wind_speed = current["wind_speed_10m"]
    weather_code = current["weather_code"]
    fetched_at = current["time"]

    # Save the weather information in SQLite.
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO api_data
        (fetched_at, location, temperature, wind_speed, weather_code)
        VALUES (?, ?, ?, ?, ?)
    """, (
        fetched_at,
        "Belmont, NC",
        temperature,
        wind_speed,
        weather_code
    ))

    conn.commit()
    conn.close()

    return {
        "fetched_at": fetched_at,
        "location": "Belmont, NC",
        "temperature": temperature,
        "wind_speed": wind_speed,
        "weather_code": weather_code
    }


@api_bp.route("/api")
def api():
    try:
        weather = get_weather()
        error = None
    except (requests.RequestException, KeyError, ValueError, sqlite3.Error) as exc:
        weather = None
        error = str(exc)

    return render_template(
        "api.html",
        weather=weather,
        error=error
    )
