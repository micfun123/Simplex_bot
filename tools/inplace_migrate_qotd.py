import sqlite3
import os

DB_PATH = "databases/qotd.db"

def migrate():
    if not os.path.exists(DB_PATH):
        print(f"❌ {DB_PATH} not found. Running setup.py first is recommended.")
        return

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # 1. Check if server_id is already a PRIMARY KEY
    cursor.execute("PRAGMA table_info(qotd)")
    columns = cursor.fetchall()
    # row[5] is the pk flag in PRAGMA table_info
    is_pk = any(row[1] == "server_id" and row[5] == 1 for row in columns)
    
    if is_pk:
        print("ℹ️ 'server_id' is already a PRIMARY KEY. No structural changes needed.")
    else:
        print("🔹 Updating 'qotd' table schema to make 'server_id' a PRIMARY KEY...")
        try:
            # Create a temporary table with the correct schema
            cursor.execute("""
                CREATE TABLE qotd_new (
                    server_id INTEGER PRIMARY KEY,
                    channel_id INTEGER,
                    role_id INTEGER
                )
            """)
            
            # Copy data from old table to new table, deduplicating by server_id
            cursor.execute("""
                INSERT INTO qotd_new (server_id, channel_id, role_id) 
                SELECT server_id, channel_id, role_id 
                FROM qotd 
                GROUP BY server_id
            """)
            
            # Drop old table and rename new one
            cursor.execute("DROP TABLE qotd")
            cursor.execute("ALTER TABLE qotd_new RENAME TO qotd")
            
            conn.commit()
            print("✅ 'qotd' table updated successfully.")
        except Exception as e:
            print(f"❌ Migration failed: {e}")
            conn.rollback()

    # 2. Final check for role_id column (just in case it was missing entirely)
    cursor.execute("PRAGMA table_info(qotd)")
    column_names = [row[1] for row in cursor.fetchall()]
    if "role_id" not in column_names:
        print("🔹 Adding missing 'role_id' column...")
        cursor.execute("ALTER TABLE qotd ADD COLUMN role_id INTEGER")
        conn.commit()
        print("✅ Added 'role_id' column.")

    conn.close()
    print("🏁 In-place QOTD migration complete.")

if __name__ == "__main__":
    migrate()
