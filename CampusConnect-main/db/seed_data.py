
import sqlite3
from pathlib import Path

# Connect to the CampusConnect database
BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "campusconnect.db"

connection = sqlite3.connect(DB_PATH)
cursor = connection.cursor()

# Add sample internal events
cursor.execute("""
INSERT INTO events (title, location, date)
VALUES
('Campus Welcome Event', 'Student Center', '2026-11-20'),
('Study Group Meeting', 'Library', '2026-11-22')
""")

# Add sample external college events
cursor.execute("""
INSERT INTO external_events (title, date, location, description)
VALUES
('Campus Community Day', '2026-11-25', 'Belmont Abbey College',
 'A campus community gathering for students'),
('Student Activities Fair', '2026-11-28', 'Student Center',
 'Explore student clubs and activities')
""")

# Add sample weather API data
cursor.execute("""
INSERT INTO api_data
(fetched_at, location, temperature, wind_speed, weather_code)
VALUES
(datetime('now'), 'Belmont, NC', 65.0, 5.2, 1)
""")

# Save changes and close the database
connection.commit()
connection.close()

print("CampusConnect database seeded successfully!")
