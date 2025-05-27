import pyaudio
import os
from utils import get_device_id_from_name


# === Audio stream configuration ===
CHUNK = 2000                      # Chunk size (tune to match ~10s)
FORMAT = pyaudio.paInt16          # 16-bit format
CHANNELS = 1                      # Mono channel
RATE = 48000                      # Sampling rate (Hz)
SILENCE_THRESHOLD = 600           # Silence detection threshold (RMS)
PRE_BUFFER = 5                    # Number of chunks to store before speech
POST_BUFFER = 20                  # Number of chunks to store after silence
MAX_CHUNK_TIME = 10               # Maximum duration of a chunk (seconds)

# === Audio device IDs ===
ID_DEVICE_sp1 = get_device_id_from_name("Monitor of AgentSink")
ID_DEVICE_sp2 = get_device_id_from_name("Monitor of ClientSink")

# === Output folders for each speaker ===
OUTPUT_FOLDER_sp1 = "chunks_sp1"
OUTPUT_FOLDER_sp2 = "chunks_sp2"

# === File to save transcriptions ===
file = "./transcription.txt"

# === Contextual segment parameters ===
numSeg = 5                        # Number of previous segments to use as context

# === Source and separated audio file paths ===
source_path = "./source_files/call.wav"
left_path = "./created_files/audio_izquierda.wav"
right_path = "./created_files/audio_derecha.wav"

# === Speaker names ===
speaker1 = "Agente"
speaker2 = "Cliente"

# === Whisper model parameters ===
whisper_model = "medium"         # Whisper model size
device = "cuda"                  # Execution device: "cpu" or "cuda"
language = "es"                  # Language for transcription
compt = "float16"                # Compute type (use float16 for GPU)

# === VAD (Voice Activity Detection) filter parameters ===
threshold = 0.95                 # VAD detection threshold
min_speech_duration = 300         #Mnimum speech duration in milliseconds

# === Transcription sorter thread parameters ===
interval = 5                     # Sort interval in seconds

# === Band-pass filter parameters for pre-processing ===
LOWCUT_FREQ = 85.0               # Minimum frequency (Hz) for human voice
HIGHCUT_FREQ = 3000.0            # Maximum frequency (Hz) for human voice
FILTER_ORDER = 5                 # Filter order (higher = more selective but slower)
THRESHOLD = 400                  # RMS threshold for speech detection

# === LLM sentiment analysis parameters ===
sentiment_interval = 30          # Frequency of satisfaction analysis (seconds)

# === Prompts for the sentiment analysis model ===
SYSTEM_PROMPT = "Eres un experto en análisis de satisfacción del cliente."
USER_TEMPLATE = """
Analiza la siguiente conversación entre un cliente (Cliente) y un agente (Agente).
Evalúa el nivel de satisfacción del cliente (Cliente) en una escala del 1 al 10.

Solo responde con un número. No añadas ninguna explicación ni texto adicional.

Conversación:
{conversacion}
"""

# === Groq API key (replace with your real key in production) ===
os.environ["GROQ_API_KEY"] = "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"

# === UI update interval (in seconds) ===
update_interval = 1

# === Prompt para generación de resumen de conversación ===
SUMMARY_SYSTEM_PROMPT = "Eres un asistente que resume conversaciones para que los nuevos agentes puedan retomarlas rápidamente."

SUMMARY_USER_TEMPLATE = """
Resume la siguiente conversación entre un cliente y un agente.
El objetivo es que un nuevo agente pueda entender rápidamente el contexto y continuar la conversación de forma efectiva.

Transcripción:
{conversacion}
"""