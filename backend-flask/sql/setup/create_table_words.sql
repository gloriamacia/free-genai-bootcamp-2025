CREATE TABLE IF NOT EXISTS words (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  catalan TEXT NOT NULL,
  english TEXT NOT NULL,
  parts TEXT NOT NULL  -- Store parts as JSON string
);