import os
from typing import Any, Dict

from ..drivers.analyze.analyze_handler import process_job
from ..views.http_types.http_request import HttpRequest
from ..services.celery_app import celery_app

class AnalyzeController:
    def enqueue(self, http_request: HttpRequest) -> Dict[str, Any]:
        body = http_request.body
        payload = body.get("payload")
        callback_url = body.get("callback_url")
        webhook_secret = os.getenv("WEBHOOK_SEND_TOKEN")
        async_result = process_job.delay(payload, callback_url, webhook_secret)

        return {
            "job_id": async_result.id,
            "status": "QUEUED",
            "external_id": payload.get("external_id"),
        }
        
    def get_status(self, http_request: HttpRequest) -> Dict[str, Any]:
        job_id = http_request.path_params.get("job_id")
        
        async_result = celery_app.AsyncResult(job_id)
        
        payload = {
            "job_id": job_id, 
            "status": async_result.state,
            "payload": None,
            "result": None,
        }
        
        if async_result.ready():
            res = async_result.result
            if async_result.successful():
                payload["payload"] = res.get("payload", payload["payload"])
                payload["result"] = res.get("result", payload["result"])
                payload["status"] = "COMPLETED"
            else:
                payload["result"] = str(res)
                payload["status"] = "FAILED"
            
        return payload