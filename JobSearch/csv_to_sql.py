import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE IF NOT EXISTS jobs (
    id           INTEGER PRIMARY KEY,
    job_url      TEXT UNIQUE NOT NULL,
    site         TEXT,
    title        TEXT,
    company      TEXT,
    location     TEXT,
    is_remote    INTEGER,
    date_posted  TEXT,
    min_amount   REAL,
    max_amount   REAL,
    description  TEXT,
    query        TEXT,
    first_seen   TEXT DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS decisions (
    id          INTEGER PRIMARY KEY,
    job_id      INTEGER NOT NULL REFERENCES jobs(id),
    decision    TEXT NOT NULL CHECK (decision IN ('applied', 'skipped')),
    reason      TEXT,
    decided_at  TEXT DEFAULT (datetime('now'))
);
"""

COLS = ["job_url", "site", "title", "company", "location", "is_remote",
        "date_posted", "min_amount", "max_amount", "description", "query"]

def get_conn(path="jobs.db"):
    conn = sqlite3.connect(path)
    conn.execute("PRAGMA foreign_keys = ON")   # off by default in SQLite
    conn.executescript(SCHEMA)
    return conn

def clean(v):
    if pd.isna(v):
        return None                      # NaN / NaT -> SQL NULL
    if hasattr(v, "item"):
        v = v.item()                     # numpy scalar -> plain Python
    if hasattr(v, "isoformat"):
        v = v.isoformat()                # date -> "2026-10-20"
    return v

def save_jobs(conn, df):
    rows = [tuple(clean(v) for v in r) for r in df[COLS].itertuples(index=False)]
    sql = f"INSERT OR IGNORE INTO jobs ({', '.join(COLS)}) VALUES ({', '.join('?' * len(COLS))})"
    with conn:
        cur = conn.executemany(sql, rows)
    return cur.rowcount   

if __name__ == "__main__":
    df = pd.read_csv("./JobSearch/outputs/test1_output_file.csv")
    saved_jobs_data = save_jobs(get_conn(), df)
    print(saved_jobs_data)