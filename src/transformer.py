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
    
    def __init__(self, animal):
        self.animal = animal
        
    def apply_transformation(self) -> dict:
        """
        Applies the transformation functions and returns the class variable animal
        """
        self.transform_field_friends()
        self.transform_field_born_at()
        return self.animal
    
    
    def transform_field_friends(self):
        if 'friends' in self.animal and isinstance(self.animal['friends'], str):
            self.animal['friends'] = self.animal['friends'].split(',')
    
    def transform_field_born_at(self):
        if 'born_at' in self.animal and self.animal['born_at']:
            iso_time_format = datetime.fromtimestamp(self.animal['born_at'] / 1000, tz=timezone.utc).isoformat()
            self.animal['born_at'] = iso_time_format
        