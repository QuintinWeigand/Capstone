---
Title: Whisper Integration for Voice Input
Date: 2025-12-14
draft: "false"
---

---
# Table of Contents
1. [Overview](#overview)
2. [Whisper Model Setup](#whisper_model_setup)
3. [Audio Processing Pipeline](#audio_processing_pipeline)
4. [Browser Audio Recording](#browser_audio_recording)
5. [Backend Integration](#backend_integration)
6. [Error Handling](#error_handling)

---
## Overview

Voice input capability was added to the multi-tool assistant using OpenAI's Whisper model for speech-to-text transcription. This allows users to interact with the AI assistant through natural speech, making the interface more accessible and user-friendly.

---
## Whisper Model Setup

### Model Selection
- **Model**: Whisper `base` model
- **Device**: CPU-based processing for compatibility
- **Language**: Auto-detection for multilingual support

### Loading Strategy
```python
def load_whisper_model():
    global whisper_model
    if whisper_model is None:
        try:
            # Load model with FP32 to avoid FP16 CPU warning
            whisper_model = whisper.load_model("base", device="cpu")
        except Exception as e:
            print(f"Error loading Whisper model: {e}")
            raise e
    return whisper_model
```

### Performance Considerations
- **Lazy loading**: Model loaded only when needed
- **Global instance**: Single model instance for efficiency
- **CPU optimization**: FP32 precision to avoid warnings

---
## Audio Processing Pipeline

### Transcription Process
```python
def transcribe_audio(audio_file_path):
    try:
        model = load_whisper_model()
        result = model.transcribe(audio_file_path)
        
        # Handle both string and list cases for text
        text = result["text"]
        if isinstance(text, list):
            text = " ".join(text)
        elif isinstance(text, str):
            text = text.strip()
        
        return text
    except Exception as e:
        print(f"Transcription error: {e}")
        return f"Transcription Error: {e}"
```

### File Management
- **Temporary files**: Use `tempfile.NamedTemporaryFile` for audio storage
- **Automatic cleanup**: Files deleted after processing
- **Format support**: Handles WebM audio from browser recording

---
## Browser Audio Recording

### MediaRecorder API Integration
```javascript
async function toggleRecording(event) {
    if (isRecording) {
        // Stop recording
        mediaRecorder.stop();
    } else {
        // Start recording
        const stream = await navigator.mediaDevices.getUserMedia({ 
            audio: {
                echoCancellation: true,
                noiseSuppression: true,
                sampleRate: 16000
            } 
        });
        
        mediaRecorder = new MediaRecorder(stream, {
            mimeType: 'audio/webm;codecs=opus'
        });
        
        mediaRecorder.start();
    }
}
```

### Audio Configuration
- **Echo cancellation**: Reduces feedback and echo
- **Noise suppression**: Improves audio quality
- **Sample rate**: 16kHz for optimal Whisper performance
- **Format**: WebM with Opus codec for browser compatibility

---
## Backend Integration

### Flask Endpoint
```python
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
        
        return jsonify({
            "user_input": transcribed_text,
            "response": response
        })
```

### Integration Flow
1. **Audio upload** from browser to Flask endpoint
2. **Temporary file storage** for processing
3. **Whisper transcription** converts speech to text
4. **AI processing** through existing message pipeline
5. **JSON response** returns both transcription and AI response
6. **File cleanup** removes temporary audio file

---
## Error Handling

### Client-Side Errors
- **Microphone access**: Graceful handling of permission denials
- **Recording failures**: User-friendly error messages
- **Network issues**: Timeout and connection error handling

### Server-Side Errors
- **File validation**: Check for audio file presence
- **Transcription failures**: Catch and report Whisper errors
- **Cleanup assurance**: Files removed even if processing fails

### User Feedback
```javascript
function showError(message) {
    const errorDiv = document.createElement('div');
    errorDiv.style.cssText = 
        'background-color: #f8d7da;' +
        'color: #721c24;' +
        'padding: 10px;' +
        'border-radius: 5px;' +
        'margin: 10px 0;';
    errorDiv.textContent = message;
    
    // Auto-remove after 5 seconds
    setTimeout(function() {
        if (errorDiv.parentNode) {
            errorDiv.parentNode.removeChild(errorDiv);
        }
    }, 5000);
}
```

---
## Conclusion

The Whisper integration successfully adds voice input capabilities to the AI assistant, providing a more natural and accessible user interface. The implementation demonstrates:

- **Modern web APIs**: MediaRecorder for browser audio capture
- **AI model integration**: Whisper for accurate speech-to-text
- **Robust error handling**: Comprehensive error management
- **User experience**: Clear feedback and intuitive controls

This feature significantly enhances the usability of the multi-tool assistant while maintaining the existing functionality and architecture patterns.