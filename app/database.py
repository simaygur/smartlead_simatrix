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
                isim NVARCHAR(150) NOT NULL,
                telefon NVARCHAR(20) NOT NULL,
                eposta NVARCHAR(150) NOT NULL,
                tarih TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        kolonlar = {
            kolon["name"]: kolon
            for kolon in db.execute("PRAGMA table_info(leads)").fetchall()
        }

        beklenen_tipler = {
            "isim": "NVARCHAR(150)",
            "telefon": "NVARCHAR(20)",
            "eposta": "NVARCHAR(150)"
        }

        migration_gerekli = (
            "mesaj" in kolonlar
            or "eposta" not in kolonlar
            or any(
                kolonlar[alan]["type"].upper() != beklenen_tip
                for alan, beklenen_tip in beklenen_tipler.items()
                if alan in kolonlar
            )
            or ("eposta" in kolonlar and not kolonlar["eposta"]["notnull"])
        )

        if migration_gerekli:
            eposta_degeri = (
                "COALESCE(eposta, '')" if "eposta" in kolonlar else "''"
            )

            db.execute("""
                CREATE TABLE leads_yeni (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    isim NVARCHAR(150) NOT NULL,
                    telefon NVARCHAR(20) NOT NULL,
                    eposta NVARCHAR(150) NOT NULL,
                    tarih TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            db.execute(f"""
                INSERT INTO leads_yeni (id, isim, telefon, eposta, tarih)
                SELECT id, isim, telefon, {eposta_degeri}, tarih
                FROM leads
            """)

            db.execute("DROP TABLE leads")
            db.execute("ALTER TABLE leads_yeni RENAME TO leads")

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
