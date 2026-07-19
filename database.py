import sqlite3
conn = sqlite3.connect('developer.db')
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS developers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    name TEXT,
    bio TEXT,
    skills TEXT,
    interests TEXT,
    location TEXT,
    followers INTEGER,
    following INTEGER,
    public_repos INTEGER,
    avatar TEXT,
    github_url TEXT,
    language TEXT
)
""")
conn.commit()
conn.close()
