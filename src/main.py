from fastapi import FastAPI

app = FastAPI()


@app.post("/crawl")
async def crawl():
    return {"message": "Crawling started"}
