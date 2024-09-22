

class AnimalExtractor:
    
    api_client = None
    logger = None
    batch_size = None
    current_page = 1
    total_pages = None  # We'll set this while fetching animals list
    # kinda setting this everytime just incase if the page count changes
    animals_queue = []
    
    def __init__(self, api_client, logger, batch_size=100):
        self.api_client = api_client
        self.logger = logger
        self.batch_size = batch_size


    def fetch_animals_list(self, page):
        """
        input: page (int)
        response_json sample:
            {
                "page": 1,
                "total_pages": 558,
                "items": [
                    {
                    "id": 0,
                    "name": "Chicken",
                    "born_at": null
                    }
                ]
            }
        """
        response_json = self.api_client.get(f"animals?page={page}")
        self.total_pages = response_json['total_pages'] # update total pages
        return response_json['items']

    def fetch_animal_details(self, animal_id):
        """
        input: animal_id (int)
        response_json sample: 
                {
                    "id": 10,
                    "name": "Hippopotamus",
                    "born_at": null,
                    "friends": "Quail,Hummingbird,Beaver,Raven,Goose"
                }
        """
        response_json = self.api_client.get(f"animals/{animal_id}")
        return response_json

    def get_next_animals_batch(self):
        animal_details = []
        while len(animal_details) < self.batch_size and (self.animals_queue or (not self.total_pages) or (self.current_page <= self.total_pages)):
            if not self.animals_queue:
                self.animals_queue = self.fetch_animals_list(self.current_page)
                self.current_page += 1

            while self.animals_queue and len(animal_details) < 100:
                animal = self.animals_queue.pop(0)
                details = self.fetch_animal_details(animal['id'])
                animal_details.append(details)

        return animal_details

