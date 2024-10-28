import random
import time
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
import pandas as pd

def clean_text(text):
    """Clean and normalize text content."""
    if not text:
        return ""
    return " ".join(text.strip().split())

def is_valid_url(url):
    """Check if URL is valid."""
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except:
        return False

def normalize_url(base_url, url):
    """Convert relative URL to absolute URL."""
    if not url:
        return None
    if is_valid_url(url):
        return url
    return urljoin(base_url, url)

def parse_table(table):
    """Convert HTML table to pandas DataFrame."""
    try:
        return pd.read_html(str(table))[0]
    except:
        return None

def extract_links(soup, base_url):
    """Extract and normalize all links from BeautifulSoup object."""
    links = []
    for a in soup.find_all('a', href=True):
        href = normalize_url(base_url, a.get('href'))
        if href:
            links.append({
                'text': clean_text(a.get_text()),
                'href': href
            })
    return links
