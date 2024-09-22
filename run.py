import os
from dotenv import load_dotenv
from animal_pipeline import (APIClient,
                             AnimalExtractor,
                             AnimalTransformer,
                             AnimalLoader,
                             Logger)

load_dotenv()

logger = Logger()


CONFIG = {
    "base_url": os.getenv("BASE_URL") or "http://localhost:3123/animals/v1/",
    "batch_size": 100
}


def main():
    base_url = CONFIG["base_url"]
    api_client = APIClient(base_url)
    extractor = AnimalExtractor(api_client, logger, batch_size=CONFIG["batch_size"])
    batch_number = 1

    print("=== STARTING ANIMAL PIPELINE. STREAM LOGS FROM 'logs/' DIRECTORY! ===")
    # Pipeline
    while True:
        logger.info(f"Fetching batch # {batch_number}")

        # extract 100 animals at a time
        animal_details = extractor.get_next_animals_batch()
        
        # End if no more animals to fetch
        if not animal_details:
            logger.info("No more animals to fetch. Exiting.")
            break
        
        # Apply transformation
        logger.info(f"Applying transformation to batch # {batch_number}")
        animal_details = AnimalTransformer().apply_transformation(animal_details=animal_details, many=True)
        logger.info(f"Transformed {len(animal_details)} animals.")
        
        # Loader: Post the batch animal list in the animal_post
        logger.info(f"Posting batch # {batch_number}")
        loader = AnimalLoader(api_client, logger)
        response_json = loader.post_batch(animal_details)
        logger.info(f"Posted {len(animal_details)} animals. Response: {response_json}")
                
        logger.info(f"Finished batch # {batch_number}")
        batch_number += 1
    logger.notify("Job Completed: All animals are fetched and posted successfully.")

if __name__ == "__main__":
    main()