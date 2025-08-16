
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

class WebsiteNotFoundError(Exception):
    """Raised when the website cannot be accessed or doesn't exist"""
    pass

class ScrapingError(Exception):
    """Raised when there's an error during the scraping process"""
    pass