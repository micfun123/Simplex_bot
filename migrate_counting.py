import sqlite3
import aiosqlite
import os
from pathlib import Path

async def migrate_counting_data():
    # Paths to database files
    old_counting_db = Path("./databases/counting.db")
    old_user_stats_db = Path("./databases/user_count_stats.db")
    backup_dir = Path("./databases/backups")
    
    # Create backup directory if it doesn't exist
    backup_dir.mkdir(exist_ok=True)
    
    # Step 1: Backup old databases
    print("Creating backups...")
    if old_counting_db.exists():
        old_counting_db.rename(backup_dir / "counting.db.old")
    if old_user_stats_db.exists():
        old_user_stats_db.rename(backup_dir / "user_count_stats.db.old")
    
    # Step 2: Create new databases with proper schema
    print("Creating new databases...")
    async with aiosqlite.connect("./databases/counting.db") as db:
        await db.execute("""
            CREATE TABLE counting (
                Guild_id INTEGER PRIMARY KEY,
                counting_channel INTEGER,
                lastcounter INTEGER DEFAULT 0,
                last_user INTEGER,
                highest INTEGER DEFAULT 0,
                attempts INTEGER DEFAULT 0
            )
        """)
        await db.commit()
    
    async with aiosqlite.connect("./databases/user_count_stats.db") as db:
        await db.execute("""
            CREATE TABLE user_count_stats (
                user_id INTEGER NOT NULL,
                guild_id INTEGER NOT NULL,
                success INTEGER DEFAULT 0,
                failed INTEGER DEFAULT 0,
                PRIMARY KEY (user_id, guild_id)
            )
        """)
        await db.commit()
    
    # Step 3: Migrate counting data if old db exists
    old_counting_path = backup_dir / "counting.db.old"
    if old_counting_path.exists():
        print("Migrating counting data...")
        # Connect to old SQLite database (synchronous)
        old_conn = sqlite3.connect(old_counting_path)
        old_cursor = old_conn.cursor()
        
        # Get all data from old counting table
        old_cursor.execute("SELECT * FROM counting")
        old_data = old_cursor.fetchall()
        
        # Migrate to new database
        async with aiosqlite.connect("./databases/counting.db") as new_db:
            for row in old_data:
                # Handle different old schema formats
                if len(row) >= 6:  # Newer schema
                    guild_id, channel, last_num, last_user, highest, attempts = row[:6]
                elif len(row) == 4:  # Older schema
                    guild_id, channel, last_num, last_user = row
                    highest = last_num if last_num > 0 else 0
                    attempts = 0
                else:
                    continue
                
                await new_db.execute(
                    "INSERT INTO counting VALUES (?, ?, ?, ?, ?, ?)",
                    (guild_id, channel, last_num or 0, last_user, highest or 0, attempts or 0)
                )
            await new_db.commit()
        old_conn.close()
    
    # Step 4: Migrate user stats if old db exists
    old_user_stats_path = backup_dir / "user_count_stats.db.old"
    if old_user_stats_path.exists():
        print("Migrating user stats data...")
        old_conn = sqlite3.connect(old_user_stats_path)
        old_cursor = old_conn.cursor()
        
        # Try to get data from old table (might have different schema)
        try:
            old_cursor.execute("SELECT * FROM user_count_stats")
            old_stats = old_cursor.fetchall()
            
            async with aiosqlite.connect("./databases/user_count_stats.db") as new_db:
                for row in old_stats:
                    if len(row) >= 4:  # Full record
                        user_id, guild_id, success, failed = row[:4]
                    elif len(row) == 2:  # Just user/guild IDs
                        user_id, guild_id = row
                        success, failed = 0, 0
                    else:
                        continue
                    
                    await new_db.execute(
                        "INSERT INTO user_count_stats VALUES (?, ?, ?, ?)",
                        (user_id, guild_id, success or 0, failed or 0)
                    )
                await new_db.commit()
        except sqlite3.OperationalError as e:
            print(f"Couldn't migrate user stats: {e}")
        finally:
            old_conn.close()
    
    print("Migration complete!")
    print(f"Old databases backed up to: {backup_dir}")

# Run the migration
if __name__ == "__main__":
    import asyncio
    asyncio.run(migrate_counting_data())