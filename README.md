# Animal Data ETL Pipeline

This ETL (Extract, Transform, Load) pipeline fetches animal data from an API, transforms the born_at timestamp to ISO UTC format & friends field to array, and loads (post request) it back to the API (home).

## Instructions to run the project 

1. Assuming you have already cloned the repo and created virtual environment, install dependencies from requirements:
    
    `pip install -r requirements.txt`
    
2.  Create a `.env` file in the root directory with BASE_URL:
    
    `BASE_URL=https://25fa-99-250-42-230.ngrok-free.app/animals/v1/`
    Hosting this on my local server, (might be up and running)
3. (Optional) if needed you can change the batch size (100 by default, since post API accepts list of 100 animals)
    
5.  Run the pipeline:
    
    `python run.py`
6. Logs streamed in `logs/info.log` file
    

## Working

The pipeline consists of four main components:

1.  **Extractor**: 
		-> Fetches the animal list with page=1
		-> for each page, gets the animal_details for each animal and stores it in class var.
		-> Keeps running for the batch size defined (100 by default)
2.  **Transformer**: Converts timestamps and splits friend lists of all the animal_detail_list.
3.  **Loader**: Posts transformed data back to the API.
4. **APIClient.retry_api_call** this decorator handles the API Retry mechnaism based on expontential wait time

The `run.py` script runs these components, processing animals in batches of 100.

## Logging

Logs are stored in the `logs/` directory. Check these for detailed pipeline execution info.
Logs for info, error, notify can be set to stream on different files. 
update `animal_pipeline/logger.py` ____init____

## Running Tests

To run tests:

`pytest`

Just mocked the API responses

## Possible Improvements

-   async parallel fetch of animal list
- Save animal_ids so no chances of duplicacy


Author: Zameer