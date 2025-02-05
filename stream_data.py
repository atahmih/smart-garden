import serial 
import asyncio
import json
import time as t
from datetime import datetime, timezone 
from zoneinfo import ZoneInfo
from azure.iot.device import IoTHubDeviceClient, Message    


async def update_twin(client, message):
	try:						
		# client.patch_twin_reported_properties(twin_patch)
		# print(f'Updated device twin')
		twin_patch = {
			'reported': message
        }
		await client.patch_twin_reported_properties(twin_patch)
		print(client.get_twin())
	except Exception as e:
		print(f'Error: {e} at twin')

async def twin_update(client, message):
	while True:
		await update_twin(client, message)
		await asyncio.sleep(3)


with open('device_connection_str.txt', 'r') as file:
    CONNECTION_STRING=file.readline().strip()

client = IoTHubDeviceClient.create_from_connection_string(CONNECTION_STRING)
print(type(client))
client.connect()

TZ = ZoneInfo('America/Halifax')
ser = serial.Serial(port='/dev/ttyACM0', baudrate=9600, timeout=.1) 

# Reset the Arduino
ser.setDTR(False)
#time.sleep(1)
ser.flushInput()
ser.setDTR(True)
#time.sleep(1)
# Values are printed in the order soil, light, temp, humidity, pump
while True:
    try:
        if ser.in_waiting > 0:
            data = ser.readline().decode('utf-8').strip()
            if data != None:
                sensorValues = data.split(',')
                if len(sensorValues) > 1:					
                    message = {
                        'soil_moisture': sensorValues[0],
                        'light_intensity': sensorValues[1],
                        'temperature': sensorValues[2],
                        'humidity': sensorValues[3],
                        'pump_relay': sensorValues[4]
                    }
                    json_data = json.dumps(message)
                    print(f'Received: {json_data}')
                    client.send_message(json_data)
                    
                    # Update device twin
                    # twin_patch = {
                    #     "reported": message
                    # }
                    # asyncio.create_task(twin_update(client, message))
                    update_twin(client, message)
    except Exception as e:
        print(f'Error: {e}')
    asyncio.sleep(3)

if __name__ == '__main__':
      asyncio.run(main())