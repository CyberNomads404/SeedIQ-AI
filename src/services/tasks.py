from __future__ import annotations

import hmac
import hashlib
import json
import os
import time
from typing import Any, Dict

import requests

from .celery_app import celery_app

def _simulate_business_logic(payload: Dict[str, Any]) -> Dict[str, Any]:
    # TODO: chame aqui sua lógica real (serviços, ML, I/O etc.)
    time.sleep(5)
    return {"echo": payload, "processed_at": time.time()}

def _sign_body(secret: str, body: Dict[str, Any]) -> str:
    msg = json.dumps(body, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    return hmac.new(secret.encode("utf-8"), msg, hashlib.sha256).hexdigest()

@celery_app.task(
    bind=True,
    name="seediq.process_job",
    autoretry_for=(requests.RequestException,),
    retry_backoff=True,
    retry_kwargs={"max_retries": 5},
)
def process_job(self, payload: Dict[str, Any], callback_url: str, webhook_secret: str | None = None) -> Dict[str, Any]:
    result = _simulate_business_logic(payload)

    body = {
        "job_id": self.request.id,
        "status": "success",
        "result": result,
    }

    headers = {"Content-Type": "application/json"}
    if webhook_secret:
        signature = _sign_body(webhook_secret, body)
        # Ajuste o nome do header para casar com seu middlewares/webhook_auth.py
        headers["X-SeedIQ-Signature"] = f"sha256={signature}"

    resp = requests.post(callback_url, json=body, headers=headers, timeout=15)
    resp.raise_for_status()
    return body