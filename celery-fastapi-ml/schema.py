from pydantic import BaseModel

class RequestData(BaseModel):
    partition_size: float

class Task(BaseModel):
    task_id: str
    status: str

class Result(BaseModel):
    task_id: str
    status: str
    