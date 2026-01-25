from app.db.models import get_connection
from datetime import datetime
import sqlite3


def insert_message(msg):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            """
            INSERT INTO messages (message_id, from_msisdn, to_msisdn, ts, text, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                msg.message_id,
                msg.from_,
                msg.to,
                msg.ts,
                msg.text,
                datetime.utcnow().isoformat() + "Z",
            ),
        )
        conn.commit()
        return True  # inserted
    except sqlite3.IntegrityError:
        return False  # duplicate
    finally:
        conn.close()
