import sqlite3
import os

DB_PATH = "databases/counting.db"
# Potential stats database locations
OLD_STATS_LOCATIONS = ["Old_DB/user_count_stats.db", "databases/user_count_stats.db"]
# Potential old counting database location
OLD_COUNTING_DB = "Old_DB/counting.db"

def migrate():
    if not os.path.exists(DB_PATH):
        print(f"❌ {DB_PATH} not found. Run setup.py first or ensure the database exists.")
        return

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # 1. Ensure 'channel_id' exists in 'counting' table
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

    # 2. Migrate server settings from old counting DB if available
    if os.path.exists(OLD_COUNTING_DB):
        print(f"🔹 Found old counting database at {OLD_COUNTING_DB}. Migrating settings...")
        try:
            old_c_conn = sqlite3.connect(OLD_COUNTING_DB)
            old_c_cursor = old_c_conn.cursor()
            
            # Check old schema - using guild_id based on schema check
            old_c_cursor.execute("SELECT guild_id, channel_id FROM counting")
            old_settings = old_c_cursor.fetchall()
            
            for guild_id, channel_id in old_settings:
                cursor.execute("""
                    INSERT OR IGNORE INTO counting (guild_id, channel_id, current_number, last_user_id, highest_number)
                    VALUES (?, ?, 0, NULL, 0)
                """, (guild_id, channel_id))
            
            conn.commit()
            old_c_conn.close()
            print(f"✅ Migrated {len(old_settings)} server settings.")
        except Exception as e:
            print(f"⚠️ Failed to migrate settings from {OLD_COUNTING_DB}: {e}")

    # 3. Migrate user stats from Old_DB if available
    stats_db_path = None
    for loc in OLD_STATS_LOCATIONS:
        if os.path.exists(loc):
            stats_db_path = loc
            break

    if stats_db_path:
        print(f"🔹 Found stats database at {stats_db_path}. Migrating user stats...")
        try:
            old_conn = sqlite3.connect(stats_db_path)
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
        print(f"ℹ️ user_count_stats.db not found in {OLD_STATS_LOCATIONS}, skipping stats migration.")

    conn.close()
    print("🏁 Migration complete.")

if __name__ == "__main__":
    migrate()

