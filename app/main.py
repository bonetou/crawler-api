from fastapi import FastAPI
from app.api.routers import crawl, internal


app = FastAPI(
    title="Crawler",
    description="Crawler API",
    version="1.0",
)
app.include_router(crawl.router)
app.include_router(internal.router)
