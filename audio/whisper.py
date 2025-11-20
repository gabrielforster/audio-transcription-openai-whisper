import whisper

def transcribe_audio(file_path: str, model_size="turbo"):
    """
    Transcribes the audio file at the given path using the Whisper model.

    :param file_path: Path to the input audio file.
    :param model_size: Size of the Whisper model to use (default is "turbo").
    :return: Transcription text.
    """

    model = whisper.load_model(model_size)
    result = model.transcribe(file_path)
    return result["text"]
