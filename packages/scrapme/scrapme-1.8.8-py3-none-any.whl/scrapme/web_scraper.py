import requests
from bs4 import BeautifulSoup
import pandas as pd
from typing import List, Dict, Optional, Union
from .exceptions import RequestException, ParsingException
from .rate_limiter import RateLimiter
from .utils import clean_text, extract_links, parse_table

class WebScraper:
    def __init__(self, headers=None, requests_per_second=1.0, proxies=None, encoding='utf-8'):
        """
        Initialize WebScraper with custom settings.
        
        Args:
            headers (dict): Custom HTTP headers
            requests_per_second (float): Maximum number of requests per second
            proxies (list): List of proxy servers to rotate through
            encoding (str): Character encoding for responses
        """
        self.headers = headers or {
            'User-Agent': 'Mozilla/5.0 (compatible; ScrapmeBot/1.0; +https://ubix.pro/)'
        }
        self.encoding = encoding
        self.rate_limiter = RateLimiter(requests_per_second)
        self.proxies = proxies or []
        self.current_proxy = 0
        
    def get_soup(self, url: str, method='GET', **kwargs) -> BeautifulSoup:
        """Get BeautifulSoup object from URL."""
        self.rate_limiter.wait()
        
        try:
            if self.proxies:
                kwargs['proxies'] = {'http': self.proxies[self.current_proxy],
                                   'https': self.proxies[self.current_proxy]}
                self.current_proxy = (self.current_proxy + 1) % len(self.proxies)
            
            response = requests.request(method, url, headers=self.headers, **kwargs)
            response.raise_for_status()
            response.encoding = self.encoding
            return BeautifulSoup(response.text, 'html.parser')
        except requests.exceptions.RequestException as e:
            raise RequestException(f"Failed to fetch {url}: {str(e)}")
        except Exception as e:
            raise ParsingException(f"Failed to parse {url}: {str(e)}")
    
    def find_by_selector(self, url: str, selector: str) -> List[BeautifulSoup]:
        """Find elements using CSS selector."""
        soup = self.get_soup(url)
        return soup.select(selector)
    
    def find_by_class(self, url: str, class_name: str) -> List[BeautifulSoup]:
        """Find elements by class name."""
        return self.find_by_selector(url, f".{class_name}")
    
    def find_by_id(self, url: str, id_name: str) -> Optional[BeautifulSoup]:
        """Find element by ID."""
        elements = self.find_by_selector(url, f"#{id_name}")
        return elements[0] if elements else None
    
    def find_by_tag(self, url: str, tag_name: str) -> List[BeautifulSoup]:
        """Find elements by tag name."""
        soup = self.get_soup(url)
        return soup.find_all(tag_name)
    
    def get_text(self, url: str, selector: Optional[str] = None) -> str:
        """Extract clean text content."""
        soup = self.get_soup(url)
        if selector:
            elements = soup.select(selector)
            return " ".join(clean_text(elem.get_text()) for elem in elements)
        return clean_text(soup.get_text())
    
    def get_links(self, url: str, selector: Optional[str] = None) -> List[Dict[str, str]]:
        """Extract links with text and URL."""
        soup = self.get_soup(url)
        if selector:
            soup = BeautifulSoup("".join(str(elem) for elem in soup.select(selector)), 'html.parser')
        return extract_links(soup, url)
    
    def get_tables(self, url: str, selector: Optional[str] = None) -> List[pd.DataFrame]:
        """Extract tables as pandas DataFrames."""
        soup = self.get_soup(url)
        if selector:
            tables = soup.select(selector)
        else:
            tables = soup.find_all('table')
        
        return [df for table in tables if (df := parse_table(table)) is not None]
    
    def set_rate_limit(self, requests_per_second: float):
        """Update rate limiting."""
        self.rate_limiter.set_rate(requests_per_second)
    
    def add_proxy(self, proxy: str):
        """Add new proxy to rotation."""
        if proxy not in self.proxies:
            self.proxies.append(proxy)
