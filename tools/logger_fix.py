import sqlite3

DB_PATH = "databases/log.db"

def column_exists(cursor, table, column):
    cursor.execute(f"PRAGMA table_info({table})")
    return any(col[1] == column for col in cursor.fetchall())

def migrate():
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()

    # Check existing columns
    cur.execute("PRAGMA table_info(log)")
    columns = cur.fetchall()
    column_names = [col[1] for col in columns]

    print(f"Current columns: {column_names}")

    # If log_bot already exists AND GuildID is primary key, do nothing
    has_log_bot = "log_bot" in column_names
    has_pk = any(col[1] == "GuildID" and col[5] == 1 for col in columns)

    if has_log_bot and has_pk:
        print("✅ Table already up to date.")
        con.close()
        return

    print("⚠️ Migrating table...")

    # Create new table with correct schema
    cur.execute("""
        CREATE TABLE log_new (
            GuildID INTEGER PRIMARY KEY,
            ChannelID INTEGER,
            log_bot INTEGER DEFAULT 1
        )
    """)

    # Copy data (handle missing log_bot safely)
    if has_log_bot:
        cur.execute("""
            INSERT INTO log_new (GuildID, ChannelID, log_bot)
            SELECT GuildID, ChannelID, log_bot FROM log
        """)
    else:
        cur.execute("""
            INSERT INTO log_new (GuildID, ChannelID, log_bot)
            SELECT GuildID, ChannelID, 1 FROM log
        """)

    # Replace old table
    cur.execute("DROP TABLE log")
    cur.execute("ALTER TABLE log_new RENAME TO log")

    con.commit()
    con.close()

    print("✅ Migration complete!")

if __name__ == "__main__":
    migrate()