package tools

import "fmt"

// NOTE: https://api.open-meteo.com/v1/forecast?latitude=52.52&longitude=13.41&hourly=temperature_2m&temperature_unit=fahrenheit
// Above is an example url for the free weather api (10,000 non-commerical uses a day) updated to use fahrenheit

type WeatherData struct {
	Temperature_2m []float32 `json:"temperature_2m"`
	Latitude       float32   `json:"latitude"`
	Longitude      float32   `json:"longitude"`
}

func findMaxTemp(temps []float32) float32 {
	var maxTemp float32 = 0.0
	for _, temp := range temps {
		if temp > maxTemp {
			maxTemp = temp
		}
	}
	return maxTemp
}

// NOTE: We are assuming that max temp is the value we even want.
// TODO: Find out what value we desire from the API data
func (self WeatherData) String() string {
	return fmt.Sprintf("Lat: %f | Long: %f | Max Temp: %f", self.Latitude, self.Longitude, findMaxTemp(self.Temperature_2m))
}
