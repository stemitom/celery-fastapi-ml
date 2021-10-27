from fastapi import APIRouter
from fastapi import responses
from fastapi.responses import JSONResponse
from celery.result import AsyncResult
from schema import RequestData, Task, Result
from diabetes.diabs import train


router = APIRouter()

@router.get('/')
def touch(): return "API is currently running"

@router.post("/train", response_model=Task, status_code=202)
async def run_training(requestData:RequestData):
    task_id = train.delay(requestData.partition_size)
    return {
        'task_id': str(task_id),
        'status': 'Processing'
    }

@router.get("/result/{task_id}", response_model=Result, status_code=200, responses={202: {'model': Task}})
async def fetch_result(task_id):
    task = AsyncResult(task_id)
    if not task.ready():
        return JSONResponse(status_code=202, content={'task_id': str(task_id), 'status': 'Processing'})
    result = task.get()
    return {'task_id': task_id, 'status': str(result)}