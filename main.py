from celery.result import AsyncResult

from fastapi import FastAPI
from fastapi.responses import JSONResponse
from worker import start_task
from pydantic import BaseModel
from fastapi.staticfiles import StaticFiles

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")


class RequestBody(BaseModel):
    prompt: str
    speaker_index: int
    output_file_name: str


@app.post("api/generate", status_code=201)
def run_task(request_body: RequestBody):
    task = start_task.delay(
        request_body.prompt, request_body.speaker_index, request_body.output_file_name)
    return JSONResponse({"task_id": task.id})


@app.get("api/tasks/{task_id}")
def get_status(task_id):
    task_result = AsyncResult(task_id)
    if task_result.failed():
        return JSONResponse({
            "task_id": task_id,
            "task_status": task_result.state,
            "exception": task_result.result.args[0]
        })
    result = {
        "task_id": task_id,
        "task_status": task_result.state,
        "task_result": task_result.result
    }
    return JSONResponse(result)
