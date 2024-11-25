import serial 
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import time as t
from datetime import datetime, timezone 
import csv


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
pumpRelay = []

def read_data():
	try:
		data = arduino.readline().decode().strip()
	except UnicodeDecodeError:
		data = None
	# print((data))
	if data != None:
		sensorValues = data.split(',')
		# print(sensorValues)	
		if len(sensorValues) > 1:
			timeStamp.append(datetime.now(timezone.utc))
			# print((sensorValues))
			print(datetime.now(timezone.utc), sensorValues[0], sensorValues[1], sensorValues[2])
			soilMoisture.append(int(sensorValues[0]))
			lightIntensity.append(int(sensorValues[1]))
			pumpRelay.append(sensorValues[2])
start_time = datetime.now(timezone.utc)
while True:
	read_data()
	with open(f'arduino_data_{start_time}.csv', 'w', newline='') as csvfile:
		writer = csv.writer(csvfile)
		writer.writerow(['Time', 'Soil_Moisture', 'Light_Intensity', 'Pump Signal'])
		for time, moisture, light, pump in zip(timeStamp, soilMoisture, lightIntensity, pumpRelay):
			writer.writerow([time, moisture, light, pump])
	t.sleep(30)	
