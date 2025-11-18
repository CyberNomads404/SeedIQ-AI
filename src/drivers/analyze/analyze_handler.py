from __future__ import annotations

import hmac
import hashlib
import json
import os
import time
from typing import Any, Dict

import requests

from src.services.celery_service import celery_app

def _simulate_business_logic(payload: Dict[str, Any]) -> Dict[str, Any]:
    time.sleep(10)
    return {
        "good_grains": 126,
        "burned": 17,
        "greenish": 14,
    }

@celery_app.task(
    bind=True,
    name="seediq.process_job",
    autoretry_for=(requests.RequestException,), 
    retry_backoff=True,
    retry_kwargs={"max_retries": 3},
)
def process_job(self, payload: Dict[str, Any], callback_url: str, webhook_secret: str) -> Dict[str, Any]:
    result = _simulate_business_logic(payload)
    
    headers = {"Content-Type": "application/json"}
    headers["WEBHOOK-API-KEY"] = webhook_secret

    resp = requests.post(callback_url, json={
        "status": True,
        "message": "Analysis completed successfully",
        "data": {
            "job_id": self.request.id,
            "status": "COMPLETED",
            "payload": payload,
            "result": result,
        }
    }, headers=headers, timeout=30)
    resp.raise_for_status()
    return {
        "payload": payload,
        "result": result,
    }