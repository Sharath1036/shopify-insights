
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(__file__)), 'models'))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(__file__)), 'services'))

from fastapi import APIRouter, HTTPException
from schemas import BrandInsights
from scraper import ShopifyScraper, WebsiteNotFoundError, ScrapingError
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(__file__)), 'llm'))
from structurizer import structurize_website_data

router = APIRouter()

@router.get("/insights")
async def get_shopify_insights(website_url: str):
    try:
        scraper = ShopifyScraper(website_url)
        insights = scraper.get_all_insights()
        # Use LLM to structure the insights
        structured = structurize_website_data(insights.__dict__ if hasattr(insights, '__dict__') else insights)
        return structured
    except WebsiteNotFoundError:
        raise HTTPException(status_code=404, detail="Website not found or inaccessible")
    except ScrapingError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")