from flask import Flask, render_template, request, jsonify
from langchain.prompts import ChatPromptTemplate
from langchain_ollama import OllamaLLM
import requests
import re
import json
import whisper
import tempfile
import os

MCP_SERVER_URL = "http://localhost:8080/tool"

whisper_model = None

app = Flask(__name__, static_folder="static", static_url_path="/static")


@app.route("/")
def index():
    return render_template("chat.html")


@app.route("/send", methods=["POST"])
def send_message():
    user_input = request.form["message"]
    response = process_message(user_input)
    return render_template("chat.html", user_input=user_input, response=response)


@app.route("/transcribe", methods=["POST"])
def transcribe_audio_endpoint():
    if "audio" not in request.files:
        return jsonify({"error": "No audio file"}), 400

    audio_file = request.files["audio"]

    with tempfile.NamedTemporaryFile(delete=False, suffix=".webm") as tmp:
        audio_file.save(tmp.name)

        # Transcribe audio
        transcribed_text = transcribe_audio(tmp.name)

        # Process transcribed text through existing pipeline
        response = process_message(transcribed_text)

        # Cleanup
        os.unlink(tmp.name)

        return render_template(
            "chat.html", user_input=transcribed_text, response=response
        )


def load_system_prompt(file):
    try:
        with open(file, "r") as f:
            return f.read().strip()
    except FileNotFoundError:
        print(f"Error: {file} not found!")
        return ""
    except Exception as e:
        print(f"Error reading system prompt -> {e}")
        return ""


def load_whisper_model():
    global whisper_model
    if whisper_model is None:
        whisper_model = whisper.load_model("base")
    return whisper_model


def transcribe_audio(audio_file_path):
    try:
        model = load_whisper_model()
        result = model.transcribe(audio_file_path)
        return result["text"]
    except Exception as e:
        return f"Transcription Error -> {e}"


def create_chain():
    template = load_system_prompt("system_prompt.txt")

    prompt = ChatPromptTemplate.from_template(template)
    try:
        model = OllamaLLM(model="llama3.1:8b", base_url="http://100.64.246.90:11434")
        model.invoke("test")
    except Exception as e:
        print(
            "Error: Could not connect to Ollama Server. Please make sure it is running"
        )
        print(f"Error Details: {e}")
        exit(1)

    # Modern LangChain syntax
    return prompt | model


def call_mcp_server(tool_data):
    try:
        response = requests.post(MCP_SERVER_URL, json=tool_data, timeout=10)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        return f"Error calling MCP Server: {e}"


def process_message(user_input):
    # Get model response
    chain = create_chain()
    response = chain.invoke({"text": user_input}).strip()

    # Clean and parse possible JSON
    response_clean = re.sub(
        r"^```(?:json)?|```$", "", response.strip(), flags=re.MULTILINE
    ).strip()

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

    return output


if __name__ == "__main__":
    app.run(debug=True)
