from app.core.celery_app import celery_app


@celery_app.task(name="crawler.refresh_jobs")
def refresh_jobs_task(platforms: list[str] | None = None) -> dict:
    # TODO: trigger Scrapy spiders and store results
    return {"status": "queued", "platforms": platforms or ["boss", "lagou", "zhilian", "liepin"]}

