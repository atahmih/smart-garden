import React, { useState, useEffect } from "react";
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from "recharts";

function App() {
  const [sensorData, setSensorData] = useState(null);
  const [historicalData, setHistoricalData] = useState([]);
  const [xMin, setXMin] = useState(null);
  const [xMax, setXMax] = useState(null);

  useEffect(() => {
    document.title = 'Smart Garden'
    const fetchData = async () => {
      try {
        // Fetch latest sensor data
        // const response = await fetch("http://localhost:8000/latest"); 
        const response = await fetch("https://smart-garden-backend.azurewebsites.net/latest");
        const latestData = await response.json();
        setSensorData(latestData);

        // Fetch historical data
        // const historyResponse = await fetch("http://localhost:8000/history"); 
        const historyResponse = await fetch("https://smart-garden-backend.azurewebsites.net/history");
        const historyData = await historyResponse.json();
        
        // Ensure timestamps are formatted properly 
        const formattedData = historyData.map(item => ({
          time: new Date(item.timestamp).toLocaleTimeString([], { 
            hour: '2-digit', 
            minute: '2-digit',
            hour12: true 
          }),
          soil_moisture: item.soil_moisture
        })).reverse();
        
        setHistoricalData(formattedData);
        if (formattedData.length > 0) {
          const minTime = Math.min(...formattedData.map(d => d.time));
          const maxTime = Math.max(...formattedData.map(d => d.time));
          const oneHour = 60 * 60 * 1000; // 60 minutes in milliseconds
          
          setXMin(minTime - oneHour / 2); // 30 minutes before first data point
          setXMax(maxTime + oneHour / 2); // 30 minutes after last data point
        }
      } catch (error) {
        console.error("Error fetching data:", error);
      }
    };

    fetchData();
    const interval = setInterval(fetchData, 10000);
    
    return () => clearInterval(interval);
  }, []);

  return (
    <div style={{ textAlign: "center", padding: "20px" }}>
      <h1>Smart Garden Dashboard</h1>
      
      {sensorData ? (
        <div style={{ border: "1px solid #ccc", padding: "10px", display: "inline-block" }}>
          <p><strong>Soil Moisture:</strong> {sensorData.soil_moisture}</p>
          <p><strong>Light Intensity:</strong> {sensorData.light_intensity}</p>
          <p><strong>Temperature:</strong> {sensorData.temperature}°C</p>
          <p><strong>Humidity:</strong> {sensorData.humidity}%</p>
          <p><strong>Pump Status:</strong> {sensorData.pump_status ? "On" : "Off"}</p>
        </div>
      ) : (
        <p>Loading sensor data...</p>
      )}

      <h2>Moisture History</h2>
      <div style={{ width: "80%", height: 300, margin: "auto" }}>
        <ResponsiveContainer width="100%" height="100%">
          <LineChart data={historicalData}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis 
              dataKey="time" 
              interval="preserveStartEnd"
              tick={{ fontSize: 12 }}
              height={50}
              angle={-45}
              textAnchor="end"
              domain={[xMin, xMax]} 
            />
            <YAxis 
                domain={["dataMin - 10", "dataMax + 10"]}
                allowDataOverflow={false}
                tick={{ fontSize: 12 }}
              />
            <Tooltip />
            <Line type="monotone" dataKey="soil_moisture" stroke="#8884d8" strokeWidth={2} />
          </LineChart>
        </ResponsiveContainer>
      </div>

      <footer style={{ marginTop: "20px", fontSize: "14px", color: "#666" }}>
      <a href="https://www.flaticon.com/free-icons/gardening" title="gardening icons" target="_blank" rel="noopener noreferrer">
        Tab Icon
      </a>
    </footer>
    </div>
  );
}

export default App;
