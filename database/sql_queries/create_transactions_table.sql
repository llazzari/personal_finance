CREATE TABLE IF NOT EXISTS transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    description TEXT NOT NULL,
    amount REAL NOT NULL,
    year INTEGER NOT NULL,
    month INTEGER NOT NULL,
    bank TEXT NOT NULL
);