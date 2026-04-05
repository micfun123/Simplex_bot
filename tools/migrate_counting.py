import sqlite3
import os

DB_PATH = "databases/counting.db"
OLD_STATS_DB = "Old_DB/user_count_stats.db"

def migrate():
    if not os.path.exists(DB_PATH):
        print(f"❌ {DB_PATH} not found. Run setup.py first or ensure the database exists.")
        return

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # 1. Check if 'channel_id' exists in 'counting' table
    cursor.execute("PRAGMA table_info(counting)")
    columns = [row[1] for row in cursor.fetchall()]
    
    if "channel_id" not in columns:
        print("🔹 Adding 'channel_id' column to 'counting' table...")
        try:
            cursor.execute("ALTER TABLE counting ADD COLUMN channel_id INTEGER")
            conn.commit()
            print("✅ Added 'channel_id' column.")
        except Exception as e:
            print(f"❌ Failed to add 'channel_id': {e}")
    else:
        print("ℹ️ 'channel_id' already exists in 'counting' table.")

    # 2. Migrate user stats from Old_DB if available
    if os.path.exists(OLD_STATS_DB):
        print(f"🔹 Migrating stats from {OLD_STATS_DB}...")
        try:
            old_conn = sqlite3.connect(OLD_STATS_DB)
            old_cursor = old_conn.cursor()
            
            old_cursor.execute("SELECT user_id, guild_id, failed, success FROM user_count_stats")
            old_rows = old_cursor.fetchall()
            
            for user_id, guild_id, failed, success in old_rows:
                # Insert or Update in new user_counts table
                cursor.execute("""
                    INSERT INTO user_counts (guild_id, user_id, count, failures)
                    VALUES (?, ?, ?, ?)
                    ON CONFLICT(guild_id, user_id) DO UPDATE SET
                        count = count + EXCLUDED.count,
                        failures = failures + EXCLUDED.failures
                """, (guild_id, user_id, success, failed))
            
            conn.commit()
            old_conn.close()
            print(f"✅ Migrated {len(old_rows)} user stats records.")
        except Exception as e:
            print(f"❌ Failed to migrate user stats: {e}")
    else:
        print(f"ℹ️ {OLD_STATS_DB} not found, skipping user stats migration.")

    conn.close()
    print("🏁 Migration complete.")

if __name__ == "__main__":
    migrate()
