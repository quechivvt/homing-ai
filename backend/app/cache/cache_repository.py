from typing import TypeVar
from pydantic import BaseModel
from redis.asyncio import Redis
import logging

logger = logging.getLogger(__name__)

T = TypeVar("T", bound=BaseModel)


class CacheRepository:

    def __init__(self, redis: Redis):
        self.redis = redis

    async def get(
        self,
        key: str,
        model: type[T],
    ) -> T | None:
        try:
            cached = await self.redis.get(key)

            if cached is None:
                logger.info("❌ Cache MISS | %s", key)
                return None

            logger.info("✅ Cache HIT | %s", key)  

            return model.model_validate_json(cached)
        except Exception as ex:
            logger.error("[CACHE] Redis unavailable: %s", ex)
            return None

    async def set(
        self,
        key: str,
        value: BaseModel,
        ttl: int = 600,
    ) -> None:
        try:
            await self.redis.set(
                key,
                value.model_dump_json(),
                ex=ttl,
            )

            logger.info("💾 Cache SET | %s | TTL=%ss", key, ttl)
        except Exception as ex:
            logger.error("[CACHE] Redis unavailable: %s", ex)


    async def delete(
        self,
        *keys: str,
    ) -> None:
        try:
            if keys:
                await self.redis.delete(*keys)

                logger.info("🗑️ Cache DELETE | %s", ", ".join(keys))
        except Exception as ex:
            logger.error("[CACHE] Redis unavailable: %s", ex)

        

    async def delete_pattern(
        self,
        pattern: str,
    ) -> None:

        cursor = 0
        deleted = 0
        try:

            while True:

                cursor, keys = await self.redis.scan(
                    cursor=cursor,
                    match=pattern,
                    count=100,
                )

                if keys:
                    await self.redis.delete(*keys)
                    deleted += len(keys)

                if cursor == 0:
                    break

            logger.info(
                "🧹 Cache DELETE PATTERN | %s | deleted=%d",
                pattern,
                deleted,
            )
        except Exception as ex:
            logger.error("[CACHE] Redis unavailable: %s", ex)