from sys import prefix
import psutil
from fastapi import FastAPI
import schedule
from routers import cpu_performance_router
from models.models import database
from fastapi_utils.tasks import repeat_every

from models import models
from schemas import schemas


app = FastAPI()

tags_metadata = [
    {
        "name": "CPU performance",
        "description": "загрузка процесора",
    },

]


app = FastAPI(
    title="Загрузка процесора",
    docs_url=f"/cpu_performance/docs/",
    openapi_url=f"/cpu_performance/openapi.json",
    openapi_tags=tags_metadata,
)

app.include_router(cpu_performance_router)


@app.on_event("startup")
async def startup() -> None:
    # database_ = app.state.database
    # metadata.create_all(engine)
    if not database.is_connected:
        await database.connect()


@app.on_event("startup")
@repeat_every(seconds=5)
async def cpu_task() -> None:
    per = schemas.CpuPerformanceCreate(performance=psutil.cpu_percent())
    await models.CpuPerformance.objects.create(**per.dict())
