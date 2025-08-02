# Text-to-Speech API Documentation

## Overview
This API provides text-to-speech functionality using Meta's MMS-TTS English model. It converts text input to high-quality audio output in WAV format.

## Endpoints

### 1. Convert Text to Speech
**POST** `/api/tts/convert`

Convert text to speech and generate an audio file.

#### Request Body
```json
{
    "text": "Hello world! This is a test message.",
    "filename": "optional_custom_name.wav"  // Optional
}
```

#### Response
```json
{
    "success": true,
    "data": {
        "filename": "tts_20241202_143052_a1b2c3d4.wav",
        "text": "Hello world! This is a test message.",
        "duration_seconds": 2.5,
        "sampling_rate": 16000,
        "file_size_bytes": 80000,
        "created_at": "2024-12-02T14:30:52.123456"
    },
    "message": "Text converted to speech successfully"
}
```

### 2. Download Audio File
**GET** `/api/tts/download/<filename>`

Download the generated audio file.

#### Parameters
- `filename`: The filename returned from the convert endpoint

#### Response
Returns the WAV audio file for download.

### 3. Get Model Information
**GET** `/api/tts/info`

Get information about the TTS model.

#### Response
```json
{
    "success": true,
    "data": {
        "model_name": "facebook/mms-tts-eng",
        "sampling_rate": 16000,
        "is_loaded": true,
        "output_directory": "/tmp/tts_outputs"
    },
    "message": "TTS model information retrieved successfully"
}
```

### 4. Cleanup Old Files
**POST** `/api/tts/cleanup`

Clean up old generated audio files.

#### Request Body
```json
{
    "max_age_hours": 24  // Optional, default is 24 hours
}
```

#### Response
```json
{
    "success": true,
    "data": {
        "deleted_files": 5,
        "message": "Cleaned up 5 old files"
    },
    "message": "Cleanup completed successfully"
}
```

## Usage Examples

### Using curl

1. **Convert text to speech:**
```bash
curl -X POST http://localhost:5000/api/tts/convert \
  -H "Content-Type: application/json" \
  -d '{"text": "Hello world! This is a test message."}'
```

2. **Download audio file:**
```bash
curl -X GET http://localhost:5000/api/tts/download/tts_20241202_143052_a1b2c3d4.wav \
  -o output.wav
```

3. **Get model info:**
```bash
curl -X GET http://localhost:5000/api/tts/info
```

4. **Cleanup old files:**
```bash
curl -X POST http://localhost:5000/api/tts/cleanup \
  -H "Content-Type: application/json" \
  -d '{"max_age_hours": 12}'
```

### Using JavaScript/Fetch

```javascript
// Convert text to speech
async function textToSpeech(text) {
    const response = await fetch('http://localhost:5000/api/tts/convert', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ text: text })
    });
    
    const result = await response.json();
    return result;
}

// Download audio file
async function downloadAudio(filename) {
    const response = await fetch(`http://localhost:5000/api/tts/download/${filename}`);
    const blob = await response.blob();
    
    // Create download link
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    a.click();
    window.URL.revokeObjectURL(url);
}

// Example usage
textToSpeech("Hello world!").then(result => {
    if (result.success) {
        console.log('Audio generated:', result.data.filename);
        // Download the file
        downloadAudio(result.data.filename);
    }
});
```

### Using Python requests

```python
import requests
import json

# Convert text to speech
def text_to_speech(text, base_url="http://localhost:5000"):
    url = f"{base_url}/api/tts/convert"
    data = {"text": text}
    
    response = requests.post(url, json=data)
    return response.json()

# Download audio file
def download_audio(filename, base_url="http://localhost:5000"):
    url = f"{base_url}/api/tts/download/{filename}"
    response = requests.get(url)
    
    if response.status_code == 200:
        with open(filename, 'wb') as f:
            f.write(response.content)
        return True
    return False

# Example usage
result = text_to_speech("Hello world! This is a test message.")
if result['success']:
    filename = result['data']['filename']
    print(f"Audio generated: {filename}")
    
    # Download the file
    if download_audio(filename):
        print(f"Audio file downloaded: {filename}")
```

## Error Handling

All endpoints return consistent error responses:

```json
{
    "success": false,
    "error": "Error message details",
    "message": "User-friendly error description"
}
```

Common HTTP status codes:
- `200`: Success
- `400`: Bad Request (invalid input)
- `404`: Not Found (file not found)
- `500`: Internal Server Error

## Limitations

- Maximum text length: 5000 characters
- Audio format: WAV (16-bit, 16kHz sampling rate)
- Language: English only (facebook/mms-tts-eng model)
- File cleanup: Automatic cleanup of files older than 24 hours (configurable)

## Requirements

The following Python packages are required:
- torch>=1.13.0
- transformers>=4.25.0
- scipy>=1.9.0
- numpy>=1.21.0
- Flask>=2.3.3
- Flask-CORS>=4.0.0
