import os
import aiosqlite
import asyncio

async def create_tables():
    os.makedirs("./databases", exist_ok=True)

    async with aiosqlite.connect("./databases/counting.db") as db:
        # Create counting table
        await db.execute("""
            CREATE TABLE IF NOT EXISTS counting (
                Guild_id INTEGER PRIMARY KEY,
                counting_channel INTEGER,
                lastcounter INTEGER DEFAULT 0,
                last_user INTEGER,
                highest INTEGER DEFAULT 0,
                attempts INTEGER DEFAULT 0
            )
        """)
        # Create user_count_stats table in same DB
        await db.execute("""
            CREATE TABLE IF NOT EXISTS user_count_stats (
                user_id INTEGER NOT NULL,
                guild_id INTEGER NOT NULL,
                success INTEGER DEFAULT 0,
                failed INTEGER DEFAULT 0,
                PRIMARY KEY (user_id, guild_id)
            )
        """)
        await db.commit()

    print("✅ Both tables created in ./databases/counting.db")

if __name__ == "__main__":
    asyncio.run(create_tables())
