import sqlite3

DB_PATH = "dependency_checker.db"


def init_db():
    conn = sqlite3.connect(DB_PATH)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS analyses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            package TEXT NOT NULL,
            current_version TEXT,
            target_version TEXT,
            affected BOOLEAN,
            impact TEXT,
            reason TEXT,
            recommendation TEXT
        )
    """)

    conn.commit()
    conn.close()


def save_analysis(result: dict):
    conn = sqlite3.connect(DB_PATH)

    conn.execute("""
        INSERT INTO analyses (
            package,
            current_version,
            target_version,
            affected,
            impact,
            reason,
            recommendation
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        result["package"],
        result["current_version"],
        result["target_version"],
        result["affected"],
        result["impact"],
        result["reason"],
        result["recommendation"],
    ))

    conn.commit()
    conn.close()


def get_analyses():
    conn = sqlite3.connect(DB_PATH)

    rows = conn.execute("""
        SELECT * FROM analyses
        ORDER BY id DESC
    """).fetchall()

    conn.close()
    return rows


if __name__ == "__main__":
    init_db()
    print("Database ready.")