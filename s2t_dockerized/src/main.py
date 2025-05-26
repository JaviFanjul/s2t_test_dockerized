import threading
import queue
import time
import pyaudio
import logging

from config import *
from utils import create_file, delete_directory
from voice_recorder import VoiceRecorder
from transcriber import Transcriber
from sink_writer import SinkWriter
from load_model import ModelLoader


class SystemOrchestrator:
    """
    Orchestrates the complete audio transcription and sentiment analysis pipeline.

    Responsibilities:
        - Initializes queues, components, and UI.
        - Loads Whisper models for both speakers.
        - Sets up and launches each component in separate threads.
        - Handles graceful shutdown on interruption.
    """

    def __init__(self):
        """
        Initializes the system: components, queues, model loader, and GUI.
        """
        self.q_sp1 = queue.Queue()
        self.q_sp2 = queue.Queue()
        self.q_sink = queue.Queue()
        self.threads = []

        self.pyaudio_instance = pyaudio.PyAudio()
       
        self.model_loader = ModelLoader()
        self.model_sp1, self.options_sp1 = self.model_loader.load()
        self.model_sp2, self.options_sp2 = self.model_loader.load()

        self._prepare_environment()

    def _prepare_environment(self):
        """
        Sets up the environment before starting the system:
        - Creates the transcription file.
        - Deletes any previous transcription output folders.
        """
        create_file(file)
        delete_directory(OUTPUT_FOLDER_sp1)
        delete_directory(OUTPUT_FOLDER_sp2)

    def _safe_thread(self, target):
        """
        Wraps a function to run it in a safe daemon thread with exception handling.

        Args:
            target (function): The function to run in the thread.
        """
        def wrapped():
            try:
                target()
            except Exception as e:
                logging.error(f"Thread {target.__name__} failed: {e}")

        t = threading.Thread(target=wrapped, daemon=True)
        self.threads.append(t)

    def start(self):
        """
        Starts the entire system pipeline:
        - Initializes all components.
        - Launches each one in its own thread.
        - Keeps the main loop alive via the GUI.
        """
        logging.info("Starting system...")

        # Component instances
        recorder1 = VoiceRecorder(OUTPUT_FOLDER_sp1, ID_DEVICE_sp1, self.pyaudio_instance, self.q_sp1)
        recorder2 = VoiceRecorder(OUTPUT_FOLDER_sp2, ID_DEVICE_sp2, self.pyaudio_instance, self.q_sp2)

        transcriber1 = Transcriber(self.q_sp1, self.model_sp1, self.options_sp1, file, speaker1, self.q_sink)
        transcriber2 = Transcriber(self.q_sp2, self.model_sp2, self.options_sp2, file, speaker2, self.q_sink)

        sink = SinkWriter(self.q_sink, file)
        

        # Thread launching
        self._safe_thread(recorder1.start)
        self._safe_thread(transcriber1.start)
        self._safe_thread(recorder2.start)
        self._safe_thread(transcriber2.start)
        self._safe_thread(sink.start)

        
        

        for t in self.threads:
            t.start()

        try:
            while all(t.is_alive() for t in self.threads):
                time.sleep(0.1)

        except KeyboardInterrupt:
            logging.warning("Interrupt signal received, shutting down...")
            self.q_sp1.put(None)
            self.q_sp2.put(None)
            self.q_sink.put(None)

        finally:
            self.pyaudio_instance.terminate()
            logging.info("System successfully shut down.")


if __name__ == "__main__":
    orchestrator = SystemOrchestrator()
    orchestrator.start()
