import time
from typing import Dict, Tuple
from fastapi import HTTPException, status
from app.config import settings

class RateLimiter:
    def __init__(self, max_requests: int = 10, window: int = 60):
        self.max_requests = max_requests
        self.window = window
        self.requests: Dict[str, list] = {}  # api_key -> [timestamps]
    
    def check_rate_limit(self, api_key: str) -> Tuple[bool, int]:
        """
        Check if request is within rate limit
        Returns: (is_allowed, remaining_requests)
        """
        current_time = time.time()
        
        if api_key not in self.requests:
            self.requests[api_key] = []
        
        # Remove old requests outside the window
        self.requests[api_key] = [
            ts for ts in self.requests[api_key]
            if current_time - ts < self.window
        ]
        
        request_count = len(self.requests[api_key])
        
        if request_count >= self.max_requests:
            return False, 0
        
        # Record this request
        self.requests[api_key].append(current_time)
        remaining = self.max_requests - (request_count + 1)
        
        return True, remaining
    
    def get_remaining(self, api_key: str) -> int:
        """Get remaining requests for API key"""
        current_time = time.time()
        if api_key not in self.requests:
            return self.max_requests
        
        self.requests[api_key] = [
            ts for ts in self.requests[api_key]
            if current_time - ts < self.window
        ]
        
        return max(0, self.max_requests - len(self.requests[api_key]))

rate_limiter = RateLimiter(
    max_requests=settings.RATE_LIMIT_REQUESTS,
    window=settings.RATE_LIMIT_WINDOW
)

