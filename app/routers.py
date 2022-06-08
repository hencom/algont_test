from re import M
from tkinter import S
from fastapi import APIRouter
from datetime import datetime, timedelta
from typing import List

from models import models
from schemas import schemas

cpu_performance_router = APIRouter(
    prefix="/cpu_performance",
    tags=["CPU performance"],
)


async def cpu_performance_all(cpu_performance_obj: models.CpuPerformance, time_interval: int) -> schemas.CpuPerformanceAll:
    delta = timedelta(seconds=time_interval)
    average_performance = await models.CpuPerformance.objects.filter(
        date_time__gt=cpu_performance_obj.date_time - delta).filter(date_time__lte=cpu_performance_obj.date_time).avg('performance')
    result = schemas.CpuPerformanceAll(
        **cpu_performance_obj.dict(), average_performance=round(average_performance, 1))
    return result


@cpu_performance_router.get("/root", response_model=List[schemas.CpuPerformanceAll])
async def root(time_interval: int = 60, averaging_time: int = 60):
    result = []
    delta = timedelta(minutes=time_interval)
    # db_obj_count = await models.CpuPerformance.objects.count()
    # ofset = db_obj_count-count
    # if ofset < 0:
    #     db_obj_list = await models.CpuPerformance.objects.offset(0).limit(db_obj_count).all()
    # else:
    #     db_obj_list = await models.CpuPerformance.objects.offset(ofset).limit(count).all()
    # time_1 = db_obj_list[0].date_time
    # print((db_obj_list[1].date_time - db_obj_list[0].date_time).seconds)
    db_obj_list = await models.CpuPerformance.objects.filter(
        date_time__gt=datetime.now() - delta).all()
    time_1 = db_obj_list[0].date_time
    for db_obj in db_obj_list:
        time_delta = db_obj.date_time - time_1

        time_1 = db_obj.date_time
        if time_delta.seconds > 5:
            s = schemas.CpuPerformanceAll(
                id=-1, performance=-1, average_performance=-1)
            result.append(s)
        else:
            result.append(await cpu_performance_all(
                cpu_performance_obj=db_obj, time_interval=averaging_time))

    return result


@cpu_performance_router.get("/root/{id}", response_model=schemas.CpuPerformanceAll)
async def root(id: int, time_interval: int = 60):
    db_obj = await models.CpuPerformance.objects.get(id=id)
    return await cpu_performance_all(cpu_performance_obj=db_obj, time_interval=time_interval)


@cpu_performance_router.post("/root", response_model=schemas.CpuPerformance)
async def root(schema: schemas.CpuPerformanceCreate):
    return await models.CpuPerformance.objects.create(**schema.dict())
