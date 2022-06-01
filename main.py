# run with `uvicorn demo_app:app`
import typing
import aioredis
import fastapi
import pydantic
import fastapi_plugins
import uvicorn

# from fastapi_plugins._redis import Other

class OtherSettings(pydantic.BaseSettings):
    other: str = 'other'
    
class AppSettings(OtherSettings, fastapi_plugins.RedisSettings):
    api_name: str = str(__name__)

app = fastapi_plugins.register_middleware(fastapi.FastAPI())
config = AppSettings()
    
@app.get("/")
async def root_get(cache: aioredis.Redis=fastapi.Depends(fastapi_plugins.depends_redis),) -> typing.Dict:
    return dict(ping=await cache.ping())
    
@app.on_event('startup')
async def on_startup() -> None:
    await fastapi_plugins.redis_plugin.init_app(app, config=config)
    await fastapi_plugins.redis_plugin.init()
    
@app.on_event('shutdown')
async def on_shutdown() -> None:
    await fastapi_plugins.redis_plugin.terminate()
    
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)