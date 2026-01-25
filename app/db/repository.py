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
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()


def get_messages(limit=50, offset=0, from_filter=None, since=None, q=None):
    conn = get_connection()
    cursor = conn.cursor()

    where_clauses = []
    params = []

    if from_filter:
        where_clauses.append("from_msisdn = ?")
        params.append(from_filter)

    if since:
        where_clauses.append("ts >= ?")
        params.append(since)

    if q:
        where_clauses.append("text LIKE ?")
        params.append(f"%{q}%")

    where_sql = ""
    if where_clauses:
        where_sql = "WHERE " + " AND ".join(where_clauses)

    cursor.execute(f"SELECT COUNT(*) FROM messages {where_sql}", params)
    total = cursor.fetchone()[0]

    cursor.execute(
        f"""
        SELECT message_id, from_msisdn, to_msisdn, ts, text
        FROM messages
        {where_sql}
        ORDER BY ts ASC, message_id ASC
        LIMIT ? OFFSET ?
        """,
        params + [limit, offset],
    )

    rows = cursor.fetchall()
    conn.close()

    return [
        {"message_id": r[0], "from": r[1], "to": r[2], "ts": r[3], "text": r[4]}
        for r in rows
    ], total

def get_stats():
    conn = get_connection()
    cursor = conn.cursor()

    # total messages
    cursor.execute("SELECT COUNT(*) FROM messages")
    total_messages = cursor.fetchone()[0]

    # unique senders
    cursor.execute("SELECT COUNT(DISTINCT from_msisdn) FROM messages")
    senders_count = cursor.fetchone()[0]

    # messages per sender (top 10)
    cursor.execute("""
        SELECT from_msisdn, COUNT(*) 
        FROM messages 
        GROUP BY from_msisdn 
        ORDER BY COUNT(*) DESC 
        LIMIT 10
    """)
    messages_per_sender = [
        {"from": row[0], "count": row[1]}
        for row in cursor.fetchall()
    ]

    # first and last timestamps
    cursor.execute("SELECT MIN(ts), MAX(ts) FROM messages")
    first_ts, last_ts = cursor.fetchone()

    conn.close()

    return {
        "total_messages": total_messages,
        "senders_count": senders_count,
        "messages_per_sender": messages_per_sender,
        "first_message_ts": first_ts,
        "last_message_ts": last_ts,
    }
