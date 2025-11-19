package tools

import (
	"encoding/json"
	"fmt"
	"net/http"
)

// Example json call from Python:
// {
// 	"tool": "weather",
// 	"action": "get_weather",
// 	"parameters": {
// 		"latitude": x,
// 		"longitude": y
// 	}
// }

// weight, ok := tc.Parameters["weight"].(float64)
//

type WeatherData struct {
	Latitude  float64 `json:"latitude"`
	Longitude float64 `json:"longitude"`
	Hourly    struct {
		Temperature_2m []float64 `json:"temperature_2m"`
	} `json:"hourly"`
}

func (self WeatherData) String() string {
	return fmt.Sprintf("Lat: %f | Long: %f | Current Temp: %f", self.Latitude, self.Longitude, self.Hourly.Temperature_2m[0])
}

func callWeatherAPI(lat float64, long float64) (float64, error) {
	var wd WeatherData
	url := fmt.Sprintf("https://api.open-meteo.com/v1/forecast?latitude=%f&longitude=%f&hourly=temperature_2m&temperature_unit=fahrenheit", lat, long)
	resp, err := http.Get(url)
	if err != nil {
		return 0.0, fmt.Errorf("Failed to call Weather API")
	}
	defer resp.Body.Close()

	if resp.StatusCode != http.StatusOK {
		return 0.0, fmt.Errorf("Weather API returned status: %d", resp.StatusCode)
	}
	err = json.NewDecoder(resp.Body).Decode(&wd)
	if err != nil {
		return 0.0, fmt.Errorf("Failed to decode JSON for Weather API")
	}

	return wd.Hourly.Temperature_2m[0], nil
}
