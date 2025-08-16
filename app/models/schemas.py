
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))
from pydantic import BaseModel, HttpUrl
from typing import List, Optional, Dict

class FAQItem(BaseModel):
    question: str
    answer: str

class Product(BaseModel):
    id: str
    title: str
    description: Optional[str]
    price: str
    available: bool
    url: Optional[HttpUrl]
    image_url: Optional[HttpUrl]

class SocialHandle(BaseModel):
    platform: str
    url: HttpUrl
    handle: Optional[str]

class ContactInfo(BaseModel):
    emails: List[str]
    phone_numbers: List[str]
    addresses: List[str]

class BrandInsights(BaseModel):
    store_url: HttpUrl
    product_catalog: List[Product]
    hero_products: List[Product]
    privacy_policy: str
    return_refund_policy: str
    faqs: List[FAQItem]
    social_handles: List[SocialHandle]
    contact_info: ContactInfo
    about_brand: str
    important_links: Dict[str, HttpUrl]
    extracted_at: str
    metadata: Optional[Dict] = {}