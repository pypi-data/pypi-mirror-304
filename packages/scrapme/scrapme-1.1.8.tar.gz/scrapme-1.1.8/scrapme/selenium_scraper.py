from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from bs4 import BeautifulSoup
import time
from typing import Optional, Any
from .exceptions import RequestException, ParsingException
from .utils import clean_text
from .driver_manager import DriverManager

class SeleniumScraper:
    def __init__(self, headless=True, encoding='utf-8'):
        """
        Initialize Selenium-based scraper.
        
        Args:
            headless (bool): Run browser in headless mode
            encoding (str): Character encoding for responses
        """
        self.encoding = encoding
        options = Options()
        if headless:
            options.add_argument('-headless')
        
        try:
            # Get geckodriver path using DriverManager
            driver_path = DriverManager.setup_driver()
            service = Service(executable_path=driver_path)
            self.driver = webdriver.Firefox(options=options, service=service)
        except Exception as e:
            raise RequestException(f"Failed to initialize Firefox driver: {str(e)}")
    
    def __del__(self):
        """Clean up resources."""
        if hasattr(self, 'driver'):
            self.driver.quit()
    
    def get_soup(self, url: str, wait_for: Optional[str] = None, wait_type: str = 'presence') -> BeautifulSoup:
        """
        Get page content after JavaScript rendering.
        
        Args:
            url (str): Target URL
            wait_for (str): CSS selector to wait for
            wait_type (str): Type of wait condition ('presence' or 'visibility')
        """
        try:
            self.driver.get(url)
            
            if wait_for:
                wait = WebDriverWait(self.driver, 10)
                if wait_type == 'visibility':
                    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, wait_for)))
                else:
                    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, wait_for)))
            
            return BeautifulSoup(self.driver.page_source, 'html.parser')
        except Exception as e:
            raise RequestException(f"Failed to load {url}: {str(e)}")
    
    def execute_script(self, script: str) -> Any:
        """Execute JavaScript code."""
        try:
            return self.driver.execute_script(script)
        except Exception as e:
            raise ParsingException(f"Failed to execute script: {str(e)}")
    
    def scroll_to_bottom(self):
        """Scroll page to bottom."""
        self.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)  # Wait for content to load
    
    def scroll_infinite(self, max_scrolls: int = 5):
        """
        Handle infinite scrolling pages.
        
        Args:
            max_scrolls (int): Maximum number of scroll attempts
        """
        last_height = self.execute_script("return document.body.scrollHeight")
        scrolls = 0
        
        while scrolls < max_scrolls:
            self.scroll_to_bottom()
            new_height = self.execute_script("return document.body.scrollHeight")
            
            if new_height == last_height:
                break
                
            last_height = new_height
            scrolls += 1
            time.sleep(1)  # Wait for content to load
    
    def get_text(self, url: str, selector: Optional[str] = None) -> str:
        """Extract text from JavaScript-rendered page."""
        soup = self.get_soup(url, wait_for=selector)
        if selector:
            elements = soup.select(selector)
            return " ".join(clean_text(elem.get_text()) for elem in elements)
        return clean_text(soup.get_text())
