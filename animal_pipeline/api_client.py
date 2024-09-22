import requests
import time
from functools import wraps
from animal_pipeline.logger import Logger


logging = Logger()


def retry_api_call(max_retries=10, initial_backoff=5):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            retries = 0
            backoff = initial_backoff
            while retries <= max_retries:
                try:
                    response = func(*args, **kwargs)
                    # Only 2xx is accepted,
                    # According to problem statement only 5xx response is expected ocassionally
                    # but sometimes RateLimitter gives 429 response 
                    if not (200 <= response.status_code < 300):
                        raise requests.exceptions.RequestException(f"API call error status_code: {response.status_code}", response=response)
                    return response.json()
                except requests.exceptions.RequestException as e:
                    # retry exponentially for any error apart from 2xx
                    if hasattr(e, 'response') and hasattr(e.response, 'status_code'):
                        if not (200 <= e.response.status_code < 300):
                            retries += 1
                            if retries > max_retries:
                                raise
                            logging.error(f"Received non-2xx error: {e.response.status_code}. Retrying in {backoff} seconds...")
                            time.sleep(backoff)
                            backoff *= 2  # exponential retry seconds
                        else:
                            raise 
                    else:
                        logging.error(f"Received exception: {e}. Retrying in {backoff} seconds...")      
        return wrapper
    return decorator


class APIClient:
    def __init__(self, base_url):
        if not base_url:
            raise ValueError("base_url required for APIClient")
        self.base_url = base_url
        self.logger = None
        
    @retry_api_call(max_retries=10, initial_backoff=5)
    def get(self, endpoint):
        url = f"{self.base_url}/{endpoint}"
        # print(url)
        response = requests.get(url)
        response.raise_for_status()
        return response
    
    @retry_api_call(max_retries=10, initial_backoff=5)
    def post(self, endpoint, data):
        url = f"{self.base_url}/{endpoint}"
        # print(url)
        response = requests.post(url, json=data)
        response.raise_for_status()
        return response