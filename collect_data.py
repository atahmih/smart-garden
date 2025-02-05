import serial 
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import time as t
from datetime import datetime, timezone 
from zoneinfo import ZoneInfo
import csv

tz = ZoneInfo('America/Halifax')
arduino = serial.Serial(port='/dev/ttyACM0', baudrate=9600, timeout=.1) 

# Reset the Arduino
arduino.setDTR(False)
#time.sleep(1)
arduino.flushInput()
arduino.setDTR(True)
#time.sleep(1)

x = []
timeStamp = []
soilMoisture = []
lightIntensity = []
temperature = []
humidity = []
pumpRelay = []

def read_data():
	try:
		data = arduino.readline().decode().strip()
	except UnicodeDecodeError:
		data = None
	# print((data))
	if data != None:
		sensorValues = data.split(',')
		# Values are printed in the order soil, light, temp, humidity, pump
		if len(sensorValues) > 1:
			timeStamp.append(datetime.now(tz))
			# print((sensorValues))
			print(datetime.now(tz), sensorValues[0], sensorValues[1], sensorValues[2], sensorValues[3], sensorValues[4])
			soilMoisture.append(int(sensorValues[0]))
			lightIntensity.append(int(sensorValues[1]))
			temperature.append(float(sensorValues[2]))
			humidity.append(float(sensorValues[3]))
			pumpRelay.append(sensorValues[4])
start_time = datetime.now(timezone.utc).strftime("%Y-%m-%d")
while True:
	read_data()
	with open(f'data/data_{start_time}.csv', 'w', newline='') as csvfile:
		writer = csv.writer(csvfile)
		writer.writerow(['Time', 'Soil_Moisture', 'Light_Intensity', 'Temperature', 'Humidity', 'Pump Signal'])
		for time, moisture, light, temp, hum, pump in zip(timeStamp, soilMoisture, lightIntensity, temperature, humidity, pumpRelay):
			writer.writerow([time, moisture, light, temp, hum, pump])
	t.sleep(30)	
