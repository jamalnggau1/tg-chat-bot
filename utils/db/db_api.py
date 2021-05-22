import asyncio

import aiosqlite

from data.config import PATH as path


class DB:

    _connection = None

    def __init__(self):
        loop = asyncio.get_event_loop()
        self._connection = loop.run_until_complete(aiosqlite.connect(path).__aenter__())

    async def execute_query(self, query):
        await self._connection.execute(query)
        await self._connection.commit()

    async def execute_all_query(self, query):
        cursor = await self._connection.execute(query)
        rows = await cursor.fetchall()
        await cursor.close()
        return rows

    async def execute_one_query(self, query):
        cursor = await self._connection.execute(query)
        row = await cursor.fetchone()
        await cursor.close()
        if row != None and len(row) == 1:
            return row[0]
        return row


__all__ = [
    "DB",
]
