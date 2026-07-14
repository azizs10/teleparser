import aiosqlite

DB_NAME = "bot_database.db"

async def init_db():
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY
            )
        """)
        await db.execute("""
            CREATE TABLE IF NOT EXISTS subscriptions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                url TEXT,
                keyword TEXT,
                FOREIGN KEY(user_id) REFERENCES users(user_id)
            )
        """)
        await db.execute("""
            CREATE TABLE IF NOT EXISTS sent_items (
                key TEXT PRIMARY KEY
            )
        """)
        await db.commit()

async def add_user(user_id: int):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("INSERT OR IGNORE INTO users (user_id) VALUES (?)", (user_id,))
        await db.commit()

async def add_subscription(user_id: int, url: str, keyword: str):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute(
            "INSERT INTO subscriptions (user_id, url, keyword) VALUES (?, ?, ?)",
            (user_id, url, keyword)
        )
        await db.commit()

async def get_subscriptions():
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute("SELECT user_id, url, keyword FROM subscriptions") as cursor:
            return await cursor.fetchall()

async def is_item_sent(item_key: str) -> bool:
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute("SELECT 1 FROM sent_items WHERE key = ?", (item_key,)) as cursor:
            res = await cursor.fetchone()
            return res is not None

async def save_sent_item(item_key: str):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("INSERT OR IGNORE INTO sent_items (key) VALUES (?)", (item_key,))
        await db.commit()