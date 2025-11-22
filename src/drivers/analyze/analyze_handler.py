from typing import Any, Dict
import requests
from src.services.celery_service import celery_app
from src.drivers.analyze.analyze_loader import AnalyzerLoader

@celery_app.task(
    bind=True,
    name="seediq.process_job",
    autoretry_for=(requests.RequestException,), 
    retry_backoff=True,
    retry_kwargs={"max_retries": 3},
)
def process_job(self, payload: Dict[str, Any], callback_url: str, webhook_secret: str) -> Dict[str, Any]:
    try:
        seed_category = payload["seed_category"]
        analyzer = AnalyzerLoader.load(seed_category)
        result = analyzer.analyze(payload)

        status = "COMPLETED"
        message = "Analysis completed successfully"

    except Exception as e:
        result = None
        status = "FAILED"
        message = f"Analysis failed: {str(e)}"

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
        }
    }, headers=headers, timeout=30)
    resp.raise_for_status()

    return {
        "payload": payload,
        "status": status,
        "result": result,
        "error": str(e) if status == "FAILED" else None
    }
