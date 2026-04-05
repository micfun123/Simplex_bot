import sqlite3
import os

def migrate():
    old_server_db = "databases/server_brithdays.db"
    old_user_db = "databases/user_brithdays.db"
    new_db = "databases/birthdays.db"

    if not os.path.exists(old_server_db) and not os.path.exists(old_user_db):
        print("Old databases not found. Skipping migration.")
        return

    print("🚀 Starting birthday database migration...")

    # Connect to new DB
    conn_new = sqlite3.connect(new_db)
    curr_new = conn_new.cursor()

    # Create new tables
    curr_new.execute("""
        CREATE TABLE IF NOT EXISTS guild_config (
            guild_id INTEGER PRIMARY KEY,
            enabled INTEGER DEFAULT 0,
            channel_id INTEGER,
            message TEXT
        )
    """)
    curr_new.execute("""
        CREATE TABLE IF NOT EXISTS user_birthdays (
            user_id INTEGER PRIMARY KEY,
            birthday TEXT
        )
    """)
    conn_new.commit()

    # Migrate Guilds
    if os.path.exists(old_server_db):
        print("📦 Migrating guild configurations...")
        conn_old = sqlite3.connect(old_server_db)
        curr_old = conn_old.cursor()
        try:
            curr_old.execute("SELECT ServerID, Servertoggle, birthdaychannel, birthdaymessage FROM server")
            rows = curr_old.fetchall()
            for row in rows:
                curr_new.execute(
                    "INSERT OR REPLACE INTO guild_config (guild_id, enabled, channel_id, message) VALUES (?, ?, ?, ?)",
                    (row[0], 1 if row[1] else 0, row[2], row[3])
                )
            print(f"✅ Migrated {len(rows)} guilds.")
        except Exception as e:
            print(f"❌ Error migrating guilds: {e}")
        finally:
            conn_old.close()

    # Migrate Users
    if os.path.exists(old_user_db):
        print("👤 Migrating user birthdays...")
        conn_old = sqlite3.connect(old_user_db)
        curr_old = conn_old.cursor()
        try:
            curr_old.execute("SELECT UsersID, birthday FROM birthday")
            rows = curr_old.fetchall()
            for row in rows:
                curr_new.execute(
                    "INSERT OR REPLACE INTO user_birthdays (user_id, birthday) VALUES (?, ?)",
                    (row[0], row[1])
                )
            print(f"✅ Migrated {len(rows)} users.")
        except Exception as e:
            print(f"❌ Error migrating users: {e}")
        finally:
            conn_old.close()

    conn_new.commit()
    conn_new.close()
    print("🎉 Migration complete!")

if __name__ == "__main__":
    migrate()
