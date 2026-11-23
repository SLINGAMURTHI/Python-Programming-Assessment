"""Q3: Import users (name,email) from CSV into SQLite.
Assumptions: CSV has a header row 'name,email'; email is unique (duplicates skipped)."""
import csv
import sqlite3
import sys

def import_csv(csv_path="users.csv", db_path="users.db"):
    with sqlite3.connect(db_path) as conn:
        conn.execute("""CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE)""")
        with open(csv_path, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            rows = [(r["name"].strip(), r["email"].strip().lower())
                    for r in reader if r.get("name") and r.get("email")]
        before = conn.total_changes
        conn.executemany("INSERT OR IGNORE INTO users (name,email) VALUES (?,?)", rows)
        conn.commit()
        print(f"Read {len(rows)} rows, inserted {conn.total_changes - before}.")
        for row in conn.execute("SELECT * FROM users"):
            print(row)

if __name__ == "__main__":
    import_csv(*(sys.argv[1:3]))