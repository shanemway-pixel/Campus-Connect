
-- SQLite database schema for CampusConnect

-- Create users table
DROP TABLE IF EXISTS users;
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    preferences TEXT
);

-- Create original internal events table
DROP TABLE IF EXISTS events;
CREATE TABLE events (
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    location TEXT,
    date TEXT
);

-- Store scraped Belmont Abbey College events
DROP TABLE IF EXISTS external_events;
CREATE TABLE external_events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    date TEXT,
    location TEXT,
    description TEXT
);

-- Store weather information from Open-Meteo API
DROP TABLE IF EXISTS api_data;
CREATE TABLE api_data (
    api_id INTEGER PRIMARY KEY AUTOINCREMENT,
    fetched_at TEXT,
    location TEXT,
    temperature REAL,
    wind_speed REAL,
    weather_code INTEGER
);
