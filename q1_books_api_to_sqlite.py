"""Q1: Fetch books from a REST API, store in SQLite, display.
Assumption: Open Library search API (public, no key) stands in for "the books API".
Fields used: title, author_name[0], first_publish_year."""
import sqlite3
import requests

API_URL = "https://openlibrary.org/search.json"
DB_PATH = "books.db"

def fetch_books(query="python", limit=20):
    r = requests.get(API_URL, params={"q": query, "limit": limit,
                     "fields": "title,author_name,first_publish_year"}, timeout=15)
    r.raise_for_status()
    return r.json().get("docs", [])

def init_db(conn):
    conn.execute("""CREATE TABLE IF NOT EXISTS books (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        author TEXT,
        publication_year INTEGER,
        UNIQUE(title, author))""")

def store_books(conn, docs):
    rows = [(d.get("title"), (d.get("author_name") or ["Unknown"])[0],
             d.get("first_publish_year")) for d in docs if d.get("title")]
    conn.executemany(
        "INSERT OR IGNORE INTO books (title, author, publication_year) VALUES (?,?,?)", rows)
    conn.commit()

def display_books(conn):
    print(f"{'ID':<4}{'Title':<50}{'Author':<30}{'Year'}")
    print("-" * 94)
    for i, t, a, y in conn.execute("SELECT id,title,author,publication_year FROM books"):
        print(f"{i:<4}{t[:48]:<50}{a[:28]:<30}{y or 'N/A'}")

if __name__ == "__main__":
    with sqlite3.connect(DB_PATH) as conn:
        init_db(conn)
        store_books(conn, fetch_books())
        display_books(conn)