
import pytest
from unittest.mock import Mock, patch
from animal_pipeline.api_client import APIClient
from animal_pipeline.extractor import AnimalExtractor
from animal_pipeline.transformer import AnimalTransformer
from animal_pipeline.loader import AnimalLoader

# Mock API responses
mock_animals_list = {
    "page": 1,
    "total_pages": 1,
    "items": [
        {"id": 1, "name": "Lion", "born_at": None},
        {"id": 2, "name": "Elephant", "born_at": None}
    ]
}

mock_animal_details_list = [{
    "id": 1,
    "name": "Lion",
    "born_at": 1617115838888,
    "friends": "Tiger,Giraffe,Zebra"
},{
    "id": 2,
    "name": "Elephant",
    "born_at": 1617115835678,
    "friends": "Dog,Cat,Parrot"
}]

# Mock API Client
class MockAPIClient:
    def get(self, endpoint):
        if "animals?page=" in endpoint:
            return mock_animals_list
        elif "animals/" in endpoint:
            animal_id = int(endpoint.split("/")[-1])
            animal_data = mock_animal_details_list[animal_id - 1]
            return animal_data
        raise ValueError("Unknown endpoint")

    def post(self, endpoint, data):
        return {"message": "Helped 2 find home"}

# Extractor tests
def test_extractor():
    mock_logger = Mock()
    extractor = AnimalExtractor(MockAPIClient(), mock_logger, batch_size=2)
    batch = extractor.get_next_animals_batch()

    assert len(batch) == 2
    assert batch[0]["id"] == 1
    assert batch[1]["id"] == 2

# Transformer tests
def test_transformer():
    transformer = AnimalTransformer()
    
    
    transformed = transformer.apply_transformation(mock_animal_details_list[0])
    print(transformed)
    assert isinstance(transformed["friends"], list)
    assert len(transformed["friends"]) == 3
    assert transformed["born_at"].endswith("Z")

# Loader tests
def test_loader():
    mock_api_client = MockAPIClient()
    mock_logger = Mock()
    loader = AnimalLoader(mock_api_client, mock_logger)
    
    animals = [
        {"id": 1, "name": "Lion", "born_at": "2021-03-30T12:30:38.888Z", "friends": ["Tiger", "Giraffe", "Zebra"]},
        {"id": 2, "name": "Elephant", "born_at": "2021-04-01T10:15:00.000Z", "friends": ["Rhino", "Hippo"]}
    ]
    
    response = loader.post_batch(animals)
    
    assert "message" in response

