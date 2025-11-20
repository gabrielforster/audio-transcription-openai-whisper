# Audio Transcription Service

A FastAPI-based service that transcribes audio files using OpenAI's Whisper model. The service downloads audio files from URLs, slows them down using FFmpeg for better transcription accuracy, and returns the transcribed text.

## Features

- **Streaming Downloads**: Audio files are downloaded in chunks to avoid loading large files entirely into memory
- **Audio Processing**: Automatically slows down audio files (0.8x speed) using FFmpeg before transcription
- **Synchronous & Asynchronous Endpoints**: Process audio synchronously or asynchronously with webhook callbacks
- **Memory Efficient**: Uses streaming to handle large audio files without memory issues

### System Requirements

- Python 3.10+
- FFmpeg 
- Node.js (optional for running the "audio" files server)

## Installation

1. **Create a virtual environment**:
```bash
python3 -m venv venv
source venv/bin/activate
```

2. **Install Python dependencies**:
```bash
pip install -r requirements.txt
```

3. **Running the Server**:

Start the FastAPI server using Uvicorn:

```bash
uvicorn app:app --port 8000 --reload
```

### Optionally run the Test Audio Server

A simple Node.js server is provided in the `audios-server` folder for testing purposes.

1. **Navigate to the audios-server directory**:
```bash
cd audios-server
```

2. **Place audio files** (`.ogg`, `.mp3`, etc.) in the `audios-server` folder

3. **Start the Node.js server**:
```bash
node index.js
```

## API Endpoints

### Health Check

**GET** `/health`

**Example**:
```bash
curl -X POST http://localhost:8000/health
```

**Response**:
```json
{
  "status": "up"
}
```

Check if the service is running.

### Synchronous Audio Transcription

**POST** `/audio`

Transcribe an audio file synchronously. The request will wait until transcription is complete.

**Request Body**:
```json
{
  "audio_url": "http://localhost:3000/audio.ogg"
}
```

**Response**:
```json
{
  "transcription": "The transcribed text from the audio file.",
  "processing_time": 12.34
}
```

**Example**:
```bash
curl -X POST http://localhost:8000/audio \
  -H "Content-Type: application/json" \
  -d '{"audio_url": "http://localhost:3000/audio.ogg"}'
```

### Asynchronous Audio Transcription

**POST** `/audio/async`

Transcribe an audio file asynchronously. Returns immediately with a processing status, then sends results to a webhook URL when complete.

**Request Body**:
```json
{
  "audio_url": "http://localhost:3000/audio.ogg",
  "webhook_url": "http://localhost:8080/webhook"
}
```

**Response** (immediate):
```json
{
  "status": "processing"
}
```

**Webhook Payload** (on success):
```json
{
  "status": "success",
  "transcription": "The transcribed text from the audio file.",
  "processing_time": 12.34
}
```

**Webhook Payload** (on error):
```json
{
  "status": "error",
  "error": "Error message here"
}
```

**Example**:
```bash
curl -X POST http://localhost:8000/audio/async \
  -H "Content-Type: application/json" \
  -d '{
    "audio_url": "http://localhost:3000/audio2.ogg",
    "webhook_url": "http://localhost:8080/webhook"
  }'
```

## How It Works

1. **Download**: The service downloads the audio file from the provided URL using streaming to avoid loading the entire file into memory
2. **Slow Down**: The audio is processed through FFmpeg to slow it down to 0.8x speed (using the `atempo` filter) for better transcription accuracy
3. **Transcribe**: The slowed audio is transcribed using OpenAI's Whisper model (default: "turbo" model)
4. **Return**: The transcription text is returned to the client (synchronously) or sent to the webhook URL (asynchronously)

## Notes

- Temporary audio files are stored in `/tmp/` during processing
- The service validates that the URL points to an audio file by checking the `Content-Type` header
- Audio files are processed in chunks (128 bytes) to minimize memory usage
- The Whisper model is loaded on first use and cached for subsequent requests

