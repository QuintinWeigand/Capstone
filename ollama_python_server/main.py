import json
import re
from langchain_ollama import OllamaLLM
from langchain.prompts import ChatPromptTemplate
import requests

MCP_SERVER_URL = "http://localhost:8080/tool"


def call_mcp_server(tool_data):
    try:
        response = requests.post(MCP_SERVER_URL, json=tool_data, timeout=10)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        return f"Error calling MCP Server: {e}"


# -------------------------
# LangChain / Ollama Setup
# -------------------------
def create_chain():
    template = """
You are a multi-tool assistant. You can either respond normally in conversation,
or call a tool when needed.

Tools available:
1. weight_logger – for logging and viewing weight (in pounds).

Guidelines:
- All weights must be in pounds (lbs).
- If the user provides their weight in kilograms (kg), DO NOT log it.
  Instead, politely ask them to provide their weight in pounds.
- If the user mentions or wants to log their weight in lbs, respond ONLY in JSON like this:
  {{"tool": "weight_logger", "action": "log", "parameters": {{"weight": <number_in_lbs>}}}}
- If the user wants to see their weight history:
  {{"tool": "weight_logger", "action": "history"}}
- If the user asks for weight change:
  {{"tool": "weight_logger", "action": "change"}}
- For anything else, respond normally with text.

User input: {text}
"""
    prompt = ChatPromptTemplate.from_template(template)
    try:
        model = OllamaLLM(model="llama3.1:8b",
                          base_url="http://100.64.246.90:11434")
        model.invoke("test")
    except Exception as e:
        print(f"Error: Could not connect to Ollama Server. Please make sure it is running")
        print(f"Error Details: {e}")
        exit(1)

    # Modern LangChain syntax
    return prompt | model


# -------------------------
# Main Loop
# -------------------------
def main():
    chain = create_chain()
    print("Welcome to your multi-tool assistant! Type 'exit' to quit.")

    while True:
        user_input = input("Enter command -> ").strip()
        if user_input.lower() in {"exit", "quit"}:
            print("Goodbye!")
            break

        # Get model response
        response = chain.invoke({"text": user_input}).strip()

        # --- Clean and parse possible JSON ---
        # Remove Markdown code fences if present
        response_clean = re.sub(r"^```(?:json)?|```$", "",
                                response.strip(), flags=re.MULTILINE).strip()

        # Try to find JSON object
        json_match = re.search(r"\{.*\}", response_clean, re.DOTALL)

        if json_match:
            try:
                tool_data = json.loads(json_match.group())
                output = call_mcp_server(tool_data)
            except json.JSONDecodeError:
                output = response_clean
        else:
            # Normal conversation
            output = response_clean

        print(output)


# -------------------------
if __name__ == "__main__":
    main()
