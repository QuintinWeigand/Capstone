curl -X POST http://localhost:8080/tool \
  -H "Content-Type: application/json" \
  -d '{
    "tool": "weather",
    "action": "get_weather", 
    "parameters": {
      "latitude": 43.13,
      "longitude": -75.23 
    }
  }'
