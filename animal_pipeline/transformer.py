from datetime import datetime, timezone


class AnimalTransformer:
    
    """
    This class would be responsible for the complete transformation of animal.
    raw animal detail would look like this:
        {
            "id": 4,
            "name": "Salamander",
            "born_at": 1617115838888,
            "friends": "Jackal,Monkey,Finch,Starling,Elephant"
        }
    """
    
    def __init__(self):
        pass
    
    def apply_transformation(self, animal_details=None, many=False) -> dict:
        """
        Applies the transformation functions and returns the class variable animal
        """
        if many:
            for animal in animal_details:
                animal = self.transform_field_friends(animal_details=animal)
                animal = self.transform_field_born_at(animal_details=animal)
            return animal_details
        else:
            animal_details = self.transform_field_friends(animal_details=animal_details)
            animal_details = self.transform_field_born_at(animal_details=animal_details)
        return animal_details
    
    
    def transform_field_friends(self, animal_details):
        if 'friends' in animal_details and isinstance(animal_details['friends'], str):
            animal_details['friends'] = animal_details['friends'].split(',')
        return animal_details
    
    def transform_field_born_at(self, animal_details):
        if 'born_at' in animal_details and animal_details['born_at']:
            # iso_time_format = datetime.fromtimestamp(animal_details['born_at'] / 1000, tz=timezone.utc).isoformat()
            # iso_time_format = datetime.fromtimestamp(animal_details['born_at'], tz=timezone.utc)
            timestamp_seconds = animal_details['born_at'] / 1000
            iso_time_format = datetime.fromtimestamp(timestamp_seconds, tz=timezone.utc)
            animal_details['born_at'] = iso_time_format.isoformat().replace("+00:00", "Z")  
        return animal_details
        