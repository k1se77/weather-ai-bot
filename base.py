import aiosqlite

DB = "base.db"
class DataBase:

    async def init_db(self):

        async with aiosqlite.connect(DB) as db:
            await db.execute('CREATE TABLE IF NOT EXISTS users ('
                             'id INTEGER PRIMARY KEY AUTOINCREMENT,'
                             'tg_id INTEGER UNIQUE,'
                             'city TEXT NOT NULL)')
            await db.commit()

    async def save_city(self,city,tg_id):
        async with aiosqlite.connect(DB) as db:

            await db.execute('INSERT OR REPLACE INTO users (city, tg_id) VALUES (?,?)',
                             (city,tg_id))
            await db.commit()

    async def get_city(self,tg_id):
        try:
            async with aiosqlite.connect(DB) as db:
                cursor = await db.execute('SELECT city FROM users WHERE tg_id = ?',
                                          (tg_id,))
                row = await cursor.fetchone()
                return row[0] if row else None
        except:
            return []

    async def get_all_users(self):
        try:
            async with aiosqlite.connect(DB) as db:
                cursor = await db.execute('SELECT tg_id, city FROM users')
                return await cursor.fetchall() if cursor else []
        except:
            return []