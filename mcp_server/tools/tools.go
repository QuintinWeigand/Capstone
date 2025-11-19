package tools

import (
	"encoding/json"
	"fmt"
)

type ToolCall struct {
	Tool       string         `json:"tool"`
	Action     string         `json:"action"`
	Parameters map[string]any `json:"parameters"`
}

func (self ToolCall) String() string {
	parameters, _ := json.Marshal(self.Parameters)
	return fmt.Sprintf("Tool: %s | Action: %s | Parameters %s", self.Tool, self.Action, string(parameters))
}

func ValidateTool(tc *ToolCall) error {
	switch {
	case tc.Tool == "":
		return fmt.Errorf("tool name is required")
	case tc.Action == "":
		return fmt.Errorf("action is required")
	case tc.Tool == "weight_logger":
		switch tc.Action {
		case "log", "history", "change":
			return nil
		default:
			return fmt.Errorf("unknown action: %s", tc.Action)
		}
	case tc.Tool == "weather":
		switch tc.Action {
		case "get_weather":
			return nil
		default:
			return fmt.Errorf("unknown action: %s", tc.Action)
		}
	default:
		return fmt.Errorf("unknown tool: %s", tc.Tool)
	}
}

func ExecuteTool(tc *ToolCall) (string, error) {
	switch tc.Tool {
	case "weight_logger":
		collection, err := GetMongoCollection()
		if err != nil {
			return "", err
		}
		weightDB := NewWeightDB(collection)

		switch tc.Action {
		case "log":
			weight, ok := tc.Parameters["weight"].(float64)
			if !ok {
				return "", fmt.Errorf("weight parameter must be a number")
			}
			err := weightDB.logWeight(weight)
			if err != nil {
				return "", fmt.Errorf("failed to log weight: %v", err)
			}
			return fmt.Sprintf("Logged weight: %.1f", weight), nil

		case "history":
			history, err := weightDB.getHistory()
			if err != nil {
				return "", fmt.Errorf("failed to get history: %v", err)
			}
			if len(history) == 0 {
				return "No weight entries yet.", nil
			}
			var result string
			for index, h := range history {
				result += fmt.Sprintf("%s: %.1f lbs", h.DateTime, h.WeightLbs)
				if index != len(history)-1 {
					result += "\n"
				}
			}
			return result, nil

		case "change":
			change, err := weightDB.weightChange()
			if err != nil {
				if err.Error() == "not enough data to compute change" {
					return "Not enough data to compute change", nil
				}
				return "", fmt.Errorf("failed to compute change: %v", err)
			}
			return fmt.Sprintf("Weight change: %+.1f lbs", change), nil
		default:
			return "", fmt.Errorf("unknown action of weight_logger: %s", tc.Tool)
		}
	case "weather":
		switch tc.Action {
		case "get_weather":
			lat, ok := tc.Parameters["latitude"].(float64)
			if !ok {
				return "", fmt.Errorf("latitude must be a floating point number")
			}
			long, ok := tc.Parameters["longitude"].(float64)
			if !ok {
				return "", fmt.Errorf("latitude must be a floating point number")
			}

			temperature, err := callWeatherAPI(lat, long)
			if err != nil {
				return "", fmt.Errorf("failed to get temperature data: %v", err)
			}
			return fmt.Sprintf("Weather at lat: %f long: %f | %f", lat, long, temperature), nil
		default:
			return "", fmt.Errorf("unknown action of weather: %s", tc.Action)
		}
	default:
		return "", fmt.Errorf("unknown tool: %s", tc.Tool)
	}
}
