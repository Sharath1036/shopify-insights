
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(__file__)), 'models'))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(__file__)), 'utils'))
import json
import re
from typing import Optional, Dict, List
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from datetime import datetime
from schemas import BrandInsights, Product, FAQItem, SocialHandle, ContactInfo
from exceptions import WebsiteNotFoundError, ScrapingError
from helpers import clean_text, extract_emails, extract_phone_numbers

class ShopifyScraper:
    def __init__(self, website_url: str):
        self.base_url = website_url
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        
    def fetch_website_content(self, url_suffix: str = "") -> Optional[BeautifulSoup]:
        try:
            url = urljoin(self.base_url, url_suffix)
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            return BeautifulSoup(response.text, 'html.parser')
        except requests.exceptions.RequestException as e:
            raise WebsiteNotFoundError(f"Failed to fetch website: {str(e)}")

    def get_products_json(self) -> List[Dict]:
        try:
            products_url = urljoin(self.base_url, "/products.json")
            response = self.session.get(products_url, timeout=10)
            response.raise_for_status()
            return response.json().get('products', [])
        except (requests.exceptions.RequestException, json.JSONDecodeError):
            return []

    def extract_product_catalog(self) -> List[Product]:
        products_data = self.get_products_json()
        products = []
        
        for product in products_data:
            products.append(Product(
                id=str(product.get('id', '')),
                title=product.get('title', ''),
                description=clean_text(product.get('body_html', '')),
                price=self._get_product_price(product),
                available=product.get('available', False),
                url=urljoin(self.base_url, f"/products/{product.get('handle', '')}"),
                image_url=self._get_product_image(product)
            ))
        
        return products

    def _get_product_price(self, product: Dict) -> str:
        variants = product.get('variants', [{}])
        if variants:
            return f"{variants[0].get('price', '0')} {variants[0].get('currency', '')}"
        return "0"

    def _get_product_image(self, product: Dict) -> Optional[str]:
        images = product.get('images', [])
        if images:
            return images[0].get('src')
        return None

    def extract_hero_products(self) -> List[Product]:
        soup = self.fetch_website_content()
        if not soup:
            return []
            
        hero_products = []
        # Common patterns for hero products
        selectors = [
            '.hero__product', 
            '.featured-product', 
            '.product-slider__slide',
            'section[data-section-type="featured-product"]'
        ]
        
        for selector in selectors:
            elements = soup.select(selector)
            for element in elements:
                try:
                    title = element.select_one('.product-title, .product__title').get_text(strip=True)
                    price = element.select_one('.product-price, .price__regular').get_text(strip=True)
                    url = element.find('a', href=True)['href']
                    if not url.startswith('http'):
                        url = urljoin(self.base_url, url)
                    
                    hero_products.append(Product(
                        id='hero-' + re.sub(r'\W+', '-', title.lower()),
                        title=title,
                        description='',
                        price=price,
                        available=True,
                        url=url,
                        image_url=self._get_hero_product_image(element)
                    ))
                except (AttributeError, KeyError):
                    continue
        
        return hero_products

    def _get_hero_product_image(self, element) -> Optional[str]:
        img = element.find('img', src=True)
        if img:
            src = img['src']
            if src.startswith('//'):
                return f"https:{src}"
            elif not src.startswith('http'):
                return urljoin(self.base_url, src)
            return src
        return None



    def get_all_insights(self) -> BrandInsights:
        try:
            product_catalog = self.extract_product_catalog()
            hero_products = self.extract_hero_products()
            # Scrape the main page for all info
            soup = self.fetch_website_content()
            text = soup.get_text() if soup else ""
            # Extract emails and phone numbers from the main page
            emails = list(set(extract_emails(text)))
            phone_numbers = list(set(extract_phone_numbers(text)))
            # Try to find addresses in the main page
            addresses = []
            if soup:
                address_elements = soup.select('.footer-address, .contact-address, address')
                for elem in address_elements:
                    address = clean_text(elem.get_text())
                    if address and len(address.split()) > 3:
                        addresses.append(address)
            # Extract social links from the main page
            social_links = []
            platforms = {
                'facebook.com': 'facebook',
                'twitter.com': 'twitter',
                'instagram.com': 'instagram',
                'pinterest.com': 'pinterest',
                'tiktok.com': 'tiktok',
                'youtube.com': 'youtube'
            }
            if soup:
                for a in soup.find_all('a', href=True):
                    href = a['href'].lower()
                    for domain, platform in platforms.items():
                        if domain in href:
                            social_links.append(SocialHandle(
                                platform=platform,
                                url=href,
                                handle=None
                            ))
                            break
            # Extract FAQs from the main page
            faqs = []
            if soup:
                items = soup.select('.faq-item, .accordion__item')
                for item in items:
                    try:
                        question = item.select_one('.faq-question, .accordion__title').get_text(strip=True)
                        answer = item.select_one('.faq-answer, .accordion__content').get_text(strip=True)
                        faqs.append(FAQItem(question=question, answer=answer))
                    except AttributeError:
                        continue
                headings = soup.select('h3, h4')
                for heading in headings:
                    question = heading.get_text(strip=True)
                    answer = []
                    next_sib = heading.next_sibling
                    while next_sib and getattr(next_sib, 'name', None) not in ['h3', 'h4']:
                        if getattr(next_sib, 'name', None) == 'p':
                            answer.append(next_sib.get_text(strip=True))
                        next_sib = next_sib.next_sibling
                    if question and answer:
                        faqs.append(FAQItem(
                            question=question,
                            answer=' '.join(answer)
                        ))
            # About brand: try to get from main page content blocks
            about_brand = ""
            if soup:
                about_blocks = soup.select('.about-content, .about, .about-us, .rte, .page-content')
                for block in about_blocks:
                    text_block = clean_text(block.get_text())
                    if text_block and len(text_block.split()) > 10:
                        about_brand = text_block
                        break
            # Important links: collect all footer links, only http/https
            important_links = {}
            if soup:
                footer = soup.find('footer')
                if footer:
                    for a in footer.find_all('a', href=True):
                        text_link = clean_text(a.get_text())
                        if text_link and len(text_link) > 2:
                            href = a['href']
                            if not href.startswith('http') and not href.startswith('https'):
                                # skip mailto:, tel:, javascript:, etc.
                                continue
                            important_links[text_link.lower().replace(' ', '_')] = href
            return BrandInsights(
                store_url=self.base_url,
                product_catalog=product_catalog,
                hero_products=hero_products,
                privacy_policy="",  # Not scraping specific policy pages
                return_refund_policy="",  # Not scraping specific policy pages
                faqs=faqs,
                social_handles=social_links,
                contact_info=ContactInfo(emails=emails, phone_numbers=phone_numbers, addresses=addresses),
                about_brand=about_brand,
                important_links=important_links,
                extracted_at=datetime.utcnow().isoformat()
            )
        except Exception as e:
            raise ScrapingError(f"Error while scraping website: {str(e)}")