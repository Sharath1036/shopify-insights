
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))
from fastapi import FastAPI
from routes import insights


app = FastAPI(
    title="Shopify Store Insights Fetcher",
    description="API to extract insights from Shopify stores without using official API",
    version="1.0.0"
)

app.include_router(insights.router, prefix="/api/v1", tags=["insights"])