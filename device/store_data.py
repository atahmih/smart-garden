# Eliminates the need for stream_data.py and collect_data.py
# Directly sends the data to the Azure Cosmos DB

from azure.cosmos import CosmosClient
import os
from dotenv import load_dotenv

import serial
import time
import json

import uuid
from datetime import datetime
from zoneinfo import ZoneInfo

def setup_db(client):
    
    # Create a database if not exists
    database = client.create_database_if_not_exists(
        id=os.getenv('DATABASE_NAME')
    )

    # Create a container if not exists
    container = database.create_container_if_not_exists(
        id=os.getenv('CONTAINER_NAME'),
        partition_key='/timestamp'
    )

    print('Database and container setup complete')
    return container

TZ = ZoneInfo('America/Halifax')

load_dotenv()

ser = serial.Serial(port='/dev/ttyACM0', baudrate=9600, timeout=1) 
client = CosmosClient.from_connection_string(os.getenv('COSMOS_CONNECTION_STRING'))

container = setup_db(client)

while True:
    try:
        if ser.in_waiting > 0:
            data = ser.readline().decode('utf-8').strip()
            if data != None:
                sensorValues = data.split(',')
                if len(sensorValues) > 1:
                    data = {
                        'id': str(uuid.uuid4()),
                        'timestamp': datetime.now(TZ).strftime('%Y-%m-%d %H:%M:%S'),
                        'soil_moisture': float(sensorValues[0]),
                        'light_intensity': float(sensorValues[1]),
                        'temperature': float(sensorValues[2]),
                        'humidity': float(sensorValues[3]),
                        'pump_relay': sensorValues[4]
                    }
                    container.create_item(body=data)
                    print(f"✔ Data stored: {data}")

    except Exception as e:
        print(f'Error: {e}')
    time.sleep(1)

