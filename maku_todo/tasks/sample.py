from maku_todo.celery_app import celery_app

@celery_app.task(bind=True, autoretry_for=(Exception,), retry_kwargs={"max_retries": 3, "countdown": 5})
def sample(self, email: str):
    # later: real SMTP / SendGrid
    print(f"📧 Sending welcome email to {email}")

    # simulate failure if you want to test retries
    # raise Exception("SMTP down")

    return {"status": "sent", "email": email}