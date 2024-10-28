import time
from threading import Lock

class RateLimiter:
    """Rate limiter for controlling request frequency."""
    
    def __init__(self, requests_per_second=1.0):
        """
        Initialize rate limiter.
        
        Args:
            requests_per_second (float): Maximum number of requests per second.
        """
        self.delay = 1.0 / float(requests_per_second)
        self.last_request = 0.0
        self.lock = Lock()
    
    def wait(self):
        """Wait for the appropriate delay between requests."""
        with self.lock:
            elapsed = time.time() - self.last_request
            if elapsed < self.delay:
                time.sleep(self.delay - elapsed)
            self.last_request = time.time()
    
    def set_rate(self, requests_per_second):
        """
        Update the rate limit.
        
        Args:
            requests_per_second (float): New maximum number of requests per second.
        """
        with self.lock:
            self.delay = 1.0 / float(requests_per_second)
