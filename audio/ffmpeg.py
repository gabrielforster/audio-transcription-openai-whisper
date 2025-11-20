import subprocess

def slow_audio(input_file: str, output_file: str, speed_factor: float) -> bool:
    """
    Slows down the audio of the input file by the given speed factor and saves it to the output file.

    :param input_file: Path to the input audio file.
    :param output_file: Path to save the slowed down audio file.
    :param speed_factor: Factor by which to slow down the audio (e.g., 0.5 for half speed).
    """

    command = [
        'ffmpeg',
        '-i', input_file,
        '-filter:a', f'atempo={speed_factor}',
        '-vn',
        output_file
    ]

    try:
        subprocess.run(command, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
        return True
    except subprocess.CalledProcessError as e:
        print(f"an error occurred: {e}")
        return False
