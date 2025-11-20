import time
import requests
from pydantic import BaseModel
from fastapi import FastAPI, BackgroundTasks
from fastapi.responses import JSONResponse

from audio.whisper import transcribe_audio
from audio.ffmpeg import slow_audio

app = FastAPI()

class AudioRequestBody(BaseModel):
    audio_url: str

class AsyncAudioRequestBody(AudioRequestBody):
    webhook_url: str

@app.get("/health")
def health_check():
    return JSONResponse(content={"status": "up"})


def process_audio_from_url(audio_url: str) -> str:
    audio_response = requests.get(audio_url)
    if audio_response.status_code != 200:
        return JSONResponse(content={"error": "failed to download audio"}, status_code=400)

    audio_content_type = audio_response.headers.get("Content-Type", "")

    if "audio" not in audio_content_type:
        return JSONResponse(content={"error": "url does not point to an audio file"}, status_code=400)

    audio_extension = audio_content_type.split("/")[-1]

    now = time.time()
    audio_file_path = f"/tmp/audio_{now}.{audio_extension}"
    with open(audio_file_path, "wb") as audio_file:
        audio_file.write(audio_response.content)

    audio_file_out_path = f"/tmp/slow_audio_{now}.{audio_extension}"
    slow_audio(audio_file_path, audio_file_out_path, speed_factor=0.8)

    audio_trascription = transcribe_audio(audio_file_out_path).strip()
    print(f"Transcription: {audio_trascription}")
    return audio_trascription

@app.post("/audio")
async def get_audio_transcription(body: AudioRequestBody):
    try:
        request_init = time.time()
        audio_trascription = process_audio_from_url(body.audio_url)
        took_time = time.time() - request_init
        return JSONResponse(content={"transcription": audio_trascription, "processing_time": took_time})
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

def async_process_audio(data: dict):
    request_init = data["request_init"]
    audio_url = data["audio_url"]
    webhook_url = data["webhook_url"]

    try:
        audio_trascription = process_audio_from_url(audio_url)
        took_time = time.time() - request_init
        requests.post(webhook_url, json={"status": "success", "transcription": audio_trascription,"processing_time": took_time})
    except Exception as e:
        requests.post(webhook_url, json={"status": "error", "error": str(e)})

@app.post("/audio/async")
async def post_audio_transcription(body: AsyncAudioRequestBody, background_tasks: BackgroundTasks):
    data = {
        "audio_url": body.audio_url,
        "webhook_url": body.webhook_url,
        "request_init": time.time()
    }
    background_tasks.add_task(async_process_audio, data)
    return JSONResponse(status_code=202, content={"status": "processing"})

