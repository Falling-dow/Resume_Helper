from app.core.celery_app import celery_app


@celery_app.task(name="ai.optimize_resume")
def optimize_resume_task(payload: dict) -> dict:
    # TODO: call optimizer.optimize_resume
    return {"status": "ok", "payload": payload}

