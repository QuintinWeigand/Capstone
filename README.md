# Capstone Project

A multi-tool AI assistant that combines a local LLM with practical tools. Users interact through a web chat interface, and the AI can call tools to perform real actions like logging weight or fetching weather data.

## What It Does

This application is an AI-powered assistant that can:

- **Chat with you** — Have conversations with a local Llama 3.1 LLM through a web interface
- **Voice input** — Speak your queries; audio is transcribed using Whisper before processing
- **Log weight** — Track weight measurements over time, stored in MongoDB. Ask to see your history or calculate changes between entries
- **Check weather** — Get current temperature by providing latitude/longitude coordinates

The AI decides when to use a tool based on your message. For example, if you say "I weigh 175 lbs" it will log it. If you ask "what's the weather in 40.7, -74.0" it will fetch the temperature.

## Components

- **Flask web server** — Serves the chat interface and handles voice transcription
- **Ollama (Llama 3.1)** — Local LLM that powers the conversational AI
- **MCP Server (Go)** — Executes tool calls (weight logging, weather lookups)
- **MongoDB** — Stores weight history
- **Open-Meteo API** — Provides weather data
- **Hugo blog** — Documents the development process at `/blog`
