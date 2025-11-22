from typing import Any, Dict
import requests
from src.services.celery_service import celery_app
from src.drivers.analyze.analyze_loader import AnalyzeLoader

@celery_app.task(
    bind=True,
    name="seediq.process_job",
    autoretry_for=(requests.RequestException,), 
    retry_backoff=True,
    retry_kwargs={"max_retries": 3},
)
def process_job(self, payload: Dict[str, Any], callback_url: str, webhook_secret: str) -> Dict[str, Any]:
    error_message = None
    params_ai = None
    result = None

    try:
        seed_category = payload["seed_category"]
        analyzer = AnalyzeLoader.load(seed_category)
        result, params_ai = analyzer.analyze(payload)

        status = "COMPLETED"
        message = "Analysis completed successfully"

    except Exception as e:
        result = None
        status = "FAILED"
        message = f"Analysis failed: {str(e)}"
        error_message = str(e)

    headers = {"Content-Type": "application/json"}
    headers["WEBHOOK-API-KEY"] = webhook_secret

    resp = requests.post(callback_url, json={
        "status": True if status == "COMPLETED" else False,
        "message": message,
        "data": {
            "job_id": self.request.id,
            "status": status,
            "payload": payload,
            "result": result,
            "params_ai": params_ai
        }
    }, headers=headers, timeout=30)
    resp.raise_for_status()

    return {
        "payload": payload,
        "status": status,
        "result": result,
        "params_ai": params_ai ,
        "error": error_message
    }
