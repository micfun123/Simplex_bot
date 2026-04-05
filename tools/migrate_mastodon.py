import sqlite3
import os

def migrate():
    db_path = "databases/mastodon.db"
    if not os.path.exists(db_path):
        print("Mastodon database not found. Skipping migration.")
        return

    print("🚀 Starting Mastodon database migration...")
    conn = sqlite3.connect(db_path)
    curr = conn.cursor()

    # Create new table with better schema
    curr.execute("""
        CREATE TABLE IF NOT EXISTS mastodon_new (
            channel_id INTEGER,
            guild_id INTEGER,
            username TEXT,
            instance TEXT DEFAULT 'mastodon.social',
            mastodon_user_id TEXT,
            last_posted TEXT,
            PRIMARY KEY (channel_id, username, instance)
        )
    """)

    # Migrate data
    curr.execute("SELECT channel_id, guild_id, username, last_posted FROM mastodon")
    rows = curr_old = curr.fetchall()
    
    for row in rows:
        # Default to mastodon.social for old entries
        curr.execute("""
            INSERT OR IGNORE INTO mastodon_new (channel_id, guild_id, username, instance, last_posted)
            VALUES (?, ?, ?, ?, ?)
        """, (row[0], row[1], row[2], 'mastodon.social', row[3]))

    curr.execute("DROP TABLE mastodon")
    curr.execute("ALTER TABLE mastodon_new RENAME TO mastodon")
    
    conn.commit()
    conn.close()
    print("🎉 Mastodon migration complete!")

if __name__ == "__main__":
    migrate()
