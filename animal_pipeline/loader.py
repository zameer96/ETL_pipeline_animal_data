
class AnimalLoader:
    def __init__(self, api_client, logger=None):
        self.api_client = api_client
        self.logger = logger
        

    def post_batch(self, animals):
        """
        Posts a batch of animal details to the '/home' endpoint.
        This assumes that 'animals' is a list of transformed animal details.
        """
        endpoint = "home"
        response_json = self.api_client.post(endpoint, data=animals)
        self.logger.info(f"Posted {len(animals)} animals to {endpoint}. Response: {response_json}")
        self.logger.notify(f"Completed animals list: {animals}")
        return response_json