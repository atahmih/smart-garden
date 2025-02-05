import { useEffect, useState } from "react";
import { Card, CardContent } from "@/components/ui/card";
import { Line } from "react-chartjs-2";
import "chart.js/auto";

export default function Dashboard() {
  const [sensorData, setSensorData] = useState([]);
  const [latest, setLatest] = useState({ temperature: 0, humidity: 0, soil_moisture: 0 });

  useEffect(() => {
    const fetchData = async () => {
      const response = await fetch("https://your-api-endpoint.azurewebsites.net/data");
      const data = await response.json();
      setSensorData(data);
      setLatest(data[data.length - 1] || {});
    };

    fetchData();
    const interval = setInterval(fetchData, 5000);
    return () => clearInterval(interval);
  }, []);

  const chartData = {
    labels: sensorData.map((_, i) => i),
    datasets: [
      {
        label: "Temperature (°C)",
        data: sensorData.map(d => d.temperature),
        borderColor: "#ff6384",
        fill: false,
      },
      {
        label: "Humidity (%)",
        data: sensorData.map(d => d.humidity),
        borderColor: "#36a2eb",
        fill: false,
      },
      {
        label: "Soil Moisture",
        data: sensorData.map(d => d.soil_moisture),
        borderColor: "#4bc0c0",
        fill: false,
      }
    ]
  };

  return (
    <div className="p-4 grid gap-4 grid-cols-1 md:grid-cols-3">
      <Card>
        <CardContent>
          <h2 className="text-xl font-bold">Temperature</h2>
          <p className="text-4xl">{latest.temperature}°C</p>
        </CardContent>
      </Card>
      <Card>
        <CardContent>
          <h2 className="text-xl font-bold">Humidity</h2>
          <p className="text-4xl">{latest.humidity}%</p>
        </CardContent>
      </Card>
      <Card>
        <CardContent>
          <h2 className="text-xl font-bold">Soil Moisture</h2>
          <p className="text-4xl">{latest.soil_moisture}</p>
        </CardContent>
      </Card>
      <div className="col-span-3">
        <h2 className="text-xl font-bold">Sensor Data Over Time</h2>
        <Line data={chartData} />
      </div>
    </div>
  );
}
