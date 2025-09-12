from app.core.celery_app import celery_app


@celery_app.task(name="email.send_verification")
def send_verification_email_task(email: str, token: str) -> dict:
    # TODO: implement actual email sending
    return {"sent": True, "email": email}

