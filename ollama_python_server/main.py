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


def load_system_prompt(file):
    try:
        with open(file, 'r') as f:
            return f.read().strip()
    except FileNotFoundError:
        print(f"Error: {file} not found!")
        return ""
    except Exception as e:
        print(f"Error reading system prompt -> {e}")
        return ""


# -------------------------
# LangChain / Ollama Setup
# -------------------------
def create_chain():
    template = load_system_prompt("system_prompt.txt")

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
