class ScraperException(Exception):
    """Base exception class for the scrapme package."""
    pass

class RequestException(ScraperException):
    """Exception raised for errors during HTTP requests."""
    pass

class ParsingException(ScraperException):
    """Exception raised for errors during content parsing."""
    pass
