# Connect to Cosmos DB, fetch data through API, return JSON for frontend

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from azure.cosmos import CosmosClient
import os
from dotenv import load_dotenv
import logging

load_dotenv() # Load the environment variables

app = FastAPI()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

# Cosmos DB Connection
try:
    client = CosmosClient.from_connection_string(os.getenv('COSMOS_CONNECTION_STRING'))
    database = client.get_database_client(os.getenv('DATABASE_NAME'))
    container = database.get_container_client(os.getenv('CONTAINER_NAME'))
    logger.info("Successfully connected to Cosmos DB")
except Exception as e:
    logger.error(f"Failed to connect to Cosmos DB: {str(e)}")
    raise

@app.on_event('startup')
def startup_event():
    logger.info('Starting application...')
    try:
        database_test = list(container.query_items(
            query='SELECT VALUE COUNT(1) FROM c',
            enable_cross_partition_query=True
        ))
        logger.info(f'Connected to database. Record count: {database_test[0]}')
    except Exception as e:
        logger.error(f'Failed to connect to DB: {str(e)}')
        raise

@app.get('/')
def home():
    return {'message': 'Smart Garden API Up and Running'}

# Fetch the latest data
@app.get('/latest')
def get_latest_data():
    try:
        query = ' SELECT * FROM c ORDER BY c.timestamp DESC OFFSET 0 LIMIT 1' # Get the latest data
        items = list(container.query_items(query=query, enable_cross_partition_query=True)) # Run query and get the items from COSMOS DB

        if not items:
            raise HTTPException(status_code=404, detail='No data found')
        return items[0] # latest data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.get('/history')
def get_sensor_history(limit: int = 10):
    # Fetch the last limit sensor readings
    try:
        query = f'SELECT * FROM c ORDER BY c.timestamp DESC OFFSET 0 LIMIT {limit}' 
        items = list(container.query_items(query=query, enable_cross_partition_query=True))

        if not items:
            raise HTTPException(status_code=404, detail='No data found')
        return items
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Uncomment to run locally
if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8000) 
    