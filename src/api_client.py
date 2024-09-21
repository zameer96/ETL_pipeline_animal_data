import requests


class APIClient:
    def __init__(self, base_url):
        if not base_url:
            raise ValueError("base_url required for APIClient")
        self.base_url = base_url
        self.logger = None
        
        
    def get(self, endpoint):
        response = requests.get(f"{self.base_url}/{endpoint}")
        return response.json()
    
    def post(self, endpoint, data):
        response = requests.post(f"{self.base_url}/{endpoint}", json=data)
        return response.json()
