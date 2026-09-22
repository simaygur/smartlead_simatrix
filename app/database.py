import sqlite3
from pathlib import Path

from flask import current_app, g


def get_db():
    if "db" not in g:
        database_path = current_app.config["DATABASE_URL"]

        if database_path != ":memory:":
            Path(database_path).expanduser().parent.mkdir(parents=True, exist_ok=True)

        g.db = sqlite3.connect(database_path)
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    db = g.pop("db", None)

    if db is not None:
        db.close()


def init_db(app):
    with app.app_context():
        db = get_db()

        db.execute("""
            CREATE TABLE IF NOT EXISTS leads (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                isim TEXT NOT NULL,
                telefon TEXT NOT NULL,
                eposta TEXT,
                tarih TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        kolonlar = {
            kolon["name"]
            for kolon in db.execute("PRAGMA table_info(leads)").fetchall()
        }

        if "eposta" not in kolonlar:
            db.execute("ALTER TABLE leads ADD COLUMN eposta TEXT")

        if "mesaj" in kolonlar:
            db.execute("ALTER TABLE leads DROP COLUMN mesaj")

        db.commit()

    app.teardown_appcontext(close_db)


def lead_ekle(isim, telefon, eposta=None):
    db = get_db()

    db.execute(
        "INSERT INTO leads (isim, telefon, eposta) VALUES (?, ?, ?)",
        (isim, telefon, eposta)
    )

    db.commit()


def tum_leadler():
    db = get_db()

    kayitlar = db.execute(
        "SELECT * FROM leads ORDER BY tarih DESC"
    ).fetchall()

    return [dict(kayit) for kayit in kayitlar]
