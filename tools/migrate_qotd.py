import sqlite3
import os

OLD_DB = "Old_DB/qotd copy.db"
NEW_DB = "databases/qotd.db"

def migrate():
    if not os.path.exists(OLD_DB):
        print(f"❌ {OLD_DB} not found. Skipping QOTD migration.")
        return

    # Ensure the target directory exists
    os.makedirs(os.path.dirname(NEW_DB), exist_ok=True)

    # Connect to the new database
    new_conn = sqlite3.connect(NEW_DB)
    new_cursor = new_conn.cursor()

    # 1. Create the new table if it doesn't exist
    # Based on cogs/QOTD.py: (server_id INTEGER PRIMARY KEY, channel_id INTEGER, role_id INTEGER)
    new_cursor.execute("""
        CREATE TABLE IF NOT EXISTS qotd (
            server_id INTEGER PRIMARY KEY,
            channel_id INTEGER,
            role_id INTEGER
        )
    """)
    new_conn.commit()

    # 2. Check if role_id column exists (just in case)
    new_cursor.execute("PRAGMA table_info(qotd)")
    columns = [row[1] for row in new_cursor.fetchall()]
    if "role_id" not in columns:
        print("🔹 Adding 'role_id' column to 'qotd' table...")
        new_cursor.execute("ALTER TABLE qotd ADD COLUMN role_id INTEGER")
        new_conn.commit()

    # 3. Migrate data from old database
    try:
        old_conn = sqlite3.connect(OLD_DB)
        old_cursor = old_conn.cursor()
        
        print(f"🔹 Fetching data from {OLD_DB}...")
        old_cursor.execute("SELECT server_id, channel_id FROM qotd")
        rows = old_cursor.fetchall()
        
        migrated_count = 0
        for server_id, channel_id in rows:
            try:
                # Using INSERT OR IGNORE to avoid overwriting existing new data
                # Or use INSERT OR REPLACE if we want the old data to take precedence
                new_cursor.execute("""
                    INSERT OR IGNORE INTO qotd (server_id, channel_id, role_id)
                    VALUES (?, ?, NULL)
                """, (server_id, channel_id))
                migrated_count += 1
            except Exception as e:
                print(f"⚠️ Failed to migrate server {server_id}: {e}")
        
        new_conn.commit()
        old_conn.close()
        print(f"✅ Successfully migrated {migrated_count} QOTD records.")
        
    except Exception as e:
        print(f"❌ Migration error: {e}")
    finally:
        new_conn.close()

    print("🏁 QOTD Migration complete.")

if __name__ == "__main__":
    migrate()
