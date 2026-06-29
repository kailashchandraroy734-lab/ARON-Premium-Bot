import aiosqlite
import os

DB_PATH = "data/bot.db"


async def init_db():
    os.makedirs("data", exist_ok=True)

    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
        CREATE TABLE IF NOT EXISTS settings (
            guild_id INTEGER PRIMARY KEY,
            prefix TEXT DEFAULT '!'
        )
        """)

        await db.commit()
