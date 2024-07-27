from fastapi import FastAPI, Depends, HTTPException, Header
from pydantic import BaseModel
import os
from scraper import Scraper
from cache import Cache
from utils import authenticate
from typing import Optional

app = FastAPI()

DATA_FILE = "scraped_data.json"
CACHE_FILE = "cache.json"

class ScrapeSettings(BaseModel):
    pages: int
    proxy: Optional[str] = None

cache = Cache(CACHE_FILE)

@app.post("/scrape", dependencies=[Depends(authenticate)])
async def scrape_data(settings: ScrapeSettings):
    scraper = Scraper(settings.pages, settings.proxy, cache)
    scraped_products = scraper.scrape()
    scraper.save_data(DATA_FILE)
    scraper.notify()
    return {"scraped_products": [product.dict() for product in scraped_products], "message": f"Scraped {len(scraped_products)} products"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
