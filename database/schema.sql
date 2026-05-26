-- SQLite Schema for Poop Journal (v1.0)

-- Enable foreign key support in SQLite (needs to be run per connection, but good to doc here)
PRAGMA foreign_keys = ON;

-- 1. Users Table
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username VARCHAR(80) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 2. Poop Logs Table
CREATE TABLE IF NOT EXISTS poop_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    bristol_type INTEGER NOT NULL CHECK (bristol_type BETWEEN 1 AND 7),
    color VARCHAR(30) NOT NULL,
    odor VARCHAR(30),
    mood VARCHAR(30) NOT NULL,
    note TEXT,
    date_time DATETIME NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- 3. Diet Suggestions Table (Cached/Logged suggestions)
CREATE TABLE IF NOT EXISTS diet_suggestions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    summary VARCHAR(100) NOT NULL,
    content TEXT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);
