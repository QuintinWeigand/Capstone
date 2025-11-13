import json
import re
from datetime import datetime
from pymongo import MongoClient
from langchain_ollama import OllamaLLM
from langchain.prompts import ChatPromptTemplate


# -------------------------
# MongoDB Setup
# -------------------------
try:
    client = MongoClient("mongodb://localhost:27017")
    client.admin.command('ping')
    db = client.weight_tracker
    weights_collection = db.weights
except Exception as e:
    print(f"Error: Could not connect to MongoDB. Please make sure it is running")
    print(f"Error Details: {e}")
    exit(1)

# -------------------------
# Weight Logger Functions
# -------------------------


def log_weight(weight):
    """Insert a new weight record (in lbs) with timestamp."""
    entry = {
        "datetime": datetime.now().isoformat(),
        "weight_lbs": weight
    }
    weights_collection.insert_one(entry)


def get_history():
    """Return all weight entries sorted chronologically."""
    return list(weights_collection.find({}, {"_id": 0}).sort("datetime", 1))


def weight_change():
    """Compute total weight change in lbs from first to last entry."""
    history = get_history()
    if len(history) < 2:
        return None
    return history[-1]["weight_lbs"] - history[0]["weight_lbs"]


# -------------------------
# Dispatcher
# -------------------------
def dispatch_tool(tool_data):
    tool = tool_data.get("tool")
    action = tool_data.get("action")
    params = tool_data.get("parameters", {})

    print("DEBUG: ", tool_data)

    if tool == "weight_logger":
        if action == "log":
            weight = params.get("weight")
            if weight is not None:
                log_weight(weight)
                return f"Logged weight: {weight:.1f} lbs"
            return "Error: No weight provided."
        elif action == "history":
            history = get_history()
            if not history:
                return "No weight entries yet."
            return "\n".join(f"{h['datetime']}: {h['weight_lbs']} lbs" for h in history)
        elif action == "change":
            change = weight_change()
            if change is None:
                return "Not enough data to compute change."
            return f"Weight change: {change:+.1f} lbs"
        else:
            return f"Unknown action '{action}' for weight_logger."
    else:
        return f"Unknown tool '{tool}'."


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
                output = dispatch_tool(tool_data)
            except json.JSONDecodeError:
                output = response_clean
        else:
            # Normal conversation
            output = response_clean

        print(output)


# -------------------------
if __name__ == "__main__":
    main()
