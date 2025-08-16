
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))
import re
from typing import List

def clean_text(text: str) -> str:
    """Clean and normalize text by removing extra whitespace and special characters"""
    if not text:
        return ""
    text = re.sub(r'\s+', ' ', text)  # Replace multiple whitespace with single space
    text = text.strip()
    return text

def extract_emails(text: str) -> List[str]:
    """Extract all email addresses from text"""
    email_regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    return re.findall(email_regex, text, re.IGNORECASE)

def extract_phone_numbers(text: str) -> List[str]:
    """Extract phone numbers from text (international formats)"""
    phone_regex = r'(\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b'
    matches = re.finditer(phone_regex, text)
    return [match.group() for match in matches]