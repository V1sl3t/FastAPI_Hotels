from contextlib import asynccontextmanager
import logging
import sys
from pathlib import Path

import uvicorn
from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend

sys.path.append(str(Path(__file__).parent.parent))

logging.basicConfig(level=logging.INFO)

from src.init import redis_manager  # noqa: E402
from src.api.hotels import router as router_hotels  # noqa: E402
from src.api.auth import router as router_auth  # noqa: E402
from src.api.rooms import router as router_rooms  # noqa: E402
from src.api.bookings import router as router_bookings  # noqa: E402
from src.api.comforts import router as router_comforts  # noqa: E402
from src.api.images import router as router_images  # noqa: E402


@asynccontextmanager
async def lifespan(app: FastAPI):
    await redis_manager.connect()
    FastAPICache.init(RedisBackend(redis_manager._redis), prefix="fastapi-cache")
    logging.info("FastAPI cache initialized")
    yield
    await redis_manager.close()


app = FastAPI(lifespan=lifespan)

app.include_router(router_auth)
app.include_router(router_hotels)
app.include_router(router_rooms)
app.include_router(router_bookings)
app.include_router(router_comforts)
app.include_router(router_images)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", reload=True)
