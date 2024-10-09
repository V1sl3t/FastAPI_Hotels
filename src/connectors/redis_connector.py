import redis.asyncio as redis


class RedisManager:
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port
        self.redis = None

    async def connect(self):
        self.redis = await redis.Redis(host=self.host, port=self.port)

    async def set(self, key: str, value: str, expire: int = None):
        if expire:
            await self.redis.set(key, value, ex=expire)
        else:
            await self.redis.set(key, value)

    async def get(self, key: str):
        return await self.redis.get(key)

    async def delete(self, key: str):
        await self.redis.delete(key)

    async def close(self):
        if self.redis:
            await self.redis.close()


# Пример использования:
# redis_manager = RedisManager(redis_url="redis://localhost")
# await redis_manager.connect()
# await redis_manager.set("key", "value", expire=60)
# value = await redis_manager.get("key")
# await redis_manager.delete("key")
# await redis_manager.close()