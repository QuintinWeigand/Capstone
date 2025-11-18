package main

import (
	"encoding/json"
	"fmt"
	"mcp_server/tools"
	"net/http"
)

const PORT int = 8080

func toolHandler(w http.ResponseWriter, r *http.Request) {
	var toolCall tools.ToolCall
	var err error
	var result string

	err = json.NewDecoder(r.Body).Decode(&toolCall)

	// This parses and decodes the JSON
	if err != nil {
		http.Error(w, "Invalid JSON", http.StatusBadRequest)
		return
	}

	// This will validate the toolCall
	err = tools.ValidateTool(&toolCall)
	if err != nil {
		http.Error(w, err.Error(), http.StatusBadRequest)
		return
	}

	result, err = tools.ExecuteTool(&toolCall)
	if err != nil {
		http.Error(w, err.Error(), http.StatusBadRequest)
		return
	}

	fmt.Fprint(w, result)
}

func main() {
	http.HandleFunc("/tool", toolHandler)
	fmt.Printf("Server listening on PORT: %d\n", PORT)
	http.ListenAndServe(fmt.Sprintf(":%d", PORT), nil)
}
