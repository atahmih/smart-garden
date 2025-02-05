import { useEffect, useState } from "react";
import { Line } from 'react-chartjs-2';
import 'chart.js/auto';

const API_URL='https://smart-garden-api.azurewebsites.net/data';

export default function App(){
  const [sensorData, setSensorData] = useState([]);
  const [latest, setLatest] = useState({temperature: 0, humidity: 0, soil_moisture: 0, light_intensity: 0, pump_relay: 'OFF'});

  useEffect(() => {
    const fetchData = async() => {
      const response = await fetch(API_URL);
      const data = await response.json();
      setSensorData((prev) => [...prev, data].slice(-20)) //Keep the last 20 readings
      setLatest(data);
    };

    fetchData();
    const interval = setInterval(fetchData, 5000);
    return () => clearInterval(interval);
  }, []);

  const chartData = {
    labels: sensorData.map((_, i) => i),
    datasets: [
      {label: 'Temperature (°C)', data: sensorData.map((data) => data.temperature), borderColor: 'red', fill: false},
      {label: 'Humidity (%)', data: sensorData.map(d => d.humidity), borderColor: 'blue', fill: false},
      {label: 'Soil Moisture', data: sensorData.map(d => d.soil_moisture), borderColor: 'green', fill: false},
      {label: 'Light Intensity', data: sensorData.map(d => d.light_intensity), borderColor: 'yellow', fill: false}
    ]
  };

  return (
    <div className='container'>
      <h1>Smart Garden Dashboard</h1>
      <div className='grid'>
        <div className='card'>
          <h2>Temperature</h2>
          <p>{latest.temperature} °C</p>
        </div>
        <div className='card'>
          <h2>Humidity</h2>
          <p>{latest.humidity} %</p>
        </div>
        <div className='card'>
          <h2>Soil Moisture</h2>
          <p>{latest.soil_moisture}</p>
        </div>
        <div className='card'>
          <h2>Light Intensity</h2>
          <p>{latest.light_intensity}</p>
        </div>
        {/* <div className='card'>
          <h2>Pump Relay</h2>
          <p>{latest.pump_relay}</p>
        </div> */}
      </div>
      <Line data={chartData} />
    </div>
  );

}