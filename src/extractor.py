
class AnimalExtractor:
    
    CURRENT_PAGE = 1
    TOTAL_PAGES = None
    
    
    def __init__(self, api_client, logger):
        self.api_client = api_client
        self.logger = logger

    def fetch_animals_list(self, page=1):
        return self.api_client.get(f"/animals?page={page}")
    
    def fetch_animal_details(self, animal_id):
        return self.api_client.get(f"/animals/{animal_id}")