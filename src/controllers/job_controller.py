import os
from typing import Any, Dict

from ..services.tasks import process_job
from ..views.http_types.http_response import HttpResponse
from ..views.http_types.http_request import HttpRequest
from ..services.celery_app import celery_app

def enqueue(http_request: HttpRequest) -> HttpResponse:
    body: Dict[str, Any] = http_request.body or {}
    callback_url = body.get("callback_url")
    payload = body.get("payload", {})

    if not callback_url:
        return HttpResponse(status_code=400, body={"error": "callback_url é obrigatório"})

    webhook_secret = os.getenv("WEBHOOK_SEND_TOKEN")

    async_result = process_job.delay(payload, callback_url, webhook_secret)

    return HttpResponse(
        status_code=202,
        body={"job_id": async_result.id, "status": "queued"},
        # headers={"Location": f"/api/jobs/{async_result.id}"},
    )
    
def get_status(http_request: HttpRequest) -> HttpResponse:
    job_id = http_request.query_params.get("job_id")
    
    if not job_id:
        return HttpResponse(status_code=400, body={"error": "job_id é obrigatório"})
    async_result = celery_app.AsyncResult(job_id)
    payload = {"job_id": job_id, "state": async_result.state}
    if async_result.ready():
        payload["result"] = async_result.result
    return HttpResponse(status_code=200, body=payload)