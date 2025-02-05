from fastapi import FastAPI
import json
from azure.iot.hub import IoTHubRegistryManager

with open('backend_connection_str.txt', 'r') as file:
    CONNECTION_STRING=file.readline().strip()

DEVICE_ID = 'arduino-node'

app = FastAPI()

@app.get("/data")
async def get_sensor_data():
    try:
        # Connect to the IoT Hub
        registry_manager = IoTHubRegistryManager(CONNECTION_STRING)
        twin = registry_manager.get_twin(DEVICE_ID)

        # Get the reported properties
        data = twin.properties.reported
        return {
                        'soil_moisture': data.get('soil_moisture'),
                        'light_intensity': data.get('light_intensity'),
                        'temperature': data.get('temperature'),
                        'humidity': data.get('humidity'),
                        'pump_relay': data.get('pump_relay')
                    }
    except Exception as e:
        return {'error': str(e)}