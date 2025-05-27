from pydub import AudioSegment
from pydub.utils import which
import logging
import os
import sys

# Forzar uso explícito de ffmpeg
AudioSegment.converter = which("ffmpeg")

# Loggers visibles
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)

def split_stereo(audio_path, left_output, right_output):
    try:
        print("[DEBUG] Working directory:", os.getcwd())
        print("[DEBUG] Files available:", os.listdir("."))

        logging.info("Splitting stereo audio...")

        audio = AudioSegment.from_file(audio_path)
        left, right = audio.split_to_mono()

        left.export(left_output, format="wav")
        right.export(right_output, format="wav")

        logging.info(f"Exported {left_output} and {right_output}")
    except Exception as e:
        print("[ERROR] Exception occurred")
        logging.exception(e)

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python3 split_audio.py stereo.wav left.wav right.wav")
        sys.exit(1)

    split_stereo(sys.argv[1], sys.argv[2], sys.argv[3])
